import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


def get_llm(model=None):
    # TODO: OPENAI_CHAT_MODEL을 읽고 ChatOpenAI 객체를 반환하세요.
    raise NotImplementedError


if __name__ == "__main__":
    llm = get_llm()
    print(llm.invoke("RAG를 한 문장으로 설명해 주세요.").content)
