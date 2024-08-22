import bs4
from langchain.document_loaders import WebBaseLoader
from langsmith import traceable

@traceable
def load_documents(urls):
    all_docs = []
    for url in urls:
        loader = WebBaseLoader(
            web_paths=(url,),
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    "div",
                    attrs={"class": ["newsct_article _article_body", "media_end_head_title"]},
                )
            ),
        )
        docs = loader.load()
        all_docs.extend(docs)
        print(f"URL: {url} - 문서의 수: {len(docs)}")
        
        if docs:
            print(f"첫 문서 내용: {docs[0].page_content[:1000]}...")
            soup = bs4.BeautifulSoup(docs[0].page_content, 'html.parser')
            elements = soup.find_all("div", class_=["newsct_article _article_body", "media_end_head_title"])
            print(f"추출된 요소의 개수: {len(elements)}")
            if elements:
                print(f"첫 번째 요소의 내용: {elements[0].text[:200]}...")
    
    return all_docs
