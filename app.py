import streamlit as st
import requests
import random
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
HF_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

# IBM Models (via Hugging Face)
IBM_MODELS = {
    "Granite 3.0 2B": "ibm-granite/granite-3.0-2b-instruct",
    "Granite 7B": "ibm/granite-7b-instruct",
    "Granite 3.0 8B": "ibm-granite/granite-3.0-8b-instruct"
}

# Headers for Hugging Face API
headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# Query Function
def query_ibm_model(prompt, model_id):
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    payload = {"inputs": prompt, "options": {"wait_for_model": True}}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list):
            return result[0]["generated_text"]
        elif "generated_text" in result:
            return result["generated_text"]
        else:
            return str(result)
    except Exception as e:
        return f"❌ Error: {e}"

# Neon Theme
st.set_page_config(page_title="FinBot - IBM Hugging Face", layout="wide")
st.markdown("""
<style>
    body, .main {
        background-color: #0d1117;
        color: #c0f7ff;
    }
    h1, h2, h3 {
        color: #00ffff;
    }
    .stButton>button {
        background-color: #00ffff;
        color: black;
        font-weight: bold;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Page Title
st.title("💸 FinBot – IBM Hugging Face Powered Finance Assistant")

# Tabs
tabs = st.tabs(["🤖 AI Chatbot", "📚 Finance Tips", "📊 Calculators", "🎉 Fun Facts"])

# ---------------------- Chatbot ----------------------
with tabs[0]:
    st.subheader("Ask Finance Questions (powered by IBM Models)")
    user_input = st.text_area("💬 Enter your question:", height=120)
    selected_model = st.selectbox("Choose a model:", list(IBM_MODELS.keys()))

    if st.button("Get Answer"):
        if user_input.strip():
            with st.spinner("Fetching response..."):
                model_id = IBM_MODELS[selected_model]
                reply = query_ibm_model(user_input, model_id)
                st.success(reply)
        else:
            st.warning("Please enter a question.")

# ---------------------- Finance Tips ----------------------
finance_tips = [
    "Always spend less than you earn.",
    "Invest early to take advantage of compound interest.",
    "Create and maintain a budget.",
    "Keep an emergency fund worth 6 months of expenses.",
    "Avoid unnecessary debt. Pay credit cards in full.",
    "Track expenses with personal finance apps.",
    "Review subscriptions annually.",
    "Understand risk before investing.",
    "Diversify your portfolio.",
    "Start retirement savings early."
]

with tabs[1]:
    st.subheader("📚 Financial Tips & Advice")
    if st.button("🔁 Shuffle Tips"):
        random.shuffle(finance_tips)
    for tip in finance_tips[:10]:
        st.markdown(f"✅ {tip}")

# ---------------------- Calculators ----------------------
with tabs[2]:
    st.subheader("📊 Financial Calculators")
    calc = st.selectbox("Select Calculator", ["Income Tax", "EMI", "Fixed Deposit"])

    if calc == "Income Tax":
        income = st.number_input("Enter Annual Income (₹)", min_value=0)
        if st.button("Calculate Tax"):
            tax = 0
            if income <= 250000:
                tax = 0
            elif income <= 500000:
                tax = (income - 250000) * 0.05
            elif income <= 1000000:
                tax = 12500 + (income - 500000) * 0.2
            else:
                tax = 112500 + (income - 1000000) * 0.3
            st.success(f"Estimated Tax: ₹{tax:,.2f}")

    elif calc == "EMI":
        loan = st.number_input("Loan Amount (₹)", min_value=0)
        rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)
        months = st.number_input("Tenure in Months", min_value=1)
        if st.button("Calculate EMI"):
            monthly_rate = rate / (12 * 100)
            emi = (loan * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
            st.success(f"Monthly EMI: ₹{emi:,.2f}")

    elif calc == "Fixed Deposit":
        principal = st.number_input("Principal Amount (₹)", min_value=0)
        fd_rate = st.number_input("Annual Interest Rate (%)", value=6.5)
        years = st.number_input("Duration (Years)", min_value=1)
        if st.button("Calculate Maturity"):
            maturity = principal * ((1 + fd_rate / 100) ** years)
            st.success(f"Maturity Value: ₹{maturity:,.2f}")

# ---------------------- Fun Facts ----------------------
fun_facts = [
    "The first credit card was introduced in 1950.",
    "Compound interest is called the 8th wonder of the world.",
    "Most millionaires have 7 income streams.",
    "In India, UPI handles over 10 billion transactions monthly.",
    "Savings of just ₹500/month can grow to ₹10L+ in 20 years (with compounding)."
]

with tabs[3]:
    st.subheader("🎉 Fun Finance Facts")
    if st.button("🔁 Refresh Fact"):
        st.session_state["fact"] = random.choice(fun_facts)
    if "fact" not in st.session_state:
        st.session_state["fact"] = random.choice(fun_facts)
    st.info(st.session_state["fact"])
