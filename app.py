import streamlit as st
import requests
import random

# ✅ Read API key from secrets.toml
HF_API_KEY = st.secrets["HUGGING_FACE_API_KEY"]

# Hugging Face API headers
headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# IBM Granite models on Hugging Face
IBM_MODELS = {
    "Granite 3.0 2B": "ibm-granite/granite-3.0-2b-instruct",
    "Granite 7B": "ibm/granite-7b-instruct",
    "Granite 3.0 8B": "ibm-granite/granite-3.0-8b-instruct"
}

# Query function
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
        return f"❌ API Error: {e}"

# UI Configuration
st.set_page_config(page_title="FinBot – Finance Assistant", layout="wide")
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

st.title("💸 FinBot – Powered by IBM Models on Hugging Face")

tabs = st.tabs(["🤖 AI Chatbot", "📚 Finance Tips", "📊 Calculators", "🎉 Fun Facts"])

# Tab 1: Chatbot
with tabs[0]:
    st.subheader("Ask any finance-related question:")
    user_input = st.text_area("Your question:", height=120)
    selected_model = st.selectbox("Choose a model:", list(IBM_MODELS.keys()))

    if st.button("Get Answer"):
        if user_input.strip():
            with st.spinner("Thinking..."):
                model_id = IBM_MODELS[selected_model]
                reply = query_ibm_model(user_input, model_id)
                st.success(reply)
        else:
            st.warning("Please enter a question.")

# Tab 2: Finance Tips
finance_tips = [
    "Spend less than you earn.",
    "Start investing early.",
    "Keep an emergency fund.",
    "Pay off high-interest debt first.",
    "Diversify your investments.",
    "Use budgeting tools.",
    "Avoid emotional investing.",
    "Automate your savings.",
    "Review expenses monthly.",
    "Save at least 20% of your income."
]

with tabs[1]:
    st.subheader("📚 Financial Tips")
    if st.button("🔁 Shuffle Tips"):
        random.shuffle(finance_tips)
    for tip in finance_tips[:10]:
        st.markdown(f"✅ {tip}")

# Tab 3: Calculators
with tabs[2]:
    st.subheader("📊 Financial Calculators")
    calc = st.selectbox("Choose calculator:", ["Income Tax", "EMI", "Fixed Deposit"])

    if calc == "Income Tax":
        income = st.number_input("Annual Income (₹)", min_value=0)
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
        rate = st.number_input("Interest Rate (%)", min_value=0.0)
        tenure = st.number_input("Tenure (months)", min_value=1)
        if st.button("Calculate EMI"):
            r = rate / (12 * 100)
            emi = (loan * r * (1 + r) ** tenure) / ((1 + r) ** tenure - 1)
            st.success(f"Monthly EMI: ₹{emi:,.2f}")

    elif calc == "Fixed Deposit":
        principal = st.number_input("Principal (₹)", min_value=0)
        fd_rate = st.number_input("Interest Rate (%)", value=6.5)
        years = st.number_input("Duration (years)", min_value=1)
        if st.button("Calculate Maturity"):
            maturity = principal * ((1 + fd_rate / 100) ** years)
            st.success(f"Maturity Amount: ₹{maturity:,.2f}")

# Tab 4: Fun Facts
fun_facts = [
    "The first credit card was issued in 1950.",
    "Compound interest is called the 8th wonder of the world.",
    "UPI handles over 10 billion transactions per month in India.",
    "The average millionaire has 7 income streams.",
    "Saving ₹100/day = ₹36,500/year, excluding interest!"
]

with tabs[3]:
    st.subheader("🎉 Fun Finance Facts")
    if st.button("🔁 New Fact"):
        st.session_state["fact"] = random.choice(fun_facts)
    if "fact" not in st.session_state:
        st.session_state["fact"] = random.choice(fun_facts)
    st.info(st.session_state["fact"])
