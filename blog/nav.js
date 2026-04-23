/* Vanilla-JS driver for the shared blog header:
   - Coverage dropdown (hover + focus on desktop, tap on mobile)
   - Hamburger / mobile menu toggle + swipe-close
   - Sticky-nav scroll-shadow (adds .scrolled > 20px)
   - URL-hash round trip so "#services" still lands on the SPA services page
*/
(function () {
  var nav = document.getElementById('siteNav');
  var cov = document.getElementById('navCoverage');
  var covLink = cov && cov.querySelector('.nav-link');
  var ham = document.getElementById('navHam');
  var menu = document.getElementById('mobileMenu');
  var closeBtn = document.getElementById('mobileClose');

  // Coverage dropdown ------------------------------------------------------
  if (cov && covLink) {
    var closeTimer;
    var open = function () { clearTimeout(closeTimer); cov.classList.add('is-open'); covLink.setAttribute('aria-expanded', 'true'); };
    var close = function () { cov.classList.remove('is-open'); covLink.setAttribute('aria-expanded', 'false'); };
    var closeSoon = function () { clearTimeout(closeTimer); closeTimer = setTimeout(close, 140); };

    // Hover on desktop
    cov.addEventListener('mouseenter', open);
    cov.addEventListener('mouseleave', closeSoon);
    cov.addEventListener('focusin', open);
    cov.addEventListener('focusout', function (e) {
      if (!cov.contains(e.relatedTarget)) closeSoon();
    });

    // Click on the parent link: toggle dropdown on narrow screens; on wide, let it fall through to ../#services
    covLink.addEventListener('click', function (e) {
      if (window.matchMedia('(hover:hover) and (min-width:1025px)').matches) return; // desktop: follow href
      e.preventDefault();
      cov.classList.contains('is-open') ? close() : open();
    });

    // Click outside to close
    document.addEventListener('click', function (e) {
      if (!cov.contains(e.target)) close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
  }

  // Hamburger / mobile menu ------------------------------------------------
  if (ham && menu) {
    var openMenu = function () { menu.classList.add('open'); ham.setAttribute('aria-expanded', 'true'); document.body.style.overflow = 'hidden'; };
    var closeMenu = function () { menu.classList.remove('open'); ham.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; };
    ham.addEventListener('click', function (e) { e.stopPropagation(); menu.classList.contains('open') ? closeMenu() : openMenu(); });
    if (closeBtn) closeBtn.addEventListener('click', closeMenu);
    // Any link inside the mobile menu closes it after click
    menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeMenu); });
    // Escape closes
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.classList.contains('open')) closeMenu(); });
  }

  // Sticky scroll shadow ---------------------------------------------------
  if (nav) {
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 20); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
})();
