import streamlit as st
import pdfplumber
import requests
import re

API_KEY = st.secrets["API_BBB"]

def detect_language(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return "arabic"
    return "english"

def summarize_text(text):
    lang = detect_language(text)

    system_msg = (
        "لخّص النص التالي باللغة العربية فقط."
        if lang == "arabic"
        else "Summarize the text in English only."
    )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    return result["choices"][0]["message"]["content"]


st.set_page_config(page_title="HR Brief AI", layout="wide")

st.title("HR Brief AI")
st.write("### أداة تلخيص تقارير الموارد البشرية باستخدام الذكاء الاصطناعي")

st.write("#### التقرير الأول")
file1 = st.file_uploader("ارفع تقرير PDF الأول هنا", type=["pdf"], key="pdf1")

if file1:
    with pdfplumber.open(file1) as pdf:
        text = ""
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"

    summary1 = summarize_text(text)
    st.write("## ملخص التقرير الأول")
    st.write(summary1)

st.write("---")

if "second_reports" not in st.session_state:
    st.session_state["second_reports"] = []

if st.button("تلخيص تقرير ثاني"):
    st.session_state["second_reports"].append(None)

for i in range(len(st.session_state["second_reports"])):
    st.write(f"#### التقرير الثاني رقم {i+1}")
    file2 = st.file_uploader(
        "ارفع هنا تقرير PDF",
        type=["pdf"],
        key=f"pdf2_{i}"
    )

    if file2:
        with pdfplumber.open(file2) as pdf:
            text2 = ""
            for page in pdf.pages:
                t2 = page.extract_text()
                if t2:
                    text2 += t2 + "\n"

        summary2 = summarize_text(text2)
        st.write(f"## ملخص التقرير الثاني رقم {i+1}")
        st.write(summary2)

    st.write("---")
