# Step 03 - OpenAI LLM

## 목표
- `.env`에서 API Key와 모델명을 읽습니다.
- `ChatOpenAI`를 Streamlit 채팅 UI와 연결합니다.

## 준비
루트의 `.env.example`을 `.env`로 복사하고 API Key를 입력하세요.

## LLM 단독 테스트
```bash
python step03_llm_basic/complete/llm.py
```

## Streamlit 실행
```bash
python -m streamlit run step03_llm_basic/complete/chat.py
```
