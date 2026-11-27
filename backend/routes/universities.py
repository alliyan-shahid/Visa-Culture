"""Universities routes."""
from flask import render_template


def university_of_melbourne():
    return render_template("melbourne_landing.html")


def australian_national_university():
    return render_template("anu_landing.html")


def university_of_sydney():
    return render_template("sydney_landing.html")


def unsw_sydney():
    return render_template("unsw_landing.html")


def monash_university():
    return render_template("monash_landing.html")


def university_of_queensland():
    return render_template("uq_landing.html")


def register_routes(app):
    """Register existing URLs without changing their endpoint names."""
    app.route("/australia/university-of-melbourne")(university_of_melbourne)
    app.route("/australia/australian-national-university")(australian_national_university)
    app.route("/australia/university-of-sydney")(university_of_sydney)
    app.route("/australia/unsw-sydney")(unsw_sydney)
    app.route("/australia/monash-university")(monash_university)
    app.route("/australia/university-of-queensland")(university_of_queensland)
