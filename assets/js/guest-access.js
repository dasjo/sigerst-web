/**
 * Gäste-Modus: URL ?gast=<token> aktiviert .guest-only, deaktiviert .public-only.
 * Token in _config.yml (guest_link_token). Kein Ersatz für echte Zugangskontrolle.
 */
(function () {
  var cfg = window.SIGERST_GUEST;
  if (!cfg || !cfg.param || !cfg.token) return;

  var storageKey = "sigerst_guest";
  var params = new URLSearchParams(window.location.search);
  var fromUrl = params.get(cfg.param) === cfg.token;

  if (fromUrl) {
    try {
      sessionStorage.setItem(storageKey, "1");
    } catch (e) { /* ignore */ }
  }

  var isGuest = fromUrl;
  if (!isGuest) {
    try {
      isGuest = sessionStorage.getItem(storageKey) === "1";
    } catch (e) { /* ignore */ }
  }

  if (!isGuest) return;

  document.documentElement.classList.add("guest-mode");

  document.querySelectorAll(".guest-only[hidden]").forEach(function (el) {
    el.removeAttribute("hidden");
  });
})();
