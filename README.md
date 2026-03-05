🤖 Project Meta-A1: Enterprise RAG Expert System
Apple Silicon(M1) 환경에서의 보안 우회 및 대규모 데이터 최적화 전문가 시스템

본 프로젝트는 메타(Meta) 비즈니스 도움말 데이터를 기반으로, 광고 정책 위반 및 계정 이슈에 즉각 대응할 수 있는 사내 전용 AI 전문가 시스템의 프로토타입입니다. 보안과 책임 소재가 명확한 기업용 AI 아키텍처를 지향합니다.

🏛️ System Vision: Private Multi-Agent
단순한 챗봇을 넘어, 기업 지식 자산의 보안성과 확장성을 동시에 확보한 아키텍처를 제안합니다.

1. 하이브리드 지식 구조 (Shared Brain + Private Agent)
Central Knowledge (Meta_brain): 전사 공통의 표준 지식 베이스. 수집된 고품질 정책 데이터를 모든 에이전트가 공유합니다.

Individual Agents (A1, A2...): 부서/개인별 특화 에이전트. 중앙의 Meta_brain을 참조하되, 개별 노하우를 추가 학습시켜 업무 효율을 극대화합니다.

Expected Value: 신입 사원은 즉시 표준 가이드를 활용하고, 숙련자는 자신만의 지식을 자산화할 수 있습니다.

2. 데이터 주권 및 보안 (On-premise Security)
Problem: 외부 AI 서비스 이용 시 기업 기밀 및 고객 데이터 유출 우려.

Solution: 폐쇄형 사내 네트워크 내 Docker와 Ollama를 활용한 온프레미스 구동. 모든 데이터는 사내 서버를 절대 벗어나지 않습니다.

3. 전문가 책임제 (Human-in-the-loop)
Role of AI: 방대한 문서 중 최적의 근거를 찾아주는 '고성능 보조자'.

Role of Human: AI 답변을 최종 검토 및 확정하는 주체. 답변 결과에 대한 귀책 사유를 명확히 하여 AI 과의존을 방지하고 전문성을 유지합니다.

🚀 Key Technical Challenges & Solutions
1. 보안 차단 및 동적 렌더링 극복 (Chromium Engine)
Problem: 메타 보안 시스템의 봇 탐지로 인한 접속 차단 및 JavaScript 동적 콘텐츠 렌더링 실패.

Solution: Playwright (Chromium) 기반 브라우저 자동화 도입. 실제 유저의 브라우징을 시뮬레이션하여 보안 시스템을 우회하고 수집 성공률 100% 달성.

2. 지식 관리의 진화 (Text File ➔ RAG)
Problem: 단일 텍스트 파일(txt) 방식의 한계(모델의 Context Window 초과 및 응답 지연).

Solution: ChromaDB (Vector Store) 기반 RAG 시스템 구축. 수만 개의 지식 조각 중 관련성 높은 데이터만 실시간 추출하여 정확도와 속도 동시 확보.

3. 환경 격리 및 플랫폼 최적화 (Docker)
Problem: Playwright 의존성 충돌 및 M1(arm64) 아키텍처 호환성 문제.

Solution: Docker 컨테이너화 및 --platform linux/amd64 빌드 전략 채택. 배포 범용성과 인프라 독립성을 확보했습니다.

4. 맥락 보존형 데이터 정제 (Context-Aware Chunking) ⭐️
Optimization: 700자 단위 Recursive Split + 100자 Overlap 전략 적용.

Benefit: 문장 중간이 끊기는 현상을 방지하고 조각 간 맥락을 연결하여, AI가 정책의 전후 사정을 정확히 파악하도록 설계했습니다.

💻 Hardware & Stack Optimization
Device: Apple M1 MacBook Air (8GB RAM)

Optimization: * 팬리스 환경의 발열 관리를 위해 headless 모드 및 디스플레이 절전 상태에서 백그라운드 학습 수행.

8GB 메모리 한계 내에서 최상의 퍼포먼스를 내는 Llama 3.2 (1B/3B) 모델 활용 및 최적화.

Stack: Python, Playwright, BeautifulSoup4, ChromaDB, Ollama, Docker.

📂 Project Structure
Plaintext
.
├── app.py              # Chromium 기반 크롤링 및 RAG 엔진 핵심 로직
├── Dockerfile          # Multi-platform 빌드 및 의존성 환경 설정
├── .gitignore          # 데이터 및 가상환경 유출 방지 설정
└── meta_brain/         # [Local Only] 데이터 영속성을 위한 볼륨 매핑
    ├── chroma_db/      # 10,000+ Vector Embeddings
    └── visited_urls.txt # 중복 수집 방지 필터링 로그
📈 Engineering Growth
보안 및 안티 크롤링 대응: 브라우저 엔진(Chromium)을 활용한 고급 동적 웹 핸들링 기술 습득.

데이터 아키텍처 설계: 비정형 데이터를 벡터 데이터로 구조화하여 검색 효율을 극대화하는 ETL 파이프라인 구축.

DevOps 최적화: 제한된 하드웨어 리소스(M1 Air) 내에서 Docker 기반 로컬 LLM 인프라 운용 경험 확보.

Note: The knowledge base (ChromaDB) is not included in this repository to protect data integrity. Run autostudy [URL] to build your own local database.