import pandas as pd

# Load role-skill mapping
role_df = pd.read_csv("role_skill_mapping.csv")

def calculate_score(role_name, responses):
    """
    responses = {
        'Frontend': (correct, total),
        'Computer Networks': (correct, total),
        'Operating System': (correct, total),
        'DSA': (correct, total)
    }
    """

    role_topics = role_df[role_df["Role_Name"] == role_name]

    final_score = 0
    topic_report = {}

    for _, row in role_topics.iterrows():
        topic = row["Topic"]
        weight = row["Weight"]

        if topic in responses:
            correct, total = responses[topic]
            accuracy = correct / total if total > 0 else 0
        else:
            accuracy = 0

        topic_score = accuracy * weight * 100
        final_score += topic_score

        topic_report[topic] = {
            "Accuracy": round(accuracy, 2),
            "Weighted Score": round(topic_score, 2)
        }

    return round(final_score, 2), topic_report


# -------- RUN (Sample Interview) --------
student_responses = {
    "Frontend": (2, 2),
    "Computer Networks": (1, 2),
    "Operating System": (1, 2),
    "DSA": (0, 2)
}

score, report = calculate_score("Frontend Developer", student_responses)

print("\nTopic-wise Performance")
...
print(f"\nFINAL SCORE: {score}")

if score >= 70:
    print("Decision: SHORTLIST")
elif score >= 50:
    print("Decision: WAITLIST")
else:
    print("Decision: REJECT")
