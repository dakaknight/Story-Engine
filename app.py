import streamlit as st
import requests
import os

# You can also use Streamlit secrets for safety
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")

st.set_page_config(page_title="Story Engine", layout="centered")

st.title("🎬 Story Engine")
st.markdown("Fill out the form below to generate a unique story brief.")

# --- Form Fields (abbreviated for brevity; use your full form)
org_name = st.text_input("1. Organization Name")
region = st.text_input("2. Country / Region of Operation")
focus_areas = st.multiselect("3. Focus Area", ["Health", "Education", "Gender", "Environment", "Livelihood", "Youth Empowerment", "Other"])
beneficiaries = st.multiselect("4. Primary Beneficiaries", ["Children", "Women", "Youth", "Farmers", "Elderly", "People with Disabilities", "Urban Communities", "Rural Communities", "Refugees / IDPs", "Other"])

# ... (add all your other form questions)

if st.button("🚀 Generate Story Brief"):
    with st.spinner("Crafting your story..."):

        # Construct the prompt from form responses
        prompt = f"""
        Organization: {org_name}
        Region: {region}
        Focus Areas: {", ".join(focus_areas)}
        Beneficiaries: {", ".join(beneficiaries)}
        ---
        Generate a powerful story brief that captures the essence of this project. Highlight emotion, purpose, and transformation. Be creative, specific, and impactful.
        """

        # Call Groq API
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mixtral-8x7b-32768",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            story = result["choices"][0]["message"]["content"]
            st.success("✅ Story brief generated!")
            st.markdown(story)
        else:
            st.error(f"❌ Error: {response.status_code} - {response.text}")
