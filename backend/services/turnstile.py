"""Turnstile integration."""
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import current_app, request


def turnstile_is_configured():
    return bool(current_app.config["TURNSTILE_SITEKEY"] and current_app.config["TURNSTILE_SECRET_KEY"])


def validate_turnstile(token):
    """Validate a Turnstile token without adding another runtime dependency."""
    if not turnstile_is_configured():
        current_app.logger.warning("Turnstile keys are not configured; CAPTCHA validation is skipped")
        return True
    if not token:
        return False

    payload = urlencode({
        "secret": current_app.config["TURNSTILE_SECRET_KEY"],
        "response": token,
        "remoteip": request.remote_addr or "",
    }).encode("utf-8")
    try:
        verification_request = Request(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urlopen(verification_request, timeout=5) as response:
            result = json.loads(response.read().decode("utf-8"))
        if not result.get("success"):
            current_app.logger.warning("Turnstile rejected token: %s", result.get("error-codes", []))
        return bool(result.get("success"))
    except Exception:
        current_app.logger.exception("Turnstile verification request failed")
        return False
