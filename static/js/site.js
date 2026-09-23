/* GrapheneOS Info Board: progressive enhancement.
 *
 * Two independent features, neither of which the site depends on:
 *
 *   1. The theme toggle. The theme itself is already applied by an inline
 *      script in <head>; this file only handles the button and keeps the
 *      stored preference in step with the system setting.
 *   2. Search. Fetches a small JSON index once, on first interaction, and
 *      filters it in the browser. No dependency, no network call per keystroke.
 *
 * Everything degrades to a plain, fully readable page without this file.
 */

(function () {
  "use strict";

  /* ---------------------------------------------------------------- theme */

  var root = document.documentElement;
  var STORAGE_KEY = "theme";

  function systemTheme() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function effectiveTheme() {
    var set = root.getAttribute("data-theme");
    return set === "light" || set === "dark" ? set : systemTheme();
  }

  function storedTheme() {
    try {
      var value = localStorage.getItem(STORAGE_KEY);
      return value === "light" || value === "dark" ? value : null;
    } catch (error) {
      return null;
    }
  }

  function rememberTheme(value) {
    try {
      localStorage.setItem(STORAGE_KEY, value);
    } catch (error) {
      /* Storage unavailable. The choice still applies for this page. */
    }
  }

  function setupThemeToggle() {
    var button = document.querySelector("[data-theme-toggle]");
    if (!button) return;

    function label() {
      var next = effectiveTheme() === "dark" ? "light" : "dark";
      button.setAttribute("aria-label", "Switch to " + next + " theme");
    }

    label();

    button.addEventListener("click", function () {
      var next = effectiveTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      rememberTheme(next);
      label();
    });

    // Follow the system only while the reader has not chosen for themselves.
    if (window.matchMedia) {
      var query = window.matchMedia("(prefers-color-scheme: dark)");
      var onChange = function () {
        if (!storedTheme()) {
          root.removeAttribute("data-theme");
          label();
        }
      };
      if (query.addEventListener) query.addEventListener("change", onChange);
      else if (query.addListener) query.addListener(onChange);
    }
  }

  /* --------------------------------------------------------------- search */

  var MIN_QUERY = 2;
  var MAX_RESULTS = 8;

  function normalise(value) {
    return String(value || "").toLowerCase().trim();
  }

  /* Ranked so an exact name beats a prefix, which beats a mention in the
     description, which beats a match on the package name. Anything that does
     not match at all returns -1 and is dropped. */
  function score(app, query) {
    var title = normalise(app.title);

    if (title === query) return 1000;
    if (title.indexOf(query) === 0) return 900;
    if (title.indexOf(query) !== -1) return 700;
    if (normalise(app.developer).indexOf(query) !== -1) return 500;
    if (normalise(app.package).indexOf(query) !== -1) return 450;
    if (app.haystack.indexOf(query) !== -1) return 300;

    var tokens = query.split(/\s+/).filter(Boolean);
    if (tokens.length > 1 && tokens.every(function (token) {
      return app.haystack.indexOf(token) !== -1;
    })) {
      return 200;
    }

    return -1;
  }

  function buildResult(app) {
    var item = document.createElement("li");
    item.className = "search__result";

    var link = document.createElement("a");
    link.href = app.url;

    var title = document.createElement("span");
    title.className = "search__result-title";
    title.textContent = app.title;
    link.appendChild(title);

    if (app.subtitle) {
      var subtitle = document.createElement("span");
      subtitle.className = "search__result-meta";
      subtitle.textContent = app.subtitle;
      link.appendChild(subtitle);
    }

    if (app.badges && app.badges.length) {
      var row = document.createElement("span");
      row.className = "search__result-badges";
      app.badges.forEach(function (badge) {
        var el = document.createElement("span");
        el.className = "badge badge--" + badge.tone;
        el.textContent = badge.label;
        row.appendChild(el);
      });
      link.appendChild(row);
    }

    item.appendChild(link);
    return item;
  }

  function setupSearch() {
    var form = document.querySelector("[data-search]");
    if (!form) return;

    var input = form.querySelector(".search__input");
    var results = form.querySelector(".search__results");
    var clear = form.querySelector(".search__clear");
    var status = form.querySelector("[data-search-status]");
    if (!input || !results) return;

    var index = null;
    var loading = false;
    var active = -1;

    function load() {
      if (index || loading) return;
      loading = true;
      fetch(form.getAttribute("data-index"), { credentials: "same-origin" })
        .then(function (response) {
          if (!response.ok) throw new Error("search index unavailable");
          return response.json();
        })
        .then(function (data) {
          index = (data && data.apps) || [];
        })
        .catch(function () {
          index = [];
        })
        .then(function () {
          loading = false;
          if (input.value.trim().length >= MIN_QUERY) run();
        });
    }

    function close() {
      results.hidden = true;
      results.innerHTML = "";
      input.setAttribute("aria-expanded", "false");
      active = -1;
    }

    function links() {
      return Array.prototype.slice.call(results.querySelectorAll("a"));
    }

    function highlight(next) {
      var all = links();
      if (!all.length) return;
      active = (next + all.length) % all.length;
      all[active].focus();
    }

    function run() {
      var query = normalise(input.value);
      clear.hidden = query.length === 0;

      if (query.length < MIN_QUERY) {
        close();
        if (status) status.textContent = "";
        return;
      }

      load();

      if (!index) {
        if (status) status.textContent = "Searching";
        return;
      }

      var matches = [];
      for (var i = 0; i < index.length; i++) {
        var value = score(index[i], query);
        if (value >= 0) matches.push({ app: index[i], value: value });
      }

      matches.sort(function (a, b) {
        if (b.value !== a.value) return b.value - a.value;
        return a.app.title.localeCompare(b.app.title);
      });

      var shown = matches.slice(0, MAX_RESULTS);
      results.innerHTML = "";

      if (!shown.length) {
        var empty = document.createElement("li");
        empty.className = "search__empty";
        empty.textContent = "No app matches \u201C" + input.value.trim() + "\u201D.";
        results.appendChild(empty);
        if (status) status.textContent = "No results";
      } else {
        shown.forEach(function (match) {
          results.appendChild(buildResult(match.app));
        });

        if (matches.length > shown.length) {
          var more = document.createElement("li");
          more.className = "search__more";
          more.textContent = (matches.length - shown.length) + " more \u2014 keep typing.";
          results.appendChild(more);
        }

        if (status) {
          status.textContent = matches.length + (matches.length === 1 ? " result" : " results");
        }
      }

      results.hidden = false;
      input.setAttribute("aria-expanded", "true");
      active = -1;
    }

    input.addEventListener("focus", load);
    input.addEventListener("input", run);

    input.addEventListener("keydown", function (event) {
      if (event.key === "ArrowDown" && !results.hidden) {
        event.preventDefault();
        highlight(0);
      } else if (event.key === "Enter") {
        var first = links()[0];
        if (first && !results.hidden) {
          event.preventDefault();
          first.click();
        }
      } else if (event.key === "Escape") {
        close();
      }
    });

    // Arrow keys walk the real links, so focus is where a screen reader and the
    // browser both expect it. No aria-activedescendant trickery.
    results.addEventListener("keydown", function (event) {
      if (event.key === "ArrowDown") {
        event.preventDefault();
        highlight(active + 1);
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        if (active <= 0) input.focus();
        else highlight(active - 1);
      } else if (event.key === "Escape") {
        event.preventDefault();
        input.focus();
        close();
      }
    });

    if (clear) {
      clear.addEventListener("click", function () {
        input.value = "";
        input.focus();
        close();
        clear.hidden = true;
      });
    }

    // Close when focus leaves the whole control, but not when it moves between
    // the input and the results.
    form.addEventListener("focusout", function (event) {
      if (!form.contains(event.relatedTarget)) close();
    });

    document.addEventListener("click", function (event) {
      if (!form.contains(event.target)) close();
    });
  }

  /* ----------------------------------------------------------------- init */

  setupThemeToggle();
  setupSearch();
})();
