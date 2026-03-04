🤖 Project Meta-A1: Custom RAG Knowledge Base
Apple Silicon(M1) 환경에서의 보안 우회 및 대규모 데이터 최적화 전문가 시스템

📌 Project Overview
메타(Meta) 비즈니스 도움말 데이터를 수집하여, 광고 정책 위반 및 계정 비활성화 이슈에 즉각 대응할 수 있는 한국어 특화 AI 전문가를 구축했습니다. 초기 보안 차단 및 기술적 한계를 RAG 아키텍처와 브라우저 자동화 기술로 극복한 프로젝트입니다.

🚀 Key Technical Challenges & Solutions
1. 보안 차단 및 렌더링 이슈 해결: Static ➔ Browser Automation
Problem: 초기 requests 및 BeautifulSoup 조합으로 수집 시도 시, 메타의 보안 시스템에 의해 봇(Bot)으로 탐지되어 접속이 차단되거나 본문이 비어있는 상태로 수집되는 문제 발생.

Solution: **Playwright(Chromium Engine)**를 도입하여 실제 브라우저 환경을 시뮬레이션함.

Result: JavaScript 기반의 동적 콘텐츠를 완전히 렌더링한 후 데이터를 추출함으로써 보안 차단을 우회하고 수집 성공률을 100%로 끌어올림.

2. 지식 관리 방식의 진화: Text File ➔ RAG (Vector DB)
Problem: 초기 metahelpcenter.txt 단일 파일 방식은 데이터 증가 시 모델의 Context Window 한계로 인해 정보 누락 및 응답 지연 발생.

After (RAG 채택): **ChromaDB(Vector Store)**를 도입하여 질문과 가장 관련 있는 정보만 실시간으로 추출해 제공하는 아키텍처로 전환.

3. 환경 격리의 진화: venv ➔ Docker (Multi-Platform)
Problem: Playwright의 복잡한 의존성 설치 문제와 M1 환경에서의 아키텍처 호환성 문제 발생.

After (Docker): 컨테이너화를 통해 인프라 독립성 확보. 특히 M1(arm64) 환경에서 범용성을 위해 --platform linux/amd64 빌드 전략을 채택하여 배포 안정성 검증.

4. 데이터 정제 전략: Context-Aware Chunking ⭐️
After: 700자 단위 Recursive Split + 100자 Overlap 전략 적용.

Benefit: 문장 단위 보존과 조각 간의 중첩을 통해 AI가 끊김 없는 맥락(Context)을 이해하도록 설계.

💻 Hardware & Stack Optimization
Device: Apple M1 MacBook Air (8GB RAM)

Optimization: * 팬리스 환경의 발열 관리를 위해 headless 모드 활용 및 디스플레이 절전 상태에서 백그라운드 학습 수행.

8GB 메모리 제한 내에서 최상의 성능을 내는 Llama 3.2 (1B/3B) 모델 활용.

Stack: Python, Playwright (Chromium), BeautifulSoup4, ChromaDB, Ollama, Docker.

📂 Project Structure
Plaintext
.
├── app.py              # Chromium 기반 크롤링 및 RAG 엔진
├── Dockerfile          # Multi-platform 빌드 및 Playwright 환경 설정
└── meta_brain/         # 데이터 영속성 확보를 위한 볼륨 매핑
    ├── chroma_db/      # 벡터 지식 저장소
    └── visited_urls.txt # 중복 수집 방지 필터링 로그
📈 Engineering Growth
보안 및 안티 크롤링 대응: 단순 API 호출이 아닌, 브라우저 엔진(Chromium)을 활용한 동적 웹 핸들링 기술 습득.

아키텍처 설계 역량: 데이터 크기에 따른 검색 알고리즘 변화의 필요성을 체득하고 RAG 구조로 고도화.

DevOps 및 최적화: M1 Air라는 제한된 하드웨어 리소스 내에서 Docker 환경 최적화 및 로컬 LLM 운용 경험 확보.

"Note: The knowledge base (ChromaDB) is not included in this repository. Run autostudy [URL] to build your own local database."