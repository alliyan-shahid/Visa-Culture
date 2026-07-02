import os
import time
from collections import deque
from datetime import datetime
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, flash, g, has_request_context, make_response, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, text
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv(override=False)

class Config:
    LOCAL_DB_URI = os.environ.get("LOCAL_DB_URI", "sqlite:///visaculture.db")
    DB_URI = os.environ.get("DB_URI", "")
    FORCE_ONLINE_DB = os.environ.get("FORCE_ONLINE_DB", "false").strip().lower() == "true"
    SQLALCHEMY_DATABASE_URI = DB_URI if DB_URI and FORCE_ONLINE_DB else (DB_URI if DB_URI else LOCAL_DB_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def active_db_backend():
        if Config.FORCE_ONLINE_DB and Config.DB_URI:
            return "postgres"
        if Config.DB_URI:
            return "postgres"
        return "sqlite"

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get("SECRET_KEY", "visa-culture-secret")

db = SQLAlchemy(app)
engine = None
request_metrics = deque(maxlen=2000)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(32), nullable=False)
    program = db.Column(db.String(128))
    university = db.Column(db.String(128))
    status = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    appointments = db.relationship("AppointmentRequest", back_populates="user", lazy="selectin")

class AppointmentRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128))
    phone = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    university = db.Column(db.String(128), nullable=False)
    message = db.Column(db.Text)
    date = db.Column(db.String(64), nullable=False)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", back_populates="appointments")

with app.app_context():
    db.create_all()
    engine = db.engine

    def ensure_sqlite_schema():
        if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
            pragma_rows = db.session.execute(text("PRAGMA table_info('user')")).all()
            existing_columns = [row[1] for row in pragma_rows]
            if "password_hash" not in existing_columns:
                db.session.execute(text('ALTER TABLE "user" ADD COLUMN password_hash VARCHAR(256)'))
                db.session.commit()

    ensure_sqlite_schema()

    def generate_username(base_email):
        base = base_email.split("@")[0]
        username = base
        suffix = 1
        while User.query.filter_by(username=username).first():
            username = f"{base}{suffix}"
            suffix += 1
        return username

    def ensure_default_users():
        admin_password = os.environ.get("ADMIN_PASSWORD", "***Removed***")

        developer_email = os.environ.get("DEVELOPER_EMAIL", "developer@techifyplatforms.com").strip().lower()
        developer_password = os.environ.get("DEVELOPER_PASSWORD", "***Removed***")
        developer = User.query.filter_by(email=developer_email).first()
        if developer is None:
            developer = User(
                username="developer",
                name="Developer",
                email=developer_email,
                password_hash=generate_password_hash(developer_password),
                role="developer",
            )
            db.session.add(developer)
            db.session.commit()
        elif not developer.password_hash:
            developer.password_hash = generate_password_hash(developer_password)
            db.session.add(developer)
            db.session.commit()

        if not User.query.filter_by(username="admin").first():
            app.logger.info("No admin user exists yet. Developer should create admin accounts.")

    ensure_default_users()
    app.logger.info(f"[startup] Active DB backend: {Config.active_db_backend()}")


@app.before_request
def track_request_start():
    g.request_start = time.perf_counter()
    g.request_db_time = 0.0
    g.request_query_count = 0


@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if not has_request_context():
        return
    if not hasattr(g, "request_db_time"):
        return
    g._sql_start = time.perf_counter()


@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if not has_request_context():
        return
    if not hasattr(g, "request_db_time") or not hasattr(g, "_sql_start"):
        return
    elapsed = (time.perf_counter() - g._sql_start) * 1000
    g.request_db_time += elapsed
    g.request_query_count += 1


@app.after_request
def collect_request_metrics(response):
    if not hasattr(g, "request_start"):
        return response
    duration = (time.perf_counter() - g.request_start) * 1000
    request_metrics.append({
        "path": request.path,
        "method": request.method,
        "status": response.status_code,
        "duration": duration,
        "db_time": getattr(g, "request_db_time", 0.0),
        "queries": getattr(g, "request_query_count", 0),
        "timestamp": datetime.utcnow(),
    })
    return response


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)

@app.context_processor
def inject_current_user():
    return {"current_user": get_current_user()}


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user = get_current_user()
        if not user or user.role != "admin":
            flash("Admin access is required.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


def admin_or_developer_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user = get_current_user()
        if not user or user.role not in {"admin", "developer"}:
            flash("Admin or developer access is required.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


def developer_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user = get_current_user()
        if not user or user.role != "developer":
            flash("Developer access is required.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view

@app.route("/")
def landing_page():
    return render_template("index.html")

@app.route("/admission-requirements")
def admission_requirements():
    return render_template("admission_requirements.html")

@app.route("/how-we-work")
def how_we_work():
    return render_template("how_we_work.html")

@app.route("/how-it-works")
def how_it_works_redirect():
    return redirect(url_for("how_we_work"), code=301)

@app.route("/universities/university-of-melbourne")
def university_of_melbourne():
    return render_template("melbourne_landing.html")

@app.route("/universities/australian-national-university")
def australian_national_university():
    return render_template("anu_landing.html")

@app.route("/universities/university-of-sydney")
def university_of_sydney():
    return render_template("sydney_landing.html")

@app.route("/universities/unsw-sydney")
def unsw_sydney():
    return render_template("unsw_landing.html")

@app.route("/universities/monash-university")
def monash_university():
    return render_template("monash_landing.html")

@app.route("/universities/university-of-queensland")
def university_of_queensland():
    return render_template("uq_landing.html")

@app.route("/universities")
def universities():
    university_cards = [
        {
            "name": "University of Melbourne",
            "ranking": "#1 in Australia",
            "badge": "Group of Eight",
            "region": "Melbourne",
            "category": "Research-led",
            "type": "Go8",
            "intake": "Feb / Jul",
            "tuition": "From AUD 45k+",
            "approval_focus": "High-academic achievers",
            "summary": "A strong fit for students who want globally recognized academics, premium research pathways, and a polished city-campus experience.",
            "best_for": "Business, law, and advanced research",
            "tags": ["Scholarships", "Research", "Career outcomes"],
            "image": "images/hero melbourne.webp",
            "mobile_image": "images/hero melbourne.webp",
            "url": url_for("university_of_melbourne"),
            "accent": "#0a4d8f",
            "accent_bg": "rgba(10, 77, 143, 0.12)",
        },
        {
            "name": "Australian National University",
            "ranking": "#2 in Australia",
            "badge": "Policy hub",
            "region": "Canberra",
            "category": "Research-first",
            "type": "Go8",
            "intake": "Feb / Jul",
            "tuition": "From AUD 44k+",
            "approval_focus": "Policy and research profiles",
            "summary": "Ideal for students looking for policy, politics, economics, and a serious academic environment with strong research culture.",
            "best_for": "Public policy, international relations, and economics",
            "tags": ["Research", "Government links", "High academic focus"],
            "image": "images/anu hero.webp",
            "mobile_image": "images/anu hero.webp",
            "url": url_for("australian_national_university"),
            "accent": "#0f766e",
            "accent_bg": "rgba(15, 118, 110, 0.12)",
        },
        {
            "name": "University of Sydney",
            "ranking": "#3 in Australia",
            "badge": "Historic prestige",
            "region": "Sydney",
            "category": "City campus",
            "type": "Go8",
            "intake": "Feb / Aug",
            "tuition": "From AUD 46k+",
            "approval_focus": "High-profile academic track",
            "summary": "A premium choice for ambitious students who want iconic branding, a vibrant urban setting, and strong employer recognition.",
            "best_for": "Health, arts, commerce, and global careers",
            "tags": ["Prestige", "Industry network", "Student life"],
            "image": "images/sydney hero.webp",
            "mobile_image": "images/m sydney hero.webp",
            "url": url_for("university_of_sydney"),
            "accent": "#0e7490",
            "accent_bg": "rgba(14, 116, 144, 0.12)",
        },
        {
            "name": "UNSW Sydney",
            "ranking": "#4 in Australia",
            "badge": "Innovation focus",
            "region": "Sydney",
            "category": "Career-driven",
            "type": "Go8",
            "intake": "Feb / Jun / Sep",
            "tuition": "From AUD 45k+",
            "approval_focus": "Tech and engineering profiles",
            "summary": "Best suited for students who want practical learning, technology, and pathways backed by a very strong industry reputation.",
            "best_for": "Engineering, tech, and business",
            "tags": ["Industry projects", "Co-op style learning", "Employability"],
            "image": "images/hero unsw.webp",
            "mobile_image": "images/hero unsw.webp",
            "url": url_for("unsw_sydney"),
            "accent": "#b45309",
            "accent_bg": "rgba(180, 83, 9, 0.12)",
        },
        {
            "name": "Monash University",
            "ranking": "#5 in Australia",
            "badge": "Global campus",
            "region": "Melbourne",
            "category": "International outlook",
            "type": "Go8",
            "intake": "Feb / Jul / Nov",
            "tuition": "From AUD 42k+",
            "approval_focus": "Flexible, globally minded profiles",
            "summary": "A great match for students seeking globally connected programs, flexible pathways, and broad subject options.",
            "best_for": "Pharmacy, engineering, business, and health",
            "tags": ["Global reach", "Flexible pathways", "Large alumni network"],
            "image": "images/monash hero.webp",
            "mobile_image": "images/monash hero.webp",
            "url": url_for("monash_university"),
            "accent": "#7c3aed",
            "accent_bg": "rgba(124, 58, 237, 0.12)",
        },
        {
            "name": "University of Queensland",
            "ranking": "#6 in Australia",
            "badge": "Top research",
            "region": "Brisbane",
            "category": "Balanced excellence",
            "type": "Go8",
            "intake": "Feb / Jul",
            "tuition": "From AUD 41k+",
            "approval_focus": "Strong academic and research profiles",
            "summary": "A strong option for students who want high-quality teaching, excellent research, and a warm student environment.",
            "best_for": "Science, life sciences, and business",
            "tags": ["Research", "Brisbane lifestyle", "Strong outcomes"],
            "image": "images/hero uq.webp",
            "mobile_image": "images/hero uq.webp",
            "url": url_for("university_of_queensland"),
            "accent": "#0891b2",
            "accent_bg": "rgba(8, 145, 178, 0.12)",
        },
    ]
    hero_stats = [
        {"value": "6", "label": "dedicated university guides"},
        {"value": "100%", "label": "built for Pakistani students"},
        {"value": "1", "label": "clear route to each university page"},
        {"value": "24/7", "label": "consultancy support direction"},
    ]
    journey_steps = [
        {
            "title": "Shortlist with clarity",
            "text": "We match your profile, budget, and goals with the universities that actually make sense for your journey.",
        },
        {
            "title": "Open the right guide",
            "text": "Each university page gives a tailored breakdown of admission, scholarships, costs, and student fit.",
        },
        {
            "title": "Move to application",
            "text": "Once the shortlist feels right, you can move into document preparation and application planning with confidence.",
        },
    ]
    spotlight = university_cards[0]
    return render_template(
        "universities.html",
        hero_stats=hero_stats,
        universities=university_cards,
        journey_steps=journey_steps,
        spotlight=spotlight,
        page_summary={
            "title": "Top universities with dedicated consultancy-grade guides",
            "subtitle": "Compare the best Australian universities in one polished shortlist, then jump straight into a designed page for each one.",
        },
    )

@app.route("/booking")
def booking_page():
    return render_template(
        "booking.html",
        page_summary={
            "title": "Book a consultation with Visa Culture",
            "subtitle": "Move your appointment flow into a dedicated page with a calmer, more focused experience.",
        },
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
@admin_or_developer_required
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "client")
        program = request.form.get("program", "")
        university = request.form.get("university", "")
        status = request.form.get("status", "")

        if not name or not email or not password or not role:
            flash("Please complete all required fields.", "error")
            return render_template("register.html")

        current_user = get_current_user()
        if current_user.role == "admin" and role != "client":
            flash("Admins can only create client accounts.", "error")
            return render_template("register.html")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with that email already exists.", "error")
            return render_template("register.html")

        username = generate_username(email)
        new_user = User(
            username=username,
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
            program=program,
            university=university,
            status=status,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("User account created successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    if user.role == "admin":
        clients = User.query.filter_by(role="client").all()
        requests = AppointmentRequest.query.order_by(AppointmentRequest.requested_at.desc()).all()
        return render_template("admin_dashboard.html", user=user, clients=clients, requests=requests)

    if user.role == "developer":
        total_users = User.query.count()
        total_clients = User.query.filter_by(role="client").count()
        total_admins = User.query.filter_by(role="admin").count()
        total_developers = User.query.filter_by(role="developer").count()
        total_requests = AppointmentRequest.query.count()
        total_universities = db.session.query(AppointmentRequest.university).distinct().count()
        return render_template(
            "developer_dashboard.html",
            user=user,
            total_users=total_users,
            total_clients=total_clients,
            total_admins=total_admins,
            total_developers=total_developers,
            total_requests=total_requests,
            total_universities=total_universities,
            active_db=Config.active_db_backend(),
        )

    return render_template("client_dashboard.html", user=user)


@app.route("/developer/stats")
@developer_required
def developer_stats():
    # aggregate metrics from request_metrics deque
    metrics = list(request_metrics)
    total = len(metrics)
    avg_duration = (sum(m.get("duration", 0) for m in metrics) / total) if total else 0.0
    avg_db = (sum(m.get("db_time", 0) for m in metrics) / total) if total else 0.0
    # compute simple slow endpoints aggregation
    endpoints = {}
    for m in metrics:
        path = m.get("path", "unknown")
        endpoints.setdefault(path, []).append(m.get("duration", 0))

    slow_list = []
    for path, durations in endpoints.items():
        avg = sum(durations) / len(durations) if durations else 0
        slow_list.append((path, {"avg": avg, "count": len(durations)}))

    slow_list.sort(key=lambda x: x[1]["avg"], reverse=True)
    # convert to template-friendly structure
    slow_endpoints = [(p, info) for p, info in slow_list[:10]]

    return render_template(
        "developer_stats.html",
        total_requests=total,
        avg_duration=avg_duration,
        avg_db=avg_db,
        slow_endpoints=slow_endpoints,
    )

@app.route("/appointments")
@admin_or_developer_required
def appointments_page():
    requests = AppointmentRequest.query.order_by(AppointmentRequest.requested_at.desc()).all()
    return render_template("appointments.html", requests=requests)

@app.route("/appointments/<int:request_id>")
@admin_or_developer_required
def appointment_detail(request_id):
    appointment = AppointmentRequest.query.get(request_id)
    if appointment is None:
        flash("Appointment request not found.", "error")
        return redirect(url_for("appointments_page"))
    return render_template("appointment_detail.html", request=appointment)

@app.route("/book", methods=["POST"])
def book_appointment():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    address = request.form.get("address")
    university = request.form.get("university")
    message = request.form.get("message")
    date = request.form.get("date")

    if not name or not phone or not address or not university or not date:
        flash("Please complete all required fields before booking.", "error")
        return redirect(url_for("booking_page"))

    user = get_current_user()

    appointment = AppointmentRequest(
        user_id=user.id if user else None,
        name=name,
        email=email,
        phone=phone,
        address=address,
        university=university,
        message=message,
        date=date,
    )
    db.session.add(appointment)
    db.session.commit()

    flash("Your consultancy appointment request has been submitted. Our team will reach out soon.", "success")
    return redirect(url_for("booking_page"))

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("landing_page"))

@app.route("/robots.txt")
def robots_txt():
    content = """User-agent: *
Disallow: /admin
Disallow: /developer
Disallow: /login
Disallow: /register
Disallow: /dashboard
Disallow: /book

Sitemap: {}/sitemap.xml
""".format(request.url_root.rstrip("/"))
    response = make_response(content)
    response.headers["Content-Type"] = "text/plain"
    return response

@app.route("/sitemap.xml")
def sitemap_xml():
    pages = [
        {"path": "", "priority": 1.0},
        {"path": "admission-requirements", "priority": 0.8},
        {"path": "how-we-work", "priority": 0.8},
        {"path": "universities", "priority": 0.9},
        {"path": "booking", "priority": 0.7},
    ]
    university_pages = [
        {"path": "universities/university-of-melbourne", "priority": 0.9},
        {"path": "universities/australian-national-university", "priority": 0.9},
        {"path": "universities/university-of-sydney", "priority": 0.9},
        {"path": "universities/unsw-sydney", "priority": 0.9},
        {"path": "universities/monash-university", "priority": 0.9},
        {"path": "universities/university-of-queensland", "priority": 0.9},
    ]

    url_root = request.url_root.rstrip("/")
    urls = pages + university_pages
    lastmod = datetime.utcnow().date().isoformat()

    xml_items = [
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">",
    ]
    for entry in urls:
        xml_items.append("  <url>")
        xml_items.append(f"    <loc>{url_root}/{entry['path']}</loc>")
        xml_items.append(f"    <lastmod>{lastmod}</lastmod>")
        xml_items.append("    <changefreq>weekly</changefreq>")
        xml_items.append(f"    <priority>{entry['priority']:.1f}</priority>")
        xml_items.append("  </url>")
    xml_items.append("</urlset>")

    response = make_response("\n".join(xml_items))
    response.headers["Content-Type"] = "application/xml"
    return response

if __name__ == "__main__":
    app.run(debug=True)
