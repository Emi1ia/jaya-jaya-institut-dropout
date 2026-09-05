"""Load data_dashboard.csv into a SQLite database for Metabase.

Metabase cannot read CSV files directly, so the dashboard data is
materialised into a single `students` table. SQLite is used because the
file can be mounted straight into the Metabase container and it needs no
extra Python dependencies.

    python load_dashboard_db.py            -> writes students.db

Then start Metabase with the database mounted:

    docker run -d -p 3000:3000 --name metabase \
      -v "$(pwd)/students.db:/data/students.db" \
      metabase/metabase

and add it in Metabase as a SQLite database with path /data/students.db
"""
import sqlite3
from pathlib import Path

import pandas as pd

CSV = Path("data_dashboard.csv")
DB = Path("students.db")

df = pd.read_csv(CSV)

# SQLite has no boolean type; keep is_dropout as 0/1 int for easy AVG()
df["is_dropout"] = df["is_dropout"].astype(int)

if DB.exists():
    DB.unlink()

with sqlite3.connect(DB) as con:
    df.to_sql("students", con, index=False)
    con.execute("CREATE INDEX idx_students_status ON students(status)")
    con.execute("CREATE INDEX idx_students_course ON students(course)")
    con.commit()

    n, = con.execute("SELECT COUNT(*) FROM students").fetchone()
    print(f"Wrote {DB} - table 'students', {n} rows x {df.shape[1]} columns")
    print("\nstatus breakdown:")
    for status, cnt, rate in con.execute(
        "SELECT status, COUNT(*), ROUND(AVG(is_dropout) * 100, 1) "
        "FROM students GROUP BY status ORDER BY COUNT(*) DESC"
    ):
        print(f"  {status:<10} {cnt:>5}  dropout_rate={rate}%")
