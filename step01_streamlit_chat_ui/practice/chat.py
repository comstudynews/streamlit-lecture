import streamlit as st

# TODO 1: 페이지 제목과 아이콘을 설정하세요.
st.set_page_config(page_title="TODO", page_icon="💬")

# TODO 2: 제목과 설명을 표시하세요.
st.title("TODO")
st.caption("TODO")

# TODO 3: st.chat_input()으로 질문을 입력받으세요.
user_question = None

if user_question:
    # TODO 4: 사용자 메시지를 chat_message로 표시하세요.
    st.write(user_question)
