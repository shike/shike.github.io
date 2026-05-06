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

const observerOptions = {
  root: null,
  rootMargin: '-50% 0px -50% 0px',
  threshold: 0
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.getAttribute('id');
      navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + id) {
          link.classList.add('active');
        }
      });
    }
  });
}, observerOptions);

sections.forEach(section => observer.observe(section));

// Language switching
const langSwitch = document.getElementById('langSwitch');
let currentLang = 'zh';

function switchLanguage() {
  currentLang = currentLang === 'zh' ? 'en' : 'zh';

  // Update switch button text
  if (langSwitch) {
    langSwitch.textContent = langSwitch.getAttribute('data-' + currentLang);
  }

  // Update all elements with data-zh and data-en
  document.querySelectorAll('[data-zh][data-en]').forEach(el => {
    const newText = el.getAttribute('data-' + currentLang);
    if (newText) {
      // For elements with child elements (like footer), set innerHTML
      if (el.tagName === 'FOOTER' || el.querySelector('*')) {
        // Only update if it's a simple text element or has the attributes directly
        if (el.children.length === 0) {
          el.textContent = newText;
        }
      } else {
        el.textContent = newText;
      }
    }
  });

  // Update HTML lang attribute
  document.documentElement.lang = currentLang === 'zh' ? 'zh-CN' : 'en';
}

if (langSwitch) {
  langSwitch.addEventListener('click', switchLanguage);
}
