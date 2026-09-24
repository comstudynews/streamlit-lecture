import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


def get_llm(model=None):
    model = model or os.getenv("OPENAI_CHAT_MODEL", "gpt-4o")
    return ChatOpenAI(model=model, temperature=0)


if __name__ == "__main__":
    llm = get_llm()
    response = llm.invoke("RAG를 한 문장으로 설명해 주세요.")
    print(response.content)
