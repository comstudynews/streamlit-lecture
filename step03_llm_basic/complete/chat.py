import streamlit as st

from llm import get_llm

st.set_page_config(page_title="LLM 챗봇", page_icon="🤖")
st.title("🤖 LLM 챗봇")
st.caption("아직 문서 검색을 하지 않는 기본 LLM 단계입니다.")

if "message_list" not in st.session_state:
    st.session_state.message_list = []

for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_question := st.chat_input("질문을 입력하세요."):
    st.session_state.message_list.append(
        {"role": "user", "content": user_question}
    )
    with st.chat_message("user"):
        st.write(user_question)

    with st.chat_message("assistant"):
        with st.spinner("답변을 생성하는 중입니다..."):
            answer = get_llm().invoke(user_question).content
            st.write(answer)

    st.session_state.message_list.append(
        {"role": "assistant", "content": answer}
    )
