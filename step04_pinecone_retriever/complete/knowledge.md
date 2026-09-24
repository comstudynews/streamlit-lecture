# RAG 기본 개념

RAG는 Retrieval-Augmented Generation의 약자이다.
사용자의 질문과 관련된 문서를 먼저 검색한 뒤, 검색된 문서를 LLM의 Context로 제공한다.

Retriever는 질문과 관련된 문서를 찾는 역할을 한다.
LLM은 검색된 문서를 읽고 자연어 답변을 생성하는 역할을 한다.

Vector Store는 문서를 Embedding Vector와 함께 저장하고 유사도 검색을 수행한다.
