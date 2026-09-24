# Streamlit + LangChain RAG Chatbot - Step by Step

Streamlit 채팅 UI에서 시작해 OpenAI, Pinecone, LangChain RAG, 대화 이력, Few-shot Prompt를 단계적으로 연결하는 실습 저장소입니다.

이 저장소는 공개 예제 `jasonkang14/inflearn-streamlit-lecture`의 학습 아이디어를 참고하되, 코드는 현재 패키지 구조에 맞게 교육용으로 다시 구성했습니다.

## 실습 방식

각 Step은 앞 단계에서 배운 내용을 누적해 확장합니다.

- `practice/`: 해당 단계의 핵심 부분을 직접 완성하도록 `TODO`를 둔 실습 코드
- `complete/`: 해당 단계까지 구현된 완성 코드
- 처음 학습할 때는 Step 01부터 순서대로 진행하는 것을 권장합니다.

## 전체 흐름

| Step | 주제 | 핵심 내용 |
|---|---|---|
| 01 | Streamlit Chat UI | `st.chat_input`, `st.chat_message` |
| 02 | Session State | 화면 채팅 이력 유지 |
| 03 | OpenAI LLM | `ChatOpenAI`, 환경변수 |
| 04 | Pinecone Retriever | Index 생성, 문서 적재, 검색 |
| 05 | Dictionary Chain | 질문 용어 정규화, LCEL |
| 06 | History-aware Retriever | 이전 대화를 반영한 검색 질문 재작성 |
| 07 | Conversational RAG | Few-shot, Retrieval Chain, Message History |
| 08 | Final Streamlit RAG | Streamlit + RAG + Streaming 통합 |

## 검증 기준 환경

- Python 3.11 / 3.12
- Streamlit 1.64.0
- langchain-core 1.6.3
- langchain-classic 1.0.8
- langchain-openai 1.6.5
- langchain-pinecone 0.2.13
- langchain-text-splitters 1.1.2
- pinecone 7.3.0
- python-dotenv 1.2.3

검증 기준일: 2026-09-24

## 빠른 시작

```bash
git clone https://github.com/comstudynews/streamlit-lecture.git
cd streamlit-lecture
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

패키지 설치:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
```

환경변수 파일 생성:

Windows:

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

`.env`에 본인의 API Key를 입력합니다.

```text
OPENAI_API_KEY=...
PINECONE_API_KEY=...
PINECONE_INDEX_NAME=streamlit-rag-demo
OPENAI_CHAT_MODEL=gpt-4o
```

> API Key는 절대 GitHub에 커밋하지 않습니다.

## Step 04부터 필요한 Pinecone 준비

Step 04 완성본에는 원본 예제에 없던 **Index 생성 + 문서 적재 코드**를 추가했습니다.

```bash
python step04_pinecone_retriever/complete/prepare_index.py
python step04_pinecone_retriever/complete/retriever_demo.py
```

이후 Step에서도 같은 Pinecone Index를 재사용합니다.

## 최종 앱 실행

```bash
python -m streamlit run step08_final_streamlit_rag/complete/chat.py
```

브라우저에서 Streamlit이 안내하는 Local URL을 엽니다.

## 최종 프로젝트 흐름

```text
사용자 질문
  ↓
Streamlit Chat UI
  ↓
Dictionary Chain
  ↓
History-aware Retriever
  ↓
Pinecone Vector Search
  ↓
Few-shot Prompt + 검색 Context
  ↓
ChatOpenAI
  ↓
RunnableWithMessageHistory
  ↓
Streaming Response
```

## 디버깅 순서

전체 앱이 한 번에 동작하지 않을 때는 다음 순서로 확인합니다.

1. `python --version`
2. `python -m pip check`
3. `.env`의 API Key
4. `python step03_llm_basic/complete/llm.py`
5. `python step04_pinecone_retriever/complete/prepare_index.py`
6. `python step04_pinecone_retriever/complete/retriever_demo.py`
7. 최종 Streamlit 앱

## 주의사항

- 이 저장소의 테스트 문서는 RAG 동작 확인을 위한 일반 예시입니다.
- 실제 법률·세무·의료 등 전문 영역에 적용할 때는 최신 공식 문서를 별도로 검증해야 합니다.
- Pinecone Index를 다른 Embedding 모델로 만든 경우 현재 예제의 `text-embedding-3-large`와 Vector dimension이 일치하지 않을 수 있습니다.
- 현재 Message History는 Python 프로세스 메모리에 저장되므로 앱을 재시작하면 사라집니다.
- 운영 환경에서는 인증, 비용 제어, 로그 개인정보 제거, Redis/DB 기반 History 저장 등을 추가해야 합니다.

## 참고

- Original reference: https://github.com/jasonkang14/inflearn-streamlit-lecture
- Streamlit: https://docs.streamlit.io/
- LangChain: https://python.langchain.com/
- Pinecone: https://docs.pinecone.io/

이 저장소는 원본 저장소를 그대로 복제한 것이 아니라, 단계별 실습을 위해 새로 구성한 교육용 코드입니다.
