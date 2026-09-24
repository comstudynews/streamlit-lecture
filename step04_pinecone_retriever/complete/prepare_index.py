import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

index_name = os.getenv("PINECONE_INDEX_NAME", "streamlit-rag-demo")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_dimension = len(embeddings.embed_query("dimension check"))

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=vector_dimension,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        timeout=120,
    )

index_info = pc.describe_index(index_name)
existing_dimension = getattr(index_info, "dimension", None)
if existing_dimension is not None and existing_dimension != vector_dimension:
    raise ValueError(
        f"Index dimension={existing_dimension}, "
        f"Embedding dimension={vector_dimension}. "
        "같은 Embedding 모델로 만든 Index를 사용하세요."
    )

text = (BASE_DIR / "knowledge.md").read_text(encoding="utf-8")
document = Document(
    page_content=text,
    metadata={"source": "knowledge.md"},
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
chunks = splitter.split_documents([document])

vectorstore = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings,
)

chunk_ids = [f"knowledge-{i}" for i in range(len(chunks))]
vectorstore.add_documents(documents=chunks, ids=chunk_ids)

print("Index 준비 완료:", index_name)
print("Embedding dimension:", vector_dimension)
print("적재 Chunk 수:", len(chunks))
