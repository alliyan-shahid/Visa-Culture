"""Behavior snapshots captured before modularization; no live email or CAPTCHA calls."""
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import app as entry

from tests.contracts import ROOT, FIXTURES, canonical_body, normalized_body, expand_css, css_contract


def response_snapshot(response):
    return {
        "status": response.status_code,
        "content_type": response.content_type,
        "location": response.headers.get("Location"),
        "body_sha256": hashlib.sha256(canonical_body(normalized_body(response)).encode()).hexdigest(),
    }


def capture():
    application = entry.app
    application.config.update(TESTING=True, SECRET_KEY="regression-test-key",
        SMTP_USER="sender@example.test", SMTP_PASSWORD="test-password",
        SMTP_HOST="smtp.example.test", SMTP_PORT=465,
        BOOKING_RECIPIENTS="one@example.test, two@example.test",
        TURNSTILE_SITEKEY="", TURNSTILE_SECRET_KEY="")
    from backend.services import booking_email as email_module
    from backend.routes import booking as booking_module
    from backend.services import turnstile as captcha_module
    result = {"routes": sorted([
        [rule.rule, rule.endpoint, sorted(rule.methods)]
        for rule in application.url_map.iter_rules()
    ]), "responses": {}, "emails": {}, "captcha": {}}
    for rule in application.url_map.iter_rules():
        if rule.endpoint == "static" or "GET" not in rule.methods:
            continue
        with application.test_client() as client:
            result["responses"][rule.rule] = response_snapshot(client.get(rule.rule))
    form = dict(name="  Example Applicant  ", phone="  12345  ",
                address="  Example Address  ", service_type="study_abroad",
                university="Australia", email="applicant@example.test", message="Hello")
    scenarios = {
        "honeypot": ({**form, "website": "spam"}, True, False),
        "captcha_failure": (form, False, False),
        "missing_fields": ({"name": "Example"}, True, False),
        "mail_failure": (form, True, True),
        "success": (form, True, False),
        "test_preparation": ({**form, "service_type": "test_preparation", "university": "IELTS"}, True, False),
    }
    for name, (data, verified, mail_failure) in scenarios.items():
        with application.test_client() as client, patch.object(booking_module, "validate_turnstile", return_value=verified) as captcha, patch.object(booking_module, "send_booking_email", side_effect=RuntimeError("simulated failure") if mail_failure else None) as send:
            response = client.post("/booking", data=data)
            with client.session_transaction() as session:
                flashes = session.get("_flashes", [])
            result["responses"]["POST " + name] = {
                **response_snapshot(response), "flashes": flashes,
                "captcha_calls": captcha.call_count, "email_calls": send.call_count,
                "email_data": send.call_args.args[0] if send.called else None,
            }
            if response.status_code == 302:
                result["responses"]["FOLLOW " + name] = response_snapshot(client.get(response.location))
    for name, data in {
        "study": form, "test": {**form, "service_type": "test_preparation"},
        "no_email": {**form, "email": ""}, "unsafe_email": {**form, "email": "bad\r\n@example.test"},
    }.items():
        with application.app_context(), patch.object(email_module.smtplib, "SMTP_SSL") as smtp:
            email_module.send_booking_email(data)
            connection = smtp.return_value.__enter__.return_value
            result["emails"][name] = {
                "host": smtp.call_args.args[:2], "login": connection.login.call_args.args,
                "messages": [call.args[0].as_string() for call in connection.send_message.call_args_list],
            }
    with application.app_context():
        application.config["SMTP_PASSWORD"] = ""
        try:
            email_module.send_booking_email(form)
        except RuntimeError as error:
            result["emails"]["missing_config"] = str(error)
        application.config["SMTP_PASSWORD"] = "test-password"
    with application.test_request_context("/booking", environ_base={"REMOTE_ADDR": "192.0.2.1"}):
        result["captcha"]["unconfigured"] = captcha_module.validate_turnstile("")
        application.config.update(TURNSTILE_SITEKEY="test-site", TURNSTILE_SECRET_KEY="test-secret")
        result["captcha"]["missing_token"] = captcha_module.validate_turnstile("")
        for name, payload in [("success", b'{"success": true}'), ("rejected", b'{"success": false, "error-codes": ["invalid"]}'), ("malformed", b'not json')]:
            with patch.object(captcha_module, "urlopen") as remote:
                remote.return_value.__enter__.return_value.read.return_value = payload
                result["captcha"][name] = captcha_module.validate_turnstile("test-token")
                req = remote.call_args.args[0]
                result["captcha"][name + "_request"] = [req.full_url, req.data.decode(), remote.call_args.kwargs]
        with patch.object(captcha_module, "urlopen", side_effect=OSError("offline")):
            result["captcha"]["network_failure"] = captcha_module.validate_turnstile("test-token")
        application.config.update(TURNSTILE_SITEKEY="", TURNSTILE_SECRET_KEY="")
    return json.loads(json.dumps(result))


class RegressionTests(unittest.TestCase):
    def test_existing_behavior(self):
        expected = json.loads((FIXTURES / "behavior.json").read_text(encoding="utf-8"))
        self.maxDiff = None
        # Failures identify the affected URL, booking case, email, or integration.
        with patch.object(entry.app.logger, "error"), patch.object(entry.app.logger, "warning"):
            actual = capture()
        for category, entries in expected.items():
            if isinstance(entries, dict):
                self.assertEqual(set(entries), set(actual[category]))
                for name, value in entries.items():
                    with self.subTest(category=category, case=name):
                        self.assertEqual(value, actual[category][name])
            else:
                with self.subTest(category=category):
                    self.assertEqual(entries, actual[category])

    def test_extracted_assets_are_served(self):
        with entry.app.test_client() as client:
            for path in sorted((ROOT / "static").rglob("*")):
                if path.suffix not in {".css", ".js"}:
                    continue
                filename = path.relative_to(ROOT / "static").as_posix()
                with self.subTest(asset=filename):
                    response = client.get("/static/" + filename)
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.data, path.read_bytes())
                    expected_type = "text/css" if path.suffix == ".css" else "javascript"
                    self.assertIn(expected_type, response.content_type)
                    response.close()

    def test_original_stylesheet_rules(self):
        expected = json.loads((FIXTURES / "styles.json").read_text(encoding="utf-8"))
        for filename, digest in expected.items():
            with self.subTest(stylesheet=filename):
                actual = css_contract(expand_css(ROOT / "static" / filename))
                self.assertEqual(digest, hashlib.sha256(json.dumps(actual, ensure_ascii=False).encode()).hexdigest())

    def test_script_extraction_preserves_source(self):
        expected = json.loads((FIXTURES / "scripts.json").read_text(encoding="utf-8"))
        for name, contract in expected.items():
            with self.subTest(script=name):
                source = "".join((ROOT / "static" / filename).read_text(encoding="utf-8") for filename in contract["files"])
                self.assertEqual(contract["sha256"], hashlib.sha256(source.encode()).hexdigest())


    def test_multiple_app_instances(self):
        from backend import create_app
        first, second = create_app(), create_app()
        first.config["TURNSTILE_SITEKEY"] = "first-instance"
        self.assertNotEqual(first.config["TURNSTILE_SITEKEY"], second.config["TURNSTILE_SITEKEY"])
        self.assertEqual(sorted(str(r) for r in first.url_map.iter_rules()),
                         sorted(str(r) for r in second.url_map.iter_rules()))
        for application in (first, second):
            with application.test_client() as client:
                self.assertEqual(client.get("/").status_code, 200)


if __name__ == "__main__":
    unittest.main()
