"""Optional browser comparison: python -m tests.browser_check (requires Playwright Chromium)."""
import hashlib
from pathlib import Path
import tempfile
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

from app import app
from tests.reference_app import load_reference


PATHS = ["/", "/booking", "/australia", "/usa", "/uk", "/canada", "/europe", "/more",
         "/ielts-preparation", "/pte-preparation", "/australia/university-of-melbourne",
         "/australia/australian-national-university", "/australia/university-of-sydney",
         "/australia/unsw-sydney", "/australia/monash-university",
         "/australia/university-of-queensland"]
ORIGIN = "http://visa-culture.test"


def main():
    app.config.update(TESTING=True, TURNSTILE_SITEKEY="", TURNSTILE_SECRET_KEY="")
    remote_cache = {}
    unavailable = set()
    reference, reference_assets = load_reference()
    clients = {True: reference.test_client(), False: app.test_client()}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(timeout=15000)
        try:
            for width, height in [(1440, 900), (390, 844)]:
                for path in PATHS:
                    results = []
                    for original in [True, False]:
                        context = browser.new_context(viewport={"width": width, "height": height},
                                                      reduced_motion="reduce")
                        def handle(route):
                            url = urlsplit(route.request.url)
                            if url.hostname == "visa-culture.test":
                                response = clients[original].get(url.path + ("?" + url.query if url.query else ""))
                                body = reference_assets.get(url.path, response.data) if original else response.data
                                route.fulfill(status=response.status_code, body=body,
                                              content_type=response.content_type)
                                response.close()
                            else:
                                key = route.request.url
                                if key not in remote_cache:
                                    try:
                                        response = context.request.get(key, timeout=10000)
                                        remote_cache[key] = (response.status, response.body(), response.headers.get("content-type", "application/octet-stream"))
                                    except Exception:
                                        unavailable.add(url.hostname)
                                        remote_cache[key] = None
                                cached = remote_cache[key]
                                if cached:
                                    route.fulfill(status=cached[0], body=cached[1], content_type=cached[2])
                                else:
                                    route.abort()
                        context.route("**/*", handle)
                        # Make pre/post capture deterministic without waiting for autoplay cycles.
                        context.add_init_script("window.setInterval = () => 0;")
                        page = context.new_page()
                        page.set_default_timeout(5000)
                        errors = []
                        page.on("pageerror", lambda error: errors.append(str(error)))
                        page.goto(ORIGIN + path, wait_until="networkidle", timeout=60000)
                        page.add_style_tag(content="*, *::before, *::after { animation: none !important; transition: none !important; caret-color: transparent !important; }")
                        page.evaluate("async () => { await document.fonts.ready; await Promise.all(Array.from(document.images).filter(img => { const r = img.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0; }).map(img => img.decode().catch(() => {}))); await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))); }")
                        screenshot = page.screenshot(animations="disabled", timeout=20000)
                        layout = page.locator("section, header, footer, .mobile-top-navbar").evaluate_all("els => els.map(el => { const r = el.getBoundingClientRect(); return [el.id, ...[r.x,r.y,r.width,r.height].map(v => Math.round(v * 10) / 10)]; })")
                        interactions = {}
                        if path == "/":
                            page.locator("#heroNextBtn").dispatch_event("click")
                            interactions["next_slide"] = page.locator(".hero-slide").evaluate_all("els => els.map(el => el.classList.contains('active'))")
                            if width < 768:
                                page.locator("#mobileNavDestinations").dispatch_event("click")
                                interactions["destinations_open"] = page.locator("#mobileNavDestinations").get_attribute("aria-expanded")
                                page.keyboard.press("Escape")
                                interactions["destinations_closed"] = page.locator("#mobileNavDestinations").get_attribute("aria-expanded")
                        if path == "/booking":
                            page.locator("#service_type").select_option("test_preparation")
                            interactions["test_label"] = page.locator("#preferred-choice-label").inner_text()
                            interactions["test_placeholder"] = page.locator("#university").get_attribute("placeholder")
                            page.locator("#service_type").select_option("consultancy")
                            interactions["study_label"] = page.locator("#preferred-choice-label").inner_text()
                        page.locator("#bookBtn").dispatch_event("click")
                        interactions["booking_widget"] = page.locator("#bookBtn").get_attribute("aria-expanded")
                        page.keyboard.press("Escape")
                        interactions["booking_widget_closed"] = page.locator("#bookBtn").get_attribute("aria-expanded")
                        results.append(dict(png=screenshot, image=hashlib.sha256(screenshot).hexdigest(), layout=layout,
                                            interactions=interactions, errors=errors))
                        context.close()
                    differences = [field for field in ["image", "layout", "interactions", "errors"] if results[0][field] != results[1][field]]
                    if differences:
                        output = Path(tempfile.mkdtemp(prefix="visa-browser-"))
                        for index, label in enumerate(["original", "modular"]):
                            (output / (label + ".png")).write_bytes(results[index]["png"])
                        print("Comparison images: " + str(output), flush=True)
                    assert not differences, f"Mismatch: {width}px {path}: {differences}"
                    print(f"PASS {width}px {path}: screenshot, layout, interactions, errors", flush=True)
        finally:
            browser.close()
    if unavailable:
        print("Unavailable external hosts (identical in both versions): " + ", ".join(sorted(unavailable)))


if __name__ == "__main__":
    main()
