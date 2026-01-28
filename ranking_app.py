import streamlit as st
import pandas as pd

st.set_page_config(page_title="Interview Ranking Dashboard", layout="wide")

st.title("📊 Interview Ranking & Shortlisting Dashboard")
st.caption("Rank-based evaluation of all interviewed candidates")

# ---------- LOAD DATA ----------
try:
    df = pd.read_csv("all_interview_results.csv")
except FileNotFoundError:
    st.error("all_interview_results.csv not found. Please conduct interviews first.")
    st.stop()

# ---------- REQUIRED COLUMNS CHECK ----------
required_cols = {"Student_ID", "Student_Name", "Role", "Final_Score"}
if not required_cols.issubset(df.columns):
    st.error("Required columns missing in dataset.")
    st.stop()

# ---------- SORT & RANK (USING Final_Score INTERNALLY) ----------
df_sorted = df.sort_values(by="Final_Score", ascending=False).copy()

df_sorted["Rank"] = (
    df_sorted["Final_Score"]
    .rank(method="dense", ascending=False)
    .astype(int)
)

# ---------- PERCENTILE ----------
df_sorted["Percentile"] = (
    df_sorted["Final_Score"].rank(pct=True) * 100
).round(2)

# ---------- SERIAL NUMBER (1-BASED) ----------
df_sorted.insert(0, "S.No", range(1, len(df_sorted) + 1))

# ---------- SEARCH ----------
st.subheader("🔍 Search Student")
search_id = st.text_input("Search by Student ID / Name / Role")

if search_id:
    search_df = df_sorted[
        df_sorted["Student_ID"].str.contains(search_id, case=False) |
        df_sorted["Student_Name"].str.contains(search_id, case=False) |
        df_sorted["Role"].str.contains(search_id, case=False)
    ]

    st.dataframe(
        search_df[["S.No", "Rank", "Student_ID", "Student_Name", "Role", "Percentile"]],
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ---------- FULL RANK TABLE ----------
st.subheader("📋 Full Ranking of All Students")
st.dataframe(
    df_sorted[["S.No", "Rank", "Student_ID", "Student_Name", "Role", "Percentile"]],
    use_container_width=True,
    hide_index=True
)

st.divider()

# ---------- TOP-N SHORTLIST ----------
st.subheader("🎯 Generate Final Shortlist")

max_students = len(df_sorted)

if max_students == 0:
    st.warning("No interview data available. Please conduct interviews first.")
    st.stop()

top_n = st.slider(
    "Select number of students to shortlist (Top-N)",
    min_value=1,
    max_value=max_students,
    value=min(10, max_students)
)


shortlist_df = df_sorted.head(top_n)

st.subheader(f"🏆 Top {top_n} Shortlisted Students")
st.dataframe(
    shortlist_df[["S.No", "Rank", "Student_ID", "Student_Name", "Role", "Percentile"]],
    use_container_width=True,
    hide_index=True
)

# ---------- DOWNLOAD BUTTON ----------
shortlist_df["Student_ID"] = "'" + shortlist_df["Student_ID"].astype(str)

csv_data = shortlist_df[
    ["S.No", "Rank", "Student_ID", "Student_Name", "Role", "Percentile"]
].to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Shortlist as CSV",
    data=csv_data,
    file_name="final_shortlist.csv",
    mime="text/csv"
)

