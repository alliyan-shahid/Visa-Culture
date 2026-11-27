"""Booking routes."""
from flask import current_app, flash, redirect, render_template, request, url_for
from ..services.booking_email import send_booking_email
from ..services.turnstile import validate_turnstile


def _render_booking(form_data):
    """Render the common booking context without changing submitted values."""
    return render_template(
        "booking.html",
        page_summary={
            "title": "Book a consultation with Visa Culture",
            "subtitle": "Move your appointment flow into a dedicated page with a calmer, more focused experience.",
        },
        form_data=form_data,
        turnstile_sitekey=current_app.config["TURNSTILE_SITEKEY"],
    )


def booking_page():
    if request.method == "POST":
        form_data = {key: value.strip() for key, value in request.form.items()}
        if form_data.get("website"):
            flash("We could not verify this request. Please try again.", "error")
            return _render_booking(form_data)
        if not validate_turnstile(request.form.get("cf-turnstile-response", "")):
            flash("Please complete the security check and try submitting again.", "error")
            return _render_booking(form_data)
        required_fields = (
            ("name", "full name"),
            ("phone", "phone number"),
            ("address", "address"),
            ("service_type", "service type"),
        )
        missing = [label for key, label in required_fields if not form_data.get(key)]
        if missing:
            flash(f"Please fill in the required field(s): {', '.join(missing)}.", "error")
            return _render_booking(form_data)
        try:
            send_booking_email(form_data)
        except Exception:
            current_app.logger.exception("Booking email could not be sent")
            flash("We could not send your request right now. Please try again shortly.", "error")
        else:
            flash("Thank you. Your consultation request has been sent successfully.", "success")
            return redirect(url_for("booking_page"))

    return _render_booking(request.form)


def register_routes(app):
    """Register existing URLs without changing their endpoint names."""
    app.route("/booking", methods=["GET", "POST"])(booking_page)
