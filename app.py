import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Career & Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Career & Skill Gap Analyzer")

st.write(
    "Analyze your skills and discover "
    "what you need to learn for your dream career."
)

st.divider()

# Step 1: User Information
st.header("👤 Your Information")

name = st.text_input("Jeel Patel")

education = st.selectbox(
    "Select your Education",
    [
        "Computer Engineering"
    ]
)

career = st.selectbox(
    "Choose Your Target Career",
    [
        "Data Analyst"
    ]
)

# Step 2: Career Skill Requirements
career_skills = {
    "Data Analyst": {
        "Excel": 3,
        "SQL": 3,
        "Power BI": 3,
        "Python": 2,
        "Statistics": 2
    },


    }

level_names = {
    0: "Not Learned",
    1: "Beginner",
    2: "Intermediate",
    3: "Advanced"
}

# Step 3: User Skill Assessment
st.divider()
st.header("📚 Assess Your Current Skills")

st.write("Select your current level for each skill.")

required_skills = career_skills[career]
user_skills = {}

for skill, required_level in required_skills.items():

    user_skills[skill] = st.select_slider(
        skill,
        options=[0, 1, 2, 3],
        value=0,
        format_func=lambda x: level_names[x]
    )

# Step 4: Analyze Skills
if st.button("🔍 Analyze My Skills", type="primary"):

    if not name.strip():
        st.warning("Jeel Patel")

    else:
        results = []

        for skill, required_level in required_skills.items():

            current_level = user_skills[skill]

            gap = max(
                required_level - current_level,
                0
            )

            results.append({
                "Skill": skill,
                "Your Level": level_names[current_level],
                "Required Level": level_names[required_level],
                "Skill Gap": gap
            })

        result_df = pd.DataFrame(results)

        st.divider()
        st.header("📊 Your Skill Gap Report")

        st.success(
            f"Hello {name}! Your analysis is ready."
        )

        st.write("Education:", education)
        st.write("Target Career:", career)

        st.dataframe(
            result_df,
            use_container_width=True,
            hide_index=True
        )

        # Step 5: Calculate Skill Match
        total_required = sum(required_skills.values())

        total_gap = sum(
            max(
                required_skills[skill] - user_skills[skill],
                0
            )
            for skill in required_skills
        )

        match_percentage = (
            (total_required - total_gap)
            / total_required
        ) * 100

        st.subheader("📈 Career Skill Match")

        st.metric(
            "Skill Match Score",
            f"{match_percentage:.1f}%"
        )

        st.progress(int(match_percentage))

        st.caption(
            "This score compares your selected skill levels "
            "with the levels defined in our sample database. "
            "It does not measure your actual job readiness."
        )

        # Step 6: Display Missing Skills
        st.subheader("🎯 Skills You Should Improve")

        missing_skills = result_df[
            result_df["Skill Gap"] > 0
        ]

        if missing_skills.empty:

            st.success(
                "You meet all skill levels defined "
                "for this career in our database!"
            )

        else:

            for _, row in missing_skills.iterrows():

                st.write(
                    f"📌 {row['Skill']} — "
                    f"Current: {row['Your Level']} | "
                    f"Target: {row['Required Level']}"
                )

        # Step 7: Skill Gap Chart
        st.subheader("📊 Skill Gap Visualization")

        chart_df = result_df.set_index("Skill")

        st.bar_chart(chart_df["Skill Gap"])

        # Step 8: Learning Roadmap
        st.divider()
        st.header("🗺️ Recommended Learning Roadmap")

        learning_resources = {
            "Excel": "Learn formulas, Pivot Tables and charts.",
            "SQL": "Learn SELECT, WHERE, GROUP BY and JOIN.",
            "Power BI": "Learn Power Query, dashboards and DAX basics.",
            "Python": "Learn Python basics, functions and Pandas.",
            "Statistics": "Learn averages, probability and correlation.",
            "Git": "Learn Git commands and GitHub basics.",
            "Problem Solving": "Practice programming problems regularly.",
            "HTML": "Learn HTML tags and page structure.",
            "CSS": "Learn styling, layouts and responsive design.",
            "JavaScript": "Learn variables, functions and DOM basics."
        }

        if missing_skills.empty:

            st.write(
                "Continue practicing and build real-world projects."
            )

        else:

            for _, row in missing_skills.iterrows():

                skill = row["Skill"]

                st.write(
                    f"**{skill}:** "
                    f"{learning_resources[skill]}"
                )

        # Step 9: Download Report
        st.divider()

        csv_data = result_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Skill Gap Report",
            data=csv_data,
            file_name="career_skill_gap_report.csv",
            mime="text/csv"
        )

        # AI Career Recommendation Feature

st.divider()

st.header("🤖 Career Recommendation System")

st.write(
    "Select your interests to discover "
    "career options that may suit you."
)

interests = st.multiselect(
    "What are you interested in?",
    [
        "Data Analysis",
        "Mathematics",
        "Programming",
        "Artificial Intelligence",
        "Web Development",
        "Problem Solving",
        "Cybersecurity",
        "Working with Data"
    ]
)

if st.button("Recommend My Career"):

    if not interests:
        st.warning("Please select at least one interest.")

    else:
        career_scores = {
            "Data Analyst": 0,
            "Python Developer": 0,
            "AI/ML Engineer": 0,
            "Web Developer": 0,
            "Cybersecurity Analyst": 0
        }

        interest_mapping = {
            "Data Analysis": ["Data Analyst"],
            "Mathematics": [
                "Data Analyst",
                "AI/ML Engineer"
            ],
            "Programming": [
                "Python Developer",
                "Web Developer",
                "AI/ML Engineer"
            ],
            "Artificial Intelligence": [
                "AI/ML Engineer",
                "Data Analyst"
            ],
            "Web Development": ["Web Developer"],
            "Problem Solving": [
                "Python Developer",
                "Cybersecurity Analyst"
            ],
            "Cybersecurity": ["Cybersecurity Analyst"],
            "Working with Data": [
                "Data Analyst",
                "AI/ML Engineer"
            ]
        }

        for interest in interests:
            for career_name in interest_mapping[interest]:
                career_scores[career_name] += 1

        recommendations = sorted(
            career_scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        st.subheader("🎯 Your Recommended Careers")

        for career_name, score in recommendations[:3]:

            if score > 0:
                st.success(
                    f"**{career_name}** — "
                    f"Interest Match Score: {score}"
                )

        st.info(
            "These suggestions are based on your selected "
            "interests. They are not a guarantee of career "
            "success or job suitability."
        )