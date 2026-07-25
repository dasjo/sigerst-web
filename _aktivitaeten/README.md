# Aktivitäten-Datenbank

Eine Datei pro Aktivität. Das Front Matter ist die Datenstruktur, der Body eine kurze Beschreibung.

## Schema

| Feld | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `title` | String | ✅ | Anzeigename |
| `kategorie` | Enum | ✅ | `wandern`, `klettern`, `bike`, `laufen`, `winter`, `baden`, `kulinarik` |
| `dauer.von` / `dauer.bis` | Zahl (h) | ✅ | Reine Aktivitätsdauer |
| `dauer.zustieg` | Zahl (h) | – | Falls relevant |
| `schwierigkeit.skala` | Enum | ✅ | `SAC-T`, `franzoesisch`, `S`, `keine` |
| `schwierigkeit.wert` | String | ✅ | z. B. `T3`, `3a–6b` |
| `schwierigkeit.einfach` | Enum | ✅ | `leicht`, `mittel`, `schwer` (für Filter) |
| `saison.monate` | Liste 1–12 | ✅ | Maschinenlesbar für Filter |
| `saison.hinweis` | String | – | Freitext |
| `gpx` | Pfad | – | GPX in `/assets/gpx/`, `null` falls noch keiner vorliegt |
| `gpx_quelle` | String | – | Herkunft/Qualität des Tracks (z. B. «BRouter, grob – prüfen») |
| `start.name` | String | ✅ | Ausgangspunkt |
| `start.koordinaten` | [lat, lon] | – | Fallback-Marker ohne GPX |
| `distanz_km`, `hoehenmeter` | Zahl | – | |
| `familienfreundlich` | Bool | – | |
| `anreise` | String | – | Vom Ferienhaus |
| `seite` | Pfad | – | Detailseite/-anker auf der Website |
| `links` | Liste | – | `titel` + `url` |

Alle Start-Koordinaten sind über die swisstopo-API (api3.geo.admin.ch) verifiziert.

⚠️ Die GPX-Tracks sind automatisch entlang des OSM-Wanderwegnetzes generiert (BRouter, Profil `hiking-mountain`) und **grob aufgelöst** – für die Kartenübersicht geeignet, nicht zur Navigation im Gelände. Bessere Tracks (z. B. Schweiz-Mobil-/Outdooractive-Export) können die Dateien in `docs/assets/gpx/` einfach ersetzen.

⚠️ **Komoot-Links:** Einige Einträge verlinken auf private Komoot-Touren („Sichtbarkeit: Nur für dich"). Diese Links funktionieren für Website-Besucher nicht, bis die Sichtbarkeit in Komoot auf „Öffentlich" oder „Follower" gestellt wird.
