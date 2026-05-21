import os
import time
from collections import deque
from datetime import datetime
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, flash, g, has_request_context, redirect, render_template, request, session, url_for
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

UNIVERSITY_PROFILES = {
    "melbourne": {
        "slug": "melbourne",
        "name": "University of Melbourne",
        "short_name": "Melbourne",
        "city": "Melbourne",
        "country": "Australia",
        "ranking": "Globally recognized research university",
        "hero_tagline": "Academic excellence, global reputation, and strong graduate outcomes",
        "hero_image": "https://images.unsplash.com/photo-1514432324607-2e4c9c1b7291?w=1600&h=1000&fit=crop",
        "theme": {
            "primary": "#1e3a8a",
            "secondary": "#3b82f6",
            "accent": "#38bdf8",
            "surface": "#eff6ff",
            "hero": "linear-gradient(120deg, #0b1638 0%, #1e3a8a 50%, #0f172a 100%)",
        },
    },
    "anu": {
        "slug": "anu",
        "name": "Australian National University",
        "short_name": "ANU",
        "city": "Canberra",
        "country": "Australia",
        "ranking": "#1 in Australia for graduate employability (QS 2025 indicator context)",
        "hero_tagline": "Research powered education in Australia's policy capital",
        "hero_image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1600&h=1000&fit=crop",
        "theme": {
            "primary": "#0f766e",
            "secondary": "#14b8a6",
            "accent": "#f59e0b",
            "surface": "#f0fdfa",
            "hero": "linear-gradient(120deg, #042f2e 0%, #134e4a 50%, #0f172a 100%)",
        },
    },
    "sydney": {
        "slug": "sydney",
        "name": "University of Sydney",
        "short_name": "USYD",
        "city": "Sydney",
        "country": "Australia",
        "ranking": "Top 20 globally in multiple disciplines",
        "hero_tagline": "Global prestige with world-class city career access",
        "hero_image": "https://images.unsplash.com/photo-1506973035872-a4ec16b8d6df?w=1600&h=1000&fit=crop",
        "theme": {
            "primary": "#1d4ed8",
            "secondary": "#3b82f6",
            "accent": "#f97316",
            "surface": "#eff6ff",
            "hero": "linear-gradient(120deg, #172554 0%, #1e3a8a 50%, #0f172a 100%)",
        },
    },
    "unsw": {
        "slug": "unsw",
        "name": "UNSW Sydney",
        "short_name": "UNSW",
        "city": "Sydney",
        "country": "Australia",
        "ranking": "World-leading for engineering, business and technology",
        "hero_tagline": "High-impact degrees built around innovation and industry",
        "hero_image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=1600&h=1000&fit=crop",
        "theme": {
            "primary": "#7c2d12",
            "secondary": "#ea580c",
            "accent": "#facc15",
            "surface": "#fff7ed",
            "hero": "linear-gradient(120deg, #431407 0%, #9a3412 50%, #1f2937 100%)",
        },
    },
    "monash": {
        "slug": "monash",
        "name": "Monash University",
        "short_name": "Monash",
        "city": "Melbourne",
        "country": "Australia",
        "ranking": "Top global university with strong research and employability outcomes",
        "hero_tagline": "Future-ready degrees with practical global pathways",
        "hero_image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1600&h=1000&fit=crop",
        "theme": {
            "primary": "#7e22ce",
            "secondary": "#a855f7",
            "accent": "#f59e0b",
            "surface": "#faf5ff",
            "hero": "linear-gradient(120deg, #3b0764 0%, #6b21a8 50%, #111827 100%)",
        },
    },
    "uq": {
        "slug": "uq",
        "name": "The University of Queensland",
        "short_name": "UQ",
        "city": "Brisbane",
        "country": "Australia",
        "ranking": "Top-ranked Australian university for life sciences and research impact",
        "hero_tagline": "Academic excellence in a student-friendly lifestyle city",
        "hero_image": "https://images.unsplash.com/photo-1562774053-701939374585?w=1600&h=1000&fit=crop",
        "theme": {
            "primary": "#0f766e",
            "secondary": "#0891b2",
            "accent": "#eab308",
            "surface": "#f0fdfa",
            "hero": "linear-gradient(120deg, #022c22 0%, #115e59 50%, #0f172a 100%)",
        },
    },
}

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


def build_university_content(profile):
    name = profile["name"]
    city = profile["city"]
    return {
        "hero_cards": [
            {"title": "Scholarship Window", "value": "20% to 100% fee relief"},
            {"title": "Pakistani Student Community", "value": "Active mentoring and social groups"},
            {"title": "Graduate Employability", "value": "Strong employer reputation and outcomes"},
        ],
        "stats": [
            {"label": "Programs", "value": "350+"},
            {"label": "International Students", "value": "15,000+"},
            {"label": "Graduate Employment", "value": "90%+"},
            {"label": "Research Impact", "value": "Global Top Tier"},
        ],
        "about_points": [
            f"{name} is recognized for high academic standards, innovation-driven teaching, and global alumni outcomes.",
            f"The {city} campus environment combines research infrastructure, student support systems, and vibrant city access.",
            "Students benefit from internationally connected faculties, exchange opportunities, and industry-facing projects.",
        ],
        "pakistan_why": [
            "Strong track record of Pakistani student admissions and visa success with profile-matched pathways.",
            "Scholarships and staged tuition planning reduce first-year financial pressure for families.",
            "Part-time work options and post-study work visa pathways support long-term career planning.",
            "Faith-friendly lifestyle options, halal food availability, and multicultural neighborhoods improve comfort.",
            "Career services, internships, and networking events improve graduate job outcomes in Australia and globally.",
        ],
        "admission": {
            "undergrad": [
                "Higher Secondary School Certificate with competitive percentages (generally 70%+ for strong programs).",
                "English proficiency: IELTS Academic, PTE Academic, or accepted equivalent.",
                "Program-specific prerequisites (for example, mathematics for engineering and business analytics).",
            ],
            "masters": [
                "Recognized bachelor's degree with relevant discipline background.",
                "Typical entry expectation around 2.7 to 3.2 GPA equivalent depending on faculty.",
                "CV/resume and statement of purpose for competitive coursework programs.",
            ],
            "phd": [
                "Research-aligned supervisor match and high-quality proposal.",
                "Strong master's or honors-level research background.",
                "Evidence of academic writing, publications, or research project experience.",
            ],
            "docs": [
                "Academic transcripts and degree certificates",
                "Passport and national identity documents",
                "English language test report",
                "Statement of Purpose tailored to program goals",
                "Two or three Letters of Recommendation",
                "Updated CV and portfolio/interview evidence where required",
            ],
            "english": [
                "IELTS Academic: typically 6.5 overall (no band less than 6.0)",
                "PTE Academic: typically 58 to 64 overall equivalent",
                "Duolingo English Test: accepted by selected programs with minimum thresholds",
            ],
        },
        "fees": [
            {"item": "Tuition (Business/IT)", "cost": "AUD 42,000 to 52,000"},
            {"item": "Tuition (Engineering)", "cost": "AUD 48,000 to 58,000"},
            {"item": "Tuition (Health/Law pathways)", "cost": "AUD 50,000 to 65,000"},
            {"item": "Accommodation", "cost": "AUD 11,000 to 22,000"},
            {"item": "Food and groceries", "cost": "AUD 4,500 to 7,000"},
            {"item": "Transport", "cost": "AUD 1,200 to 2,000"},
            {"item": "OSHC/Health insurance", "cost": "AUD 600 to 900"},
        ],
        "budget_cards": [
            {"label": "Estimated Annual Budget", "value": "AUD 60,000 to 85,000"},
            {"label": "Approx PKR Planning", "value": "PKR 1.1 Cr to 1.6 Cr"},
            {"label": "Safe Family Buffer", "value": "Add 10% contingency"},
        ],
        "scholarships": [
            {
                "name": "International Merit Scholarship",
                "coverage": "15% to 30% tuition reduction",
                "eligibility": "Strong academics, leadership profile, quality SOP",
                "deadline": "Main rounds for Semester 1 and Semester 2",
                "process": "Apply through university portal with complete profile documents",
                "tip": "Submit early and tailor personal statement to faculty outcomes.",
            },
            {
                "name": "Faculty Excellence Awards",
                "coverage": "Up to AUD 10,000 per year",
                "eligibility": "Program-specific merit criteria",
                "deadline": "Varies by faculty and intake",
                "process": "Auto-assessed or separate form depending on school",
                "tip": "Highlight competitions, projects, and internship impact.",
            },
            {
                "name": "Research Training Scholarships (PhD)",
                "coverage": "Tuition plus stipend (competitive)",
                "eligibility": "Strong research proposal and supervisor alignment",
                "deadline": "Multiple annual rounds",
                "process": "Supervisor engagement first, then formal scholarship submission",
                "tip": "Build a focused proposal with clear methodology and outcomes.",
            },
        ],
        "courses": [
            {"name": "Computer Science and AI", "duration": "2 to 4 years", "career": "Data, software, product, cyber"},
            {"name": "Business and Finance", "duration": "1.5 to 3 years", "career": "Consulting, banking, analytics"},
            {"name": "Engineering", "duration": "2 to 4 years", "career": "Infrastructure, energy, automation"},
            {"name": "Public Health and Biosciences", "duration": "2 to 4 years", "career": "Healthcare, research, policy"},
        ],
        "student_life": [
            "Pakistani student societies, welcome meetups, and peer mentoring networks.",
            "Halal food options near campus plus grocery clusters in multicultural suburbs.",
            "Prayer rooms and mosque access through campus and nearby community centers.",
            "Part-time job opportunities in retail, hospitality, tutoring, and support roles.",
            "Clubs, sports, festivals, and orientation events with strong international participation.",
            "Campus counseling, wellbeing services, and safety support available year-round.",
        ],
        "accommodation": [
            {"type": "On-campus residence", "range": "AUD 280 to 520/week", "fit": "Structured and social start"},
            {"type": "Shared apartment", "range": "AUD 180 to 350/week", "fit": "Budget-friendly and flexible"},
            {"type": "Studio apartment", "range": "AUD 350 to 650/week", "fit": "Privacy and independence"},
        ],
        "areas": [
            "Transport-connected student zones near campus",
            "Suburbs with halal food and multicultural communities",
            "Balanced areas for budget, safety, and commute convenience",
        ],
        "visa_steps": [
            "Receive CoE and prepare genuine temporary entrant aligned statement.",
            "Arrange financial documents showing tuition plus living cost capacity.",
            "Complete health checks, insurance, and visa application documents.",
            "Submit biometrics and attend interview only if requested.",
            "Track processing timeline and prepare pre-departure checklist.",
        ],
        "visa_tips": [
            "Maintain consistency between SOP, finances, and academic goals.",
            "Avoid unclear transaction history in sponsor accounts.",
            "Prepare concise interview responses around study and return/career plan.",
        ],
        "career": [
            "Post-study work rights available through Graduate Visa pathways subject to policy settings.",
            "Internships and industry projects improve employability before graduation.",
            "High demand sectors: technology, healthcare, finance, engineering, and analytics.",
            "Typical graduate salaries vary by field, often starting around AUD 65,000 to 95,000.",
        ],
        "timeline": [
            "Research programs and shortlist",
            "Prepare documents and tests",
            "Submit application",
            "Receive offer and accept CoE",
            "Apply visa and complete medicals",
            "Book travel and pre-arrival setup",
        ],
        "testimonials": [
            {"name": "Areeba N.", "program": "MS Data Science", "quote": f"{name} gave me strong project exposure and internship confidence before graduation."},
            {"name": "Hamza R.", "program": "Bachelor of Engineering", "quote": "The Pakistani student community helped me settle quickly and stay motivated academically."},
            {"name": "Sana K.", "program": "Master of Public Policy", "quote": "Career coaching and networking events directly helped me secure graduate interviews."},
        ],
        "faqs": [
            {"q": "Can I apply without final result?", "a": "Yes, many applicants use provisional transcripts and submit final documents later on condition."},
            {"q": "What is the safe IELTS score target?", "a": "Target 6.5 overall with no band below 6.0 unless your selected faculty requires higher scores."},
            {"q": "How early should I start?", "a": "Start at least 8 to 10 months before intake for test prep, scholarship windows, and visa confidence."},
            {"q": "Can family sponsor my education?", "a": "Yes, with clear relationship proof, consistent banking history, and complete financial documentation."},
            {"q": "Are internships available for internationals?", "a": "Yes, most faculties provide placement support, employability labs, and networking channels."},
        ],
    }

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
        return redirect(url_for("landing_page"))

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
    return redirect(url_for("landing_page"))

@app.route("/university/melbourne")
def unimelb_landing():
    """University of Melbourne premium landing page for Pakistani students"""
    profile = UNIVERSITY_PROFILES["melbourne"]
    return render_template("university_master.html", profile=profile, content=build_university_content(profile))


@app.route("/university/anu")
def anu_landing():
    """Australian National University premium landing page"""
    profile = UNIVERSITY_PROFILES["anu"]
    return render_template("university_master.html", profile=profile, content=build_university_content(profile))


@app.route("/university/sydney")
def sydney_landing():
    """University of Sydney premium landing page"""
    profile = UNIVERSITY_PROFILES["sydney"]
    return render_template("university_master.html", profile=profile, content=build_university_content(profile))


@app.route("/university/unsw")
def unsw_landing():
    """UNSW Sydney premium landing page"""
    profile = UNIVERSITY_PROFILES["unsw"]
    return render_template("university_master.html", profile=profile, content=build_university_content(profile))


@app.route("/university/monash")
def monash_landing():
    """Monash University premium landing page"""
    profile = UNIVERSITY_PROFILES["monash"]
    return render_template("university_master.html", profile=profile, content=build_university_content(profile))


@app.route("/university/uq")
def uq_landing():
    """University of Queensland premium landing page"""
    profile = UNIVERSITY_PROFILES["uq"]
    return render_template("university_master.html", profile=profile, content=build_university_content(profile))

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("landing_page"))

if __name__ == "__main__":
    app.run(debug=True)
