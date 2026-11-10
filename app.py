#
import os
import smtplib
import ssl
import json
from datetime import datetime
from email.message import EmailMessage
from email.utils import parseaddr
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from dotenv import load_dotenv
from flask import Flask, flash, make_response, redirect, render_template, request, url_for

load_dotenv(override=False)


class Config:
    SECRET_KEY = "***Removed***"
    SMTP_HOST = "***Removed***"
    SMTP_PORT = "***Removed***"
    SMTP_USER = "***Removed***"
    SMTP_PASSWORD = "***Removed***"
    BOOKING_RECIPIENTS = "***Removed***"
    TURNSTILE_SITEKEY = "***Removed***"
    TURNSTILE_SECRET_KEY = "***Removed***"


def turnstile_is_configured():
    return bool(app.config["TURNSTILE_SITEKEY"] and app.config["TURNSTILE_SECRET_KEY"])


def validate_turnstile(token):
    """Validate a Turnstile token without adding another runtime dependency."""
    if not turnstile_is_configured():
        app.logger.warning("Turnstile keys are not configured; CAPTCHA validation is skipped")
        return True
    if not token:
        return False

    payload = urlencode({
        "secret": app.config["TURNSTILE_SECRET_KEY"],
        "response": token,
        "remoteip": request.remote_addr or "",
    }).encode("utf-8")
    try:
        verification_request = Request(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urlopen(verification_request, timeout=5) as response:
            result = json.loads(response.read().decode("utf-8"))
        if not result.get("success"):
            app.logger.warning("Turnstile rejected token: %s", result.get("error-codes", []))
        return bool(result.get("success"))
    except Exception:
        app.logger.exception("Turnstile verification request failed")
        return False


app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def landing_page():
    return render_template("index.html")

@app.route("/australia/university-of-melbourne")
def university_of_melbourne():
    return render_template("melbourne_landing.html")

@app.route("/usa")
def usa_destination():
    universities = [
        {
            "id": "mit",
            "name": "Massachusetts Institute of Technology (MIT)",
            "category": "Private research university",
            "region": "Cambridge, Massachusetts",
            "summary": "Explore engineering, computing and the sciences, with hands-on research through MIT's Undergraduate Research Opportunities Program.",
            "url": "https://www.mit.edu/",
        },
        {
            "id": "stanford",
            "name": "Stanford University",
            "category": "Private research university",
            "region": "Stanford, California",
            "summary": "Explore engineering, computer science, humanities and interdisciplinary study in Silicon Valley.",
            "url": "https://www.stanford.edu/",
        },
        {
            "id": "harvard",
            "name": "Harvard University",
            "category": "Private research university",
            "region": "Cambridge, Massachusetts",
            "summary": "Harvard College offers a liberal arts and sciences education with concentrations across the humanities, social sciences and natural sciences.",
            "url": "https://www.harvard.edu/",
        },
        {
            "id": "caltech",
            "name": "California Institute of Technology (Caltech)",
            "category": "Private research university",
            "region": "Pasadena, California",
            "summary": "A small institution focused on science and engineering, with undergraduate research opportunities in areas such as physics and aerospace.",
            "url": "https://www.caltech.edu/",
        },
        {
            "id": "princeton",
            "name": "Princeton University",
            "category": "Private research university",
            "region": "Princeton, New Jersey",
            "summary": "Explore liberal arts and engineering programs that emphasize independent work, including junior projects and senior theses.",
            "url": "https://www.princeton.edu/",
        },
        {
            "id": "berkeley",
            "name": "University of California, Berkeley",
            "category": "Public research university",
            "region": "Berkeley, California",
            "summary": "A University of California campus offering programs across engineering, computing, business, the sciences and the liberal arts.",
            "url": "https://www.berkeley.edu/",
        },
    ]
    return render_template("usa.html", universities=universities)

@app.route("/uk")
def uk_destination():
    universities = [
        {
            "id": "oxford",
            "name": "University of Oxford",
            "category": "Collegiate university",
            "region": "Oxford, England",
            "summary": "Explore humanities, sciences and social sciences in a collegiate system where undergraduate tutorials are central to teaching.",
            "url": "https://www.ox.ac.uk/",
        },
        {
            "id": "cambridge",
            "name": "University of Cambridge",
            "category": "Collegiate university",
            "region": "Cambridge, England",
            "summary": "Choose from arts, sciences and engineering, with small-group undergraduate teaching known as supervisions.",
            "url": "https://www.cam.ac.uk/",
        },
        {
            "id": "imperial",
            "name": "Imperial College London",
            "category": "Specialist research university",
            "region": "London, England",
            "summary": "Study science, engineering, medicine or business at a university with a strong focus on applied research.",
            "url": "https://www.imperial.ac.uk/",
        },
        {
            "id": "ucl",
            "name": "University College London (UCL)",
            "category": "Research university",
            "region": "London, England",
            "summary": "Explore architecture, education, health sciences, engineering and the humanities at a university based in central London.",
            "url": "https://www.ucl.ac.uk/",
        },
        {
            "id": "edinburgh",
            "name": "University of Edinburgh",
            "category": "Research university",
            "region": "Edinburgh, Scotland",
            "summary": "Explore subjects from informatics and medicine to literature and social sciences in Scotland’s capital.",
            "url": "https://www.ed.ac.uk/",
        },
        {
            "id": "manchester",
            "name": "University of Manchester",
            "category": "Research university",
            "region": "Manchester, England",
            "summary": "Choose from engineering, science, business and humanities programmes at a large university in northern England.",
            "url": "https://www.manchester.ac.uk/",
        },
    ]
    return render_template("uk.html", universities=universities)

@app.route("/canada")
def canada_destination():
    universities = [
        {
            "id": "toronto",
            "name": "University of Toronto",
            "category": "Research university",
            "region": "Greater Toronto Area, Ontario",
            "summary": "Explore programs in computing, engineering, health sciences, humanities and social sciences across three campuses.",
            "url": "https://www.utoronto.ca/",
        },
        {
            "id": "ubc",
            "name": "University of British Columbia (UBC)",
            "category": "Research university",
            "region": "Vancouver and Kelowna, British Columbia",
            "summary": "Compare programs in science, forestry, engineering and business at the Vancouver and Okanagan campuses.",
            "url": "https://www.ubc.ca/",
        },
        {
            "id": "mcgill",
            "name": "McGill University",
            "category": "Research university",
            "region": "Montréal, Québec",
            "summary": "Explore programs in life sciences, engineering, management and the arts in an English-language university in Montréal.",
            "url": "https://www.mcgill.ca/",
        },
        {
            "id": "waterloo",
            "name": "University of Waterloo",
            "category": "Research university",
            "region": "Waterloo, Ontario",
            "summary": "Explore mathematics, computer science and engineering, with co-op options in many undergraduate programs.",
            "url": "https://uwaterloo.ca/",
        },
        {
            "id": "alberta",
            "name": "University of Alberta",
            "category": "Research university",
            "region": "Edmonton, Alberta",
            "summary": "Compare programs in engineering, computing, agriculture, health sciences and the humanities.",
            "url": "https://www.ualberta.ca/",
        },
        {
            "id": "mcmaster",
            "name": "McMaster University",
            "category": "Research university",
            "region": "Hamilton, Ontario",
            "summary": "Explore health sciences, engineering, business and the humanities, including programs with inquiry-based learning.",
            "url": "https://www.mcmaster.ca/",
        },
    ]
    return render_template("canada.html", universities=universities)

@app.route("/australia/australian-national-university")
def australian_national_university():
    return render_template("anu_landing.html")

@app.route("/australia/university-of-sydney")
def university_of_sydney():
    return render_template("sydney_landing.html")

@app.route("/australia/unsw-sydney")
def unsw_sydney():
    return render_template("unsw_landing.html")

@app.route("/australia/monash-university")
def monash_university():
    return render_template("monash_landing.html")

@app.route("/australia/university-of-queensland")
def university_of_queensland():
    return render_template("uq_landing.html")

@app.route("/australia")
def australia_destination():
    university_cards = [
        {
            "name": "University of Melbourne",
            "ranking": "Australia #2 · QS #=22 worldwide (2027)",
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
            "ranking": "Australia #4 · QS #29 worldwide (2027)",
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
            "ranking": "Australia #3 · QS #28 worldwide (2027)",
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
            "ranking": "Australia #1 · QS #19 worldwide (2027)",
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
            "ranking": "Australia #5 · QS #31 worldwide (2027)",
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
            "ranking": "Australia #6 · QS #=40 worldwide (2027)",
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
        {"value": "6", "label": "leading university guides"},
        {"value": "8", "label": "major study cities"},
        {"value": "1", "label": "globally respected destination"},
        {"value": "24/7", "label": "student support direction"},
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
        "australia.html",
        hero_stats=hero_stats,
        universities=university_cards,
        journey_steps=journey_steps,
        spotlight=spotlight,
        page_summary={
            "title": "Study in Australia with a clearer plan",
            "subtitle": "Explore education, lifestyle, work possibilities, cities, and leading universities through one practical destination guide.",
        },
    )

def _valid_reply_to(value):
    """Return a safe reply-to address or an empty string."""
    if not value or "\r" in value or "\n" in value:
        return ""
    _, address = parseaddr(value)
    return address if "@" in address else ""


def send_booking_email(form_data):
    sender = app.config["SMTP_USER"]
    password = app.config["SMTP_PASSWORD"]
    recipients = [
        address.strip()
        for address in app.config["BOOKING_RECIPIENTS"].split(",")
        if address.strip()
    ]
    if not sender or not password or not recipients:
        raise RuntimeError("Booking email settings are not configured")

    fields = [
        ("Full name", form_data.get("name") or "Not provided"),
        ("Phone number", form_data.get("phone") or "Not provided"),
        ("Email address", form_data.get("email") or "Not provided"),
        ("Service type", form_data.get("service_type") or "Not provided"),
        ("Preferred date", form_data.get("date") or "Not provided"),
        (
            "Preferred test" if form_data.get("service_type") == "test_preparation" else "Preferred destination",
            form_data.get("university") or "Not provided",
        ),
        ("Address", form_data.get("address") or "Not provided"),
        ("Message", form_data.get("message") or "Not provided"),
    ]
    details = "\n".join(f"{label}: {value}" for label, value in fields)

    applicant_email = _valid_reply_to(form_data.get("email", "").strip())

    message = EmailMessage()
    message["Subject"] = f"New Consultation Booking Request | {form_data.get('name') or 'Website Visitor'} | Visa Culture"
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    if applicant_email:
        message["Reply-To"] = applicant_email
    message.set_content(
        "A new consultation request was submitted through the Visa Culture booking form.\n\n"
        "BOOKING DETAILS\n"
        "================\n"
        f"{details}\n\n"
        "Please follow up with the applicant using the details above."
    )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(app.config["SMTP_HOST"], app.config["SMTP_PORT"], context=context) as smtp:
        smtp.login(sender, password)
        smtp.send_message(message)
        if applicant_email:
            confirmation = EmailMessage()
            confirmation["Subject"] = "Booking Received — Visa Culture Will Contact You Soon"
            confirmation["From"] = sender
            confirmation["To"] = applicant_email
            confirmation.set_content(
                f"Dear {form_data.get('name') or 'Applicant'},\n\n"
                "Thank you for contacting Visa Culture. We have received your booking request successfully.\n\n"
                "Our team will review your details and contact you shortly regarding the next steps.\n\n"
                "Regards,\n"
                "Visa Culture Team\n"
                "info@visaculture.com"
            )
            smtp.send_message(confirmation)


@app.route("/booking", methods=["GET", "POST"])
def booking_page():
    if request.method == "POST":
        form_data = {key: value.strip() for key, value in request.form.items()}
        if form_data.get("website"):
            flash("We could not verify this request. Please try again.", "error")
            return render_template("booking.html", page_summary={
                "title": "Book a consultation with Visa Culture",
                "subtitle": "Move your appointment flow into a dedicated page with a calmer, more focused experience.",
            }, form_data=form_data, turnstile_sitekey=app.config["TURNSTILE_SITEKEY"])
        if not validate_turnstile(request.form.get("cf-turnstile-response", "")):
            flash("Please complete the security check and try submitting again.", "error")
            return render_template("booking.html", page_summary={
                "title": "Book a consultation with Visa Culture",
                "subtitle": "Move your appointment flow into a dedicated page with a calmer, more focused experience.",
            }, form_data=form_data, turnstile_sitekey=app.config["TURNSTILE_SITEKEY"])
        missing = [label for key, label in (("name", "full name"), ("phone", "phone number"), ("address", "address"), ("service_type", "service type")) if not form_data.get(key)]
        if missing:
            flash(f"Please fill in the required field(s): {', '.join(missing)}.", "error")
            return render_template(
                "booking.html",
                page_summary={
                    "title": "Book a consultation with Visa Culture",
                    "subtitle": "Move your appointment flow into a dedicated page with a calmer, more focused experience.",
                },
                form_data=form_data,
                turnstile_sitekey=app.config["TURNSTILE_SITEKEY"],
            )
        try:
            send_booking_email(form_data)
        except Exception:
            app.logger.exception("Booking email could not be sent")
            flash("We could not send your request right now. Please try again shortly.", "error")
        else:
            flash("Thank you. Your consultation request has been sent successfully.", "success")
            return redirect(url_for("booking_page"))

    return render_template(
        "booking.html",
        page_summary={
            "title": "Book a consultation with Visa Culture",
            "subtitle": "Move your appointment flow into a dedicated page with a calmer, more focused experience.",
        },
        form_data=request.form,
        turnstile_sitekey=app.config["TURNSTILE_SITEKEY"],
    )

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/robots.txt")
def robots_txt():
    content = """User-agent: *
Disallow: /login

Sitemap: {}/sitemap.xml
""".format(request.url_root.rstrip("/"))
    response = make_response(content)
    response.headers["Content-Type"] = "text/plain"
    return response

@app.route("/sitemap.xml")
def sitemap_xml():
    pages = [
        {"path": "", "priority": 1.0},
        {"path": "universities", "priority": 0.9},
        {"path": "usa", "priority": 0.9},
        {"path": "uk", "priority": 0.9},
        {"path": "canada", "priority": 0.9},
        {"path": "booking", "priority": 0.7},
    ]
    university_pages = [
        {"path": "australia/university-of-melbourne", "priority": 0.9},
        {"path": "australia/australian-national-university", "priority": 0.9},
        {"path": "australia/university-of-sydney", "priority": 0.9},
        {"path": "australia/unsw-sydney", "priority": 0.9},
        {"path": "australia/monash-university", "priority": 0.9},
        {"path": "australia/university-of-queensland", "priority": 0.9},
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
    app.run(debug=False)
