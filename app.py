import streamlit as st
import requests
import os

# Replace this with your actual Groq API key or use secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "xai-mCeY6L1212Ni1ICpNyPSoD7ueMUrSMToVfDECaSNrjhmg1xai7J9GKwNvwBwHDqeaMH1VsSiuP23vZMz")

st.set_page_config(page_title="Story Engine", layout="centered")
st.title("🎬 Story Engine")
st.markdown("Fill out this form to generate a compelling story brief for your project.")

with st.form("story_form"):
    st.subheader("SECTION 1: Organization Info")
    org_name = st.text_input("1. Organization Name")
    region = st.text_input("2. Country / Region of Operation")
    focus_areas = st.multiselect("3. Focus Area", ["Health", "Education", "Gender", "Environment", "Livelihood", "Youth Empowerment", "Other"])
    beneficiaries = st.multiselect("4. Primary Beneficiaries", ["Children", "Women", "Youth", "Farmers", "Elderly", "People with Disabilities", "Urban Communities", "Rural Communities", "Refugees / IDPs", "Other"])

    st.subheader("SECTION 2: Project / Story Details")
    project_name = st.text_input("5. Project Name")
    goal = st.text_area("6. What is the main goal of the project?")
    activities = st.text_area("7. Key Activities in the Project (up to 3 highlights):")
    duration = st.radio("8. Duration of the Project", ["Less than 6 months", "6–12 months", "1–2 years", "Over 2 years"])
    funders = st.text_input("9. Who funded or partnered on this project?")

    st.subheader("SECTION 3: Impact and Transformation")
    problem = st.text_area("10. What problem did this project aim to solve?")
    change = st.text_area("11. Describe the change you’ve seen after the intervention:")
    impacted = st.text_input("12. Approximate number of people impacted:")
    testimonial = st.text_area("13. Do you have a powerful individual story or testimonial we can feature?")

    st.subheader("SECTION 4: Creative Direction")
    emotion = st.radio("14. What kind of emotional response do you want from the viewer?", ["Hopeful", "Urgent", "Inspiring", "Informative", "Celebratory", "Other"])
    style = st.radio("15. What style of video would you prefer?", ["Documentary (interviews + b-roll)", "Voiceover-driven", "Cinematic + Music only (no dialogue)", "Storytelling with one main subject", "Other"])
    length = st.radio("16. Ideal Video Length", ["Under 2 minutes", "2–4 minutes", "5–7 minutes", "7+ minutes"])
    extras = st.text_area("17. Anything else you’d like to share that we should consider for the video?")

    submit = st.form_submit_button("🚀 Generate Story Brief")

if submit:
    with st.spinner("Generating story brief with AI..."):
        # Build the prompt
        prompt = f"""
        Organization: {org_name}
        Region: {region}
        Focus Areas: {', '.join(focus_areas)}
        Beneficiaries: {', '.join(beneficiaries)}

        Project: {project_name}
        Goal: {goal}
        Activities: {activities}
        Duration: {duration}
        Funders/Partners: {funders}

        Problem: {problem}
        Observed Change: {change}
        People Impacted: {impacted}
        Testimonial: {testimonial}

        Desired Emotion: {emotion}
        Preferred Style: {style}
        Ideal Length: {length}
        Other Notes: {extras}

        Based on the details above, write a creative and emotionally compelling story brief suitable for a video production team. Highlight transformation, emotion, and the human element. Keep it engaging and inspiring.
        """

        # Send to Groq
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mixtral-8x7b-32768",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            story = response.json()["choices"][0]["message"]["content"]
            st.success("✅ Story brief generated successfully!")
            st.markdown("### 🎯 Generated Story Brief")
            st.markdown(story)
        else:
            st.error(f"❌ An error occurred: {response.status_code} - {response.text}")
