import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
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


def get_llm():
    return ChatOpenAI(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o"),
        temperature=0,
    )


def get_retriever():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore = PineconeVectorStore.from_existing_index(
        index_name=os.getenv("PINECONE_INDEX_NAME", "streamlit-rag-demo"),
        embedding=embeddings,
    )
    return vectorstore.as_retriever(search_kwargs={"k": 3})


def get_dictionary_chain():
    dictionary = [
        "사람을 나타내는 일반 표현 -> 거주자",
    ]

    prompt = ChatPromptTemplate.from_template(
        """
사용자의 질문을 보고 아래 사전을 참고하여 검색하기 좋은 질문으로 바꾸세요.
변경이 필요하지 않으면 원래 질문을 그대로 반환하세요.
설명은 붙이지 말고 질문만 반환하세요.

사전:
{dictionary}

질문:
{question}
""".strip()
    ).partial(dictionary="\n".join(dictionary))

    return prompt | get_llm() | StrOutputParser()


def get_history_retriever():
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "이전 대화와 최신 질문을 보고, 이전 대화 없이도 이해할 수 있는 "
            "독립적인 검색 질문으로 다시 작성하세요. 답변하지 말고 질문만 반환하세요.",
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    return create_history_aware_retriever(
        get_llm(),
        get_retriever(),
        prompt,
    )


def get_few_shot_prompt():
    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "{input}"),
        ("ai", "{answer}"),
    ])
    return FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=answer_examples,
    )


def get_conversational_rag_chain():
    qa_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "당신은 제공된 문서를 바탕으로 질문에 답하는 도우미입니다. "
            "반드시 검색된 Context를 우선 근거로 사용하세요. "
            "Context에서 확인할 수 없으면 확인할 수 없다고 답하세요.\n\n"
            "Context:\n{context}",
        ),
        get_few_shot_prompt(),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    qa_chain = create_stuff_documents_chain(
        get_llm(),
        qa_prompt,
    )
    rag_chain = create_retrieval_chain(
        get_history_retriever(),
        qa_chain,
    )

    history_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    return history_chain.pick("answer")


def get_ai_response(user_message: str, session_id: str):
    dictionary_chain = get_dictionary_chain()
    rag_chain = get_conversational_rag_chain()

    full_chain = {"input": dictionary_chain} | rag_chain

    return full_chain.stream(
        {"question": user_message},
        config={"configurable": {"session_id": session_id}},
    )
