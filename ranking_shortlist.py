import pandas as pd

# Load interview results
df = pd.read_csv("all_interview_results.csv")

# ---------- SAFETY: Final_Score ensure ----------
if "Final_Score" not in df.columns:
    raise ValueError("Final_Score column missing. Please add it first.")

# ---------- SORT ALL STUDENTS ----------
df_sorted = df.sort_values(by="Final_Score", ascending=False).copy()

# ---------- ASSIGN RANK TO ALL ----------
df_sorted["Rank"] = range(1, len(df_sorted) + 1)

# ---------- DISPLAY RESULT ----------
print("\nFULL RANKING OF ALL STUDENTS\n")
print(df_sorted[["Rank", "Student_ID", "Final_Score", "ML_Decision"]])

# ---------- SAVE RANKED LIST ----------
df_sorted.to_csv("ranked_all_students.csv", index=False)
print("\nranked_all_students.csv created successfully")
