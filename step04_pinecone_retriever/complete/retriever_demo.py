import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

index_name = os.getenv("PINECONE_INDEX_NAME", "streamlit-rag-demo")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings,
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

question = "RAG에서 Retriever는 무슨 일을 하나요?"
docs = retriever.invoke(question)

print("질문:", question)
for i, doc in enumerate(docs, 1):
    print(f"\n===== 검색 결과 {i} =====")
    print(doc.page_content)
