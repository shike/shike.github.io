const STORAGE_KEY = 'lang';
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');
const langSwitch = document.getElementById('langSwitch');

const META = {
  zh: {
    title: '施可｜连续创业者、Dropleap 创始人、企业级 AI 实践者',
    description: '施可，水滴跃动 Dropleap 创始人、连续创业者、中科大软件工程硕士。16 年横跨软件工程、互联网产品与企业经营，现聚焦企业级 AI Agent、GEO 与应用工程。'
  },
  en: {
    title: 'Shi Ke — Serial Entrepreneur, Founder of Dropleap, Enterprise AI Practitioner',
    description: 'Shi Ke is a serial entrepreneur, founder of Dropleap, and an enterprise AI practitioner with 16 years across software engineering, internet products, and business operations. He now focuses on enterprise AI Agents, GEO, and application engineering.'
  }
};

const textElements = document.querySelectorAll('[data-en]');
const ariaElements = document.querySelectorAll('[data-en-aria]');
const zhTextCache = new WeakMap();
const zhAriaCache = new WeakMap();

textElements.forEach(el => zhTextCache.set(el, el.textContent));
ariaElements.forEach(el => zhAriaCache.set(el, el.getAttribute('aria-label') || ''));

function setMeta(name, content) {
  const el = document.querySelector(`meta[name="${name}"]`);
  if (el) el.setAttribute('content', content);
}

function setOg(prop, content) {
  const el = document.querySelector(`meta[property="${prop}"]`);
  if (el) el.setAttribute('content', content);
}

function setLanguage(lang) {
  const isEn = lang === 'en';
  const key = isEn ? 'en' : 'zh';

  textElements.forEach(el => {
    el.textContent = isEn ? el.getAttribute('data-en') : zhTextCache.get(el);
  });
  ariaElements.forEach(el => {
    el.setAttribute('aria-label', isEn ? el.getAttribute('data-en-aria') : zhAriaCache.get(el));
  });

  document.documentElement.lang = isEn ? 'en' : 'zh-CN';
  document.title = META[key].title;
  setMeta('description', META[key].description);
  setOg('og:title', META[key].title);
  setOg('og:description', META[key].description);
  setOg('og:locale', isEn ? 'en_US' : 'zh_CN');

  const twitterTitle = document.querySelector('meta[name="twitter:title"]');
  const twitterDesc = document.querySelector('meta[name="twitter:description"]');
  if (twitterTitle) twitterTitle.setAttribute('content', META[key].title);
  if (twitterDesc) twitterDesc.setAttribute('content', META[key].description);

  localStorage.setItem(STORAGE_KEY, lang);
}

function closeMobileMenu() {
  if (!navMenu || !navMenu.classList.contains('active')) return;
  navMenu.classList.remove('active');
  navToggle.classList.remove('active');
  navToggle.setAttribute('aria-expanded', 'false');
}

if (navToggle) {
  navToggle.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('active');
    navToggle.classList.toggle('active', isOpen);
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && navMenu && navMenu.classList.contains('active')) {
    closeMobileMenu();
    navToggle.focus();
  }
});

document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', closeMobileMenu);
});

const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const id = entry.target.getAttribute('id');
    navLinks.forEach(link => {
      const isActive = link.getAttribute('href') === '#' + id;
      link.classList.toggle('active', isActive);
      if (isActive) {
        link.setAttribute('aria-current', 'page');
      } else {
        link.removeAttribute('aria-current');
      }
    });
  });
}, { rootMargin: '-50% 0px -50% 0px', threshold: 0 });

sections.forEach(section => observer.observe(section));

if (langSwitch) {
  langSwitch.addEventListener('click', () => {
    const next = document.documentElement.lang === 'en' ? 'zh' : 'en';
    setLanguage(next);
  });
}

const saved = localStorage.getItem(STORAGE_KEY);
if (saved === 'en') setLanguage('en');

// QR modal — agency product inquiry (星启 GEO / 呼波特 WhoBot)
const qrModal = document.getElementById('qrModal');
const qrTitle = document.getElementById('qrModalTitle');
const qrDesc = document.getElementById('qrModalDesc');
let qrLastFocus = null;

function openQrModal(title, desc) {
  if (!qrModal) return;
  qrLastFocus = document.activeElement;
  if (title && qrTitle) qrTitle.textContent = title;
  if (desc && qrDesc) qrDesc.textContent = desc;
  qrModal.hidden = false;
  document.body.style.overflow = 'hidden';
  const closeBtn = qrModal.querySelector('.qr-modal-close');
  if (closeBtn) closeBtn.focus();
}

function closeQrModal() {
  if (!qrModal || qrModal.hidden) return;
  qrModal.hidden = true;
  document.body.style.overflow = '';
  if (qrLastFocus && typeof qrLastFocus.focus === 'function') qrLastFocus.focus();
}

document.querySelectorAll('[data-qr-trigger]').forEach(btn => {
  btn.addEventListener('click', () => {
    openQrModal(btn.getAttribute('data-qr-title'), btn.getAttribute('data-qr-desc'));
  });
});

if (qrModal) {
  qrModal.querySelectorAll('[data-qr-close]').forEach(el => {
    el.addEventListener('click', closeQrModal);
  });
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && qrModal && !qrModal.hidden) closeQrModal();
});
