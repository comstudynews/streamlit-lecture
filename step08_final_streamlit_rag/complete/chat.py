from uuid import uuid4

import streamlit as st

from llm import get_ai_response

st.set_page_config(page_title="Streamlit RAG 챗봇", page_icon="🤖")

st.title("🤖 Streamlit RAG 챗봇")
st.caption("Pinecone 검색과 대화 이력을 사용하는 단계별 실습 완성본입니다.")

if "message_list" not in st.session_state:
    st.session_state.message_list = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_question := st.chat_input("질문을 입력하세요."):
    with st.chat_message("user"):
        st.write(user_question)

    st.session_state.message_list.append(
        {"role": "user", "content": user_question}
    )

    with st.chat_message("assistant"):
        with st.spinner("답변을 생성하는 중입니다..."):
            response_stream = get_ai_response(
                user_question,
                st.session_state.session_id,
            )
            ai_message = st.write_stream(response_stream)

    st.session_state.message_list.append(
        {"role": "assistant", "content": ai_message}
    )
