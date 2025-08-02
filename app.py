import streamlit as st
import requests
import json
import random

# Load Hugging Face API Key from Streamlit secrets
HF_API_KEY = st.secrets["HUGGING_FACE_API_KEY"]

# ------------------------
# IBM Granite Model Config
# ------------------------
MODEL_ID = "ibm-granite/granite-3b-instruct"  # or 7b/8b as needed
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# ------------------------
# Generate AI Response
# ------------------------
def query_ibm(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "return_full_text": False
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        try:
            output = response.json()
            return output[0]["generated_text"]
        except Exception as e:
            return f"❌ Error parsing response: {str(e)}"
    elif response.status_code == 503:
        return "⏳ Model is loading or busy. Please wait a moment and try again."
    else:
        return f"❌ API Error {response.status_code}: {response.text}"

# ------------------------
# Streamlit UI
# ------------------------
st.set_page_config(page_title="FinBot", layout="centered")
st.title("🤖 FinBot – Your Finance AI Assistant")

prompt = st.text_area("💬 Ask FinBot anything about finance, tax, savings, or investment:")

if st.button("🚀 Generate Answer"):
    if prompt.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            answer = query_ibm(prompt)
        st.success("Here's the answer:")
        st.markdown(f"> {answer}")

st.markdown("---")
st.caption("Powered by IBM Granite on Hugging Face • Built with ❤️ in Streamlit")
