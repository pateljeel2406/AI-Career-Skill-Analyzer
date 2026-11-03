
import streamlit as st
import pandas as pd
from modules.skill_analysis import analyze_skills
from modules.career_recommendation import recommend_career
from modules.roadmap import create_roadmap

# PAGE SETTINGS
st.set_page_config(
    page_title="AI Career Analyzer",
    page_icon="🎯",
    layout="wide"
)

# CUSTOM DESIGN
st.markdown("""
<style>
.stApp {
    background-color: #F0F4FF;
}
h1 {
    color: #263B80;
    text-align: center;
}
h2, h3 {
    color: #263B80;
}
div.stButton > button {
    background-color: #4939C8;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.title("🎯 AI Career & Skill Gap Analyzer")
st.markdown(
    "<h4 style='text-align:center;'>"
    "Discover Your Skills | Find Your Career | Build Your Future"
    "</h4>",
    unsafe_allow_html=True
)

st.divider()

# SIDEBAR
st.sidebar.title("🎓 Student Dashboard")
page = st.sidebar.radio(
    "Select Page",
    ["Home", "Skill Assessment", "About Project"]
)

if page == "Home":

    st.header("Welcome to AI Career Analyzer 👋")

    st.write("""
    This system helps students to:

    - Understand their technical skills.
    - Find suitable career options.
    - Identify missing skills.
    - Get personalized learning roadmaps.
    - Improve career readiness.
    """)

    col1, col2, col3 = st.columns(3)

    col1.info("💻 Skill Assessment")
    col2.success("🎯 Career Recommendation")
    col3.warning("📚 Learning Roadmap")

    st.subheader("🚀 Start Your Career Journey")

    if st.button("Start Skill Assessment"):
        st.session_state.page = "Skill Assessment"
        st.rerun()

elif page == "About Project":

    st.header("📖 About Our Project")

    st.write("""
    AI Career & Skill Gap Analyzer is a student career
    guidance system.

    It compares student skills with career requirements
    and recommends suitable career paths.

    Technology Used:
    - Python
    - Streamlit
    - Pandas
    - Machine Learning (future enhancement)
    - CSV Dataset
    """)

elif page == "Skill Assessment" or st.session_state.get("page") == "Skill Assessment":

    st.header("👩‍🎓 Student Information")

    name = st.text_input("Enter Your Name")

    email = st.text_input("Enter Your Email")

    education = st.selectbox(
        "Select Education",
        ["Diploma", "Degree", "B.E.", "B.Tech"]
    )

    semester = st.selectbox(
        "Select Semester",
        ["1", "2", "3", "4", "5", "6", "7", "8"]
    )

    st.divider()

    st.header("💻 Rate Your Technical Skills")

    st.write("Give yourself a rating from 0 to 5.")

    skill_names = [
        "Python", "SQL", "Excel",
        "Power BI", "HTML", "CSS", "Java"
    ]

    student_skills = {}

    col1, col2 = st.columns(2)

    for i, skill in enumerate(skill_names):

        with col1 if i % 2 == 0 else col2:

            student_skills[skill] = st.slider(
                skill,
                min_value=0,
                max_value=5,
                value=0,
                key=skill
            )

    st.divider()

    st.header("🎯 Select Your Career Interest")

    interest = st.selectbox(
        "Which career interests you?",
        [
            "Data Analyst",
            "Python Developer",
            "Web Developer",
            "Java Developer",
            "Software Engineer",
            "Cyber Security Analyst"
        ]
    )

    if st.button("🔍 Analyze My Career"):

        if not name.strip() or not email.strip():

            st.error("Please enter your Name and Email.")

        else:

            careers = pd.read_csv("data/careers.csv")

            results = recommend_career(
                student_skills, careers
            )

            best_career = results[0]["Career"]

            required = careers[
                careers["Career"] == best_career
            ].iloc[0]

            required_skills = {
                skill: int(required[skill])
                for skill in skill_names
            }

            score, missing = analyze_skills(
                student_skills,
                required_skills
            )

            st.success("Your Career Analysis is Ready!")

            st.divider()

            st.header("📊 Your Career Dashboard")

            c1, c2, c3 = st.columns(3)

            c1.metric("Student Name", name)

            c2.metric(
                "Career Match",
                f"{score:.1f}%"
            )

            c3.metric(
                "Skills to Improve",
                len(missing)
            )

            st.subheader("🏆 Top Career Recommendations")

            chart_data = pd.DataFrame(results)

            st.bar_chart(
                chart_data,
                x="Career",
                y="Match"
            )

            st.subheader("💪 Your Skill Analysis")

            for skill, rating in student_skills.items():

                st.write(f"**{skill} - {rating}/5**")

                st.progress(rating / 5)

            st.divider()

            st.header("⚠️ Your Missing Skills")

            if missing:

                for skill in missing:
                    st.warning(
                        f"Improve your {skill} skills."
                    )

            else:

                st.success(
                    "Excellent! You meet all the listed skill requirements."
                )

            st.divider()

            st.header("📚 Your Learning Roadmap")

            plan = create_roadmap(missing)

            if plan:

                for item in plan:

                    with st.expander(
                        f"📅 {item['Day']} - {item['Skill']}"
                    ):

                        st.write(item["Task"])

            else:

                st.success("No skill gaps found!")

            st.divider()

            st.header("🌐 Free Learning Resources")

            resources = {
                "Python": "https://www.w3schools.com/python/",
                "SQL": "https://www.w3schools.com/sql/",
                "Excel": "https://support.microsoft.com/excel",
                "Power BI": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/",
                "HTML": "https://www.w3schools.com/html/",
                "CSS": "https://www.w3schools.com/css/",
                "Java": "https://www.w3schools.com/java/"
            }

            for skill in missing:

                st.markdown(
                    f"[Learn {skill}]({resources[skill]})"
                )

            st.divider()

            st.info(
                "Your recommended career based on skill matching: "
                + best_career
            )

            report = f"""
AI CAREER & SKILL GAP ANALYZER

Student Name: {name}
Email: {email}
Education: {education}
Semester: {semester}

Career Interest: {interest}

Best Recommended Career: {best_career}

Career Match Score: {score:.1f}%

SKILLS:
{student_skills}

SKILLS TO IMPROVE:
{missing}

Thank you for using AI Career Analyzer!
"""

            st.download_button(
                "📥 Download Career Report",
                data=report,
                file_name="Career_Report.txt",
                mime="text/plain"
            )
