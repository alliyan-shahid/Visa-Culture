"""Destinations routes."""
from flask import render_template
from ..data.destinations import (
    get_usa_universities,
    get_uk_universities,
    get_canada_universities,
    get_europe_countries,
    get_more_countries
)
from ..data.australia import get_australia_content


def usa_destination():
    universities = get_usa_universities()
    return render_template("usa.html", universities=universities)


def uk_destination():
    universities = get_uk_universities()
    return render_template("uk.html", universities=universities)


def canada_destination():
    universities = get_canada_universities()
    return render_template("canada.html", universities=universities)


def europe_destination():
    countries = get_europe_countries()
    return render_template("europe.html", countries=countries)


def more_destinations():
    countries = get_more_countries()
    return render_template("more.html", countries=countries)


def australia_destination():
    content = get_australia_content()
    university_cards = content["university_cards"]
    hero_stats = content["hero_stats"]
    journey_steps = content["journey_steps"]
    spotlight = content["spotlight"]
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


def register_routes(app):
    """Register existing URLs without changing their endpoint names."""
    app.route("/usa")(usa_destination)
    app.route("/uk")(uk_destination)
    app.route("/canada")(canada_destination)
    app.route("/europe")(europe_destination)
    app.route("/more")(more_destinations)
    app.route("/australia")(australia_destination)
