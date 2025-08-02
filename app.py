import streamlit as st
import google.generativeai as genai
import PyPDF2
import random
import datetime
import requests
import base64

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Theme toggle
st.set_page_config(page_title="FinBot - Finance Assistant", layout="centered")

# Style: Neon light/dark mode
LIGHT_THEME = """
<style>
body {
    background-color: #f5f5f5;
    color: #222;
}
</style>
"""

DARK_THEME = """
<style>
body {
    background-color: #0f0f0f;
    color: #0affef;
}
</style>
"""

# Toggle
theme = st.toggle("🌗 Toggle Dark/Light Mode")
st.markdown(DARK_THEME if theme else LIGHT_THEME, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📊 FinBot Menu")
choice = st.sidebar.selectbox("Choose a tool", [
    "🤖 FinBot Chat (Gemini)",
    "📄 PDF Summarizer",
    "🧮 Tax Calculator",
    "🏦 EMI Calculator",
    "💰 FD Calculator",
    "💡 Finance Tips & Facts",
    "📧 Set Tax Reminder"
])

# FinBot Gemini Chat
if choice == "🤖 FinBot Chat (Gemini)":
    st.title("🤖 Ask FinBot (Gemini)")
    user_input = st.text_input("Ask anything about personal finance...")
    if user_input:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input)
        st.write("💬", response.text)

# PDF Summarizer
elif choice == "📄 PDF Summarizer":
    st.title("📄 Financial Document Summarizer")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file:
        reader = PyPDF2.PdfReader(uploaded_file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text()

        st.subheader("🔍 Summary:")
        model = genai.GenerativeModel("gemini-pro")
        summary = model.generate_content(f"Summarize this financial document:\n\n{full_text}")
        st.write(summary.text)

# Tax Calculator
elif choice == "🧮 Tax Calculator":
    st.title("🧮 Income Tax Calculator (India)")
    income = st.number_input("Enter your annual income (₹)", min_value=0)
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
        st.success(f"Your estimated tax is ₹{round(tax, 2)}")

# EMI Calculator
elif choice == "🏦 EMI Calculator":
    st.title("🏦 Loan EMI Calculator")
    principal = st.number_input("Loan Amount (₹)", min_value=0)
    rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)
    time = st.number_input("Loan Tenure (in years)", min_value=0)
    if st.button("Calculate EMI"):
        monthly_rate = rate / (12 * 100)
        months = time * 12
        if monthly_rate == 0:
            emi = principal / months
        else:
            emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
        st.success(f"Monthly EMI: ₹{round(emi, 2)}")

# FD Calculator
elif choice == "💰 FD Calculator":
    st.title("💰 Fixed Deposit Calculator")
    principal = st.number_input("Principal Amount (₹)", min_value=0)
    rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)
    time = st.number_input("Duration (in years)", min_value=0.0)
    if st.button("Calculate Maturity Amount"):
        amount = principal * (1 + rate / 100) ** time
        st.success(f"Maturity Amount: ₹{round(amount, 2)}")

# Fun Tips & Facts
elif choice == "💡 Finance Tips & Facts":
    st.title("💡 Random Finance Tips or Facts")
    tips = [
        "Start investing early to maximize compound interest.",
        "Create an emergency fund with 6 months of expenses.",
        "Use the 50-30-20 rule: Needs, Wants, Savings.",
        "Review your credit report annually.",
        "Avoid impulse purchases by waiting 24 hours.",
        "Pay off high-interest debt first.",
        "Set financial goals and track them regularly.",
        "Diversify your investment portfolio.",
        "Automate your savings every month.",
        "Invest in term insurance for financial security."
        # Add up to 1000 if desired
    ]
    st.info(random.choice(tips))
    if st.button("🔁 Click to get another tip"):
        st.info(random.choice(tips))

# Tax Reminder (Gmail via MailerSend)
elif choice == "📧 Set Tax Reminder":
    st.title("📧 Set Yearly Tax Filing Reminder")
    user_email = st.text_input("Enter your Gmail address")
    if st.button("Send Reminder"):
        year = datetime.datetime.now().year + 1
        msg = {
            "from": {"email": "your_mailersend_email@example.com", "name": "FinBot Reminder"},
            "to": [{"email": user_email}],
            "subject": f"⏰ Reminder: File Your Taxes for FY {year-1}-{year}",
            "text": f"Don't forget to file your taxes for the financial year {year-1}-{year}. Visit income tax portal!"
        }
        headers = {
            "Authorization": f"Bearer {st.secrets['MAILERSEND_API_TOKEN']}",
            "Content-Type": "application/json"
        }
        response = requests.post("https://api.mailersend.com/v1/email", json=msg, headers=headers)
        if response.status_code == 202:
            st.success("✅ Reminder sent successfully!")
        else:
            st.error("❌ Failed to send reminder. Check your API key/email.")

st.caption("© 2025 FinBot • Built with ❤️ using Streamlit & Gemini")
