"""Check search information in the finished pages."""
import json
import unittest
from urllib.parse import urlsplit
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from app import app


class SEOTests(unittest.TestCase):
    def test_indexable_pages_and_structured_data(self):
        titles = set()
        with app.test_client() as client:
            sitemap = ElementTree.fromstring(client.get("/sitemap.xml").data)
            for loc in sitemap.findall("s:url/s:loc", {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}):
                with self.subTest(url=loc.text):
                    response = client.get(urlsplit(loc.text).path)
                    self.assertEqual(response.status_code, 200)
                    page = BeautifulSoup(response.data, "html.parser")
                    title = page.title.get_text().strip()
                    self.assertTrue(title)
                    self.assertNotIn(title, titles)
                    titles.add(title)
                    self.assertTrue(page.select_one('meta[name="description"]')["content"].strip())
                    self.assertEqual(page.select_one('link[rel="canonical"]')["href"], loc.text)
                    self.assertNotIn("noindex", response.headers.get("X-Robots-Tag", "").lower())
                    for script in page.select('script[type="application/ld+json"]'):
                        json.loads(script.string or script.get_text())

    def test_local_business_consistency_and_links(self):
        with app.test_client() as client:
            page = BeautifulSoup(client.get("/").data, "html.parser")
            graph = json.loads(page.select_one('script[type="application/ld+json"]').string)["@graph"]
            business = next(node for node in graph if node["@type"] == "LocalBusiness")
            self.assertEqual(business["address"]["addressLocality"], "Sheikhupura")
            self.assertEqual(business["address"]["addressRegion"], "Punjab")
            footer = page.select_one("footer")
            self.assertIn(business["telephone"], footer.get_text())
            self.assertIn(business["address"]["streetAddress"], footer.get_text())
            self.assertIsNone(page.select_one("#sheikhupura-consultation"))
            for link in footer.select('a[href^="/"]'):
                self.assertEqual(client.get(link["href"]).status_code, 200)
            self.assertIn("Sitemap: https://visaculture.com/sitemap.xml", client.get("/robots.txt").get_data(as_text=True))
