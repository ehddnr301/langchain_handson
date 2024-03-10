import json
import requests
import streamlit as st

st.set_page_config(page_title="점심 추천 서비스", page_icon="🍽️", layout="wide")

st.markdown(
    """
<style>
.big-font {
    font-size:20px !important;
}
</style>
""",
    unsafe_allow_html=True,
)


st.title("🍽️ 점심 추천 서비스")
st.markdown("##### 오늘 점심 뭐 먹을까요? 여기에 입력해보세요!")

with st.sidebar:
    st.info("이 서비스는 여러분의 점심 메뉴를 추천해드립니다.")
    st.markdown("추후 기능 추가 예정입니다.")

with st.form(key="my-form"):
    sentence = st.text_input(
        "문장을 입력하세요", "", help="점심에 대한 당신의 생각이나 조건을 입력해주세요."
    )
    submit = st.form_submit_button("제출")

if submit:
    res = requests.get("http://127.0.0.1:8881/sentences/" + sentence)

    if res.status_code == 200:
        food = res.text
        food = food.replace('"', "")

        st.write(f"답변이에요: {res.text}")

    else:
        st.error("Chatbot 서버에 접속할 수 없습니다. 서버를 확인해주세요.")
        st.stop()
