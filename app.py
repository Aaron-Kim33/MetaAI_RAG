import os
import time
import random
import re
import chromadb
import ollama
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

# 1. 경로 및 DB 설정
DATA_DIR = "/app/data"
CHROMA_PATH = os.path.join(DATA_DIR, "chroma_db")
URL_LOG_PATH = os.path.join(DATA_DIR, "visited_urls.txt")

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="meta_knowledge_base")

def load_visited_urls():
    if os.path.exists(URL_LOG_PATH):
        with open(URL_LOG_PATH, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_visited_url(url):
    with open(URL_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(url + "\n")

visited_urls = load_visited_urls()

def is_valid_help_url(url):
    url_lower = url.lower()
    
    # 1. 제외 확장자 (동일)
    if any(ext in url_lower for ext in ['.pdf', '.jpg', '.png', '.jpeg', '.mp4']): 
        return False

    parsed = urlparse(url_lower)
    query_params = parsed.query.lower()
    
    # 2. 메타 도메인 확인
    is_meta_domain = "facebook.com" in parsed.netloc or "fb.com" in parsed.netloc
    if not is_meta_domain: return False

    # 3. ⭐️ 강력한 언어 필터링
    # A. 한국어 서브도메인 혹은 기본 도메인(www, business) 허용
    allowed_subdomains = ["ko-kr.", "www.", "business."]
    is_allowed_sub = any(sub in parsed.netloc for sub in allowed_subdomains) or parsed.netloc == "facebook.com"
    
    # B. 타국어 서브도메인 차단 (예: pl-pl, nl-nl 등은 여기서 걸러짐)
    # 서브도메인이 5글자 형태(xx-xx.)인데 allowed에 없으면 차단
    if "-" in parsed.netloc.split('.')[0] and not parsed.netloc.startswith("ko-kr"):
        return False

    # C. 주소창 파라미터 확인 (locale이 붙어있을 경우 ko_kr만 허용)
    if "locale=" in query_params and "ko_kr" not in query_params:
        return False

    # 4. 경로 확인 (동일)
    is_help_path = "/help/" in parsed.path or "/business/help/" in parsed.path

    return is_help_path and is_allowed_sub

# 2. Playwright 기반 학습 함수
def auto_learn(start_url):
    with sync_playwright() as p:
        # 브라우저 실행 (headless=True로 백그라운드 실행)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        page = context.new_page()
        
        to_visit = [start_url]
        current_idx = 0

        print(f"\n🕵️ Playwright 엔진 가동 (현재 지식: {collection.count()}개)")

        while to_visit:
            current_url = to_visit.pop(0).split('#')[0]
            if current_url in visited_urls: continue
            
            current_idx += 1
            print(f"\n📊 [{current_idx}번째 학습 시도] 대기열: {len(to_visit)}")
            
            try:
                # 페이지 접속 및 대기
                print(f"🔗 접속 중: {current_url}")
                page.goto(current_url, wait_until="networkidle", timeout=60000)
                
                # 자바스크립트 렌더링 완료를 위해 추가 대기
                time.sleep(3) 
                
                # 전체 HTML 가져오기
                html = page.content()
                soup = BeautifulSoup(html, 'lxml')
                
                # 본문 추출
                content = soup.get_text(separator=' ', strip=True)
                print(f"📝 본문 길이: {len(content)} 자")

                # 수정 후 (나중에 적용할 것):
                if len(content) > 500:
                    # --- 여기서부터 맥락 보존형 청크 로직 시작 ---
                    chunks = []
                    size, overlap, start = 700, 100, 0
                    while start < len(content):
                        end = start + size
                        if end >= len(content):
                            chunks.append(content[start:])
                            break
                        last_period = content.rfind('.', start, end)
                        if last_period != -1 and last_period > start + (size // 2):
                            end = last_period + 1
                        chunks.append(content[start:end])
                        start = end - overlap
                    # --- 로직 끝 ---

                    for i, chunk in enumerate(chunks):
                        collection.add(
                            documents=[chunk],
                            metadatas=[{"source": current_url}],
                            ids=[f"{current_url}_{i}"]
                        )
                    visited_urls.add(current_url)
                    save_visited_url(current_url)
                    print(f"✅ 저장 성공 ({len(chunks)}개 조각)")

                    # 새로운 링크 수집
                    new_added = 0
                    for link in soup.find_all('a', href=True):
                        full_url = urljoin(current_url, link['href']).split('#')[0]
                        if is_valid_help_url(full_url) and full_url not in visited_urls:
                            if full_url not in to_visit:
                                to_visit.append(full_url)
                                new_added += 1
                    print(f"➕ 새로 발견된 링크: {new_added}개")
                else:
                    print("⚠️ 본문 부족 스킵 (렌더링 미완료 혹은 차단)")

            except Exception as e:
                print(f"❌ 에러: {e}")
            
            # 매너 대기
            time.sleep(random.uniform(2, 4))

        browser.close()

# 3. 답변 생성 (RAG)
def ask_a1(question, client):
    try:
        # 1. 문자열 변환 및 특수문자 제거
        raw_text = str(question[0]) if isinstance(question, list) else str(question)
        
        # 'clean_question'으로 이름을 통일합니다.
        clean_question = re.sub(r'[^가-힣a-zA-Z0-9\s.?!\'\"%]', '', raw_text).strip()

        print(f"DEBUG: 정제된 질문 -> '{clean_question}' (Type: {type(clean_question)})")

        if not clean_question:
            return "질문이 비어있습니다."

        # 2. 컬렉션 로드 (학습 시와 동일한 이름 확인)
        curr_collection = chroma_client.get_or_create_collection(name="meta_knowledge_base")
        
        # 3. 쿼리 실행
        results = curr_collection.query(
            query_texts=[clean_question], 
            n_results=3
        )
        
        if not results['documents'] or not results['documents'][0]:
            return "죄송합니다. 관련 정책 지식을 찾지 못했습니다."

        # 4. Ollama 답변 생성 (여기서 clean_question을 사용함)
        context = "\n".join(results['documents'][0])
        prompt = f"당신은 메타 정책 전문가입니다. 참고 자료를 바탕으로 질문에 '한국어'로만 친절하게 답하세요.\n\n참고 자료:\n{context}\n\n질문: {clean_question}"
        
        client = ollama.Client(host='http://host.docker.internal:11434')
        response = client.chat(model='llama3.2', messages=[
            {'role': 'user', 'content': prompt},
        ])
        
        return response['message']['content']

    except Exception as e:
        import traceback
        print(traceback.format_exc()) # 상세 에러 출력
        return f"답변 생성 중 오류 발생: {str(e)}"

if __name__ == "__main__":
    # Ollama 클라이언트 설정 (로컬 구동 시 기본 호스트 사용 가능)
    # 도커 내부에서 외부 Ollama 접근 시 host.docker.internal 사용
    print("🤖 Playwright 기반 A1 시스템 온라인 (48,515개 지식 장착 완료)")

    while True:
        user_input = input("\n💬 질문 혹은 'autostudy [URL]' (종료: exit): ").strip()
        if user_input.lower() == 'exit': break
        if not user_input: continue
        
        if user_input.startswith("autostudy "):
            url = user_input.split(" ")[1]
            auto_learn(url)
        else:
            print("\n🔍 검색 및 답변 생성 중...")
            # ask_a1 함수 내에서 chroma_client를 전역으로 쓰거나 인자로 넘겨야 합니다.
            answer = ask_a1(user_input, None) 
            print(f"\n--- [ A1 답변 ] ---\n{answer}")