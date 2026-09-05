"""Prepare a human-readable CSV for the Metabase dashboard.

Maps the encoded categorical columns to labels and adds helper columns
(age group, approval ratio, risk score from the trained model) so the
dashboard charts are easy to build and easy to read.
"""
import joblib
import pandas as pd

df = pd.read_csv("data.csv", sep=";")

COURSE = {
    33: "Biofuel Production Tech", 171: "Animation & Multimedia Design",
    8014: "Social Service (evening)", 9003: "Agronomy",
    9070: "Communication Design", 9085: "Veterinary Nursing",
    9119: "Informatics Engineering", 9130: "Equinculture",
    9147: "Management", 9238: "Social Service", 9254: "Tourism",
    9500: "Nursing", 9556: "Oral Hygiene",
    9670: "Advertising & Marketing", 9773: "Journalism & Communication",
    9853: "Basic Education", 9991: "Management (evening)",
}
MARITAL = {1: "Single", 2: "Married", 3: "Widower", 4: "Divorced",
           5: "Facto union", 6: "Legally separated"}
YESNO = {0: "No", 1: "Yes"}
GENDER = {0: "Female", 1: "Male"}
ATTEND = {0: "Evening", 1: "Daytime"}

out = pd.DataFrame({
    "status": df["Status"],
    "course": df["Course"].map(COURSE),
    "gender": df["Gender"].map(GENDER),
    "marital_status": df["Marital_status"].map(MARITAL),
    "attendance": df["Daytime_evening_attendance"].map(ATTEND),
    "scholarship_holder": df["Scholarship_holder"].map(YESNO),
    "tuition_up_to_date": df["Tuition_fees_up_to_date"].map(YESNO),
    "debtor": df["Debtor"].map(YESNO),
    "displaced": df["Displaced"].map(YESNO),
    "international": df["International"].map(YESNO),
    "age_at_enrollment": df["Age_at_enrollment"],
    "age_group": pd.cut(df["Age_at_enrollment"], [16, 20, 24, 29, 39, 70],
                        labels=["17-20", "21-24", "25-29", "30-39", "40+"]),
    "admission_grade": df["Admission_grade"],
    "prev_qualification_grade": df["Previous_qualification_grade"],
    "units_1st_sem_enrolled": df["Curricular_units_1st_sem_enrolled"],
    "units_1st_sem_approved": df["Curricular_units_1st_sem_approved"],
    "grade_1st_sem": df["Curricular_units_1st_sem_grade"],
    "units_2nd_sem_enrolled": df["Curricular_units_2nd_sem_enrolled"],
    "units_2nd_sem_approved": df["Curricular_units_2nd_sem_approved"],
    "grade_2nd_sem": df["Curricular_units_2nd_sem_grade"],
})
out["approval_ratio_2nd_sem"] = (
    df["Curricular_units_2nd_sem_approved"]
    / df["Curricular_units_2nd_sem_enrolled"].replace(0, float("nan"))
).round(3)
out["is_dropout"] = (df["Status"] == "Dropout").astype(int)

# Dropout-risk score from the trained model (useful to monitor Enrolled students)
model = joblib.load("model/model.joblib")
X = df.drop(columns=["Status"])
out["dropout_risk_score"] = model.predict_proba(X)[:, 1].round(3)

out.to_csv("data_dashboard.csv", index=False)
print("Saved data_dashboard.csv", out.shape)
print(out.groupby("status")["dropout_risk_score"].mean().round(3))
