import streamlit as st

st.set_page_config(page_title="RAG 챗봇", page_icon="🤖")

st.title("🤖 RAG 챗봇")
st.caption("질문을 입력하면 채팅 형태로 표시합니다.")

user_question = st.chat_input(placeholder="질문을 입력하세요.")

if user_question:
    with st.chat_message("user"):
        st.write(user_question)
