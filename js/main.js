(function () {
  'use strict';

  const STORAGE_KEY = 'lang';

  // 只有英文需要在这里声明；中文一律从文档本身读取，避免 title/description 有两份真相。
  const EN_META = {
    title: 'Shi Ke — Founder of Dropleap, Enterprise AI Practitioner',
    description: 'Shi Ke — founder of Dropleap, serial entrepreneur, USTC MSc. Authorized WorkBuddy agent: first manufacturing AI scenario live in 2-4 weeks, 100+ manufacturers served.'
  };

  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');
  const langSwitch = document.getElementById('langSwitch');
  const qrModal = document.getElementById('qrModal');

  /* ------------------------------------------------------------------ i18n */

  const textElements = document.querySelectorAll('[data-en]');
  const ariaElements = document.querySelectorAll('[data-en-aria]');
  const altElements = document.querySelectorAll('[data-en-alt]');
  const zhText = new WeakMap();
  const zhAria = new WeakMap();
  const zhAlt = new WeakMap();

  textElements.forEach(el => zhText.set(el, el.textContent));
  ariaElements.forEach(el => zhAria.set(el, el.getAttribute('aria-label') || ''));
  altElements.forEach(el => zhAlt.set(el, el.getAttribute('alt') || ''));

  const zhMeta = {
    title: document.title,
    description: metaContent('name', 'description')
  };

  function metaContent(attr, value) {
    const el = document.querySelector('meta[' + attr + '="' + value + '"]');
    return el ? el.getAttribute('content') || '' : '';
  }

  function setMeta(attr, name, content) {
    const el = document.querySelector('meta[' + attr + '="' + name + '"]');
    if (el) el.setAttribute('content', content);
  }

  // 只替换叶子元素的文本。带子元素的元素一旦被 textContent 覆盖，其中的行内链接、
  // <code> 等节点会被永久删除，切回中文也找不回来。
  function setText(el, value) {
    if (value == null) return;
    if (el.children.length > 0) return;
    el.textContent = value;
  }

  function setLanguage(lang) {
    const isEn = lang === 'en';
    const meta = isEn ? EN_META : zhMeta;

    textElements.forEach(el => setText(el, isEn ? el.getAttribute('data-en') : zhText.get(el)));
    ariaElements.forEach(el => {
      el.setAttribute('aria-label', isEn ? el.getAttribute('data-en-aria') : zhAria.get(el));
    });
    altElements.forEach(el => {
      el.setAttribute('alt', isEn ? el.getAttribute('data-en-alt') : zhAlt.get(el));
    });

    document.documentElement.lang = isEn ? 'en' : 'zh-CN';
    document.title = meta.title;
    setMeta('name', 'description', meta.description);
    setMeta('property', 'og:title', meta.title);
    setMeta('property', 'og:description', meta.description);
    setMeta('property', 'og:locale', isEn ? 'en_US' : 'zh_CN');
    setMeta('name', 'twitter:title', meta.title);
    setMeta('name', 'twitter:description', meta.description);

    localStorage.setItem(STORAGE_KEY, lang);
  }

  if (langSwitch) {
    langSwitch.addEventListener('click', () => {
      setLanguage(document.documentElement.lang === 'en' ? 'zh' : 'en');
    });
  }

  if (localStorage.getItem(STORAGE_KEY) === 'en') setLanguage('en');

  /* -------------------------------------------------------------- 移动菜单 */

  function closeMobileMenu() {
    if (!navMenu || !navMenu.classList.contains('active')) return;
    navMenu.classList.remove('active');
    if (navToggle) {
      navToggle.classList.remove('active');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  }

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      const isOpen = navMenu.classList.toggle('active');
      navToggle.classList.toggle('active', isOpen);
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && navMenu.classList.contains('active')) {
        closeMobileMenu();
        navToggle.focus();
      }
    });

    navMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', closeMobileMenu);
    });
  }

  /* ------------------------------------------------------------ 当前板块高亮 */

  const navLinks = document.querySelectorAll('.nav-link');

  if (navLinks.length && 'IntersectionObserver' in window) {
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

    document.querySelectorAll('section[id]').forEach(section => observer.observe(section));
    observer.observe(document.getElementById('hero'));
  }

  /* ---------------------------------------------------------------- 二维码弹窗 */

  let qrLastFocus = null;

  function openQrModal() {
    if (!qrModal) return;
    qrLastFocus = document.activeElement;
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

  document.querySelectorAll('[data-qr-trigger]').forEach(trigger => {
    trigger.addEventListener('click', openQrModal);
  });

  if (qrModal) {
    qrModal.querySelectorAll('[data-qr-close]').forEach(el => {
      el.addEventListener('click', closeQrModal);
    });

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && !qrModal.hidden) closeQrModal();
    });
  }
})();
