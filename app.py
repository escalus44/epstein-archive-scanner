from flask import Flask, render_template, request
import sqlite3
import os

# ---------- CONFIG ----------
BASE_OUTPUT = "/OUTPUTFOLDER"
DB_PATH = os.path.join(BASE_OUTPUT, "results.db")
FULLTEXT_DIR = os.path.join(BASE_OUTPUT, "fulltext")
FACES_DIR = os.path.join(BASE_OUTPUT, "faces")

app = Flask(__name__)


# ---------- DATABASE HELPERS ----------
def query(sql, params=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def query_results(q=None, kw=None, faces=None, limit=500):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    sql = "SELECT * FROM results WHERE 1=1"
    params = []

    if q:
        sql += " AND (real_file LIKE ? OR snippet LIKE ? OR names LIKE ? OR keywords LIKE ?)"
        like = f"%{q}%"
        params.extend([like, like, like, like])

    if kw:
        sql += " AND keywords LIKE ?"
        params.append(f"%{kw}%")

    if faces in ("0", "1"):
        sql += " AND has_faces = ?"
        params.append(int(faces))

    sql += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows


# ---------- ROUTES ----------

@app.route("/")
def index():
    q = request.args.get("q", "").strip() or None
    kw = request.args.get("kw", "").strip() or None
    faces = request.args.get("faces", "").strip() or None

    rows = query_results(q=q, kw=kw, faces=faces, limit=500)

    return render_template(
        "index.html",
        rows=rows,
        q=q,
        kw=kw,
        faces=faces,
        fulltext_dir=FULLTEXT_DIR,
        faces_dir=FACES_DIR,
    )


@app.route("/live")
def live():
    rows = query(
        """
        SELECT * FROM results
        ORDER BY id DESC
        LIMIT 100
        """
    )
    return render_template("live.html", rows=rows)


@app.route("/trump")
def trump_only():
    rows = query_results(kw="trump", limit=500)
    return render_template("trump.html", rows=rows)


@app.route("/flightlogs")
def flight_logs():
    rows = query_results(kw="flight", limit=500)
    return render_template("flightlogs.html", rows=rows)


@app.route("/faces")
def faces_only():
    rows = query_results(faces="1", limit=500)
    return render_template("faces.html", rows=rows)


@app.route("/view/<int:doc_id>")
def view_fulltext(doc_id):
    # Get the DB row
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM results WHERE id = ?", (doc_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return "Not found", 404

    # Load OCR text
    fulltext_path = os.path.join(FULLTEXT_DIR, row["fulltext_file"])

    try:
        with open(fulltext_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except:
        text = "(Could not load full text file)"

    return render_template("fulltext.html", row=row, text=text)


# ---------- MAIN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
