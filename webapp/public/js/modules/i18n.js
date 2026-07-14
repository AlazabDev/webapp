
(function(){
  const SUPPORTED = ['ar','en'];
  const DEFAULT = localStorage.getItem('lang') || (navigator.language && navigator.language.startsWith('ar') ? 'ar':'en');

  async function loadLang(lang){
    if(!SUPPORTED.includes(lang)) lang = 'en';
    const res = await fetch(`locales/${lang}.json`, { cache: 'no-cache' });
    const dict = await res.json();
    applyLang(lang, dict);
  }

  function resolve(obj, path){
    return path.split('.').reduce((o,k)=> (o && o[k]!==undefined) ? o[k] : null, obj);
  }

  async function applyLang(lang, dict){
    const html = document.documentElement;
    html.setAttribute('lang', lang);
    html.setAttribute('dir', lang==='ar' ? 'rtl' : 'ltr');

    document.body && document.body.classList.toggle('rtl', lang==='ar');

    document.querySelectorAll('[data-i18n]').forEach(el=>{
      const key = el.getAttribute('data-i18n');
      const val = resolve(dict, key);
      if(val==null) return;
      if(el.tagName==='INPUT' || el.tagName==='TEXTAREA'){
        if(el.hasAttribute('placeholder')) el.setAttribute('placeholder', val);
        else el.value = val;
      }else{
        el.textContent = val;
      }
    });
    document.querySelectorAll('[data-i18n-html]').forEach(el=>{
      const key = el.getAttribute('data-i18n-html');
      const val = resolve(dict, key);
      if(val==null) return;
      el.innerHTML = val;
    });

    await Promise.all(Array.from(document.querySelectorAll('[data-i18n-url]')).map(async el =>{
      const name = el.getAttribute('data-i18n-url');
      if(!name) return;
      try{
        const res = await fetch(`locales/${lang}/${name}.html`, { cache: 'no-cache' });
        if(!res.ok) throw new Error(`${res.status}`);
        el.innerHTML = await res.text();
      }catch(err){
        console.warn('i18n external load failed', name, err);
      }
    }));

    document.querySelectorAll('[data-lang]').forEach(btn=>{
      btn.classList.toggle('active', btn.getAttribute('data-lang')===lang);
    });
    localStorage.setItem('lang', lang);
  }

  function attachSwitchers(){
    document.querySelectorAll('[data-lang]').forEach(btn=>{
      // avoid duplicate listeners
      btn.__i18nBound || btn.addEventListener('click', ()=>{
        const lang = btn.getAttribute('data-lang');
        loadLang(lang);
      });
      btn.__i18nBound = true;
    });
  }

  window.__i18n = { loadLang, applyLang };

  function init(){
    attachSwitchers();
    loadLang(DEFAULT);
  }

  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
