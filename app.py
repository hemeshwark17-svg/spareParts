import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "local-demo-change-this")

def db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "vehicle_spares")
    )

def admin_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def home():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    conn = db()
    cur = conn.cursor(dictionary=True)
    sql = "SELECT * FROM spare_parts WHERE is_active=1"
    args = []
    if q:
        sql += " AND (part_name LIKE %s OR part_number LIKE %s OR vehicle_compatibility LIKE %s)"
        args += [f"%{q}%"] * 3
    if category:
        sql += " AND category=%s"
        args.append(category)
    sql += " ORDER BY part_name"
    cur.execute(sql, args)
    parts = cur.fetchall()
    cur.execute("SELECT DISTINCT category FROM spare_parts WHERE is_active=1 ORDER BY category")
    categories = [x["category"] for x in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template("index.html", parts=parts, categories=categories, q=q, selected=category)

@app.route("/part/<int:part_id>")
def detail(part_id):
    conn = db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM spare_parts WHERE part_id=%s AND is_active=1", (part_id,))
    part = cur.fetchone()
    cur.close()
    conn.close()
    if not part:
        return render_template("not_found.html"), 404
    return render_template("detail.html", part=part)

@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == os.getenv("ADMIN_PASSWORD", "change-me-now"):
            session["admin"] = True
            return redirect(url_for("admin"))
        flash("Password was incorrect.")
    return render_template("login.html")

@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/admin")
@admin_only
def admin():
    conn = db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM spare_parts ORDER BY part_id DESC")
    parts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("admin.html", parts=parts)

def form_data():
    return {
        "part_number": request.form.get("part_number", "").strip(),
        "part_name": request.form.get("part_name", "").strip(),
        "category": request.form.get("category", "Other").strip() or "Other",
        "vehicle_compatibility": request.form.get("vehicle_compatibility", "Multiple models").strip(),
        "price": request.form.get("price", "0").strip(),
        "stock_quantity": request.form.get("stock_quantity", "0").strip(),
        "supplier_name": request.form.get("supplier_name", "Demo Supplier").strip(),
        "description": request.form.get("description", "").strip(),
        "is_active": 1 if request.form.get("is_active") == "on" else 0
    }

@app.route("/admin/add", methods=["GET", "POST"])
@admin_only
def add():
    if request.method == "POST":
        d = form_data()
        if not d["part_number"] or not d["part_name"]:
            flash("Part number and part name are required.")
            return render_template("part_form.html", part=d, heading="Add part")
        conn = db()
        cur = conn.cursor()
        try:
            cur.execute("""INSERT INTO spare_parts
              (part_number,part_name,category,vehicle_compatibility,price,stock_quantity,supplier_name,description,is_active)
              VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
              (d["part_number"],d["part_name"],d["category"],d["vehicle_compatibility"],d["price"],
               d["stock_quantity"],d["supplier_name"],d["description"],d["is_active"]))
            conn.commit()
            flash("Part added successfully.")
        except Error:
            conn.rollback()
            flash("Could not add part. Check the unique part number and values.")
        finally:
            cur.close()
            conn.close()
        return redirect(url_for("admin"))
    return render_template("part_form.html", part=None, heading="Add part")

@app.route("/admin/edit/<int:part_id>", methods=["GET", "POST"])
@admin_only
def edit(part_id):
    conn = db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM spare_parts WHERE part_id=%s", (part_id,))
    part = cur.fetchone()
    if not part:
        cur.close(); conn.close()
        return render_template("not_found.html"), 404
    if request.method == "POST":
        d = form_data()
        try:
            cur.execute("""UPDATE spare_parts SET part_number=%s,part_name=%s,category=%s,
              vehicle_compatibility=%s,price=%s,stock_quantity=%s,supplier_name=%s,description=%s,is_active=%s
              WHERE part_id=%s""",
              (d["part_number"],d["part_name"],d["category"],d["vehicle_compatibility"],d["price"],
               d["stock_quantity"],d["supplier_name"],d["description"],d["is_active"],part_id))
            conn.commit()
            flash("Part updated.")
            cur.close(); conn.close()
            return redirect(url_for("admin"))
        except Error:
            conn.rollback()
            flash("Update failed. Check the part number and values.")
    cur.close(); conn.close()
    return render_template("part_form.html", part=part, heading="Edit part")

@app.route("/admin/hide/<int:part_id>", methods=["POST"])
@admin_only
def hide(part_id):
    conn = db()
    cur = conn.cursor()
    cur.execute("UPDATE spare_parts SET is_active=0 WHERE part_id=%s", (part_id,))
    conn.commit()
    cur.close(); conn.close()
    flash("Part hidden from the public catalogue.")
    return redirect(url_for("admin"))

@app.errorhandler(Error)
def database_error(error):
    app.logger.exception("Database error")
    return "Database connection failed. Check MySQL and your DB_* environment variables.", 500

if __name__ == "__main__":
    app.run(debug=True)
