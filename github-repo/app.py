"""Jaya Jaya Institut — Student Dropout Early-Warning Prototype (Streamlit).

Run locally:
    streamlit run app.py
"""
import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Jaya Jaya Institut — Dropout Prediction",
    page_icon="🎓",
    layout="wide",
)

BASE = Path(__file__).parent


@st.cache_resource
def load_artifacts():
    model = joblib.load(BASE / "model" / "model.joblib")
    meta = json.loads((BASE / "model" / "metadata.json").read_text())
    defaults = json.loads((BASE / "model" / "feature_defaults.json").read_text())
    return model, meta, defaults


model, meta, defaults = load_artifacts()

COURSE = {
    "Biofuel Production Technologies": 33,
    "Animation & Multimedia Design": 171,
    "Social Service (evening)": 8014,
    "Agronomy": 9003,
    "Communication Design": 9070,
    "Veterinary Nursing": 9085,
    "Informatics Engineering": 9119,
    "Equinculture": 9130,
    "Management": 9147,
    "Social Service": 9238,
    "Tourism": 9254,
    "Nursing": 9500,
    "Oral Hygiene": 9556,
    "Advertising & Marketing Management": 9670,
    "Journalism & Communication": 9773,
    "Basic Education": 9853,
    "Management (evening)": 9991,
}
MARITAL = {"Single": 1, "Married": 2, "Widower": 3, "Divorced": 4,
           "Facto union": 5, "Legally separated": 6}
YESNO = {"No": 0, "Yes": 1}

# ---------------------------------------------------------------- header
st.title("🎓 Jaya Jaya Institut — Student Dropout Early Warning")
st.caption(
    "Prototype machine learning untuk mendeteksi siswa berisiko dropout "
    "sedini mungkin, agar dapat diberikan bimbingan khusus."
)

m = meta["metrics"][meta["best_model"]]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Model", meta["best_model"])
c2.metric("Accuracy", f"{m['accuracy']:.1%}")
c3.metric("Recall (Dropout)", f"{m['recall']:.1%}")
c4.metric("ROC-AUC", f"{m['roc_auc']:.3f}")
st.divider()

# ---------------------------------------------------------------- inputs
st.subheader("📋 Data Siswa")
tab_ac, tab_fin, tab_demo = st.tabs(
    ["📚 Akademik", "💰 Finansial", "👤 Demografi"])

with tab_ac:
    a1, a2 = st.columns(2)
    with a1:
        course = st.selectbox("Program studi (course)", list(COURSE))
        attendance = st.radio("Waktu kuliah", ["Daytime", "Evening"],
                              horizontal=True)
        admission_grade = st.slider("Admission grade (0–200)", 0.0, 200.0, 127.0)
        prev_grade = st.slider("Previous qualification grade (0–200)",
                               0.0, 200.0, 133.0)
    with a2:
        enrolled1 = st.number_input("SKS diambil — semester 1", 0, 26, 6)
        approved1 = st.number_input("SKS lulus — semester 1", 0, 26, 5)
        grade1 = st.slider("Rata-rata nilai semester 1 (0–20)", 0.0, 20.0, 12.3)
        enrolled2 = st.number_input("SKS diambil — semester 2", 0, 23, 6)
        approved2 = st.number_input("SKS lulus — semester 2", 0, 20, 5)
        grade2 = st.slider("Rata-rata nilai semester 2 (0–20)", 0.0, 20.0, 12.2)

with tab_fin:
    f1, f2, f3 = st.columns(3)
    tuition = f1.radio("Biaya kuliah lancar (up to date)?", ["Yes", "No"],
                       horizontal=True)
    scholarship = f2.radio("Penerima beasiswa?", ["No", "Yes"], horizontal=True)
    debtor = f3.radio("Memiliki tunggakan (debtor)?", ["No", "Yes"],
                      horizontal=True)

with tab_demo:
    d1, d2 = st.columns(2)
    with d1:
        age = st.slider("Usia saat mendaftar", 17, 70, 20)
        gender = st.radio("Gender", ["Female", "Male"], horizontal=True)
    with d2:
        marital = st.selectbox("Status pernikahan", list(MARITAL))
        displaced = st.radio("Displaced (tinggal jauh dari rumah)?",
                             ["No", "Yes"], horizontal=True)
        international = st.radio("Siswa internasional?", ["No", "Yes"],
                                 horizontal=True)

# ---------------------------------------------------------------- predict
row = dict(defaults)  # start from training medians for unexposed features
row.update({
    "Course": COURSE[course],
    "Daytime_evening_attendance": 1 if attendance == "Daytime" else 0,
    "Admission_grade": admission_grade,
    "Previous_qualification_grade": prev_grade,
    "Curricular_units_1st_sem_enrolled": enrolled1,
    "Curricular_units_1st_sem_approved": approved1,
    "Curricular_units_1st_sem_grade": grade1,
    "Curricular_units_2nd_sem_enrolled": enrolled2,
    "Curricular_units_2nd_sem_approved": approved2,
    "Curricular_units_2nd_sem_grade": grade2,
    "Tuition_fees_up_to_date": YESNO[tuition],
    "Scholarship_holder": YESNO[scholarship],
    "Debtor": YESNO[debtor],
    "Age_at_enrollment": age,
    "Gender": 1 if gender == "Male" else 0,
    "Marital_status": MARITAL[marital],
    "Displaced": YESNO[displaced],
    "International": YESNO[international],
})
X = pd.DataFrame([row])[meta["feature_names"]]

st.divider()
if st.button("🔮 Prediksi Risiko Dropout", type="primary",
             use_container_width=True):
    proba = float(model.predict_proba(X)[0, 1])

    r1, r2 = st.columns([1, 2])
    with r1:
        st.metric("Probabilitas Dropout", f"{proba:.1%}")
        st.progress(proba)
    with r2:
        if proba >= 0.60:
            st.error(
                "🔴 **RISIKO TINGGI** — siswa ini sangat berisiko dropout. "
                "Segera masukkan ke program bimbingan khusus: academic "
                "advising, cek status pembayaran, dan konseling.")
        elif proba >= 0.30:
            st.warning(
                "🟡 **RISIKO SEDANG** — perlu dipantau. Jadwalkan sesi "
                "konsultasi akademik dan verifikasi kondisi finansial siswa.")
        else:
            st.success(
                "🟢 **RISIKO RENDAH** — siswa dalam kondisi baik. "
                "Lanjutkan monitoring rutin per semester.")

    with st.expander("Faktor yang paling memengaruhi model (global)"):
        imp = pd.Series(meta["top_features"]).sort_values()
        st.bar_chart(imp, horizontal=True, color="#4C72B0")

st.divider()
st.caption("Proyek Akhir Dicoding — Emilia Loho · lohoemilia@gmail.com")
