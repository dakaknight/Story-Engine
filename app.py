import streamlit as st
from openai import OpenAI
import os

# Set your OpenAI API key securely
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # or os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.set_page_config(page_title="Story Engine", layout="centered")

st.title("📽️ Story Engine – Generate a Creative Brief")
st.markdown("Fill in the form below to generate a story brief for your organization.")

with st.form("story_form"):
    st.header("📌 Organization Info")
    org_name = st.text_input("Organization Name")
    country = st.text_input("Country / Region of Operation")
    focus_areas = st.multiselect("Focus Area", [
        "Health", "Education", "Gender", "Environment", "Livelihood",
        "Youth Empowerment", "Other"
    ])
    beneficiaries = st.multiselect("Primary Beneficiaries", [
        "Children", "Women", "Youth", "Farmers", "Elderly", "People with Disabilities",
        "Urban Communities", "Rural Communities", "Refugees / IDPs", "Other"
    ])

    st.header("📋 Project / Story Details")
    project_name = st.text_input("Project Name")
    project_goal = st.text_area("What is the main goal of the project?")
    key_activities = st.text_area("Key Activities in the Project (up to 3 highlights):")
    project_duration = st.selectbox("Duration of the Project", [
        "Less than 6 months", "6–12 months", "1–2 years", "Over 2 years"
    ])
    funder_info = st.text_input("Who funded or partnered on this project?")

    st.header("📈 Impact and Transformation")
    problem_solved = st.text_area("What problem did this project aim to solve?")
    seen_change = st.text_area("Describe the change you’ve seen after the intervention:")
    people_impacted = st.text_input("Approximate number of people impacted:")
    testimonial = st.text_area("Do you have a powerful individual story or testimonial we can feature?")

    st.header("🎨 Creative Direction")
    emotion = st.selectbox("What kind of emotional response do you want from the viewer?", [
        "Hopeful", "Urgent", "Inspiring", "Informative", "Celebratory", "Other"
    ])
    video_style = st.selectbox("What style of video would you prefer?", [
        "Documentary (interviews + b-roll)", "Voiceover-driven",
        "Cinematic + Music only (no dialogue)", "Storytelling with one main subject", "Other"
    ])
    video_length = st.selectbox("Ideal Video Length", [
        "Under 2 minutes", "2–4 minutes", "5–7 minutes", "7+ minutes"
    ])
    extra_notes = st.text_area("Anything else you’d like to share that we should consider for the video?")

    # Optional toggle for creative AI twist
    creative_mode = st.toggle("Let AI creatively reinterpret this story for originality?", value=True)

    submitted = st.form_submit_button("🚀 Generate Story Brief")

if submitted:
    # Construct user prompt
    user_prompt = f"""
You are a creative strategist and story expert for social impact. Based on the inputs below, create a compelling story brief for a short video. 
Make it emotionally engaging and suitable for production teams, but don't use corporate clichés. 
Respond in a way that inspires originality and emotional connection.

Organization: {org_name}
Country / Region: {country}
Focus Areas: {", ".join(focus_areas)}
Primary Beneficiaries: {", ".join(beneficiaries)}

Project Name: {project_name}
Project Goal: {project_goal}
Key Activities: {key_activities}
Duration: {project_duration}
Funder/Partner: {funder_info}

Problem Solved: {problem_solved}
Change Observed: {seen_change}
People Impacted: {people_impacted}
Testimonial: {testimonial}

Desired Emotion: {emotion}
Preferred Video Style: {video_style}
Video Length: {video_length}
Extra Notes: {extra_notes}
"""

    if creative_mode:
        user_prompt += "\n\nNegative Prompts: Avoid buzzwords like 'empower', 'impact', or 'solutions'. Think fresh, human, cinematic. No generic messaging."

    # Call OpenAI API
    with st.spinner("Generating your story brief..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a storytelling and creative strategy assistant."},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8
            )
            story_brief = response.choices[0].message.content
            st.success("✅ Story brief generated!")
            st.markdown("### ✍️ Story Brief")
            st.write(story_brief)
        except Exception as e:
            st.error(f"❌ Error: {e}")
