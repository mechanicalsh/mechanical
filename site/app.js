/* Mechanical — Enterprise
   Header: add a hairline once scrolled, hide on scroll-down / show on scroll-up.
   Reveal: fade figures in as they enter the viewport.
   Progressive enhancement: if this never loads, the page is fully usable. */
(function () {
  var hdr = document.getElementById('hdr');
  var last = window.scrollY || 0, ticking = false;

  function onScroll() {
    var y = window.scrollY || 0;
    if (hdr) {
      hdr.classList.toggle('scrolled', y > 8);
      if (y > last && y > 120) hdr.classList.add('hide');
      else if (y < last) hdr.classList.remove('hide');
    }
    last = y; ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });

  // reveal on scroll
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && els.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }
})();
