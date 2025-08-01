import streamlit as st
import os
import requests
import json
import google.generativeai as genai
import random

# -------------------------
# Load secrets
# -------------------------
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
NEWSDATA_API_KEY = st.secrets["NEWSDATA_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(page_title="FinBot - Your Finance Assistant", layout="wide")

# -------------------------
# Theme toggle
# -------------------------
theme = st.sidebar.radio("Choose Theme", ["🌞 Light", "🌚 Dark"])
neon_css = """
    <style>
    html, body, [class*="css"] {
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

# -------------------------
# Logo & Title
# -------------------------
st.image("finbot_logo.png", width=60)
st.markdown("<h1 style='color:#0ff; font-weight:bold;'>FinBot - Your Finance Assistant</h1>", unsafe_allow_html=True)

# -------------------------
# Tabs
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Tools", "🤖 AI Advisor", "📰 News", "🎓 Fun Facts"])

# -------------------------
# Tab 1: Financial Tools
# -------------------------
with tab1:
    st.subheader("📌 Finance Tools")

    with st.expander("💰 Income Tax Calculator"):
        income = st.number_input("Enter your annual income (₹)", min_value
