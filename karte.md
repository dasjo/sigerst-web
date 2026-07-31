---
layout: default
title: Karte der Aktivitäten
description: Alle Aktivitäten rund um das Ferienhaus auf einer Karte - Dauer, Schwierigkeit und Saison auf einen Blick
wide: true
body_class: karte-fullscreen
---

<div class="karte-app" id="karte-app">
  <aside class="karte-sidebar" id="karte-sidebar">
    <div class="karte-sidebar-scroll">
      <ul class="aktivitaeten-liste" id="aktivitaeten-liste"></ul>
    </div>
    <div class="karte-sidebar-footer">
      <div class="map-legend" id="map-legend"></div>
      <p><a href="{{ site.baseurl }}/aktivitaeten/">← Zurück zur Aktivitäten-Übersicht</a></p>
    </div>
  </aside>

  <div class="filter-pills" id="filter-pills">
    <div class="pill" data-filter="kategorie">
      <button type="button" class="pill-btn">Kategorie <span class="pill-count" id="pill-count-kategorie"></span></button>
      <div class="pill-dropdown">
        <fieldset id="filter-kategorie">
          <legend>Kategorie</legend>
          {% assign kategorien = site.aktivitaeten | map: "kategorie" | uniq | sort %}
          {% for k in kategorien %}
          <label><input type="checkbox" class="filter-kat" value="{{ k }}" checked> {{ k | capitalize }}</label>
          {% endfor %}
        </fieldset>
      </div>
    </div>

    <div class="pill" data-filter="schwierigkeit">
      <button type="button" class="pill-btn">Schwierigkeit <span class="pill-count" id="pill-count-schwierigkeit"></span></button>
      <div class="pill-dropdown">
        <fieldset id="filter-schwierigkeit">
          <legend>Schwierigkeit</legend>
          <label><input type="radio" name="schwierigkeit" value="alle" checked> Alle</label>
          <label><input type="radio" name="schwierigkeit" value="leicht"> Leicht</label>
          <label><input type="radio" name="schwierigkeit" value="mittel"> Mittel</label>
          <label><input type="radio" name="schwierigkeit" value="schwer"> Schwer</label>
        </fieldset>
      </div>
    </div>

    <div class="pill" data-filter="monat">
      <button type="button" class="pill-btn">Monat <span class="pill-count" id="pill-count-monat"></span></button>
      <div class="pill-dropdown">
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
    </div>
  </div>

  <div class="karte-mapwrap">
    <div id="aktivitaeten-map"></div>
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
      "url": {{ a.url | jsonify }},
      "bild": {{ a.bild | jsonify }}
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

  function detailsHtml(a) {
    var monate = (a.saison_monate || []).map(function (m) { return MONATE[m - 1]; }).join(", ");
    var detailLink = a.url ? '<a class="liste-detail-link" href="' + BASEURL + a.url + '">Details zur Tour →</a>' : "";
    var bildHtml = a.bild
      ? '<img src="' + BASEURL + a.bild + '" alt="" class="eintrag-bild" loading="lazy">'
      : "";
    return (
      '<div class="eintrag-details">' +
      bildHtml +
      '<div class="eintrag-info">' +
      "Saison: " + monate + "<br>" +
      "Start: " + escapeHtml(a.start_name) +
      (a.anreise ? "<br>Anreise: " + escapeHtml(a.anreise) : "") +
      "</div>" +
      detailLink +
      "</div>"
    );
  }

  // Lädt ein GPX und liefert alle <trk>-Elemente als eigene Segmente zurück (statt sie zu
  // einer Linie zu verschmelzen) – so können mehrere, nicht direkt verbundene Trails in
  // einer Datei stecken (z.B. ein Trailnetz mit mehreren Routen + Zubringerwegen).
  async function ladeGpx(url) {
    try {
      var res = await fetch(url);
      if (!res.ok) return { segments: [], wpts: [] };
      var text = await res.text();
      var xml = new DOMParser().parseFromString(text, "application/xml");
      var segments = Array.prototype.slice.call(xml.querySelectorAll("trk"))
        .map(function (trkEl) {
          var nameEl = trkEl.querySelector("name");
          var pts = Array.prototype.slice.call(trkEl.querySelectorAll("trkpt")).map(function (el) {
            return [parseFloat(el.getAttribute("lat")), parseFloat(el.getAttribute("lon"))];
          });
          return { name: nameEl ? nameEl.textContent : "", pts: pts };
        })
        .filter(function (seg) { return seg.pts.length > 1; });
      var wpts = Array.prototype.slice.call(xml.querySelectorAll("wpt")).map(function (el) {
        var nameEl = el.querySelector("name");
        return {
          lat: parseFloat(el.getAttribute("lat")),
          lon: parseFloat(el.getAttribute("lon")),
          name: nameEl ? nameEl.textContent : ""
        };
      });
      return { segments: segments, wpts: wpts };
    } catch (e) {
      console.warn("GPX konnte nicht geladen werden:", url, e);
      return { segments: [], wpts: [] };
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

    // Ab 761px ist die Karte fullscreen mit schwebender Liste (Komoot-Style);
    // darunter bleibt es beim ursprünglichen, gestapelten Layout (Karte oben,
    // Liste darunter). Diese Grenze muss zur @media-Breakpoint in style.css
    // passen (760px).
    var desktopQuery = window.matchMedia("(min-width: 761px)");
    function istDesktopFloating() { return desktopQuery.matches; }

    // Die Kopfzeile hat keine feste Höhe (umbricht bei Bedarf) – daher wird die
    // tatsächliche Höhe gemessen und als CSS-Variable hinterlegt, bevor die
    // Karte (die sich per calc(100vh - Kopfzeile) berechnet) initialisiert wird.
    function aktualisiereHeaderHoehe() {
      var header = document.querySelector(".site-header");
      if (header) {
        document.documentElement.style.setProperty("--header-height", header.offsetHeight + "px");
      }
    }
    aktualisiereHeaderHoehe();

    // zoomControl: false + eigene Kontrolle unten rechts, da "topleft" (Standard)
    // sich mit der schwebenden Liste oben links überlappen würde.
    var map = L.map("aktivitaeten-map", { scrollWheelZoom: false, zoomControl: false });
    L.control.zoom({ position: "bottomright" }).addTo(map);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>-Mitwirkende'
    }).addTo(map);

    var alleMarker = [];
    var eintraege = [];
    var listeEl = document.getElementById("aktivitaeten-liste");

    // Aktuell ausgewählte Aktivität: hebt Track hervor (zuoberst + Animation)
    // und zeigt Start-/Endpunkt des Tracks als kleine Kreise.
    var aktivesEintrag = null;
    var aktiveMarker = [];
    var aktiveOutlines = [];

    function pfadElement(layer) {
      return layer.getElement ? layer.getElement() : layer._path;
    }

    // Auf Desktop schwebt die Liste über der linken Kartenhälfte – ohne
    // asymmetrisches Padding würde fitBounds Touren dort hinter der Liste
    // "verstecken". Auf Mobile (gestapeltes Layout) reicht symmetrisches Padding.
    function fitBoundsMitPadding(bounds) {
      if (istDesktopFloating()) {
        map.fitBounds(bounds, { paddingTopLeft: [420, 40], paddingBottomRight: [40, 40] });
      } else {
        map.fitBounds(bounds, { padding: [40, 40] });
      }
    }

    // Zoomt/verschiebt die Karte so, dass die ganze Tour (alle Segmente, sonst nur
    // Startpunkt) sichtbar ist.
    function zeigeGesamteTour(eintrag) {
      if (eintrag.trkpts && eintrag.trkpts.length > 1) {
        fitBoundsMitPadding(L.latLngBounds(eintrag.trkpts));
      } else if (eintrag.data.start_koordinaten) {
        map.setView(eintrag.data.start_koordinaten, 14, { animate: true });
      }
    }

    // Aktiviert die Hervorhebung für alle Segmente einer Aktivität: dicker/deckender,
    // fließende Dash-Animation (.track-aktiv) und eine weisse, leicht transparente
    // Aussenlinie dahinter, damit die Tour auch dort erkennbar bleibt, wo mehrere Tracks
    // übereinanderliegen. Zubringer-/Verbindungswege (istAccess) bleiben dünner als
    // die "echten" Trails, werden aber im gleichen Verhältnis hervorgehoben.
    function trackStyleAn(eintrag, outlineListe) {
      eintrag.linien.forEach(function (linie, i) {
        var istAccess = eintrag.istAccessArr[i];
        var outline = L.polyline(eintrag.trkSegments[i], {
          color: "#fff",
          weight: istAccess ? 6 : 10,
          opacity: 0.85,
          interactive: false
        }).addTo(map);
        outlineListe.push(outline);
        linie.setStyle({ weight: istAccess ? 3 : 6, opacity: 1 });
        linie.bringToFront();
        var el = pfadElement(linie);
        if (el) el.classList.add("track-aktiv");
      });
    }

    // Kehrt die Hervorhebung wieder in den Normalzustand um und entfernt die Aussenlinien.
    function trackStyleAus(eintrag, outlineListe) {
      eintrag.linien.forEach(function (linie, i) {
        var istAccess = eintrag.istAccessArr[i];
        linie.setStyle({ weight: istAccess ? 2 : 4, opacity: istAccess ? 0.5 : 0.75 });
        var el = pfadElement(linie);
        if (el) el.classList.remove("track-aktiv");
      });
      outlineListe.forEach(function (o) { map.removeLayer(o); });
      outlineListe.length = 0;
    }

    // Start-/Ende-Kreise ergeben nur bei einem einzelnen, durchgehenden Track Sinn
    // (bei mehreren Segmenten/Trailnetzen gibt es keinen eindeutigen Start-/Endpunkt).
    function zeigeStartEndeMarker(eintrag) {
      if (eintrag.linien.length !== 1) return;
      var pts = eintrag.trkSegments[0];
      if (!pts || pts.length < 2) return;
      var start = pts[0];
      var ende = pts[pts.length - 1];
      var startMarker = L.circleMarker(start, {
        radius: 7,
        color: "#fff",
        weight: 2,
        fillColor: "#2e8b3c",
        fillOpacity: 1
      }).bindTooltip("Start", { direction: "top", offset: [0, -6] });
      var endMarker = L.circleMarker(ende, {
        radius: 7,
        color: "#fff",
        weight: 2,
        fillColor: "#b8322f",
        fillOpacity: 1
      }).bindTooltip("Ende", { direction: "top", offset: [0, -6] });
      startMarker.addTo(map);
      endMarker.addTo(map);
      startMarker.bringToFront();
      endMarker.bringToFront();
      aktiveMarker.push(startMarker, endMarker);
    }

    // Hover-Hervorhebung: identische Optik wie die aktive Tour (dicker, Dash-Animation,
    // weisse Aussenlinie, nach vorne geholt), aber nur temporär. Solange gehovert wird,
    // blendet sich eine evtl. aktive (angeklickte) Tour aus – sonst überlagern sich zwei
    // Hervorhebungen. Endet der Hover, kommt die aktive Tour zurück, ausser es wurde in
    // der Zwischenzeit eine andere Tour angeklickt (dann hat waehleAktivitaet diese
    // bereits selbst hervorgehoben, aktiveOutlines ist dann schon wieder befüllt).
    var hoverEintrag = null;
    var hoverOutlines = [];
    // Kurze Verzögerung, bevor ein Hover-Ende tatsächlich umgesetzt wird: an den
    // Rändern einer (unsichtbaren) Hit-Linie kann die Maus beim Stillhalten durch
    // minimales Zittern kurz raus- und wieder reinwandern, was ohne Debounce zu
    // einem Flackern (aktivieren/deaktivieren im Kreis) führen kann. Erst wenn
    // die Maus den Track für diese Zeitspanne wirklich verlassen hat, wird
    // deaktiviert bzw. die vorher aktive Tour wiederhergestellt.
    var hoverAusTimer = null;
    function hoverEin(eintrag) {
      if (eintrag === aktivesEintrag || !eintrag.linien.length) return;
      clearTimeout(hoverAusTimer);
      if (hoverEintrag === eintrag) return;
      if (hoverEintrag) {
        trackStyleAus(hoverEintrag, hoverOutlines);
      }
      hoverEintrag = eintrag;
      if (aktivesEintrag && aktiveOutlines.length) {
        trackStyleAus(aktivesEintrag, aktiveOutlines);
      }
      trackStyleAn(eintrag, hoverOutlines);
    }
    function hoverAus(eintrag) {
      if (eintrag === aktivesEintrag || !eintrag.linien.length) return;
      if (hoverEintrag !== eintrag) return;
      clearTimeout(hoverAusTimer);
      hoverAusTimer = setTimeout(function () {
        if (hoverEintrag !== eintrag) return;
        trackStyleAus(eintrag, hoverOutlines);
        hoverEintrag = null;
        if (aktivesEintrag && !aktiveOutlines.length) {
          trackStyleAn(aktivesEintrag, aktiveOutlines);
        }
      }, 60);
    }

    // Beim Hover eines Listeneintrags zusätzlich auf die ganze Tour zoomen.
    // Leicht verzögert (debounced), damit schnelles Drüberfahren über mehrere
    // Einträge die Karte nicht wild hin- und herspringen lässt.
    var hoverZoomTimer = null;
    function hoverEinListe(eintrag) {
      hoverEin(eintrag);
      clearTimeout(hoverZoomTimer);
      hoverZoomTimer = setTimeout(function () { zeigeGesamteTour(eintrag); }, 180);
    }
    function hoverAusListe(eintrag) {
      clearTimeout(hoverZoomTimer);
      hoverAus(eintrag);
    }

    // Scrollt den Listeneintrag in den sichtbaren Bereich der Sidebar. Der
    // scrollbare Container ist `.karte-sidebar-scroll` (nicht `.karte-sidebar`
    // selbst, das ist nur der äussere Rahmen der schwebenden Liste mit Header
    // + Footer). Element.scrollIntoView() / scrollTo({behavior:"smooth"}) /
    // requestAnimationFrame-Tweens scrollen hier nicht zuverlässig (beobachtet:
    // alles, was auf Animationsframes wartet, bleibt wirkungslos, sobald der
    // Tab kurz nicht sichtbar/fokussiert ist). Direktes Setzen von scrollTop
    // funktioniert dagegen immer synchron, daher springt der Eintrag ohne
    // Animation an die nächstgelegene sichtbare Position (analog zu block: "nearest").
    function scrolleZuEintrag(eintrag) {
      var sidebar = eintrag.li.closest(".karte-sidebar-scroll");
      if (!sidebar) return;
      var sidebarRect = sidebar.getBoundingClientRect();
      var liRect = eintrag.li.getBoundingClientRect();
      var delta = 0;
      if (liRect.top < sidebarRect.top) {
        delta = liRect.top - sidebarRect.top;
      } else if (liRect.bottom > sidebarRect.bottom) {
        delta = liRect.bottom - sidebarRect.bottom;
      }
      if (delta === 0) return;
      var ziel = Math.max(0, Math.min(sidebar.scrollHeight - sidebar.clientHeight, sidebar.scrollTop + delta));
      sidebar.scrollTop = ziel;
    }

    function waehleAktivitaet(eintrag) {
      if (aktivesEintrag === eintrag) return;

      clearTimeout(hoverAusTimer);
      if (hoverEintrag) {
        trackStyleAus(hoverEintrag, hoverOutlines);
        hoverEintrag = null;
      }

      if (aktivesEintrag) {
        aktivesEintrag.li.classList.remove("aktiv");
        trackStyleAus(aktivesEintrag, aktiveOutlines);
      }
      aktiveMarker.forEach(function (m) { map.removeLayer(m); });
      aktiveMarker = [];

      aktivesEintrag = eintrag;
      eintrag.li.classList.add("aktiv");
      scrolleZuEintrag(eintrag);
      zeigeGesamteTour(eintrag);

      if (eintrag.linien.length) {
        trackStyleAn(eintrag, aktiveOutlines);
      }
      zeigeStartEndeMarker(eintrag);
    }

    DATA.forEach(function (a) {
      var farbeKat = farbe(a.kategorie);
      var layerGroup = L.layerGroup();

      var eintrag = {
        data: a,
        layerGroup: layerGroup,
        li: null,
        linien: [],
        istAccessArr: [],
        trkSegments: [],
        trkpts: []
      };

      if (a.start_koordinaten && a.start_koordinaten.length === 2) {
        var marker = L.circleMarker(a.start_koordinaten, {
          radius: 8,
          color: "#fff",
          weight: 2,
          fillColor: farbeKat,
          fillOpacity: 0.9
        });
        marker.on("click", function () { waehleAktivitaet(eintrag); });
        marker.on("mouseover", function () { hoverEin(eintrag); });
        marker.on("mouseout", function () { hoverAus(eintrag); });
        layerGroup.addLayer(marker);
        alleMarker.push(marker);
      }

      layerGroup.addTo(map);

      var kategorieLabel = a.kategorie ? a.kategorie.charAt(0).toUpperCase() + a.kategorie.slice(1) : "";
      var badges =
        '<span class="badge badge-kategorie">' + escapeHtml(kategorieLabel) + "</span>" +
        '<span class="badge">' + escapeHtml(a.schwierigkeit_wert) + "</span>" +
        '<span class="badge">' + a.dauer_von + "–" + a.dauer_bis + " h</span>" +
        (a.hoehenmeter ? '<span class="badge">' + a.hoehenmeter + " Hm</span>" : "") +
        (a.familienfreundlich ? '<span class="badge badge-familie">Familienfreundlich</span>' : "");

      var li = document.createElement("li");
      li.innerHTML =
        '<span class="titel">' + escapeHtml(a.title) + "</span>" +
        '<span class="meta">' + badges + "</span>" +
        detailsHtml(a);
      li.addEventListener("click", function (ev) {
        if (ev.target && ev.target.classList.contains("liste-detail-link")) return;
        waehleAktivitaet(eintrag);
      });
      li.addEventListener("mouseenter", function () { hoverEinListe(eintrag); });
      li.addEventListener("mouseleave", function () { hoverAusListe(eintrag); });
      listeEl.appendChild(li);
      eintrag.li = li;
      eintraege.push(eintrag);

      if (a.gpx) {
        ladeGpx(BASEURL + a.gpx).then(function (gpx) {
          var allePts = [];
          gpx.segments.forEach(function (seg) {
            var istAccess = /access|connector/i.test(seg.name || "");
            var linie = L.polyline(seg.pts, {
              color: farbeKat,
              weight: istAccess ? 2 : 4,
              opacity: istAccess ? 0.5 : 0.75,
              dashArray: istAccess ? "2 6" : null,
              interactive: false
            });
            // Die sichtbare Linie ist oft nur 2-4px breit – das ist mit der Maus
            // kaum präzise zu treffen. Eine unsichtbare, breitere "Hit-Linie"
            // (gleiche Punkte, opacity 0, weight 16) übernimmt Klick/Hover statt
            // der sichtbaren Linie, damit ein Klick "in der Nähe" des Tracks reicht.
            var hitLinie = L.polyline(seg.pts, {
              color: "#000",
              weight: 16,
              opacity: 0
            });
            hitLinie.on("click", function () { waehleAktivitaet(eintrag); });
            hitLinie.on("mouseover", function () { hoverEin(eintrag); });
            hitLinie.on("mouseout", function () { hoverAus(eintrag); });
            layerGroup.addLayer(linie);
            layerGroup.addLayer(hitLinie);
            eintrag.linien.push(linie);
            eintrag.istAccessArr.push(istAccess);
            eintrag.trkSegments.push(seg.pts);
            allePts = allePts.concat(seg.pts);
          });
          eintrag.trkpts = allePts;
          // Falls die Aktivität schon aktiviert wurde, bevor der Track geladen war:
          // Hervorhebung + Kartenausschnitt nachträglich anwenden.
          if (aktivesEintrag === eintrag && eintrag.linien.length) {
            trackStyleAn(eintrag, aktiveOutlines);
            zeigeStartEndeMarker(eintrag);
            zeigeGesamteTour(eintrag);
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
      fitBoundsMitPadding(L.featureGroup(alleMarker).getBounds());
    } else {
      map.setView([47.205, 9.35], 12);
    }

    // Nach Layout-Änderungen (Fenstergrösse, Wechsel Desktop/Mobile-Breakpoint)
    // muss Leaflet die Kartengrösse neu vermessen, sonst bleiben Kacheln
    // verzerrt/abgeschnitten. Ausserdem: Header kann bei Zeilenumbruch der Nav
    // seine Höhe ändern, offene Filter-Dropdowns sollen bei Resize schliessen.
    window.addEventListener("resize", function () {
      aktualisiereHeaderHoehe();
      map.invalidateSize();
      schliesseAllePills();
    });

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
          if (aktivesEintrag === e) {
            aktiveMarker.forEach(function (m) { map.removeLayer(m); });
            aktiveMarker = [];
            aktiveOutlines.forEach(function (o) { map.removeLayer(o); });
            aktiveOutlines = [];
            aktivesEintrag = null;
          }
          if (hoverEintrag === e) {
            hoverOutlines.forEach(function (o) { map.removeLayer(o); });
            hoverOutlines = [];
            hoverEintrag = null;
          }
        }
      });

      aktualisierePillCounts();
    }

    // Zeigt im Pill-Button an, wie stark ein Filter vom Standard ("alles an")
    // abweicht, z.B. "Kategorie (3)" wenn nur 3 von 6 Kategorien aktiv sind.
    var monatsnamenPill = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"];
    function aktualisierePillCounts() {
      var kategorieCount = document.getElementById("pill-count-kategorie");
      var aktiveKategorien = katCheckboxen.filter(function (c) { return c.checked; });
      kategorieCount.textContent = aktiveKategorien.length < katCheckboxen.length ? "(" + aktiveKategorien.length + ")" : "";

      var schwierigkeitCount = document.getElementById("pill-count-schwierigkeit");
      var schwierigkeit = schwierigkeitRadios.filter(function (r) { return r.checked; })[0].value;
      schwierigkeitCount.textContent = schwierigkeit === "alle" ? "" : "(" + schwierigkeit.charAt(0).toUpperCase() + schwierigkeit.slice(1) + ")";

      var monatCount = document.getElementById("pill-count-monat");
      var monat = parseInt(monatSelect.value, 10);
      monatCount.textContent = monat === 0 ? "" : "(" + monatsnamenPill[monat - 1] + ")";
    }

    // Filter-Pills: Klick auf einen Pill-Button öffnet/schliesst sein Dropdown;
    // dabei wird immer nur maximal ein Dropdown gleichzeitig offen gehalten.
    var pills = Array.prototype.slice.call(document.querySelectorAll(".pill"));
    function schliesseAllePills() {
      pills.forEach(function (p) { p.classList.remove("offen"); });
    }
    pills.forEach(function (pill) {
      var btn = pill.querySelector(".pill-btn");
      btn.addEventListener("click", function (ev) {
        ev.stopPropagation();
        var warOffen = pill.classList.contains("offen");
        schliesseAllePills();
        if (!warOffen) pill.classList.add("offen");
      });
      // Klicks innerhalb des Dropdowns (Checkboxen, Select) sollen es nicht
      // gleich wieder schliessen, indem sie zum document hochblubbern.
      pill.querySelector(".pill-dropdown").addEventListener("click", function (ev) {
        ev.stopPropagation();
      });
    });
    document.addEventListener("click", schliesseAllePills);
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape") schliesseAllePills();
    });

    katCheckboxen.forEach(function (c) { c.addEventListener("change", anwendenFilter); });
    schwierigkeitRadios.forEach(function (r) { r.addEventListener("change", anwendenFilter); });
    monatSelect.addEventListener("change", anwendenFilter);
    aktualisierePillCounts();
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
