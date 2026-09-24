import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from config import answer_examples

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


class InMemoryHistory(BaseChatMessageHistory):
    def __init__(self):
        self.messages: list[BaseMessage] = []

    def add_messages(self, messages: list[BaseMessage]) -> None:
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []


store: dict[str, InMemoryHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]


llm = ChatOpenAI(
    model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o"),
    temperature=0,
)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = PineconeVectorStore.from_existing_index(
    index_name=os.getenv("PINECONE_INDEX_NAME", "streamlit-rag-demo"),
    embedding=embeddings,
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

contextualize_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "이전 대화와 최신 질문을 보고 독립적인 검색 질문으로 다시 작성하세요. "
        "답변하지 말고 질문만 반환하세요.",
    ),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_prompt
)

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{answer}"),
])
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=answer_examples,
)

qa_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "제공된 Context를 우선 근거로 답하세요. "
        "Context에서 확인할 수 없으면 확인할 수 없다고 답하세요.\n\n"
        "Context:\n{context}",
    ),
    few_shot_prompt,
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

qa_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

history_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

session_id = "demo-session"

for question in [
    "RAG의 전체 흐름을 설명해 주세요.",
    "그 과정에서 Retriever는 무엇을 하나요?",
]:
    result = history_chain.invoke(
        {"input": question},
        config={"configurable": {"session_id": session_id}},
    )
    print("\nQ:", question)
    print("A:", result["answer"])
