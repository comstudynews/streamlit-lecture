import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

dictionary = [
    "문서 찾기 -> 문서 검색",
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

llm = ChatOpenAI(
    model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o"),
    temperature=0,
)

chain = prompt | llm | StrOutputParser()

question = "관련 문서를 어떻게 찾나요?"
print("입력 :", question)
print("출력 :", chain.invoke({"question": question}))
