import streamlit as st

st.set_page_config(page_title="Foundree42 Copilot")

st.title("Foundree42 Prospecting Copilot")

st.write("Simple prospecting assistant for research + outreach")

# Inputs
company = st.text_input("Company Name")
contact = st.text_input("Contact Name")
title = st.text_input("Title")
notes = st.text_area("Notes (LinkedIn, company info, etc.)")

if st.button("Generate Account Brief"):
    if company and title:
        st.subheader("Account Brief")

        st.write(f"**Company:** {company}")
        st.write(f"**Contact:** {contact} ({title})")

        st.markdown("### What they likely care about:")
        st.write("- Revenue growth and sales performance")
        st.write("- Pipeline visibility and forecasting accuracy")

        st.markdown("### What’s probably broken:")
        st.write("- Misalignment between sales process and CRM")
        st.write("- Low adoption or inconsistent usage")

        st.markdown("### Suggested angle:")
        st.write("Focus on how their current Salesforce setup may not reflect how the business actually sells.")

    else:
        st.warning("Please enter at least company and title.")
