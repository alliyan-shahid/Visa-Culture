"""Pages routes."""
from flask import render_template


def landing_page():
    return render_template("index.html")


def ielts_preparation():
    return render_template("ielts_preparation.html")


def pte_preparation():
    return render_template("pte_preparation.html")


def register_routes(app):
    """Register existing URLs without changing their endpoint names."""
    app.route("/")(landing_page)
    app.route("/ielts-preparation")(ielts_preparation)
    app.route("/pte-preparation")(pte_preparation)
