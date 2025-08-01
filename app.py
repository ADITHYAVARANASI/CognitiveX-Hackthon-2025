import streamlit as st
import os
import requests
import json
import google.generativeai as genai
import random

# Load secrets from Streamlit
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
NEWSDATA_API_KEY = st.secrets["NEWSDATA_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# Page config
st.set_page_config(page_title="FinBot - Your Finance Assistant", layout="wide")

# Theme toggle
theme = st.sidebar.radio("Choose Theme", ["🌞 Light", "🌚 Dark"])
neon_css = """
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: %s;
        color: %s;
    }
    .main-container {
        padding: 2rem;
        background: linear-gradient(145deg, %s, %s);
        border-radius: 20px;
        box-shadow: 0 0 25px rgba(0,255,200,0.2);
        margin: 20px;
    }
    .stButton>button {
        background-color: #0ff;
        color: black;
        font-weight: 600;
        border-radius: 12px;
        box-shadow: 0 0 8px #0ff;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00f7ff;
        box-shadow: 0 0 12px #00f7ff;
        color: black;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 700;
        font-size: 18px;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0ff;
        color: black;
        border-radius: 12px;
    }
    </style>
""" % (
    "#0d0d0d" if theme == "🌚 Dark" else "#f5faff",
    "#f0f0f0" if theme == "🌚 Dark" else "#000000",
    "#121212" if theme == "🌚 Dark" else "#ffffff",
    "#1a1a1a" if theme == "🌚 Dark" else "#f0f4ff"
)
st.markdown(neon_css, unsafe_allow_html=True)
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

# Logo and title
st.image("finbot_logo.png", width=60)
st.markdown("<h1 style='color:#0ff; font-weight:bold;'>FinBot - Your Finance Assistant</h1>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Tools", "🤖 AI Advisor", "📰 News", "🎓 Fun Facts"])

# Tab 1: Tools
with tab1:
    st.subheader("📌 Finance Tools")
    with st.expander("💰 Income Tax Calculator"):
        income = st.number_input("Enter your annual income (₹)", min_value=0)
        if st.button("Calculate Tax"):
            tax = 0
            if income <= 250000:
                tax = 0
            elif income <= 500000:
                tax = (income - 250000) * 0.05
            elif income <= 1000000:
                tax = (250000 * 0.05) + (income - 500000) * 0.2
            else:
                tax = (250000 * 0.05) + (500000 * 0.2) + (income - 1000000) * 0.3
            st.success(f"Estimated Tax: ₹{tax:,.2f}")

    with st.expander("🏦 EMI Calculator"):
        loan = st.number_input("Loan Amount (₹)", min_value=0)
        rate = st.number_input("Interest Rate (%)", min_value=0.0)
        tenure = st.number_input("Tenure (months)", min_value=1)
        if st.button("Calculate EMI"):
            monthly_rate = rate / (12 * 100)
            emi = loan * monthly_rate * ((1 + monthly_rate) ** tenure) / (((1 + monthly_rate) ** tenure) - 1)
            st.info(f"Monthly EMI: ₹{emi:,.2f}")

    with st.expander("📈 FD Returns"):
        fd_amount = st.number_input("FD Amount (₹)", min_value=0)
        fd_rate = st.number_input("Annual FD Rate (%)", value=6.5)
        fd_years = st.number_input("Duration (years)", value=1)
        if st.button("Calculate FD Returns"):
            maturity = fd_amount * ((1 + fd_rate / 100) ** fd_years)
            st.info(f"Maturity Amount: ₹{maturity:,.2f}")

# Tab 2: AI Advisor
with tab2:
    st.subheader("🤖 AI Financial Advisor & Summarizer")
    choice = st.selectbox("Choose a tool", ["Investment Advisor", "Financial Statement Summarizer", "Legal Document Summarizer"])
    user_input = st.text_area("Enter your query or paste document here")
    if st.button("Get AI Advice"):
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt_map = {
            "Investment Advisor": f"Act as an Indian financial investment advisor. Give suggestions for: {user_input}",
            "Financial Statement Summarizer": f"Summarize this financial document in simple Indian terms: {user_input}",
            "Legal Document Summarizer": f"Summarize this Indian financial legal document: {user_input}"
        }
        response = model.generate_content(prompt_map[choice])
        st.success(response.text)

# Tab 3: News
with tab3:
    st.subheader("📰 Latest Financial News")
    if st.button("🔁 Refresh News"):
        st.experimental_rerun()
    news_url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&q=finance&country=in&language=en&category=business"
    try:
        news_res = requests.get(news_url)
        news_data = news_res.json().get("results", [])[:5]
        for news in news_data:
            st.markdown("### " + news.get("title", "No title"))
            if news.get("image_url"):
                st.image(news["image_url"], use_column_width=True)
            st.markdown(news.get("description", "") or news.get("content", ""))
            st.markdown(f"[Read more]({news.get('link')})", unsafe_allow_html=True)
            st.markdown("---")
    except Exception as e:
        st.error(f"News loading failed: {e}")

# Tab 4: Fun Facts
with tab4:
    st.subheader("🎓 Did You Know?")
    facts = [
        "Jan Dhan Yojana holds the world record for most bank accounts opened in a week.",
        "UPI handles over 10 billion transactions monthly!",
        "Mutual funds in India crossed ₹50 lakh crore in 2025.",
        "India is among the top 3 fastest-growing digital banking markets.",
        "SIPs are the most trusted long-term investment tool among Gen Z investors."
    ]
    if st.button("🎲 Give Me a Fact"):
        st.info(random.choice(facts))

st.markdown("</div>", unsafe_allow_html=True)