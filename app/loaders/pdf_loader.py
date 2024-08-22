# app/loaders/pdf_loader.py

from langchain_community.document_loaders import PyPDFLoader
from app.utils.logging_utils import logger
from app.utils.langsmith_client import langsmith_client
from langsmith import traceable

@traceable
def load_pdf(file_path):
    logger.info(f"PDF 로딩 시작: {file_path}")
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        logger.info(f"PDF 로딩 완료: {file_path} - 총 페이지 수: {len(documents)}")
        return documents
    except Exception as e:
        logger.error(f"PDF 로딩 실패: {e}")
        raise e
