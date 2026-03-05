🤖 Project Meta-A1: Enterprise RAG Expert System
Apple Silicon(M1) 환경에서의 대규모 데이터(48k+) 처리 및 로컬 LLM 최적화 전문가 시스템

본 프로젝트는 메타(Meta) 비즈니스 도움말 데이터를 기반으로, 광고 정책 위반 및 계정 이슈에 즉각 대응할 수 있는 사내 전용 AI 전문가 시스템의 프로토타입입니다. 8GB RAM이라는 극한의 하드웨어 제약 조건 속에서 48,515개의 지식 베이스를 구축하고 로컬 추론을 성공시킨 엔지니어링 기록을 담고 있습니다.

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

🚀 Key Technical Challenges & Troubleshooting (Updated)
1. 48,000+ 대규모 지식 베이스 구축 ⭐️
Challenge: 단일 도메인을 넘어 방대한 메타 정책 데이터를 중복 없이, 누락 없이 수집해야 함.

Solution: Playwright 기반의 재귀적 크롤링 엔진을 설계하여 총 48,515개의 고유 정책 문서를 수집. visited_urls.txt를 통한 필터링으로 데이터 무결성 확보.

2. 하드웨어 제약(M1 8GB RAM) 극복 및 모델 최적화
Problem: 8B 파라미터 모델(Llama 3.1) 구동 시 시스템 메모리 부족으로 인한 터미널 강제 종료(OOM) 현상 발생.

Solution: 추론 엔진을 Llama 3.2 3B 및 1B로 최적화하여 8GB 환경에서도 안정적인 답변 루프 구현. 성능과 안정성 사이의 Trade-off를 고려한 모델 벤치마킹 수행.

3. Docker-Host 간 네트워크 및 통신 최적화
Problem: Docker 컨테이너 내부의 Python 엔진이 macOS 로컬에 구동 중인 Ollama 서버와 통신하지 못하는 문제.

Solution: host.docker.internal 브릿지 네트워크 설정 및 --add-host 실행 옵션을 적용하여 컨테이너-호스트 간 원활한 API 통신 인프라 구축.

4. 입력 데이터 전처리 및 타입 정제 (TextInputSequence Error)
Problem: 특수 문자나 인코딩 이슈가 포함된 질문 입력 시 ChromaDB 임베딩 엔진(ONNX)에서 TypeError 발생.

Solution: 정규표현식(re)을 활용한 입출력 전처리 로직을 ask_a1 함수에 통합하여 데이터 정제 프로세스 강화.

📊 Current Limitations & Future Work
본 프로젝트는 로컬 환경의 한계를 명확히 인지하고 이를 기록으로 남깁니다.

모델 체급의 한계: 1B/3B 모델의 경우 한국어 추론 및 복잡한 정책 요약 시 할루시네이션(환각) 현상이 관찰됨.

데이터 노이즈: 대규모 수집 과정에서 포함된 HTML 잔재가 답변 퀄리티에 영향을 미침.

향후 과제: 고사양 GPU 서버 도입 또는 OpenAI API 하이브리드 운영을 통한 답변 정밀도 향상, 데이터 전처리(Data Cleaning) 파이프라인 고도화 예정.

🛠 Tech Stack (Updated)
Language: Python 3.10

Database: ChromaDB (Vector Store)

LLM Engine: Ollama (Llama 3.2 1B/3B, Llama 3.1 8B)

Infrastructure: Docker (Platform: linux/amd64)

Automation: Playwright (Chromium)

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

