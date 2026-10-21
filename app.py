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
        "universities.html",
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
    app.run(debug=False)
