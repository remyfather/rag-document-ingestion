import os
import requests
from dotenv import load_dotenv
from app.utils.logging_utils import logger
from bs4 import BeautifulSoup

# .env 파일에서 환경변수 로드
load_dotenv()

def analyze_pdf_with_upstage(pdf_file):
    api_key = os.getenv('UPSTAGE_API_KEY')
    print("api _key------>", api_key)    
    url = "https://api.upstage.ai/v1/document-ai/layout-analysis"
    
    files = {
        'document': pdf_file,
        'ocr': 'true'
    }
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    logger.info("Upstage API 요청 시작")
    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        logger.info("Upstage API 요청 성공")
        return response.json()
    else:
        logger.error(f"Upstage API 요청 실패 - 상태 코드: {response.status_code}, 응답: {response.text}")
        raise Exception(f"Failed to analyze document: {response.status_code} - {response.text}")

def process_analyzed_pdf(analysis_result):
    # 요소별 텍스트 및 데이터를 수집
    headings = []
    paragraphs = []
    tables = []

    for element in analysis_result.get('elements', []):
        category = element.get('category')
        text = element.get('text', '')
        
        if category == 'heading1':
            headings.append(text)
        elif category == 'paragraph':
            paragraphs.append(text)
        elif category == 'table':
            table_data = parse_table(element.get('html', ''))
            tables.append(table_data)
    
    # 텍스트 가공
    document_summary = {
        'headings': headings,
        'paragraphs': paragraphs,
        'tables': tables
    }
    
    # 가공된 결과를 로그로 출력
    logger.info(f"가공된 결과 - Headings: {headings}")
    logger.info(f"가공된 결과 - Paragraphs: {paragraphs}")
    logger.info(f"가공된 결과 - Tables: {tables}")
    
    return document_summary

def parse_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    table_data = []
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        table_data.append(cols)
    
    # 파싱된 테이블 데이터를 로그로 출력
    logger.info(f"파싱된 테이블 데이터: {table_data}")
    
    return table_data
