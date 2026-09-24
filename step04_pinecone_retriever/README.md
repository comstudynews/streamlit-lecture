# Step 04 - Pinecone Retriever

## 목표
- 테스트 문서를 Chunk로 나눕니다.
- OpenAI Embedding으로 Vector를 만듭니다.
- Pinecone Index에 적재합니다.
- Retriever로 관련 문서를 검색합니다.

## 최초 1회
```bash
python step04_pinecone_retriever/complete/prepare_index.py
```

## 검색 테스트
```bash
python step04_pinecone_retriever/complete/retriever_demo.py
```

같은 Index에 다른 Embedding 모델을 섞어 사용하지 마세요.
