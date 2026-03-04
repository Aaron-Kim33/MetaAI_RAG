import requests
from bs4 import BeautifulSoup

# 공부할 메타 헬프센터 링크 (예시: 비즈니스 설정)
url = "https://www.facebook.com/business/help/1710077379203035"

def crawl_meta():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 제목과 본문 추출 (메타의 HTML 구조에 따라 달라질 수 있음)
        title = soup.find('title').get_text()
        content = soup.get_text(separator='\n', strip=True)
        
        print(f"--- 수집 완료: {title} ---")
        
        # 수집한 내용을 텍스트 파일로 저장 (AI가 읽을 참고서)
        with open("meta_knowledge.txt", "w", encoding="utf-8") as f:
            f.write(content)
        print("meta_knowledge.txt 파일로 저장되었습니다.")
    else:
        print("페이지를 가져오는데 실패했습니다.")

if __name__ == "__main__":
    crawl_meta()
