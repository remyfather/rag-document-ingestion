# app/routes.py

from flask import request, jsonify
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
