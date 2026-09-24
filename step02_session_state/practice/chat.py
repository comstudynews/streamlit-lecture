import streamlit as st

st.set_page_config(page_title="RAG 챗봇", page_icon="🤖")
st.title("🤖 RAG 챗봇")

# TODO 1: message_list가 없으면 빈 리스트를 만드세요.

# TODO 2: 이전 메시지를 화면에 다시 출력하세요.

if user_question := st.chat_input("질문을 입력하세요."):
    with st.chat_message("user"):
        st.write(user_question)

    # TODO 3: 새 사용자 메시지를 session_state에 저장하세요.
