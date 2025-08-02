import streamlit as st
import google.generativeai as genai
import PyPDF2
import os
import random
import requests
from datetime import datetime

# Load Gemini API key securely
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# Set up page configuration
st.set_page_config(page_title="FinAssist AI", layout="wide")

# Light/Dark Neon Theme Toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

toggle = st.sidebar.checkbox("🌗 Toggle Neon Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = toggle
theme = "dark" if toggle else "light"
bg_color = "#0f0f0f" if theme == "dark" else "#f9f9f9"
text_color = "#39FF14" if theme == "dark" else "#000000"

# Apply custom style
st.markdown(f"""
    <style>
    body {{ background-color: {bg_color}; color: {text_color}; }}
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📊 FinAssist Menu")
section = st.sidebar.radio("Choose a feature:", [
    "🤖 Chatbot", "📄 PDF Summarizer", "🧮 Tax Calculator", "🏦 EMI Calculator",
    "💰 FD Calculator", "📚 Finance Tips", "🧠 Fun Facts", "ℹ️ About"
])

# GPT-style Chatbot using Hugging Face (IBM model)
if section == "🤖 Chatbot":
    st.title("💬 FinAssist AI Chatbot")
    st.caption("Powered by IBM Granite - Ask any finance-related question!")

    HF_API_KEY = "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"  # replace with your own if needed
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    model = "ibm-granite/granite-3b-instruct-v1"
    user_input = st.text_input("💡 Ask me anything about finance...")

    if st.button("Send") and user_input:
        with st.spinner("Thinking..."):
            payload = {
                "inputs": user_input,
                "parameters": {"max_new_tokens": 150}
            }
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{model}",
                headers=headers,
                json=payload
            )
            result = response.json()
            if "error" in result:
                st.error("❌ Error: " + result["error"])
            else:
                answer = result[0]["generated_text"].split(user_input)[-1]
                st.success("🧠 FinAssist Says:")
                st.write(answer)

# PDF Upload + Gemini Summarizer
elif section == "📄 PDF Summarizer":
    st.title("📄 Upload PDF for Summary")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        st.subheader("🔍 PDF Content Extracted:")
        st.text_area("📘 Extracted Text", text, height=200)

        if st.button("🧠 Summarize with Gemini"):
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(f"Summarize this financial/legal document:\n\n{text}")
            st.subheader("📌 Summary:")
            st.success(response.text)

# Tax Calculator
elif section == "🧮 Tax Calculator":
    st.title("🧾 Tax Calculator (India - Old Regime)")
    income = st.number_input("Enter your annual income (₹)", min_value=0)

    if st.button("Calculate Tax"):
        tax = 0
        slabs = [(250000, 0), (500000, 0.05), (1000000, 0.2), (float('inf'), 0.3)]
        prev_limit = 0
        for limit, rate in slabs:
            if income > limit:
                tax += (limit - prev_limit) * rate
                prev_limit = limit
            else:
                tax += (income - prev_limit) * rate
                break
        st.success(f"Estimated Tax Payable: ₹{tax:,.2f}")

# EMI Calculator
elif section == "🏦 EMI Calculator":
    st.title("🏦 EMI Calculator")
    loan_amount = st.number_input("Loan Amount (₹)", min_value=0.0)
    interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)
    loan_tenure = st.number_input("Tenure (Years)", min_value=0.0)

    if st.button("Calculate EMI"):
        r = interest_rate / (12 * 100)
        n = loan_tenure * 12
        if r == 0:
            emi = loan_amount / n
        else:
            emi = loan_amount * r * ((1 + r)**n) / (((1 + r)**n) - 1)
        st.success(f"Estimated Monthly EMI: ₹{emi:,.2f}")

# FD Calculator
elif section == "💰 FD Calculator":
    st.title("💰 Fixed Deposit Calculator")
    principal = st.number_input("Principal Amount (₹)", min_value=0.0)
    rate = st.number_input("Interest Rate (%)", min_value=0.0)
    years = st.number_input("Time Period (Years)", min_value=0.0)
    frequency = st.selectbox("Compounding Frequency", ["Yearly", "Half-Yearly", "Quarterly", "Monthly"])

    freq_map = {"Yearly": 1, "Half-Yearly": 2, "Quarterly": 4, "Monthly": 12}
    n = freq_map[frequency]

    if st.button("Calculate FD Maturity"):
        maturity = principal * ((1 + (rate / (n * 100))) ** (n * years))
        st.success(f"Maturity Amount: ₹{maturity:,.2f}")

# Finance Tips
elif section == "📚 Finance Tips":
    st.title("📚 Smart Finance Tips")
    tips = [
        "Create a monthly budget to track spending.",
        "Start investing early to maximize compounding.",
        "Keep an emergency fund worth 3–6 months of expenses.",
        "Avoid high-interest debt like credit cards.",
        "Use credit responsibly to build a good credit score.",
        "Review your insurance coverage annually.",
        "Invest in diversified assets like mutual funds or ETFs.",
        "Automate savings and investments.",
        "Track net worth regularly.",
        "Don't chase quick profits—invest long-term."
    ]
    st.info(random.choice(tips))
    st.caption("🔁 Click refresh to see more!")

# Fun Facts
elif section == "🧠 Fun Facts":
    st.title("💸 Financial Fun Facts")
    facts = [
        "The first paper currency was created in China 1,400 years ago.",
        "Compound interest was referred to as the 8th wonder of the world by Einstein.",
        "Warren Buffett made 99% of his wealth after his 50s.",
        "India’s UPI handles billions of transactions every month.",
        "Credit cards were invented in the 1950s.",
        "The Indian Rupee symbol (₹) was officially adopted in 2010.",
        "Bitcoin was the first decentralized cryptocurrency, launched in 2009."
    ]
    st.success(random.choice(facts))
    st.caption("🔁 Click refresh to see more!")

# About Section
elif section == "ℹ️ About":
    st.title("ℹ️ About FinAssist")
    st.markdown("""
    **FinAssist** is your AI-powered finance assistant, built with ❤️ using Streamlit, Gemini, and Hugging Face.
    
    **Features:**
    - GPT-style AI finance chatbot (IBM Granite)
    - Financial tools (Tax, EMI, FD)
    - PDF financial document summarizer (Gemini)
    - Tips, facts, and light/dark neon theme

    _Developed for Hackathons, Startups, and Personal Finance Learners!_
    """)
