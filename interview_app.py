import streamlit as st
import pandas as pd

# ---------------- LOAD DATA ----------------
role_df = pd.read_csv("role_skill_mapping.csv")
question_df = pd.read_csv("question_bank.csv")

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="Interview Evaluation System", layout="wide")

st.title("🎤 Interview Evaluation System")
st.caption("Structured interview, scoring & ranking support system")

# ================== STEP 1: STUDENT DETAILS ==================
st.subheader("🧑‍🎓 Step 1: Candidate Details")

col1, col2 = st.columns(2)
with col1:
    student_id = st.text_input("Student ID (e.g. S101)")
with col2:
    student_name = st.text_input("Student Name")

# ================== STEP 2: ROLE SELECTION ==================
st.subheader("💼 Step 2: Job Role Selection")
role = st.selectbox("Select Job Role", role_df["Role_Name"].unique())
questions_per_topic = 2

# ================== SESSION STATE ==================
if "questions" not in st.session_state:
    st.session_state.questions = None
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "topic_scores" not in st.session_state:
    st.session_state.topic_scores = {}

# ================== STEP 3: GENERATE QUESTIONS ==================
st.subheader("📝 Step 3: Generate Interview Questions")

if st.button("Generate Questions"):
    if not student_id or not student_name:
        st.warning("Please enter Student ID and Name first.")
    else:
        st.session_state.questions = []
        st.session_state.responses = {}
        st.session_state.topic_scores = {}

        role_topics = role_df[role_df["Role_Name"] == role]

        for _, row in role_topics.iterrows():
            topic = row["Topic"]
            weight = row["Weight"]

            selected = question_df[
                question_df["Topic"] == topic
            ].sample(n=questions_per_topic)

            st.session_state.questions.append({
                "topic": topic,
                "weight": weight,
                "questions": selected["Question"].tolist()
            })

        st.success("Questions generated successfully.")

# ================== STEP 4: CONDUCT INTERVIEW ==================
if st.session_state.questions:
    st.divider()
    st.subheader("🎯 Step 4: Conduct Interview")

    total_topics = len(st.session_state.questions)
    completed = 0

    for q in st.session_state.questions:
        st.markdown(f"### 📌 {q['topic']}")

        for i, ques in enumerate(q["questions"], start=1):
            st.write(f"Q{i}. {ques}")

        correct = st.number_input(
            f"Correct answers in {q['topic']}",
            min_value=0,
            max_value=questions_per_topic,
            key=f"correct_{q['topic']}"
        )

        accuracy = correct / questions_per_topic
        st.session_state.responses[q["topic"]] = (
            correct,
            questions_per_topic,
            q["weight"]
        )
        st.session_state.topic_scores[q["topic"]] = accuracy * 100

        completed += 1
        st.progress(completed / total_topics)

    # ================== INTERVIEWER NOTES ==================
    st.divider()
    st.subheader("📝 Interviewer Notes")

    interviewer_notes = st.text_area(
        "Add interviewer remarks (optional)",
        placeholder="Example: Good communication skills, strong frontend basics, weak OS concepts"
    )

    # ================== STEP 5: SUBMIT INTERVIEW ==================
    st.divider()
    st.subheader("✅ Step 5: Final Submission")

    if st.button("Submit Interview"):
        final_score = 0

        for topic, (correct, total, weight) in st.session_state.responses.items():
            accuracy = correct / total
            final_score += accuracy * weight * 100

        # ---------- DUPLICATE ID CHECK ----------
        try:
            existing = pd.read_csv("all_interview_results.csv")
            if student_id in existing["Student_ID"].values:
                st.error("This Student ID already exists. Use a unique ID.")
                st.stop()
        except FileNotFoundError:
            existing = None

        # ---------- SAVE RESULT ----------
        result_row = pd.DataFrame([{
            "Student_ID": student_id,
            "Student_Name": student_name,
            "Role": role,
            "Final_Score": round(final_score, 2),
            "Interviewer_Notes": interviewer_notes
        }])

        updated = (
            pd.concat([existing, result_row], ignore_index=True)
            if existing is not None else result_row
        )

        updated.to_csv("all_interview_results.csv", index=False)

        st.success("🎉 Interview Completed Successfully")
        st.info(f"Final Score Calculated: {round(final_score, 2)}")


        st.markdown("### 📊 Next Step")
        st.markdown(
    "[👉 Go to Ranking Dashboard](http://localhost:8501/?page=ranking)",
    unsafe_allow_html=True
)


        # ================== TOPIC-WISE BREAKDOWN ==================
        st.divider()
        st.subheader("📊 Topic-wise Performance Breakdown")

        topic_df = pd.DataFrame({
            "Topic": st.session_state.topic_scores.keys(),
            "Score (%)": st.session_state.topic_scores.values()
        })

        st.bar_chart(topic_df.set_index("Topic"))
st.divider()
st.subheader("➡️ Next Step")

st.markdown(
    "[👉 Go to Ranking Dashboard](https://interview-evaluation-system2.streamlit.app/)",
    unsafe_allow_html=True
)


st.divider()
st.subheader("🧹 Interview History Controls")

if st.button("🗑️ Clear Interview History"):
    empty_df = pd.DataFrame(columns=[
        "Student_ID",
        "Student_Name",
        "Role",
        "Final_Score",
        "Interviewer_Notes"
    ])
    empty_df.to_csv("all_interview_results.csv", index=False)
    st.success("Interview history cleared successfully. Refresh to see changes.")



# ================== INTERVIEW HISTORY VIEWER ==================
st.divider()
st.subheader("📂 Interview History Viewer")

try:
    history_df = pd.read_csv("all_interview_results.csv")

    # If old CSV does not have Interviewer_Notes
    if "Interviewer_Notes" not in history_df.columns:
        history_df["Interviewer_Notes"] = ""

    st.dataframe(
        history_df[["Student_ID", "Student_Name", "Role", "Final_Score", "Interviewer_Notes"]],
        use_container_width=True,
        hide_index=True
    )

except FileNotFoundError:
    st.info("No interview history available yet.")



