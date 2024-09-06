from openai import OpenAI
import streamlit as st

st.title("친구를 만들어보세요!")

# 사용자로부터 API 키 입력 받기
api_key = st.text_input("API 키를 입력하세요:", type="password")

if api_key:
    st.session_state["api_key"] = api_key

# API 클라이언트 초기화
if "api_key" in st.session_state:
    client = OpenAI(api_key=st.session_state["api_key"])


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if "api_key" in st.session_state:
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="ft:gpt-3.5-turbo-0125:personal::A4TNlPTJ",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
