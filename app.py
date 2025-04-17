import streamlit as st
import google.generativeai as genai

# Configure Gemini with your API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="Story Brief Generator", layout="centered")

st.title("🎬 Story Brief Generator")
st.write("Fill in the form to generate a creative story concept.")

# --- SECTION 1 ---
st.header("📌 Organization Info")
org_name = st.text_input("Organization Name")
region = st.text_input("Country / Region of Operation")

focus_areas = st.multiselect("Focus Area", [
    "Health", "Education", "Gender", "Environment", "Livelihood",
    "Youth Empowerment", "Other"
])

beneficiaries = st.multiselect("Primary Beneficiaries", [
    "Children", "Women", "Youth", "Farmers", "Elderly",
    "People with Disabilities", "Urban Communities", "Rural Communities",
    "Refugees / IDPs", "Other"
])

# --- SECTION 2 ---
st.header("🎯 Project / Story Details")
project_name = st.text_input("Project Name")
project_goal = st.text_area("What is the main goal of the project?")
key_activities = st.text_area("Key Activities in the Project (up to 3 highlights)")
project_duration = st.selectbox("Duration of the Project", [
    "Less than 6 months", "6–12 months", "1–2 years", "Over 2 years"
])
partners = st.text_input("Who funded or partnered on this project?")

# --- SECTION 3 ---
st.header("🌍 Impact and Transformation")
problem_solved = st.text_area("What problem did this project aim to solve?")
change_seen = st.text_area("Describe the change you’ve seen after the intervention")
people_impacted = st.text_input("Approximate number of people impacted")
testimonial = st.text_area("Do you have a powerful individual story or testimonial we can feature?")

# --- SECTION 4 ---
st.header("🎨 Creative Direction")
emotional_response = st.selectbox("What kind of emotional response do you want from the viewer?", [
    "Hopeful", "Urgent", "Inspiring", "Informative", "Celebratory", "Other"
])
video_style = st.selectbox("What style of video would you prefer?", [
    "Documentary (interviews + b-roll)", "Voiceover-driven", "Cinematic + Music only (no dialogue)",
    "Storytelling with one main subject", "Other"
])
video_length = st.selectbox("Ideal Video Length", [
    "Under 2 minutes", "2–4 minutes", "5–7 minutes", "7+ minutes"
])
additional_notes = st.text_area("Anything else you’d like to share that we should consider for the video?")

# --- GENERATE ---
if st.button("Generate Story Brief"):
    with st.spinner("Generating story brief..."):
        prompt = f"""
You are a creative director helping an NGO create a powerful video story.

Organization: {org_name}
Region: {region}
Focus Areas: {", ".join(focus_areas)}
Beneficiaries: {", ".join(beneficiaries)}

Project Name: {project_name}
Goal: {project_goal}
Key Activities: {key_activities}
Duration: {project_duration}
Funders/Partners: {partners}

Problem Solved: {problem_solved}
Change Seen: {change_seen}
People Impacted: {people_impacted}
Testimonial: {testimonial}

Emotional Response: {emotional_response}
Preferred Video Style: {video_style}
Video Length: {video_length}
Additional Notes: {additional_notes}

Based on this, write a compelling and original story brief we can use to guide our creative team.
"""

        try:
            response = model.generate_content(prompt)
            st.success("✅ Story brief generated!")
            st.markdown("### 📝 Your Story Brief")
            st.write(response.text)
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
