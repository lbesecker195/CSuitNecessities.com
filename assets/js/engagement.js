/* Engagement + CTR instrumentation. No dependencies. */
(function () {
  "use strict";
  var s = document.currentScript || {};
  var d = s.dataset || {};
  var EV = {
    image: d.evImage || "image_click",
    anchor: d.evAnchor || "affiliate_click",
    scroll: d.evScroll || "scroll_depth",
    read: d.evRead || "read_complete",
  };
  var stickyAfter = parseFloat(d.stickyAfter || "18");

  /* ---- generic event sink: GA4 (gtag), GTM (dataLayer), Plausible, PostHog ---- */
  function track(name, props) {
    props = props || {};
    try { if (typeof window.gtag === "function") window.gtag("event", name, props); } catch (e) {}
    try { (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: name }, props)); } catch (e) {}
    try { if (typeof window.plausible === "function") window.plausible(name, { props: props }); } catch (e) {}
    try { if (window.posthog) window.posthog.capture(name, props); } catch (e) {}
    if (window.__CTR_DEBUG) console.debug("[track]", name, props);
  }

  /* ---- reading progress bar ---- */
  var bar = document.querySelector("#read-progress span");
  var article = document.querySelector(".post-body") || document.querySelector("main");

  function scrollPct() {
    var h = document.documentElement;
    var max = (h.scrollHeight - h.clientHeight) || 1;
    return Math.min(100, Math.max(0, (h.scrollTop || window.pageYOffset) / max * 100));
  }

  /* ---- sticky CTA + back-to-top ---- */
  var sticky = document.querySelector("#sticky-cta");
  var toTop = document.querySelector(".to-top");
  if (sticky) sticky.hidden = false;

  /* ---- scroll-depth milestones + read-complete ---- */
  var milestones = [25, 50, 75, 90];
  var hit = {};
  var readFired = false;
  var startTime = Date.now();

  function onScroll() {
    var p = scrollPct();
    if (bar) bar.style.width = p.toFixed(1) + "%";

    if (sticky) sticky.classList.toggle("is-in", p >= stickyAfter);
    if (toTop) toTop.classList.toggle("is-in", p >= 40);

    milestones.forEach(function (m) {
      if (!hit[m] && p >= m) {
        hit[m] = true;
        track(EV.scroll, { percent: m, path: location.pathname });
      }
    });

    if (!readFired && article) {
      var end = article.getBoundingClientRect().bottom;
      if (end - window.innerHeight < 120) {
        readFired = true;
        track(EV.read, {
          path: location.pathname,
          seconds: Math.round((Date.now() - startTime) / 1000),
        });
      }
    }
  }
  var ticking = false;
  window.addEventListener("scroll", function () {
    if (!ticking) { requestAnimationFrame(function () { onScroll(); ticking = false; }); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---- click instrumentation for images + anchors ---- */
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a");
    if (!a) return;

    var isImageClick = !!e.target.closest("img, .fig-link, .card-media, .pick-media, .offer-card-media, [data-cta$='image']");
    var affiliate = a.getAttribute("data-affiliate");
    var slot = a.getAttribute("data-cta") || "unknown";
    var outbound = a.hostname && a.hostname !== location.hostname;

    if (affiliate || (outbound && a.rel && /sponsored|nofollow/.test(a.rel))) {
      track(EV.anchor, {
        affiliate: affiliate || a.hostname,
        slot: slot,
        surface: isImageClick ? "image" : "text",
        anchor_text: (a.textContent || "").trim().slice(0, 80),
        href: a.href,
      });
    } else if (isImageClick) {
      track(EV.image, { slot: slot, href: a.href, internal: !outbound });
    }
  }, true);

  /* ---- TOC scroll-spy: keeps the sidebar feeling alive => more dwell ---- */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc nav a[href^='#']"));
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (l) {
      var id = decodeURIComponent(l.getAttribute("href").slice(1));
      var el = document.getElementById(id);
      if (el) map[id] = l;
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (l) { l.classList.remove("is-active"); });
          var active = map[en.target.id];
          if (active) active.classList.add("is-active");
        }
      });
    }, { rootMargin: "-80px 0px -70% 0px" });
    Object.keys(map).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) io.observe(el);
    });
  }

  /* ---- exit-safety: log time-on-page once ---- */
  var exitLogged = false;
  function logExit() {
    if (exitLogged) return;
    exitLogged = true;
    track("time_on_page", {
      path: location.pathname,
      seconds: Math.round((Date.now() - startTime) / 1000),
      max_scroll: Math.round(scrollPct()),
    });
  }
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") logExit();
  });
  window.addEventListener("pagehide", logExit);
})();
