---
layout: default
title: Karte der Aktivitäten
description: Alle Aktivitäten rund um das Ferienhaus auf einer Karte - Dauer, Schwierigkeit und Saison auf einen Blick
wide: true
---

# Karte der Aktivitäten

Alle Touren und Ausflugsziele aus der [Aktivitäten-Übersicht]({{ site.baseurl }}/aktivitaeten/) auf einen Blick. Filtere nach Kategorie, Schwierigkeit oder Monat.

<div class="map-toolbar">
  <fieldset id="filter-kategorie">
    <legend>Kategorie</legend>
    {% assign kategorien = site.aktivitaeten | map: "kategorie" | uniq | sort %}
    {% for k in kategorien %}
    <label><input type="checkbox" class="filter-kat" value="{{ k }}" checked> {{ k | capitalize }}</label>
    {% endfor %}
  </fieldset>

  <fieldset id="filter-schwierigkeit">
    <legend>Schwierigkeit</legend>
    <label><input type="radio" name="schwierigkeit" value="alle" checked> Alle</label>
    <label><input type="radio" name="schwierigkeit" value="leicht"> Leicht</label>
    <label><input type="radio" name="schwierigkeit" value="mittel"> Mittel</label>
    <label><input type="radio" name="schwierigkeit" value="schwer"> Schwer</label>
  </fieldset>

  <fieldset id="filter-monat">
    <legend>Monat</legend>
    <select id="monat-select">
      <option value="0">Ganzes Jahr</option>
      <option value="1">Januar</option>
      <option value="2">Februar</option>
      <option value="3">März</option>
      <option value="4">April</option>
      <option value="5">Mai</option>
      <option value="6">Juni</option>
      <option value="7">Juli</option>
      <option value="8">August</option>
      <option value="9">September</option>
      <option value="10">Oktober</option>
      <option value="11">November</option>
      <option value="12">Dezember</option>
    </select>
  </fieldset>
</div>

<div class="karte-layout">
  <div class="karte-sidebar">
    <ul class="aktivitaeten-liste" id="aktivitaeten-liste"></ul>
  </div>
  <div class="karte-mapwrap">
    <div id="aktivitaeten-map"></div>
    <div class="map-legend" id="map-legend"></div>
    <p class="map-hinweis">Hinweis: Die eingezeichneten Wanderwege dienen der groben Übersicht (automatisch entlang des Wanderwegnetzes erzeugt) und ersetzen keine Tourenplanung. Für die Navigation im Gelände empfehlen wir <a href="https://www.schweizmobil.ch/de/wanderland" target="_blank" rel="noopener">Schweiz Mobil</a> oder swisstopo.</p>
  </div>
</div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
  window.SIGERST_BASEURL = {{ site.baseurl | jsonify }};
  window.SIGERST_AKTIVITAETEN = [
    {% for a in site.aktivitaeten %}
    {
      "title": {{ a.title | jsonify }},
      "kategorie": {{ a.kategorie | jsonify }},
      "dauer_von": {{ a.dauer.von | jsonify }},
      "dauer_bis": {{ a.dauer.bis | jsonify }},
      "schwierigkeit_wert": {{ a.schwierigkeit.wert | jsonify }},
      "schwierigkeit_einfach": {{ a.schwierigkeit.einfach | jsonify }},
      "saison_monate": {{ a.saison.monate | jsonify }},
      "saison_hinweis": {{ a.saison.hinweis | jsonify }},
      "gpx": {{ a.gpx | jsonify }},
      "start_name": {{ a.start.name | jsonify }},
      "start_koordinaten": {{ a.start.koordinaten | jsonify }},
      "distanz_km": {{ a.distanz_km | jsonify }},
      "hoehenmeter": {{ a.hoehenmeter | jsonify }},
      "familienfreundlich": {{ a.familienfreundlich | jsonify }},
      "anreise": {{ a.anreise | jsonify }},
      "seite": {{ a.seite | jsonify }}
    }{% unless forloop.last %},{% endunless %}
    {% endfor %}
  ];
</script>

{% raw %}
<script>
(function () {
  var BASEURL = window.SIGERST_BASEURL || "";
  var DATA = window.SIGERST_AKTIVITAETEN || [];
  var MONATE = ["Jan","Feb","Mär","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"];
  var FARBEN = {
    wandern: "#2d5a27",
    klettern: "#b8562f",
    baden: "#1f6f8b",
    bike: "#7a4fa0",
    winter: "#3a6ea5",
    kulinarik: "#a3752c"
  };
  function farbe(kat) { return FARBEN[kat] || "#555"; }

  function escapeHtml(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function popupHtml(a) {
    var monate = (a.saison_monate || []).map(function (m) { return MONATE[m - 1]; }).join(", ");
    var detailLink = a.seite ? '<div style="margin-top:.4rem;"><a href="' + BASEURL + a.seite + '">Details auf der Wanderseite →</a></div>' : "";
    var extra = [];
    if (a.distanz_km) extra.push(a.distanz_km + " km");
    if (a.hoehenmeter) extra.push(a.hoehenmeter + " Hm");
    return (
      '<div class="popup-aktivitaet">' +
      "<strong>" + escapeHtml(a.title) + "</strong><br>" +
      '<span class="badge">' + escapeHtml(a.schwierigkeit_wert) + "</span>" +
      '<span class="badge">' + a.dauer_von + "–" + a.dauer_bis + " h</span>" +
      (extra.length ? '<span class="badge">' + extra.join(" · ") + "</span>" : "") +
      (a.familienfreundlich ? '<span class="badge">Familienfreundlich</span>' : "") +
      '<div style="margin-top:.4rem; font-size:.85rem; color:#555;">' +
      "Saison: " + monate + "<br>" +
      "Start: " + escapeHtml(a.start_name) +
      (a.anreise ? "<br>Anreise: " + escapeHtml(a.anreise) : "") +
      "</div>" +
      detailLink +
      "</div>"
    );
  }

  async function ladeGpx(url) {
    try {
      var res = await fetch(url);
      if (!res.ok) return { trkpts: [], wpts: [] };
      var text = await res.text();
      var xml = new DOMParser().parseFromString(text, "application/xml");
      var trkpts = Array.prototype.slice.call(xml.querySelectorAll("trkpt")).map(function (el) {
        return [parseFloat(el.getAttribute("lat")), parseFloat(el.getAttribute("lon"))];
      });
      var wpts = Array.prototype.slice.call(xml.querySelectorAll("wpt")).map(function (el) {
        var nameEl = el.querySelector("name");
        return {
          lat: parseFloat(el.getAttribute("lat")),
          lon: parseFloat(el.getAttribute("lon")),
          name: nameEl ? nameEl.textContent : ""
        };
      });
      return { trkpts: trkpts, wpts: wpts };
    } catch (e) {
      console.warn("GPX konnte nicht geladen werden:", url, e);
      return { trkpts: [], wpts: [] };
    }
  }

  function zeigeFehler(msg) {
    var listeEl = document.getElementById("aktivitaeten-liste");
    if (listeEl) listeEl.innerHTML = '<li style="color:#b8562f;">' + msg + "</li>";
    var mapEl = document.getElementById("aktivitaeten-map");
    if (mapEl) mapEl.innerHTML = '<p style="padding:1rem;color:#b8562f;">' + msg + "</p>";
    console.error("[Karte]", msg);
  }

  function init() {
    if (typeof L === "undefined") {
      zeigeFehler("Kartenbibliothek (Leaflet) konnte nicht geladen werden – Internetverbindung oder Adblocker prüfen und Seite neu laden.");
      return;
    }
    if (!DATA.length) {
      zeigeFehler(
        "Keine Aktivitäten gefunden. Häufigste Ursache: die Collection „aktivitaeten“ wurde erst nach dem Start von " +
        "<code>jekyll serve</code> in _config.yml aktiviert – Server stoppen (Strg+C) und neu starten, dann Seite neu laden."
      );
      return;
    }

    var map = L.map("aktivitaeten-map", { scrollWheelZoom: false });
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>-Mitwirkende'
    }).addTo(map);

    var alleMarker = [];
    var eintraege = [];
    var listeEl = document.getElementById("aktivitaeten-liste");

    DATA.forEach(function (a) {
      var farbeKat = farbe(a.kategorie);
      var layerGroup = L.layerGroup();

      if (a.start_koordinaten && a.start_koordinaten.length === 2) {
        var marker = L.circleMarker(a.start_koordinaten, {
          radius: 8,
          color: "#fff",
          weight: 2,
          fillColor: farbeKat,
          fillOpacity: 0.9
        }).bindPopup(popupHtml(a));
        layerGroup.addLayer(marker);
        alleMarker.push(marker);
      }

      layerGroup.addTo(map);

      var li = document.createElement("li");
      li.innerHTML =
        '<span class="titel">' + escapeHtml(a.title) + "</span>" +
        '<span class="meta">' +
        '<span class="badge">' + escapeHtml(a.schwierigkeit_wert) + "</span>" +
        '<span class="badge">' + a.dauer_von + "–" + a.dauer_bis + " h</span>" +
        "</span>";
      li.addEventListener("click", function () {
        if (a.start_koordinaten) {
          map.setView(a.start_koordinaten, 14, { animate: true });
        }
        layerGroup.eachLayer(function (l) {
          if (l.openPopup) l.openPopup();
        });
      });
      listeEl.appendChild(li);

      var eintrag = { data: a, layerGroup: layerGroup, li: li };
      eintraege.push(eintrag);

      if (a.gpx) {
        ladeGpx(BASEURL + a.gpx).then(function (gpx) {
          if (gpx.trkpts.length > 1) {
            var linie = L.polyline(gpx.trkpts, {
              color: farbeKat,
              weight: 4,
              opacity: 0.75
            }).bindPopup(popupHtml(a));
            layerGroup.addLayer(linie);
          }
          gpx.wpts.forEach(function (w) {
            if (w.name && w.name.indexOf(a.start_name.split(",")[0].split("(")[0].trim()) === 0) return;
            var wm = L.circleMarker([w.lat, w.lon], {
              radius: 4,
              color: farbeKat,
              weight: 1,
              fillColor: "#fff",
              fillOpacity: 1
            }).bindTooltip(w.name || "");
            layerGroup.addLayer(wm);
          });
        });
      }
    });

    if (alleMarker.length) {
      map.fitBounds(L.featureGroup(alleMarker).getBounds(), { padding: [40, 40] });
    } else {
      map.setView([47.205, 9.35], 12);
    }

    // Legende
    var kategorienImEinsatz = Array.from(new Set(DATA.map(function (a) { return a.kategorie; }))).sort();
    var legendEl = document.getElementById("map-legend");
    legendEl.innerHTML = kategorienImEinsatz
      .map(function (k) {
        return '<span><span class="dot" style="background:' + farbe(k) + ';"></span>' + k.charAt(0).toUpperCase() + k.slice(1) + "</span>";
      })
      .join("");

    // Filter
    var katCheckboxen = Array.prototype.slice.call(document.querySelectorAll(".filter-kat"));
    var schwierigkeitRadios = Array.prototype.slice.call(document.querySelectorAll('input[name="schwierigkeit"]'));
    var monatSelect = document.getElementById("monat-select");

    function anwendenFilter() {
      var aktiveKategorien = katCheckboxen.filter(function (c) { return c.checked; }).map(function (c) { return c.value; });
      var schwierigkeit = schwierigkeitRadios.filter(function (r) { return r.checked; })[0].value;
      var monat = parseInt(monatSelect.value, 10);

      eintraege.forEach(function (e) {
        var a = e.data;
        var sichtbar =
          aktiveKategorien.indexOf(a.kategorie) !== -1 &&
          (schwierigkeit === "alle" || a.schwierigkeit_einfach === schwierigkeit) &&
          (monat === 0 || (a.saison_monate || []).indexOf(monat) !== -1);

        if (sichtbar) {
          if (!map.hasLayer(e.layerGroup)) e.layerGroup.addTo(map);
          e.li.classList.remove("is-hidden");
        } else {
          if (map.hasLayer(e.layerGroup)) map.removeLayer(e.layerGroup);
          e.li.classList.add("is-hidden");
        }
      });
    }

    katCheckboxen.forEach(function (c) { c.addEventListener("change", anwendenFilter); });
    schwierigkeitRadios.forEach(function (r) { r.addEventListener("change", anwendenFilter); });
    monatSelect.addEventListener("change", anwendenFilter);
  }

  try {
    if (typeof L === "undefined") {
      window.addEventListener("load", function () { setTimeout(init, 300); });
    } else {
      init();
    }
  } catch (err) {
    zeigeFehler("Beim Laden der Karte ist ein Fehler aufgetreten (Details in der Browser-Konsole, F12).");
    console.error(err);
  }
})();
</script>
{% endraw %}

<p><a href="{{ site.baseurl }}/aktivitaeten/">← Zurück zur Aktivitäten-Übersicht</a></p>
