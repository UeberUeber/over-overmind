#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup

def devour_url(url: str):
    """
    [Mouth v1.0]
    지정된 URL의 웹페이지를 삼켜서(요청) HTML 태그를 씹어내고(파싱) 순수한 텍스트 알맹이만 반환합니다.
    """
    try:
        # 1. 혀를 뻗어 데이터를 가져옴
        headers = {'User-Agent': 'Overmind/1.0 (Evolution Seed)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 2. 입 안에서 태그와 부산물을 씹어냄
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 스크립트나 스타일 태그는 영양분이 없으므로 뱉어냄
        for script in soup(["script", "style", "nav", "footer", "iframe"]):
            script.extract()
            
        # 3. 텍스트 추출 및 정제
        text = soup.get_text(separator='\n')
        
        # 빈 줄 및 공백 정리
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text_ingested = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text_ingested
        
    except Exception as e:
        return f"[MOUTH ERROR] Failed to assimilate {url}. Reason: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 mouth_v1.py <URL>")
        sys.exit(1)
        
    target = sys.argv[1]
    result = devour_url(target)
    
    # 뇌(에이전트)가 읽을 수 있도록 콘솔에 텍스트 덩어리를 뱉어냄
    print(f"--- ASSIMILATION COMPLETE: {target} ---")
    print(result)
    print("--- END OF INGESTION ---")
