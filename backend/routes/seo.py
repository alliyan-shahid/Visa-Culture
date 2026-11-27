"""Sitemap and robots responses."""
from flask import make_response

from ..data.sitemap import get_sitemap_pages


def robots_txt():
    content = """User-agent: *
Disallow:

Sitemap: {}/sitemap.xml
""".format("https://visaculture.com")
    response = make_response(content)
    response.headers["Content-Type"] = "text/plain"
    return response


def sitemap_xml():
    url_root = "https://visaculture.com"
    urls = get_sitemap_pages()

    xml_items = [
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">",
    ]
    for entry in urls:
        xml_items.append("  <url>")
        xml_items.append(f"    <loc>{url_root}/{entry['path']}</loc>")
        xml_items.append("    <changefreq>weekly</changefreq>")
        xml_items.append(f"    <priority>{entry['priority']:.1f}</priority>")
        xml_items.append("  </url>")
    xml_items.append("</urlset>")

    response = make_response("\n".join(xml_items))
    response.headers["Content-Type"] = "application/xml"
    return response


def register_routes(app):
    """Register existing URLs without changing their endpoint names."""
    app.route("/robots.txt")(robots_txt)
    app.route("/sitemap.xml")(sitemap_xml)
