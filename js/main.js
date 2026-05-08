// Mobile menu toggle
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');

if (navToggle) {
  navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    navToggle.classList.toggle('active');
  });
}

// Close mobile menu when clicking a link
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    navMenu.classList.remove('active');
    navToggle.classList.remove('active');
  });
});

// Active nav link highlighting with IntersectionObserver
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.getAttribute('id');
      navLinks.forEach(link => {
        const isActive = link.getAttribute('href') === '#' + id;
        link.classList.toggle('active', isActive);
      });
    }
  });
}, { rootMargin: '-50% 0px -50% 0px', threshold: 0 });

sections.forEach(section => observer.observe(section));

// Language switching — inner text is canonical zh, data-en holds en translation.
// Cache original zh text once, restore from cache when switching back from en.
const STORAGE_KEY = 'lang';
const langSwitch = document.getElementById('langSwitch');
const i18nElements = document.querySelectorAll('[data-en]');
const zhCache = new WeakMap();

i18nElements.forEach(el => zhCache.set(el, el.textContent));

function setLanguage(lang) {
  i18nElements.forEach(el => {
    el.textContent = lang === 'en' ? el.getAttribute('data-en') : zhCache.get(el);
  });
  document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN';
  localStorage.setItem(STORAGE_KEY, lang);
}

if (langSwitch) {
  langSwitch.addEventListener('click', () => {
    const next = document.documentElement.lang === 'en' ? 'zh' : 'en';
    setLanguage(next);
  });
}

// Restore persisted language on load
const saved = localStorage.getItem(STORAGE_KEY);
if (saved === 'en') setLanguage('en');
