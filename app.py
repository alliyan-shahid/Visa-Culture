import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, make_response, redirect, render_template, request, url_for

load_dotenv(override=False)


class Config:
    SECRET_KEY = "***Removed***"


app = Flask(__name__)
app.config.from_object(Config)

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
