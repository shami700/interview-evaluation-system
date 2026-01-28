import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("interview_results.csv")

# Feature engineering (accuracy calculation)
df["Frontend_Acc"] = df["Frontend_Correct"] / df["Frontend_Total"]
df["CN_Acc"] = df["CN_Correct"] / df["CN_Total"]
df["OS_Acc"] = df["OS_Correct"] / df["OS_Total"]
df["DSA_Acc"] = df["DSA_Correct"] / df["DSA_Total"]

# Select features
X = df[["Frontend_Acc", "CN_Acc", "OS_Acc", "DSA_Acc", "Avg_Difficulty"]]

# Encode target
le = LabelEncoder()
y = le.fit_transform(df["Decision"])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, target_names=le.classes_))


import matplotlib.pyplot as plt

# -------- FEATURE IMPORTANCE --------
feature_names = X.columns
importances = model.feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:")
print(importance_df.to_string(index=False))

# Plot feature importance
plt.figure()
plt.bar(importance_df["Feature"], importance_df["Importance"])
plt.xlabel("Features")
plt.ylabel("Importance Score")
plt.title("Feature Importance in Interview Decision")
plt.show()



# -------- LIVE DEMO: NEW STUDENT --------

# Example new student interview performance
new_student = pd.DataFrame([{
    "Frontend_Acc": 0.8,
    "CN_Acc": 0.5,
    "OS_Acc": 0.6,
    "DSA_Acc": 0.7,
    "Avg_Difficulty": 2.3
}])

# Predict decision
predicted_class = model.predict(new_student)
predicted_label = le.inverse_transform(predicted_class)

print("\nLive Demo Result")
print("Predicted Decision for New Student:", predicted_label[0])
