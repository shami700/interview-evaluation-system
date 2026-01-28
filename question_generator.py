import pandas as pd
import random

# Load datasets
role_df = pd.read_csv("role_skill_mapping.csv")
question_df = pd.read_csv("question_bank.csv")

def generate_questions(role_name):
    print(f"\nGenerating questions for role: {role_name}\n")

    role_topics = role_df[role_df["Role_Name"] == role_name]
    selected_questions = []

    for _, row in role_topics.iterrows():
        topic = row["Topic"]

        topic_questions = question_df[question_df["Topic"] == topic]
        available = len(topic_questions)

        # Decide how many questions to pick
        n = min(2, available)

        if n == 0:
            print(f"⚠ No questions found for topic: {topic}")
            continue

        questions = topic_questions.sample(n=n, replace=False)
        selected_questions.append(questions)

    if len(selected_questions) == 0:
        print("No questions generated.")
        return None

    final_questions = pd.concat(selected_questions)
    return final_questions[["Topic", "Difficulty", "Question"]]


# ---- RUN ----
questions = generate_questions("Frontend Developer")

if questions is not None:
    print(questions.to_string(index=False))
