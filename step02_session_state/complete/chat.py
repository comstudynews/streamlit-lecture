import streamlit as st

st.set_page_config(page_title="RAG 챗봇", page_icon="🤖")
st.title("🤖 RAG 챗봇")
st.caption("Session State로 화면 대화를 유지합니다.")

if "message_list" not in st.session_state:
    st.session_state.message_list = []

for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_question := st.chat_input("질문을 입력하세요."):
    with st.chat_message("user"):
        st.write(user_question)

    st.session_state.message_list.append(
        {"role": "user", "content": user_question}
    )
