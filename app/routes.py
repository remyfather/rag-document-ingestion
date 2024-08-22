from flask import request, jsonify
from app.loaders.pdf_analyzer import analyze_pdf_with_upstage, process_analyzed_pdf
from app.loaders.pdf_loader import load_pdf
from app.loaders.web_loader import load_documents
from app.services.chunking_service import chunk_documents
from app.utils.logging_utils import logger

def configure_routes(app):
    @app.route('/ingest/pdf', methods=['POST'])
    def ingest_pdf():
        file_path = request.json.get('file_path')
        logger.info(f"/ingest/pdf 요청 수신 - 파일 경로: {file_path}")
        documents = load_pdf(file_path)
        chunks = chunk_documents(documents)
        return jsonify({"message": "PDF 로딩 및 청킹 완료", "chunk_count": len(chunks)})

    @app.route('/ingest/url', methods=['POST'])
    def ingest_url():
        urls = request.json.get('urls')
        logger.info(f"/ingest/url 요청 수신 - URLs: {urls}")
        documents = load_documents(urls)
        chunks = chunk_documents(documents)
        return jsonify({"message": "웹 페이지 로딩 및 청킹 완료", "chunk_count": len(chunks)})

    @app.route('/analyze/pdf', methods=['POST'])
    def analyze_pdf():
        if 'file' not in request.files:
            logger.error("파일이 제공되지 않음")
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        logger.info(f"/analyze/pdf 요청 수신 - 파일 이름: {file.filename}")

        try:
            # Upstage Layout Analyzer API 호출
            analysis_result = analyze_pdf_with_upstage(file)
            logger.info(f"PDF 분석 완료 - 결과: {analysis_result}")

            # 분석 결과 처리
            processed_data = process_analyzed_pdf(analysis_result)

            return jsonify(processed_data)
        except Exception as e:
            logger.error(f"PDF 분석 실패 - 오류: {str(e)}")
            return jsonify({"error": str(e)}), 500
