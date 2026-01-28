import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# ---------- LOAD & TRAIN MODEL ----------
df = pd.read_csv("interview_results.csv")

df["Frontend_Acc"] = df["Frontend_Correct"] / df["Frontend_Total"]
df["CN_Acc"] = df["CN_Correct"] / df["CN_Total"]
df["OS_Acc"] = df["OS_Correct"] / df["OS_Total"]
df["DSA_Acc"] = df["DSA_Correct"] / df["DSA_Total"]

X = df[["Frontend_Acc", "CN_Acc", "OS_Acc", "DSA_Acc", "Avg_Difficulty"]]
le = LabelEncoder()
y = le.fit_transform(df["Decision"])

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# ---------- UI ----------
st.title("Adaptive ML Interview System")
st.subheader("Live Candidate Evaluation")

st.write("Enter candidate performance:")

frontend = st.slider("Frontend Accuracy", 0.0, 1.0, 0.5)
cn = st.slider("Computer Networks Accuracy", 0.0, 1.0, 0.5)
os = st.slider("Operating System Accuracy", 0.0, 1.0, 0.5)
dsa = st.slider("DSA Accuracy", 0.0, 1.0, 0.5)
avg_diff = st.slider("Average Difficulty", 1.0, 3.0, 2.0)

if st.button("Predict Decision"):
    new_student = pd.DataFrame([{
        "Frontend_Acc": frontend,
        "CN_Acc": cn,
        "OS_Acc": os,
        "DSA_Acc": dsa,
        "Avg_Difficulty": avg_diff
    }])

    pred = model.predict(new_student)
    decision = le.inverse_transform(pred)

    st.success(f"Predicted Decision: {decision[0]}")
