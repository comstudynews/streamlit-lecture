# Step 08 - Final Streamlit RAG

## 목표
Streamlit UI, 질문 정규화, History-aware Retriever, Pinecone RAG, 대화 이력, Streaming을 통합합니다.

## 실행
```bash
python -m streamlit run step08_final_streamlit_rag/complete/chat.py
```

## 테스트
1. 첫 질문을 입력합니다.
2. 두 번째 질문에서 "그 경우", "그 과정"처럼 앞 문맥을 생략합니다.
3. 이전 문맥을 반영해 답하는지 확인합니다.
