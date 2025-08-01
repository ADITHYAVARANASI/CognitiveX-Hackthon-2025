# File: app.py
import streamlit as st
import requests
import json

# -------------------------------
# INLINE Gemini API Key
# -------------------------------
GEMINI_API_KEY = "AIzaSyDPP2WrXtbNIv-GVRFY0orP9w4S0aFIND0"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# -------------------------------
# Ask Gemini using REST API
# -------------------------------
def ask_gemini(prompt):
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Gemini Error: {e}"

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="Finance Assistant", layout="centered")
st.markdown("<h1 style='text-align:center;'>💡 Smart Finance AI Assistant</h1>", unsafe_allow_html=True)

# -------------------------------
# Tabs Layout
# -------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["🧠 AI Advisor", "🔍 Analyze Text", "💰 Budget Helper", "🧾 Tax Calculator"])

# -------------------------------
# Tab 1: AI Advisor
# -------------------------------
with tab1:
    st.subheader("💬 Ask anything about your money")
    user_input = st.text_area("Type your financial question here:")
    if st.button("Ask AI"):
        if user_input.strip():
            with st.spinner("Thinking..."):
                response = ask_gemini(f"You are a helpful finance assistant. Answer clearly.\n\nQ: {user_input}")
                st.success("AI says:")
                st.markdown(response)
        else:
            st.warning("Please enter a question.")

# -------------------------------
# Tab 2: Text Analysis
# -------------------------------
with tab2:
    st.subheader("🧠 Understand your text (Sentiment + Entities)")
    user_text = st.text_area("Enter any message or financial update:")
    if st.button("Analyze Text"):
        if user_text.strip():
            with st.spinner("Analyzing..."):
                response = ask_gemini(
                    f"""Analyze this message. First, show sentiment (positive/neutral/negative), then list any financial entities (people, companies, currencies, amounts, dates).

Message: {user_text}"""
                )
                st.markdown(response)
        else:
            st.warning("Please enter some text.")

# -------------------------------
# Tab 3: Budget Helper
# -------------------------------
with tab3:
    st.subheader("💰 Monthly Budget Estimator")
    income = st.number_input("Your Monthly Income (₹)", min_value=0, value=50000)
    expenses = st.number_input("Your Monthly Expenses (₹)", min_value=0, value=30000)
    savings = income - expenses

    st.metric(label="💸 Estimated Savings", value=f"₹{savings:,}")
    if savings < 0.2 * income:
        st.warning("You're saving less than 20%. Try to reduce some unnecessary expenses.")
    else:
        st.success("Great! You're saving a healthy portion of your income.")

# -------------------------------
# Tab 4: Tax Calculator
# -------------------------------
with tab4:
    st.subheader("🧾 Estimate Your Income Tax (Old Regime)")
    annual_income = st.number_input("Enter your Annual Income (₹)", min_value=0, value=600000)
    deductions = st.number_input("Total Deductions (80C, 80D, HRA, etc.) ₹", min_value=0, value=150000)

    taxable_income = max(0, annual_income - deductions)

    # Basic Tax Slabs (Old Regime)
    tax = 0
    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 1000000:
        tax = 12500 + (taxable_income - 500000) * 0.2
    else:
        tax = 112500 + (taxable_income - 1000000) * 0.3

    cess = 0.04 * tax
    total_tax = tax + cess

    st.write(f"**Taxable Income:** ₹{taxable_income:,}")
    st.write(f"**Estimated Tax:** ₹{total_tax:,.2f} (incl. 4% cess)")

    if annual_income > 500000 and total_tax == 0:
        st.info("You may be eligible for a rebate under Section 87A.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("""
    <hr style="margin-top:2em;">
    <div style='text-align:center; color:gray; font-size:0.9em'>
        🤖 Built with Gemini (1.5 Flash) | Making personal finance easier
    </div>
""", unsafe_allow_html=True)
