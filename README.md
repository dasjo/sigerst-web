# Ferienhaus Sigerst – Website

Static site (Jekyll) for GitHub Pages.

## Local preview

```bash
bundle install
bundle exec jekyll serve --baseurl ""
```

Open http://127.0.0.1:4000/

## Deploy

GitHub → **Settings → Pages** → Branch `main`, folder `/` (root).

See [CONTENT_STATUS.md](./CONTENT_STATUS.md) for page-by-page review progress.

## Kontakt: öffentlich vs. Gäste

| Zielgruppe | URL | Inhalt |
|------------|-----|--------|
| Öffentlich | `/kontakt/` | Buchung & Anfrage → [Berg & Bett](https://booking.bergundbett.ch/vermietung/ferienhaus-wildhaus-sigerst-441356.html) |
| Gäste | `/kontakt/?gast=sigerst-guest` | Eigenes Formular (Formspree-ID in `kontakt.html` eintragen) |

Gäste-Token in `_config.yml` (`guest_link_token`). Nach erstem Besuch mit Gäste-Link bleibt der Modus in der Browser-Session aktiv.

Tests: `python3 -m pytest tests/ -q`
