import streamlit as st
import pandas as pd

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="AI Career Analyzer",
    page_icon="🎯",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------

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
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# CAREER DATASET
# --------------------------------

careers = {
    "Career": [
        "Data Analyst",
        "Python Developer",
        "Web Developer",
        "Java Developer",
        "Software Engineer",
        "Cyber Security Analyst"
    ],

    "Python": [3, 5, 2, 2, 4, 3],
    "SQL": [5, 2, 1, 2, 4, 3],
    "Excel": [5, 2, 1, 1, 3, 2],
    "Power BI": [5, 1, 1, 1, 2, 1],
    "HTML": [1, 2, 5, 2, 4, 1],
    "CSS": [1, 2, 5, 2, 3, 1],
    "Java": [1, 3, 3, 5, 5, 3]
}

career_df = pd.DataFrame(careers)


# --------------------------------
# MAIN HEADER
# --------------------------------

st.title("🎯 AI Career & Skill Gap Analyzer")

st.markdown(
    "<h4 style='text-align:center;'>"
    "Discover Your Skills | Find Your Career | Build Your Future"
    "</h4>",
    unsafe_allow_html=True
)

st.divider()


# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title("🎓 Student Dashboard")

page = st.sidebar.radio(
    "Select Menu",
    [
        "Home",
        "Skill Assessment",
        "About Project"
    ]
)


# --------------------------------
# HOME PAGE
# --------------------------------

if page == "Home":

    st.header("Welcome to AI Career Analyzer 👋")

    st.write("""
    This website helps students to:

    1. Analyze their technical skills.
    2. Find suitable career options.
    3. Identify missing skills.
    4. Get a personalized learning roadmap.
    5. Understand their career readiness.
    """)

    col1, col2, col3 = st.columns(3)

    col1.info("💻 Skill Assessment")
    col2.success("🎯 Career Recommendation")
    col3.warning("📚 Learning Roadmap")

    st.subheader("Start Your Career Journey 🚀")

    st.write(
        "Go to Skill Assessment from the sidebar "
        "to check your career opportunities."
    )


# --------------------------------
# ABOUT PAGE
# --------------------------------

elif page == "About Project":

    st.header("📖 About Our Project")

    st.write("""
    AI Career & Skill Gap Analyzer is a career
    guidance system for students.

    It compares student skills with career
    requirements and recommends suitable careers.

    Technologies Used:

    - Python
    - Streamlit
    - Pandas
    - Data Analysis
    - Rule-Based Recommendation
    """)


# --------------------------------
# SKILL ASSESSMENT PAGE
# --------------------------------

elif page == "Skill Assessment":

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

    st.header("💻 Rate Your Skills")

    st.write("""
    Give your skill rating from 0 to 5.

    0 = No Knowledge
    1 = Beginner
    2 = Basic
    3 = Intermediate
    4 = Advanced
    5 = Expert
    """)

    skills = [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "HTML",
        "CSS",
        "Java"
    ]

    student_skills = {}

    col1, col2 = st.columns(2)

    for i, skill in enumerate(skills):

        with col1 if i % 2 == 0 else col2:

            student_skills[skill] = st.slider(
                skill,
                0,
                5,
                0,
                key=skill
            )

    st.divider()

    interest = st.selectbox(
        "Choose Your Interested Career",
        career_df["Career"].tolist()
    )

    # --------------------------------
    # ANALYZE BUTTON
    # --------------------------------

    if st.button("🔍 Analyze My Career"):

        if not name.strip() or not email.strip():

            st.error("Please enter your Name and Email.")

        else:

            results = []

            for _, career in career_df.iterrows():

                total = 0
                matched = 0

                for skill in skills:

                    required = int(career[skill])
                    student = student_skills[skill]

                    total += required
                    matched += min(student, required)

                match_score = (
                    matched / total * 100
                    if total else 0
                )

                results.append({
                    "Career": career["Career"],
                    "Match": round(match_score, 2)
                })

            results = sorted(
                results,
                key=lambda x: x["Match"],
                reverse=True
            )

            # --------------------------------
            # SELECTED CAREER ANALYSIS
            # --------------------------------

            selected = career_df[
                career_df["Career"] == interest
            ].iloc[0]

            required_skills = {
                skill: int(selected[skill])
                for skill in skills
            }

            missing = []

            total = len(skills)
            matched = 0

            for skill in skills:

                if student_skills[skill] >= required_skills[skill]:
                    matched += 1
                else:
                    missing.append(skill)

            score = matched / total * 100

            # --------------------------------
            # RESULTS
            # --------------------------------

            st.success(
                f"Hello {name}! Your analysis is ready."
            )

            st.divider()

            st.header("📊 Your Career Dashboard")

            c1, c2, c3 = st.columns(3)

            c1.metric("Student", name)

            c2.metric(
                "Skill Match",
                f"{score:.1f}%"
            )

            c3.metric(
                "Skills to Improve",
                len(missing)
            )

            # --------------------------------
            # CAREER RECOMMENDATION
            # --------------------------------

            st.header("🏆 Top Career Recommendations")

            result_df = pd.DataFrame(results)

            st.bar_chart(
                result_df,
                x="Career",
                y="Match"
            )

            st.write(
                f"Your highest matching career is: "
                f"**{results[0]['Career']}**"
            )

            # --------------------------------
            # SKILL ANALYSIS
            # --------------------------------

            st.header("💪 Your Skill Analysis")

            for skill in skills:

                rating = student_skills[skill]

                st.write(f"{skill}: {rating}/5")

                st.progress(rating / 5)

            # --------------------------------
            # MISSING SKILLS
            # --------------------------------

            st.header("⚠️ Skills to Improve")

            if missing:

                for skill in missing:

                    st.warning(
                        f"You should improve {skill}"
                    )

            else:

                st.success(
                    "You meet all listed skill requirements!"
                )

            # --------------------------------
            # LEARNING ROADMAP
            # --------------------------------

            st.header("📅 Your Learning Roadmap")

            for i, skill in enumerate(missing):

                start = i * 5 + 1
                end = start + 4

                with st.expander(
                    f"Day {start} - Day {end}: {skill}"
                ):

                    st.write(
                        f"Learn and practice {skill}."
                    )

                    st.write(
                        "Complete one small practical exercise."
                    )

            if not missing:

                st.success("No skill gaps found!")

            # --------------------------------
            # LEARNING RESOURCES
            # --------------------------------

            st.header("📚 Free Learning Resources")

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

            # --------------------------------
            # DOWNLOAD REPORT
            # --------------------------------

            st.header("📥 Download Career Report")

            report = f"""
AI CAREER & SKILL GAP ANALYZER

Student Name: {name}
Email: {email}
Education: {education}
Semester: {semester}

Career Interest: {interest}

Best Matching Career: {results[0]['Career']}

Skill Match: {score:.1f}%

Student Skills:
{student_skills}

Skills To Improve:
{missing}

Thank You!
"""

            st.download_button(
                "Download My Career Report",
                data=report,
                file_name="Career_Report.txt",
                mime="text/plain"
            )