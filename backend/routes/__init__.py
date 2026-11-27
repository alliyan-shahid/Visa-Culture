"""Register cohesive route groups while retaining public endpoint names."""
from . import booking, destinations, pages, redirects, seo, universities


def register_routes(app):
    for group in (pages, redirects, universities, destinations, booking, seo):
        group.register_routes(app)
