import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_classic.chains import create_history_aware_retriever
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = PineconeVectorStore.from_existing_index(
    index_name=os.getenv("PINECONE_INDEX_NAME", "streamlit-rag-demo"),
    embedding=embeddings,
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(
    model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o"),
    temperature=0,
)

contextualize_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "이전 대화와 최신 질문을 보고, 이전 대화 없이도 이해할 수 있는 "
        "독립적인 검색 질문으로 다시 작성하세요. 답변하지 말고 질문만 반환하세요.",
    ),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

history_retriever = create_history_aware_retriever(
    llm,
    retriever,
    contextualize_prompt,
)

chat_history = [
    HumanMessage(content="RAG의 전체 흐름을 설명해 주세요."),
    AIMessage(content="검색한 문서를 LLM의 Context로 제공해 답을 생성합니다."),
]

docs = history_retriever.invoke({
    "input": "그 과정에서 Retriever는 무엇을 하나요?",
    "chat_history": chat_history,
})

for i, doc in enumerate(docs, 1):
    print(f"\n===== 검색 결과 {i} =====")
    print(doc.page_content)
