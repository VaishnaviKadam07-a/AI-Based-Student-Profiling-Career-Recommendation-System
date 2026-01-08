'''import streamlit as st
import numpy as np
import joblib

# Load models & encoders
career_path_model = joblib.load("career_path_model.pkl")
final_model = joblib.load("final_recommendation_model.pkl")
career_path_encoder = joblib.load("career_path_encoder.pkl")
final_encoder = joblib.load("final_recommendation_encoder.pkl")

st.set_page_config(page_title="AI Career Guidance System")

st.title("🎓 AI-Based Student Career Recommendation System")

# -----------------------------
# USER INPUTS
# -----------------------------
cgpa = st.slider("CGPA", 5.0, 10.0, 7.0)
coding = st.slider("Coding Skill (1-5)", 1, 5, 3)
ml = st.slider("ML Knowledge (1-5)", 1, 5, 3)
math = st.slider("Math Skill (1-5)", 1, 5, 3)
comm = st.slider("Communication Skill (1-5)", 1, 5, 3)
projects = st.number_input("Projects Completed", 0, 10, 1)

st.subheader("Interests")
interest_ai = st.slider("AI / Data Science", 1, 5, 3)
interest_web = st.slider("Web Development", 1, 5, 3)
interest_core = st.slider("Core Domains", 1, 5, 3)
research_interest = st.slider("Research", 1, 5, 3)
management_interest = st.slider("Management", 1, 5, 3)
higher_ed_interest = st.slider("Higher Education", 1, 5, 3)

# -----------------------------
# PREDICTION
# -----------------------------
if st.button("Predict Career"):
    # Model 1 input (12 features)
    input_model1 = np.array([[cgpa, coding, ml, math, comm, projects,
                              interest_ai, interest_web, interest_core,
                              research_interest, management_interest,
                              higher_ed_interest]])

    # Career Path Prediction
    path_pred = career_path_model.predict(input_model1)
    career_path = career_path_encoder.inverse_transform(path_pred)[0]

    # Encode career path for model 2
    career_path_encoded = career_path_encoder.transform([career_path])[0]

    # Model 2 input (13 features)
    input_model2 = np.array([[cgpa, coding, ml, math, comm, projects,
                              interest_ai, interest_web, interest_core,
                              research_interest, management_interest,
                              higher_ed_interest,
                              career_path_encoded]])

    final_pred = final_model.predict(input_model2)
    final_result = final_encoder.inverse_transform(final_pred)[0]

    st.success(f"📌 Career Path: **{career_path}**")
    st.success(f"🎯 Final Recommendation: **{final_result}**")
'''
import streamlit as st
import numpy as np
import joblib
import matplotlib.pyplot as plt

# ------------------ LOAD MODELS ------------------
career_path_model = joblib.load("career_path_model.pkl")
final_model = joblib.load("final_recommendation_model.pkl")
career_path_encoder = joblib.load("career_path_encoder.pkl")
final_encoder = joblib.load("final_recommendation_encoder.pkl")

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Career Guidance System",
    layout="wide"
)

st.title("🎓 AI-Based Student Profiling & Career Recommendation System")
st.caption("Interactive ML-powered career guidance platform")

st.divider()

# ------------------ SIDEBAR : STUDENT DETAILS ------------------
st.sidebar.header("👤 Student Details")

student_name = st.sidebar.text_input("Student Name")
college = st.sidebar.text_input("College / University")
year = st.sidebar.selectbox("Year of Study", ["1st Year", "2nd Year", "3rd Year", "Final Year"])
internship = st.sidebar.selectbox("Internship Experience", ["None", "1 Internship", "2+ Internships"])

st.sidebar.divider()

# ------------------ SIDEBAR : SKILLS ------------------
st.sidebar.header("🧠 Skill Assessment")

cgpa = st.sidebar.slider("CGPA", 5.0, 10.0, 7.0)
coding = st.sidebar.slider("Coding Skill", 1, 5, 3)
ml = st.sidebar.slider("ML Knowledge", 1, 5, 3)
math = st.sidebar.slider("Math Skill", 1, 5, 3)
comm = st.sidebar.slider("Communication Skill", 1, 5, 3)
projects = st.sidebar.slider("Projects Completed", 0, 10, 1)

# ------------------ INTERESTS ------------------
st.sidebar.subheader("🎯 Interests")
interest_ai = st.sidebar.slider("AI / Data Science", 1, 5, 3)
interest_web = st.sidebar.slider("Web Development", 1, 5, 3)
interest_core = st.sidebar.slider("Core Domains", 1, 5, 3)
research_interest = st.sidebar.slider("Research", 1, 5, 3)
management_interest = st.sidebar.slider("Management", 1, 5, 3)
higher_ed_interest = st.sidebar.slider("Higher Education", 1, 5, 3)

# ------------------ CAREER SIMULATION ------------------
st.sidebar.subheader("🔮 Career Simulation")
improve_coding = st.sidebar.slider("Improve Coding", 0, 2, 0)
improve_ml = st.sidebar.slider("Improve ML", 0, 2, 0)

coding_sim = min(5, coding + improve_coding)
ml_sim = min(5, ml + improve_ml)

# ------------------ PREDICTION ------------------
if st.sidebar.button("🚀 Predict Career"):

    # ---------- PERSONALIZED GREETING ----------
    if student_name:
        st.subheader(f"Hello, {student_name} 👋")
        st.write(f"**College:** {college} | **Year:** {year} | **Internships:** {internship}")

    # ---------- MODEL 1 ----------
    input_model1 = np.array([[cgpa, coding_sim, ml_sim, math, comm, projects,
                              interest_ai, interest_web, interest_core,
                              research_interest, management_interest,
                              higher_ed_interest]])

    path_pred = career_path_model.predict(input_model1)
    career_path = career_path_encoder.inverse_transform(path_pred)[0]
    career_path_encoded = career_path_encoder.transform([career_path])[0]

    # ---------- MODEL 2 ----------
    input_model2 = np.array([[cgpa, coding_sim, ml_sim, math, comm, projects,
                              interest_ai, interest_web, interest_core,
                              research_interest, management_interest,
                              higher_ed_interest,
                              career_path_encoded]])

    final_pred = final_model.predict(input_model2)
    final_result = final_encoder.inverse_transform(final_pred)[0]

    # ------------------ OUTPUT ------------------
    col1, col2 = st.columns(2)

    # ---------- RADAR CHART ----------
    with col1:
        st.subheader("📊 Skill Profile")

        skills = ["Coding", "ML", "Math", "Communication", "Projects"]
        values = [coding_sim, ml_sim, math, comm, min(projects, 5)]
        values += values[:1]

        angles = np.linspace(0, 2 * np.pi, len(skills), endpoint=False)
        angles = np.concatenate([angles, angles[:1]])

        fig, ax = plt.subplots(subplot_kw=dict(polar=True))
        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.3)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(skills)
        ax.set_yticks([1, 2, 3, 4, 5])

        st.pyplot(fig)

    # ---------- CAREER RESULT ----------
    with col2:
        st.subheader("🎯 Career Recommendation")
        st.success(f"📌 Career Path: **{career_path}**")
        st.success(f"🏆 Final Recommendation: **{final_result}**")

        readiness_score = int(
            (coding_sim + ml_sim + math + comm + min(projects, 5)) / 25 * 100
        )
        st.metric("Career Readiness Score", f"{readiness_score} / 100")

    # ------------------ EXPLAINABLE AI ------------------
    st.divider()
    st.subheader("🧠 Why This Recommendation?")

    reasons = []
    if coding_sim >= 4: reasons.append("Strong coding skills")
    if ml_sim >= 4: reasons.append("Good ML knowledge")
    if interest_ai >= 4: reasons.append("High AI/Data Science interest")
    if research_interest >= 4: reasons.append("Research-oriented mindset")
    if projects >= 3: reasons.append("Good project experience")

    for r in reasons:
        st.write("✔", r)

    # ------------------ ROADMAP ------------------
    st.divider()
    st.subheader("🛣️ Personalized Career Roadmap")

    roadmap = {
        "Data Scientist": [
            "Python & Pandas",
            "Statistics & Probability",
            "Machine Learning",
            "Data Visualization",
            "Industry Projects"
        ],
        "ML Engineer": [
            "Advanced Python",
            "ML Algorithms",
            "Deep Learning",
            "Model Deployment",
            "MLOps Basics"
        ],
        "Web Developer": [
            "HTML/CSS",
            "JavaScript",
            "React",
            "Backend Development",
            "Full Stack Project"
        ]
    }

    for i, step in enumerate(roadmap.get(final_result, ["Skill Development", "Projects"]), 1):
        st.checkbox(f"Step {i}: {step}")

    # ------------------ FEEDBACK ------------------
    st.divider()
    feedback = st.radio("Was this recommendation helpful?", ["Yes", "No"])
    if feedback == "Yes":
        st.success("Thanks for your feedback 😊")
    else:
        st.info("We will improve the system")
