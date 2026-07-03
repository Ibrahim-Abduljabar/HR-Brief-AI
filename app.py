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
        "model": "llama-3.1-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are an AI specialized in summarizing HR reports."},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    return result["choices"][0]["message"]["content"]

st.set_page_config(page_title="HR Brief AI", layout="wide")

st.title("HR Brief AI")
st.write("### أداة تلخيص تقارير الموارد البشرية باستخدام الذكاء الاصطناعي")

if "summaries" not in st.session_state:
    st.session_state["summaries"] = []

uploaded_file = st.file_uploader("ارفع تقرير PDF هنا", type=["pdf"])

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    st.write("### جاري تلخيص التقرير...")
    summary = summarize_text(text)

    st.session_state["summaries"].append(summary)


for idx, s in enumerate(st.session_state["summaries"]):
    st.write(f"## ملخص التقرير رقم {idx+1}")
    st.write(s)
    st.write("---")

st.write("### إذا أردت تلخيص تقرير آخر:")
st.button("تلخيص تقرير ثاني +")


st.write("---")
st.write("**لحفظ الملخص كـ PDF اضغط: Ctrl + P**")
