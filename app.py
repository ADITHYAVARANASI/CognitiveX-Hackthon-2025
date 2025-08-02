import streamlit as st
import requests
import random

# Load Gemini API key from Streamlit secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Headers for Gemini API
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GEMINI_API_KEY}"
}

def call_gemini_api(prompt):
    """Call Gemini chat-bison-001 model API with user prompt."""
    body = {
        "prompt": {
            "messages": [
                {"author": "user", "content": {"text": prompt}}
            ]
        },
        "temperature": 0.7,
        "maxOutputTokens": 512
    }
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta2/models/chat-bison-001:generateMessage",
        headers=headers,
        json=body,
        timeout=30
    )
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["message"]["content"]["text"]

# Financial facts and tips
fun_facts = [
    "The first credit card was introduced in 1950 by Diners Club.",
    "Compound interest was described by Einstein as the 8th wonder of the world.",
    "The average millionaire has 7 streams of income.",
    "Roth IRA accounts allow for tax-free withdrawals in retirement.",
    "UPI handles over 10 billion transactions monthly!",
    # Add more facts here...
]

finance_tips = [
    "Always spend less than you earn.",
    "Invest early to take advantage of compound interest.",
    "Maintain an emergency fund of 3-6 months of expenses.",
    "Use budgeting apps to track and control spending.",
    "Learn the difference between good and bad debt.",
    # Add more tips here...
]

# Streamlit page config
st.set_page_config(page_title="FinBot - Your Finance Assistant", layout="wide")

# Neon blue theme CSS
neon_css = """
<style>
    body, .main {
        background-color: #0d1117;
        color: #c0f7ff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1, h2, h3, h4, h5 {
        color: #00ffff;
        font-weight: 700;
    }
    .stButton>button {
        background-color: #00ffff;
        color: #000000;
        font-weight: 600;
        border-radius: 12px;
        box-shadow: 0 0 10px #00ffff;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00e6e6;
        box-shadow: 0 0 15px #00e6e6;
    }
    .stTextInput>div>input {
        background-color: #121821;
        color: #c0f7ff;
        border-radius: 8px;
        border: 1px solid #00ffff;
    }
    .stSelectbox>div>div>div>select {
        background-color: #121821;
        color: #c0f7ff;
        border-radius: 8px;
        border: 1px solid #00ffff;
    }
</style>
"""
st.markdown(neon_css, unsafe_allow_html=True)

# Title
st.title("💸 FinBot - Your Finance Assistant")

# Tabs
tabs = st.tabs(["🤖 AI Chatbot", "📚 Learn Finance", "📊 Calculators", "🎉 Fun Facts"])

# -------- AI Chatbot Tab --------
with tabs[0]:
    st.subheader("Ask your personal finance questions!")
    user_question = st.text_area("Enter your question or topic here:", height=120)
    if st.button("Get AI Advice"):
        if user_question.strip():
            with st.spinner("Thinking..."):
                try:
                    answer = call_gemini_api(user_question)
                    st.success(answer)
                except Exception as e:
                    st.error(f"API Error: {e}")
        else:
            st.warning("Please enter a question first.")

# -------- Learn Finance Tab --------
with tabs[1]:
    st.subheader("📚 Financial Knowledge Hub")
    if st.button("🔄 Refresh Tips"):
        random.shuffle(finance_tips)
    for tip in finance_tips[:10]:  # show 10 tips max at a time
        st.markdown(f"✅ {tip}")

# -------- Calculators Tab --------
with tabs[2]:
    st.subheader("📊 Financial Calculators")

    calc = st.selectbox("Choose a calculator:", ["Income Tax", "EMI", "Fixed Deposit"])

    if calc == "Income Tax":
        income = st.number_input("Enter your annual income (₹)", min_value=0)
        if st.button("Calculate Tax", key="tax"):
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
        loan_amount = st.number_input("Loan Amount (₹)", min_value=0)
        interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)
        tenure_months = st.number_input("Tenure (Months)", min_value=1)
        if st.button("Calculate EMI", key="emi"):
            monthly_rate = interest_rate / (12 * 100)
            emi = (loan_amount * monthly_rate * ((1 + monthly_rate) ** tenure_months)) / (((1 + monthly_rate) ** tenure_months) - 1)
            st.success(f"Monthly EMI: ₹{emi:,.2f}")

    elif calc == "Fixed Deposit":
        principal = st.number_input("Principal Amount (₹)", min_value=0)
        fd_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=6.5)
        duration_years = st.number_input("Duration (Years)", min_value=1)
        if st.button("Calculate Maturity", key="fd"):
            maturity = principal * ((1 + fd_rate / 100) ** duration_years)
            st.success(f"Maturity Amount: ₹{maturity:,.2f}")

# -------- Fun Facts Tab --------
with tabs[3]:
    st.subheader("🎉 Fun Financial Facts")
    if st.button("🔄 Refresh Fact"):
        st.session_state["fact"] = random.choice(fun_facts)
    if "fact" not in st.session_state:
        st.session_state["fact"] = random.choice(fun_facts)
    st.info(st.session_state["fact"])

    st.caption("🔁 Click refresh to see more!") use the models and hugging face develop a code for me and also use all three ibm models
