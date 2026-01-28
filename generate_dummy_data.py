import pandas as pd
import random

data = []

decisions = ["Shortlist", "Waitlist", "Reject"]

for i in range(1, 101):  # 100 students
    frontend = random.randint(0, 2)
    cn = random.randint(0, 2)
    os = random.randint(0, 2)
    dsa = random.randint(0, 2)

    avg_diff = round(random.uniform(1.5, 3.0), 2)

    score = (
        (frontend/2)*0.4 +
        (cn/2)*0.2 +
        (os/2)*0.15 +
        (dsa/2)*0.25
    ) * 100

    if score >= 70:
        decision = "Shortlist"
    elif score >= 50:
        decision = "Waitlist"
    else:
        decision = "Reject"

    data.append([
        f"S{i}", "Frontend",
        frontend, 2,
        cn, 2,
        os, 2,
        dsa, 2,
        avg_diff,
        round(score, 2),
        decision
    ])

columns = [
    "Student_ID", "Role",
    "Frontend_Correct", "Frontend_Total",
    "CN_Correct", "CN_Total",
    "OS_Correct", "OS_Total",
    "DSA_Correct", "DSA_Total",
    "Avg_Difficulty",
    "Final_Score",
    "Decision"
]

df = pd.DataFrame(data, columns=columns)
df.to_csv("interview_results.csv", index=False)

print("Dummy interview_results.csv generated with 100 records")
