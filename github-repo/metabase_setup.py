"""Build the Jaya Jaya Institut Metabase dashboard via the Metabase API.

Variant: OCEAN (cool blue + teal, coral for dropout).

Code organisation
-----------------
This file is written as a *linear step pipeline*. Everything the run needs
lives in one mutable ``STATE`` dictionary; each stage of the build is a
``step_*`` function that reads from and writes to that dictionary, and
``PIPELINE`` at the bottom lists those steps in execution order. Adding a
stage means writing one function and adding one name to that list.

Layout of this module, top to bottom:

    1. settings    - hosts, credentials, names
    2. palette     - the OCEAN colour set
    3. sql         - every query, keyed by card
    4. presets     - reusable visualization_settings blocks
    5. blueprint   - CARDS: the ordered card list
    6. transport   - thin urllib wrapper over the Metabase API
    7. steps       - step_* functions, one per build stage
    8. pipeline    - PIPELINE list + main()

Prerequisites
-------------
1. ``python load_dashboard_db.py`` (parent folder) produced ``students.db``.
2. A Metabase container is running with that file mounted, e.g.
   ``docker run -d -p 3004:3000 --name metabase4
   -v "<abs path>/students.db:/data/students.db" metabase/metabase``.

Usage
-----
    python metabase_setup.py            # talks to http://localhost:3004
    MB_HOST=http://localhost:3999 python metabase_setup.py

Idempotent: the admin account is created only on a fresh instance, an
existing database connection is reused, and cards/dashboards created by an
earlier run are updated in place. Standard library only.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

# ------------------------------------------------------------- 1. settings
DEFAULT_PORT = 3004                      # OCEAN owns this instance
HOST = os.environ.get(
    "MB_HOST", "http://localhost:{}".format(DEFAULT_PORT)).rstrip("/")

EMAIL = "root@mail.com"
PASSWORD = "root123"
FIRST_NAME = "Emilia"
LAST_NAME = "Loho"
SITE_NAME = "Jaya Jaya Institut"

DB_NAME = "Jaya Jaya Institut"
DB_PATH_IN_CONTAINER = "/data/students.db"
DASHBOARD_NAME = "Jaya Jaya Institut - Student Monitoring"
DASHBOARD_DESC = ("Monitoring performa siswa & deteksi dini dropout "
                  "- Emilia Loho.")

GRID_WIDTH = 24                          # Metabase dashboards are 24 columns

# -------------------------------------------------------------- 2. palette
# Colourblind-safe, checked for contrast on Metabase's light and dark canvas.
RATE = "#3D8FC7"        # primary  - blue,  every dropout-rate bar
SECONDARY = "#2EA98C"   # support  - teal,  count / second series
DANGER = "#E4643B"      # accent   - coral, reserved for the Dropout slice
PIE_COLORS = {"Graduate": RATE, "Dropout": DANGER, "Enrolled": SECONDARY}

# ------------------------------------------------------------------ 3. sql
# One entry per card. Keeping the SQL apart from the blueprint keeps the
# blueprint readable and the queries easy to paste into Metabase's editor.
SQL = {
    "total": """
        SELECT COUNT(*) AS total_siswa
        FROM students
    """,
    "dropout_count": """
        SELECT SUM(is_dropout) AS jumlah_dropout
        FROM students
    """,
    "dropout_pct": """
        SELECT ROUND(AVG(is_dropout) * 100, 1) AS dropout_rate_pct
        FROM students
    """,
    "avg_risk": """
        SELECT ROUND(AVG(dropout_risk_score), 3) AS avg_risk_score
        FROM students
        WHERE status = 'Enrolled'
    """,
    "status_mix": """
        SELECT status AS label, COUNT(*) AS jumlah_siswa
        FROM students
        GROUP BY status
        ORDER BY jumlah_siswa DESC
    """,
    "academic": """
        SELECT status AS label,
               ROUND(AVG(units_2nd_sem_approved), 2) AS avg_units_2nd_sem_approved,
               ROUND(AVG(units_1st_sem_approved), 2) AS avg_units_1st_sem_approved
        FROM students
        GROUP BY status
        ORDER BY avg_units_2nd_sem_approved DESC
    """,
    "by_course": """
        SELECT course AS label, COUNT(*) AS jumlah_siswa,
               ROUND(AVG(is_dropout) * 100, 1) AS dropout_rate_pct
        FROM students
        GROUP BY course
        ORDER BY dropout_rate_pct DESC
    """,
    "risk_histogram": """
        SELECT CAST(dropout_risk_score * 10 AS INT) / 10.0 AS risk_bucket,
               COUNT(*) AS jumlah_siswa
        FROM students
        WHERE status = 'Enrolled'
        GROUP BY risk_bucket
        ORDER BY risk_bucket
    """,
    "high_risk": """
        SELECT course, gender, age_group, tuition_up_to_date, debtor,
               scholarship_holder, units_1st_sem_approved,
               units_2nd_sem_approved, grade_2nd_sem, dropout_risk_score
        FROM students
        WHERE status = 'Enrolled' AND dropout_risk_score > 0.6
        ORDER BY dropout_risk_score DESC
    """,
}


def rate_by(column, order="dropout_rate_pct DESC"):
    """Every 'dropout rate per <category>' card is the same query shape."""
    return """
        SELECT {col} AS label, COUNT(*) AS jumlah_siswa,
               ROUND(AVG(is_dropout) * 100, 1) AS dropout_rate_pct
        FROM students
        GROUP BY {col}
        ORDER BY {order}
    """.format(col=column, order=order)


# -------------------------------------------------------------- 4. presets
def rate_bar():
    """Vertical bar of dropout_rate_pct, painted with the primary colour."""
    return {
        "graph.dimensions": ["label"],
        "graph.metrics": ["dropout_rate_pct"],
        "graph.x_axis.title_text": "",
        "graph.y_axis.title_text": "Dropout rate (%)",
        "graph.show_values": True,
        "series_settings": {"dropout_rate_pct": {"color": RATE}},
    }


def percent_scalar(column):
    """Scalar that renders as '32.1 %'."""
    key = '["name","{}"]'.format(column)
    return {"column_settings": {key: {"suffix": " %"}}}


# ------------------------------------------------------------ 5. blueprint
# The ordered card list. OCEAN reads top-down as:
# headline numbers -> composition -> financial drivers -> demographics ->
# programme breakdown -> risk monitoring.
CARDS = [
    # -- KPI strip ---------------------------------------------------------
    {"name": "Total Siswa",
     "sql": SQL["total"], "display": "scalar",
     "description": "Jumlah seluruh siswa dalam dataset.",
     "viz": {}, "width": 6, "height": 3},

    {"name": "Jumlah Dropout",
     "sql": SQL["dropout_count"], "display": "scalar",
     "description": "Jumlah siswa berstatus Dropout.",
     "viz": {}, "width": 6, "height": 3},

    {"name": "Persentase Dropout",
     "sql": SQL["dropout_pct"], "display": "scalar",
     "description": "Dropout rate keseluruhan (%).",
     "viz": percent_scalar("dropout_rate_pct"), "width": 6, "height": 3},

    {"name": "Rata-rata Skor Risiko - Siswa Enrolled",
     "sql": SQL["avg_risk"], "display": "scalar",
     "description": "Rata-rata dropout_risk_score dari model untuk siswa "
                    "yang masih aktif.",
     "viz": {}, "width": 6, "height": 3},

    # -- composition -------------------------------------------------------
    {"name": "Distribusi Status Siswa",
     "sql": SQL["status_mix"], "display": "pie",
     "description": "Komposisi Dropout / Enrolled / Graduate.",
     "viz": {"pie.dimension": "label", "pie.metric": "jumlah_siswa",
             "pie.colors": dict(PIE_COLORS), "pie.show_legend": True},
     "width": 12, "height": 6},

    {"name": "Rata-rata SKS Lulus Semester 1-2 per Status",
     "sql": SQL["academic"], "display": "bar",
     "description": "Perbandingan performa akademik semester awal antar "
                    "status siswa.",
     "viz": {"graph.dimensions": ["label"],
             "graph.metrics": ["avg_units_2nd_sem_approved",
                               "avg_units_1st_sem_approved"],
             "graph.y_axis.title_text": "Rata-rata SKS lulus",
             "graph.show_values": True,
             "series_settings": {
                 "avg_units_2nd_sem_approved": {"color": RATE},
                 "avg_units_1st_sem_approved": {"color": SECONDARY}}},
     "width": 12, "height": 6},

    # -- financial drivers -------------------------------------------------
    {"name": "Dropout Rate per Status Pembayaran",
     "sql": rate_by("tuition_up_to_date"), "display": "bar",
     "description": "Biaya kuliah lancar (Yes) vs menunggak (No).",
     "viz": rate_bar(), "width": 8, "height": 5},

    {"name": "Dropout Rate per Status Beasiswa",
     "sql": rate_by("scholarship_holder"), "display": "bar",
     "description": "Penerima beasiswa vs bukan penerima.",
     "viz": rate_bar(), "width": 8, "height": 5},

    {"name": "Dropout Rate per Status Debtor",
     "sql": rate_by("debtor"), "display": "bar",
     "description": "Siswa dengan tunggakan vs tanpa tunggakan.",
     "viz": rate_bar(), "width": 8, "height": 5},

    # -- demographic drivers ----------------------------------------------
    {"name": "Dropout Rate per Kelompok Usia",
     "sql": rate_by("age_group", order="label"), "display": "bar",
     "description": "Dropout rate menurut usia saat mendaftar.",
     "viz": rate_bar(), "width": 12, "height": 5},

    {"name": "Dropout Rate per Gender",
     "sql": rate_by("gender"), "display": "bar",
     "description": "Dropout rate menurut gender.",
     "viz": rate_bar(), "width": 12, "height": 5},

    # -- programme breakdown ----------------------------------------------
    # Full width and deliberately tall: Metabase folds the tail of a row
    # chart into one "Other (n)" bar whose value is the SUM of the grouped
    # rows, which is meaningless for a rate. How many bars survive depends on
    # the tile height, so the tile has to be tall enough for all 17 courses.
    {"name": "Dropout Rate per Program Studi",
     "sql": SQL["by_course"], "display": "row",
     "description": "Seluruh 17 program studi, diurutkan dari dropout rate "
                    "tertinggi.",
     "viz": {"graph.dimensions": ["label"],
             "graph.metrics": ["dropout_rate_pct"],
             "graph.max_categories_enabled": False,
             "graph.max_categories": 30,
             "graph.show_values": True,
             "series_settings": {"dropout_rate_pct": {"color": RATE}}},
     "width": 24, "height": 15},

    # -- risk monitoring ---------------------------------------------------
    {"name": "Distribusi Skor Risiko - Siswa Enrolled",
     "sql": SQL["risk_histogram"], "display": "bar",
     "description": "Histogram dropout_risk_score (bin 0,1) untuk siswa "
                    "yang masih aktif.",
     "viz": {"graph.dimensions": ["risk_bucket"],
             "graph.metrics": ["jumlah_siswa"],
             "graph.x_axis.title_text": "Skor risiko dropout",
             "graph.y_axis.title_text": "Jumlah siswa",
             "graph.show_values": True,
             "series_settings": {"jumlah_siswa": {"color": SECONDARY}}},
     "width": 24, "height": 6},

    {"name": "Siswa Enrolled Berisiko Tinggi (skor > 0,6)",
     "sql": SQL["high_risk"], "display": "table",
     "description": "Daftar prioritas bimbingan khusus: siswa aktif dengan "
                    "skor risiko di atas 0,6.",
     "viz": {}, "width": 24, "height": 8},
]

# --------------------------------------------------------------- run state
# Every step reads and writes this one dictionary, so a step's inputs and
# outputs are visible from its body alone.
STATE = {
    "session": None,      # X-Metabase-Session token
    "properties": None,   # /api/session/properties payload
    "db_id": None,        # id of the SQLite connection inside Metabase
    "cards": [],          # [(card_id, blueprint entry), ...]
    "dashboard_id": None,
}


# ------------------------------------------------------------ 6. transport
def call(method, path, payload=None, expect_json=True):
    """One request against the Metabase API. Raises RuntimeError on failure."""
    url = "{}/api/{}".format(HOST, path.lstrip("/"))
    body = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(url, data=body, method=method)
    request.add_header("Content-Type", "application/json")
    if STATE["session"]:
        request.add_header("X-Metabase-Session", STATE["session"])
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:800]
        raise RuntimeError("{} {} -> HTTP {}: {}".format(
            method, path, exc.code, detail)) from None
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "cannot reach Metabase at {} ({}). Is the container running?"
            .format(HOST, exc.reason)) from None
    if not expect_json or not raw:
        return None
    return json.loads(raw)


# ---------------------------------------------------------------- 7. steps
def step_wait(timeout=300):
    """Block until the instance answers /api/session/properties."""
    print("Waiting for Metabase at {} ...".format(HOST), end="", flush=True)
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            STATE["properties"] = call("GET", "session/properties")
            print(" up.")
            return
        except RuntimeError:
            print(".", end="", flush=True)
            time.sleep(5)
    sys.exit("\nMetabase did not become ready within {}s.".format(timeout))


def step_admin():
    """Create the admin account on a fresh instance, otherwise just log in."""
    properties = STATE["properties"]
    if properties.get("has-user-setup"):
        print("Admin already exists - logging in.")
    else:
        token = properties.get("setup-token")
        if not token:
            sys.exit("Metabase reports no admin and no setup token; finish "
                     "setup manually at " + HOST)
        print("Creating admin {} ...".format(EMAIL))
        result = call("POST", "setup", {
            "token": token,
            "user": {"first_name": FIRST_NAME, "last_name": LAST_NAME,
                     "email": EMAIL, "password": PASSWORD,
                     "site_name": SITE_NAME},
            "prefs": {"site_name": SITE_NAME, "site_locale": "en",
                      "allow_tracking": False},
        })
        if isinstance(result, dict) and result.get("id"):
            STATE["session"] = result["id"]
            return
    STATE["session"] = call(
        "POST", "session", {"username": EMAIL, "password": PASSWORD})["id"]
    print("Logged in.")


def step_database():
    """Attach students.db, reusing the connection if it is already there."""
    listing = call("GET", "database")
    databases = listing["data"] if isinstance(listing, dict) else listing
    for database in databases:
        if database["name"] == DB_NAME:
            STATE["db_id"] = database["id"]
            print("Reusing database '{}' (id={}).".format(
                DB_NAME, database["id"]))
            return
    print("Adding SQLite database '{}' -> {} ...".format(
        DB_NAME, DB_PATH_IN_CONTAINER))
    created = call("POST", "database", {
        "engine": "sqlite",
        "name": DB_NAME,
        "details": {"db": DB_PATH_IN_CONTAINER, "advanced-options": False},
        "is_full_sync": True,
    })
    STATE["db_id"] = created["id"]


def step_sync(timeout=180):
    """Wait until Metabase has read the schema of the students table."""
    db_id = STATE["db_id"]
    print("Syncing schema ...", end="", flush=True)
    try:
        call("POST", "database/{}/sync_schema".format(db_id), {},
             expect_json=False)
    except RuntimeError:
        pass                              # some builds answer with no body
    deadline = time.time() + timeout
    while time.time() < deadline:
        metadata = call("GET", "database/{}/metadata".format(db_id))
        tables = [t for t in metadata.get("tables", [])
                  if t["name"] == "students"]
        if tables and tables[0].get("fields"):
            print(" done ({} fields on 'students').".format(
                len(tables[0]["fields"])))
            return
        print(".", end="", flush=True)
        time.sleep(5)
    sys.exit("\nTable 'students' never appeared. Check that students.db is "
             "mounted at {} inside the container."
             .format(DB_PATH_IN_CONTAINER))


def step_cards():
    """Create (or update) one saved question per blueprint entry."""
    print("Creating questions ...")
    existing = {c["name"]: c["id"] for c in (call("GET", "card") or [])}
    for blueprint in CARDS:
        payload = {
            "name": blueprint["name"],
            "description": blueprint["description"],
            "display": blueprint["display"],
            "visualization_settings": blueprint["viz"],
            "collection_id": None,                 # root collection
            "dataset_query": {
                "type": "native",
                "database": STATE["db_id"],
                "native": {"query": blueprint["sql"].strip(),
                           "template-tags": {}},
            },
        }
        if blueprint["name"] in existing:
            card_id = existing[blueprint["name"]]
            call("PUT", "card/{}".format(card_id), payload)
            print("  updated card: {}".format(blueprint["name"]))
        else:
            card_id = call("POST", "card", payload)["id"]
            print("  created card: {}".format(blueprint["name"]))
        STATE["cards"].append((card_id, blueprint))


def step_dashboard():
    """Create (or reuse) the dashboard and lay the cards out on its grid."""
    for dashboard in (call("GET", "dashboard") or []):
        if dashboard["name"] == DASHBOARD_NAME and not dashboard.get("archived"):
            STATE["dashboard_id"] = dashboard["id"]
            print("Reusing dashboard (id={}).".format(dashboard["id"]))
            break
    else:
        STATE["dashboard_id"] = call("POST", "dashboard", {
            "name": DASHBOARD_NAME,
            "description": DASHBOARD_DESC,
            "collection_id": None,
        })["id"]
        print("Created dashboard (id={}).".format(STATE["dashboard_id"]))

    # Flow the cards across the 24-column grid, wrapping when a row is full.
    dashcards, column, row, row_height = [], 0, 0, 0
    for index, (card_id, blueprint) in enumerate(STATE["cards"]):
        width, height = blueprint["width"], blueprint["height"]
        if column + width > GRID_WIDTH:
            row += row_height
            column, row_height = 0, 0
        dashcards.append({
            "id": -(index + 1), "card_id": card_id,
            "row": row, "col": column, "size_x": width, "size_y": height,
            "parameter_mappings": [], "visualization_settings": {},
        })
        column += width
        row_height = max(row_height, height)

    dash_id = STATE["dashboard_id"]
    try:
        call("PUT", "dashboard/{}".format(dash_id), {"dashcards": dashcards})
    except RuntimeError as exc:
        print("  (dashcards PUT failed: {}\n   falling back to per-card POST)"
              .format(exc))
        for dashcard in dashcards:
            call("POST", "dashboard/{}/cards".format(dash_id), {
                "cardId": dashcard["card_id"], "row": dashcard["row"],
                "col": dashcard["col"], "size_x": dashcard["size_x"],
                "size_y": dashcard["size_y"]})
    print("Placed {} cards on the dashboard.".format(len(dashcards)))


def step_report():
    """Print where to look and what to do next."""
    print("\nDone. Open the dashboard at:")
    print("  {}/dashboard/{}".format(HOST, STATE["dashboard_id"]))
    print("\nNext steps:")
    print("  1. Screenshot it as emilia_loho-dashboard.png")
    print("  2. docker cp <container>:/metabase.db/metabase.db.mv.db ./")


# ------------------------------------------------------------- 8. pipeline
PIPELINE = [
    step_wait,
    step_admin,
    step_database,
    step_sync,
    step_cards,
    step_dashboard,
    step_report,
]


def main():
    print("Theme: ocean  |  target: {}".format(HOST))
    for step in PIPELINE:
        step()


if __name__ == "__main__":
    main()
