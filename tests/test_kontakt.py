"""Tests for dual-mode Kontakt page (public Berg & Bett vs. guest form)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KONTAKT = ROOT / "kontakt.html"
CONFIG = ROOT / "_config.yml"
GUEST_JS = ROOT / "assets" / "js" / "guest-access.js"
BERG_URL = "https://booking.bergundbett.ch/vermietung/ferienhaus-wildhaus-sigerst-441356.html"


def test_berg_und_bett_booking_url_in_config():
    text = CONFIG.read_text(encoding="utf-8")
    assert BERG_URL in text


def test_kontakt_public_berg_und_bett():
    html = KONTAKT.read_text(encoding="utf-8")
    assert "berg_und_bett_booking_url" in html
    assert "public-only" in html
    assert "Berg &amp; Bett" in html or "Berg & Bett" in html


def test_kontakt_guest_form():
    html = KONTAKT.read_text(encoding="utf-8")
    assert "guest-only" in html
    assert "https://formspree.io/f/xdajoobd" in html
    assert 'class="contact-form"' in html


def test_guest_access_script():
    js = GUEST_JS.read_text(encoding="utf-8")
    assert "guest-mode" in js
    assert "sessionStorage" in js
    assert "SIGERST_GUEST" in js


def test_kontakt_guest_link_config():
    text = CONFIG.read_text(encoding="utf-8")
    assert "guest_link_param: gast" in text
    assert "guest_link_token:" in text
