# Interview Evaluation & Ranking System

A role-based interview evaluation and ranking system built with **Python** and **Streamlit** to support structured interviews, topic-wise scoring, interviewer notes, and fair candidate shortlisting.

---

## 🚀 Features

* Role-based interview workflow (Frontend, Backend, MERN, Data Science, etc.)
* Dynamic question generation from a topic-wise question bank
* Topic-wise scoring and performance visualization
* Interviewer notes for qualitative feedback
* Interview history viewer
* Rank-based and percentile-based shortlisting
* Excel-safe CSV export for final shortlist
* Clean interviewer and ranking dashboards

---

## 🧩 Project Structure

```
interview-evaluation-system/
│
├── interview_app.py          # Interviewer dashboard
├── ranking_app.py            # Ranking & shortlist dashboard
├── role_skill_mapping.csv    # Role-to-topic mapping with weights
├── question_bank.csv         # Topic-wise question bank (20 questions per topic)
├── all_interview_results.csv # Stored interview results
├── requirements.txt          # Project dependencies
└── README.md
```

---

## 🛠️ Technologies Used

* **Language:** Python
* **Framework:** Streamlit
* **Libraries:** Pandas
* **Data Storage:** CSV files
* **Deployment:** Streamlit Community Cloud

---

## 📊 Datasets

### 1. Role Skill Mapping (`role_skill_mapping.csv`)

Maps each job role to relevant interview topics with weights.

**Columns:**

* Role_Name
* Topic
* Weight

---

### 2. Question Bank (`question_bank.csv`)

Stores a pool of interview questions.

* Each topic contains **20 questions**
* Questions are randomly selected during interviews

**Columns:**

* Topic
* Question

---

### 3. Interview Results (`all_interview_results.csv`)

Stores interview outcomes and feedback.

**Columns:**

* Student_ID
* Student_Name
* Role
* Final_Score (used internally)
* Interviewer_Notes

---

## 🔄 Application Flow

1. Enter candidate details
2. Select job role
3. Generate role-specific interview questions
4. Conduct interview and record answers
5. Add interviewer notes
6. Save interview result
7. View ranking and generate shortlist

---


## 📈 Future Enhancements

* Difficulty-based question selection
* Database integration (Firebase / Supabase)
* Authentication for interviewers
* Role-wise cut-off scores
* PDF interview report generation

---

## 📌 Use Case

This system is suitable for:

* Campus placements
* Technical interviews
* Internal skill assessments
* Training evaluations

---

## 📄 License

This project is open-source and free to use for educational purposes.

---

## 👤 Author

**Md Shami Arzoo**  
Final-year student | Python & Streamlit Developer  
This project demonstrates a structured, role-based interview evaluation and ranking system built using Python and Streamlit.

