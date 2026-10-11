/* OP-CO Marine — scroll motion & interactions (no dependencies) */
(() => {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const nav = $('#nav');
  const burger = $('#burger');
  const hero = $('.hero');
  const stage = $('#heroStage');
  const stmt = $('#statementText');
  const cards = $$('.card-s__in');
  const stack = $('.stack');
  let flat = false;
  const measure = () => {
    // Stacking only works if every card fits on screen; otherwise let them flow normally.
    flat = innerWidth <= 980 || cards.some(c => c.offsetHeight + 110 > innerHeight);
    stack && stack.classList.toggle('flat', flat);
    if (flat) cards.forEach(c => { c.style.transform = ''; c.style.filter = ''; });
  };
  const photo = $('#aboutPhoto img');
  const sections = $$('[data-nav]');
  const links = $$('.nav__links a[href^="#"]');

  /* ---------- Year ---------- */
  const yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();

  /* ---------- Mobile menu ---------- */
  const setMenu = open => {
    document.body.classList.toggle('nav-open', open);
    burger.setAttribute('aria-expanded', String(open));
    document.documentElement.style.overflow = open ? 'hidden' : '';
  };
  burger.addEventListener('click', () => setMenu(!document.body.classList.contains('nav-open')));
  links.forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });

  /* ---------- Reveal on scroll ---------- */
  const reveals = $$('[data-reveal]');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    }), { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    reveals.forEach(el => io.observe(el));
  } else reveals.forEach(el => el.classList.add('is-in'));

  /* ---------- Statement: words light up with scroll ---------- */
  let words = [];
  if (stmt) {
    words = stmt.textContent.trim().split(/\s+/).map(t => {
      const s = document.createElement('span'); s.className = 'w'; s.textContent = t; return s;
    });
    stmt.textContent = '';
    stmt.setAttribute('aria-label', words.map(w => w.textContent).join(' '));
    words.forEach((w, i) => { w.setAttribute('aria-hidden', 'true'); stmt.append(w, i < words.length - 1 ? ' ' : ''); });
    if (reduce) words.forEach(w => w.classList.add('on'));
  }

  /* ---------- Hero video (graceful: only shows if it plays) ---------- */
  const vid = $('#heroVideo');
  if (vid && !reduce) {
    vid.addEventListener('playing', () => vid.classList.add('is-playing'));
    const p = vid.play(); if (p && p.catch) p.catch(() => {});
  }

  /* ---------- Scroll loop ---------- */
  let ticking = false;
  const update = () => {
    ticking = false;
    const y = scrollY, vh = innerHeight;

    // nav theme: look at which section sits under the bar
    let theme = 'dark';
    for (const s of sections) {
      const r = s.getBoundingClientRect();
      if (r.top <= 26 && r.bottom > 26) { theme = s.dataset.nav; break; }
    }
    nav.classList.toggle('is-light', theme === 'light' && !document.body.classList.contains('nav-open'));

    // scrollspy
    let current = '#top';
    for (const a of links) {
      const t = $(a.getAttribute('href')); if (!t) continue;
      if (t.getBoundingClientRect().top <= vh * 0.4) current = a.getAttribute('href');
    }
    links.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === current));

    if (reduce) return;

    // hero: media recedes, copy lifts and fades
    if (hero && stage) {
      const p = clamp(y / (hero.offsetHeight - vh));
      stage.style.setProperty('--p', p.toFixed(4));
      stage.style.visibility = p >= 1 && y > hero.offsetHeight + 50 ? 'hidden' : '';
    }

    // statement words
    if (stmt && words.length) {
      const r = stmt.getBoundingClientRect();
      const p = clamp((vh * 0.78 - r.top) / (r.height + vh * 0.12));
      const n = Math.round(p * words.length * 1.06);
      words.forEach((w, i) => w.classList.toggle('on', i < n));
    }

    // services: previous cards ease back as the next one stacks on
    if (!flat) cards.forEach((c, i) => {
      const nextEl = cards[i + 1]; if (!nextEl) return;
      const stickTop = parseFloat(getComputedStyle(c.parentElement).top) || 0;
      const d = nextEl.getBoundingClientRect().top - (stickTop + 16);
      const p = clamp(1 - d / (c.offsetHeight * 0.9));
      c.style.transform = `scale(${(1 - p * 0.06).toFixed(4)})`;
      c.style.filter = `brightness(${(1 - p * 0.45).toFixed(3)})`;
    });

    // about photo: gentle parallax zoom
    if (photo) {
      const r = photo.parentElement.getBoundingClientRect();
      const p = clamp((vh - r.top) / (vh + r.height));
      photo.style.setProperty('--zoom', (1.12 - p * 0.09).toFixed(4));
    }
  };
  const req = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', () => { measure(); req(); });
  measure();
  update();

  /* ---------- Projects: filter + show more ---------- */
  const grid = $('#projGrid');
  if (grid) {
    const items = $$('.proj', grid);
    const chips = $$('.chip');
    const more = $('#moreBtn');
    const count = $('#moreCount');
    const LIMIT = 9;
    let cat = 'all', expanded = false;
    const render = () => {
      const match = items.filter(i => cat === 'all' || i.dataset.cat === cat);
      items.forEach(i => { i.classList.add('is-hidden'); i.classList.remove('is-in'); });
      match.forEach((i, idx) => {
        if (expanded || idx < LIMIT) {
          i.classList.remove('is-hidden');
          i.style.animationDelay = Math.min(idx * 40, 360) + 'ms';
          void i.offsetWidth; i.classList.add('is-in');
        }
      });
      const hidden = match.length - Math.min(match.length, expanded ? match.length : LIMIT);
      more.parentElement.style.display = hidden > 0 ? '' : 'none';
      count.textContent = match.length;
    };
    chips.forEach(c => c.addEventListener('click', () => {
      cat = c.dataset.cat; expanded = false;
      chips.forEach(x => x.setAttribute('aria-pressed', String(x === c)));
      render();
    }));
    more.addEventListener('click', () => { expanded = true; render(); });
    render();
  }

  /* ---------- Contact form → opens the visitor's email app ---------- */
  const form = $('#form');
  if (form) {
    const note = $('#formNote');
    form.addEventListener('submit', e => {
      e.preventDefault();
      const d = Object.fromEntries(new FormData(form));
      if (!d.name?.trim() || !/^\S+@\S+\.\S+$/.test(d.email || '') || !d.message?.trim()) {
        note.textContent = 'Please complete your name, a valid email and a message.'; return;
      }
      const subject = encodeURIComponent('Website enquiry from ' + d.name.trim());
      const body = encodeURIComponent(d.message.trim() + '\n\n— ' + d.name.trim() + '\n' + d.email.trim());
      location.href = 'mailto:Info@OP-CO.co.uk?subject=' + subject + '&body=' + body;
      note.textContent = 'Thanks for submitting! Your email app should open — or write to us at Info@OP-CO.co.uk.';
    });
  }
})();
