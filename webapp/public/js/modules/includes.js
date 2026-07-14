document.addEventListener('DOMContentLoaded', () => {
  const includeElements = document.querySelectorAll('[data-include]');
  let pending = includeElements.length;
  if (pending === 0) {
    ensureI18N();
    setActiveNav();
    return;
  }
  includeElements.forEach(async (el) => {
    const filePath = el.getAttribute('data-include');
    if (!filePath) return done();
    try {
      const response = await fetch(filePath, { cache: 'no-cache' });
      if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
      const html = await response.text();
      el.outerHTML = html;
    } catch (error) {
      console.error('Include failed:', filePath, error);
    } finally {
      done();
    }
  });

  function done(){
    pending -= 1;
    if (pending <= 0) {
      ensureI18N();
      setActiveNav();
    }
  }

  function ensureI18N(){
    const desired = localStorage.getItem('lang') || (navigator.language && navigator.language.startsWith('ar') ? 'ar':'en');
    if (window.__i18n && typeof window.__i18n.loadLang === 'function'){
      window.__i18n.loadLang(desired);
    } else {
      const s = document.createElement('script');
      s.src = 'assets/js/i18n.js';
      s.defer = true;
      s.onload = () => { window.__i18n && window.__i18n.loadLang(desired); };
      document.head.appendChild(s);
    }
  }

  function setActiveNav(){
    const path = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('#navmenu a').forEach((link) => {
      const href = link.getAttribute('href');
      if (!href || href.startsWith('http')) return;
      link.classList.toggle('active', href === path);
    });
  }
});
