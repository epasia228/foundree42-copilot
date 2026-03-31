import streamlit as st
import anthropic

st.set_page_config(page_title="Foundree42 Copilot", layout="wide")

st.title("Foundree42 Prospecting Copilot")

# Load API key
api_key = st.secrets.get("ANTHROPIC_API_KEY")

if not api_key:
    st.error("Missing ANTHROPIC_API_KEY in Streamlit secrets.")
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

# Inputs
company = st.text_input("Company")
contact = st.text_input("Contact")
title = st.text_input("Title")
notes = st.text_area("Notes (LinkedIn, company info, etc.)")

SYSTEM_PROMPT = """
You are a senior Salesforce GTM strategist at Foundree42.

You think in terms of:
- real business problems, not features
- process and ownership breakdowns
- where Salesforce typically underperforms
- where AI and Agentforce can actually drive outcomes

Style:
- sharp
- concise
- slightly opinionated
- no generic consulting language
"""

def generate_brief():
    prompt = f"""
Company: {company}
Contact: {contact}
Title: {title}
Notes: {notes}

Create a concise account brief with these sections:

1. What they likely care about
2. What is probably broken or at risk
3. Where Salesforce is likely underperforming
4. Why this matters to Foundree42
5. Best angle to engage

Keep it tight, specific, and practical.
"""
    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-latest",
            max_tokens=800,
            temperature=0.3,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        return response.content[0].text
    except Exception as e:
        return f"Claude error: {type(e).__name__}: {str(e)}"

# Button
if st.button("Generate Account Brief"):
    if company and title:
        with st.spinner("Thinking..."):
            result = generate_brief()
            st.subheader("Account Brief")
            st.write(result)
    else:
        st.warning("Please enter at least Company and Title.")
