from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.utils.logging_utils import logger
from langsmith import traceable

@traceable
def chunk_documents(documents, chunk_size=1000, chunk_overlap=50):
    logger.info(f"문서 청킹 시작 - 총 문서 수: {len(documents)}")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(documents)
    
    logger.info(f"청크된 문서 수: {len(chunks)}")
    
    for i, chunk in enumerate(chunks[:5]):  # 청크 내용 일부를 출력 (최대 5개)
        logger.info(f"청크 {i+1}: {chunk.page_content[:100]}...")
    
    return chunks
