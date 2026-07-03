import streamlit as st
import pdfplumber
import requests

API_KEY = st.secrets["API_BBB"]

def summarize_text(text):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are an AI specialized in summarizing HR reports."},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if "choices" not in result:
        return f"⚠️ خطأ من Groq Cloud:\n\n{result}"

    return result["choices"][0]["message"]["content"]


st.set_page_config(page_title="HR Brief AI", layout="wide")

st.title("HR Brief AI")
st.write("### أداة تلخيص تقارير الموارد البشرية باستخدام الذكاء الاصطناعي")

if "summaries" not in st.session_state:
    st.session_state["summaries"] = []

if "show_second_uploader" not in st.session_state:
    st.session_state["show_second_uploader"] = False


st.write("#### التقرير الأول")
uploaded_file_1 = st.file_uploader("ارفع تقرير PDF الأول هنا", type=["pdf"], key="uploader_1")

if uploaded_file_1:
    with pdfplumber.open(uploaded_file_1) as pdf:
        text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    st.write("### جاري تلخيص التقرير الأول...")
    summary_1 = summarize_text(text)
    st.session_state["summaries"].append(("التقرير الأول", summary_1))


for idx, (label, s) in enumerate(st.session_state["summaries"], start=1):
    st.write(f"## ملخص {label} (رقم {idx})")
    st.write(s)
    st.write("---")

-
st.write("### إذا أردت تلخيص تقرير ثاني:")
if st.button("تلخيص التقرير الثاني"):
    st.session_state["show_second_uploader"] = True


if st.session_state["show_second_uploader"]:
    st.write("#### التقرير الثاني")
    uploaded_file_2 = st.file_uploader("ارفع تقرير PDF الثاني هنا", type=["pdf"], key="uploader_2")

    if uploaded_file_2:
        with pdfplumber.open(uploaded_file_2) as pdf:
            text2 = ""
            for page in pdf.pages:
                extracted2 = page.extract_text()
                if extracted2:
                    text2 += extracted2 + "\n"

        st.write("### جاري تلخيص التقرير الثاني...")
        summary_2 = summarize_text(text2)
        st.session_state["summaries"].append(("التقرير الثاني", summary_2))

st.write("---")
st.write("**لحفظ الملخص كـ PDF اضغط: Ctrl + P**")
