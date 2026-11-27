"""Redirects routes."""
from flask import redirect


def ielts_preparation_legacy():
    return redirect("https://visaculture.com/ielts-preparation", code=301)


def pte_preparation_legacy():
    return redirect("https://visaculture.com/pte-preparation", code=301)


def legacy_university_of_melbourne():
    return redirect("https://visaculture.com/australia/university-of-melbourne", code=301)


def legacy_australian_national_university():
    return redirect("https://visaculture.com/australia/australian-national-university", code=301)


def legacy_university_of_sydney():
    return redirect("https://visaculture.com/australia/university-of-sydney", code=301)


def legacy_unsw_sydney():
    return redirect("https://visaculture.com/australia/unsw-sydney", code=301)


def legacy_monash_university():
    return redirect("https://visaculture.com/australia/monash-university", code=301)


def legacy_university_of_queensland():
    return redirect("https://visaculture.com/australia/university-of-queensland", code=301)


def register_routes(app):
    """Register existing URLs without changing their endpoint names."""
    app.route("/ielts-preparation-sheikhupura")(ielts_preparation_legacy)
    app.route("/pte-preparation-sheikhupura")(pte_preparation_legacy)
    app.route("/universities/university-of-melbourne")(legacy_university_of_melbourne)
    app.route("/universities/australian-national-university")(legacy_australian_national_university)
    app.route("/universities/university-of-sydney")(legacy_university_of_sydney)
    app.route("/universities/unsw-sydney")(legacy_unsw_sydney)
    app.route("/universities/monash-university")(legacy_monash_university)
    app.route("/universities/university-of-queensland")(legacy_university_of_queensland)
