import streamlit as st
import openai
import os

# Use your OpenAI key (store securely in production)
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Creative Story Brief Generator", layout="centered")

st.title("🎬 Story Brief Generator for Impact Projects")
st.markdown("Fill out the form below to generate a powerful, original video story brief.")

with st.form("story_form"):
    st.header("📌 Organization Info")
    org_name = st.text_input("1. Organization Name")
    region = st.text_input("2. Country / Region of Operation")

    focus_area = st.multiselect("3. Focus Area", [
        "Health", "Education", "Gender", "Environment", "Livelihood",
        "Youth Empowerment", "Other"
    ])

    beneficiaries = st.multiselect("4. Primary Beneficiaries", [
        "Children", "Women", "Youth", "Farmers", "Elderly",
        "People with Disabilities", "Urban Communities",
        "Rural Communities", "Refugees / IDPs", "Other"
    ])

    st.header("🧱 Project / Story Details")
    project_name = st.text_input("5. Project Name")
    main_goal = st.text_area("6. What is the main goal of the project?")
    key_activities = st.text_area("7. Key Activities in the Project (up to 3 highlights):")

    duration = st.selectbox("8. Duration of the Project", [
        "Less than 6 months", "6–12 months", "1–2 years", "Over 2 years"
    ])

    partners = st.text_input("9. Who funded or partnered on this project?")

    st.header("🌍 Impact and Transformation")
    problem = st.text_area("10. What problem did this project aim to solve?")
    change = st.text_area("11. Describe the change you’ve seen after the intervention:")
    people_impacted = st.text_input("12. Approximate number of people impacted:")
    testimonial = st.text_area("13. Do you have a powerful individual story or testimonial we can feature?")

    st.header("🎨 Creative Direction")
    emotion = st.selectbox("14. What kind of emotional response do you want from the viewer?", [
        "Hopeful", "Urgent", "Inspiring", "Informative", "Celebratory", "Other"
    ])

    video_style = st.selectbox("15. What style of video would you prefer?", [
        "Documentary (interviews + b-roll)", "Voiceover-driven", "Cinematic + Music only",
        "Storytelling with one main subject", "Other"
    ])

    video_length = st.selectbox("16. Ideal Video Length", [
        "Under 2 minutes", "2–4 minutes", "5–7 minutes", "7+ minutes"
    ])

    extra_notes = st.text_area("17. Anything else you'd like to share that we should consider for the video?")

    submitted = st.form_submit_button("Generate Story Brief 🎉")

if submitted:
    with st.spinner("Crafting your original story brief..."):
        prompt = f"""
You are a creative director and story strategist. 
Based on the following project information, generate a compelling, original, and emotionally resonant story brief for a video.

Rules:
- Do not use clichés like “making a difference” or “changing lives.”
- Avoid NGO jargon or buzzwords.
- Do not portray the organization as a savior.
- Avoid romanticizing suffering; focus on dignity and transformation.
- Use vivid, grounded, sensory language.
- Use active voice and be creative with the structure.
        
Organization: {org_name}
Region: {region}
Focus Areas: {', '.join(focus_area)}
Primary Beneficiaries: {', '.join(beneficiaries)}
Project Name: {project_name}
Main Goal: {main_goal}
Key Activities: {key_activities}
Project Duration: {duration}
Partners/Funders: {partners}
Problem Addressed: {problem}
Transformation Seen: {change}
People Impacted: {people_impacted}
Testimonial: {testimonial}
Desired Emotion: {emotion}
Preferred Style: {video_style}
Video Length: {video_length}
Additional Notes: {extra_notes}

Format your response in a clean, readable way that the client can understand immediately.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a masterful creative director skilled in storytelling for social impact."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=1000
        )

        story_brief = response.choices[0].message["content"]
        st.success("✅ Your story brief is ready!")
        st.markdown("### 🎬 Generated Story Brief")
        st.markdown(story_brief)

        # Optional: Download
        st.download_button("📥 Download Brief as TXT", story_brief, file_name="story_brief.txt")

