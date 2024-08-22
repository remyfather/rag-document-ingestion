# app/utils/langsmith_client.py

import os
from langsmith import Client
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# LangSmith API 클라이언트 초기화
def get_langsmith_client():
    api_key = os.getenv('LANGCHAIN_API_KEY')
    
    if not api_key:
        raise ValueError("LANGCHAIN_API_KEY is not set in the environment variables.")
    
    client = Client(api_key=api_key)
    return client

# LangSmith 클라이언트를 전역적으로 사용하기 위해 인스턴스 생성
langsmith_client = get_langsmith_client()
