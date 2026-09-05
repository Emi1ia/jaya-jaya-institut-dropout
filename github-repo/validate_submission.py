"""Check the submission folder against the Dicoding requirements.

    python validate_submission.py

Exits 0 when everything required is present and valid, 1 otherwise.
Re-run this after finishing the Metabase dashboard and the Streamlit deploy.
"""
import json
import re
import sys
import zipfile
from pathlib import Path

BASE = Path(__file__).parent
ok, warn, bad = [], [], []


def check(cond, good, why):
    (ok if cond else bad).append(good if cond else why)
    return cond


def soft(cond, good, why):
    (ok if cond else warn).append(good if cond else why)
    return cond


# ---------------------------------------------------------------- structure
REQUIRED = ["notebook.ipynb", "app.py", "README.md", "requirements.txt",
            "data.csv", "data_dashboard.csv", "train_model.py",
            "prepare_dashboard_data.py",
            "model/model.joblib", "model/metadata.json",
            "model/feature_defaults.json"]
SUBMISSION_ARTEFACTS = ["metabase.db.mv.db", "emilia_loho-dashboard.png"]
OPTIONAL = ["emilia_loho-video.mp4"]

for rel in REQUIRED:
    p = BASE / rel
    check(p.is_file(), f"{rel} present ({p.stat().st_size:,} B)" if p.is_file()
          else "", f"MISSING required file: {rel}")

for rel in SUBMISSION_ARTEFACTS:
    p = BASE / rel
    check(p.is_file(), f"{rel} present ({p.stat().st_size:,} B)" if p.is_file()
          else "", f"MISSING submission artefact: {rel}")

for rel in OPTIONAL:
    p = BASE / rel
    soft(p.is_file(), f"{rel} present (optional)" if p.is_file() else "",
         f"optional file not present: {rel}")

# ----------------------------------------------------------------- notebook
nb_path = BASE / "notebook.ipynb"
if nb_path.is_file():
    try:
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        code = [c for c in nb["cells"] if c["cell_type"] == "code"]
        unrun = [c for c in code if c.get("execution_count") is None]
        errs = [o for c in code for o in c.get("outputs", [])
                if o.get("output_type") == "error"]
        check(not unrun, f"notebook.ipynb: all {len(code)} code cells executed",
              f"notebook.ipynb: {len(unrun)} code cell(s) not executed")
        check(not errs, "notebook.ipynb: no error outputs",
              f"notebook.ipynb: {len(errs)} error output(s)")
    except json.JSONDecodeError as e:
        bad.append(f"notebook.ipynb is not valid JSON: {e}")

# ------------------------------------------------------------------- README
rd_path = BASE / "README.md"
if rd_path.is_file():
    rd = rd_path.read_text(encoding="utf-8")
    placeholders = re.findall(
        r"GANTI[-\w]*|TODO|XXXX|<isi.*?>|LINK-ANDA|your-app-url", rd, re.I)
    check(not placeholders, "README.md: no placeholders left",
          f"README.md still has placeholder(s): {sorted(set(placeholders))}")
    links = re.findall(r"https://[\w.-]+\.streamlit\.app[\w/-]*", rd)
    real = [l for l in links
            if "GANTI" not in l.upper() and "change-this" not in l.lower()]
    soft(bool(real), f"README.md: Streamlit link filled in -> {real[0]}"
         if real else "",
         "README.md: Streamlit link is still a placeholder - deploy your own "
         "app and paste its URL")
    for token in ["Emilia Loho", "lohoemilia@gmail.com",
                  "emilia_loho"]:
        check(token in rd, f"README.md: identity '{token}' present",
              f"README.md: missing identity '{token}'")

# -------------------------------------------------------------------- model
try:
    import joblib
    import pandas as pd

    model = joblib.load(BASE / "model" / "model.joblib")
    meta = json.loads((BASE / "model" / "metadata.json").read_text())
    defaults = json.loads((BASE / "model" / "feature_defaults.json").read_text())
    check(set(defaults) == set(meta["feature_names"]),
          "model: feature_defaults.json matches metadata feature_names",
          "model: feature_defaults.json keys differ from metadata feature_names")

    row = dict(defaults)
    row.update({"Debtor": 1, "Tuition_fees_up_to_date": 0,
                "Curricular_units_1st_sem_approved": 1,
                "Curricular_units_2nd_sem_approved": 1,
                "Curricular_units_1st_sem_grade": 6.0,
                "Curricular_units_2nd_sem_grade": 7.0})
    p = float(model.predict_proba(
        pd.DataFrame([row])[meta["feature_names"]])[0, 1])
    check(p >= 0.60,
          f"model: high-risk smoke test -> {p:.1%} (RISIKO TINGGI)",
          f"model: high-risk smoke test only {p:.1%}, expected >= 60%")
except Exception as e:                                   # noqa: BLE001
    bad.append(f"model could not be loaded/scored: {e}")

# --------------------------------------------------------- dashboard source
db = BASE / "students.db"
soft(db.is_file(),
     f"students.db present ({db.stat().st_size:,} B) - Metabase data source"
     if db.is_file() else "",
     "students.db not built yet - run: python load_dashboard_db.py")

# ---------------------------------------------------------------------- zip
z = BASE / "submission.zip"
if z.is_file():
    with zipfile.ZipFile(z) as zf:
        names = {n.split("/", 1)[-1] if "/" in n else n for n in zf.namelist()}
    missing = [r for r in REQUIRED + SUBMISSION_ARTEFACTS
               if r not in names and Path(r).name not in names]
    soft(not missing, f"submission.zip complete ({len(names)} entries)",
         f"submission.zip is missing: {missing}")
    soft(not any(".venv" in n for n in names),
         "submission.zip: no .venv inside",
         "submission.zip contains .venv - rebuild it")
else:
    warn.append("submission.zip not built yet (Phase 4 step 3)")

# -------------------------------------------------------------------- report
print("PASS")
for line in ok:
    print("  [+]", line)
if warn:
    print("\nWARN")
    for line in warn:
        print("  [!]", line)
if bad:
    print("\nBLOCKING")
    for line in bad:
        print("  [x]", line)

print(f"\n{len(ok)} passed, {len(warn)} warning(s), {len(bad)} blocking issue(s)")
sys.exit(1 if bad else 0)
