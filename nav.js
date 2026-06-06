(function () {
  'use strict';

  // ── Navigation data ──────────────────────────────────────────────
  const NAV = [
    {
      label: '🔢 Nombres et calculs',
      color: '#a78bfa',
      pages: [
        { emoji: '🔢', title: 'Les nombres entiers',        href: 'nombres.html' },
        { emoji: '✂️', title: 'Fractions — Je découpe',     href: 'fiche1.html' },
        { emoji: '📏', title: 'Fractions — Je compare',     href: 'fiche2.html' },
        { emoji: '🍎', title: 'Fractions — Je calcule',     href: 'fiche3.html' },
        { emoji: '➕', title: 'Les opérations',             href: 'calcul.html' },
        { emoji: '⚡', title: 'Calcul mental',              href: 'calcul-mental.html' },
        { emoji: '🧩', title: 'Problèmes',                  href: 'problemes.html' },
      ],
    },
    {
      label: '📐 Grandeurs et mesures',
      color: '#93c5fd',
      pages: [
        { emoji: '📏', title: 'Longueurs, masses, contenances', href: 'mesures.html' },
        { emoji: '🕐', title: 'Le temps et la monnaie',         href: 'temps.html' },
      ],
    },
    {
      label: '🔷 Espace et géométrie',
      color: '#6ee7b7',
      pages: [
        { emoji: '🔷', title: 'Géométrie plane', href: 'geometrie.html' },
        { emoji: '🎲', title: 'Les solides',     href: 'solides.html' },
      ],
    },
    {
      label: '📊 Organisation des données',
      color: '#fcd34d',
      pages: [
        { emoji: '📊', title: 'Tableaux et graphiques', href: 'donnees.html' },
      ],
    },
  ];

  const current = window.location.pathname.split('/').pop() || 'index.html';

  // ── Styles ───────────────────────────────────────────────────────
  const css = `
    /* ===== NAV TOGGLE BUTTON ===== */
    .nav-toggle {
      position: fixed;
      top: 14px;
      right: 14px;
      z-index: 1200;
      width: 46px;
      height: 46px;
      background: rgba(255,255,255,0.22);
      border: 2px solid rgba(255,255,255,0.45);
      border-radius: 12px;
      color: white;
      font-size: 1.35rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s, transform 0.15s;
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      flex-shrink: 0;
    }
    .nav-toggle:hover { background: rgba(255,255,255,0.38); }
    .nav-toggle.is-open { transform: rotate(90deg); }

    /* ===== OVERLAY ===== */
    .nav-overlay {
      position: fixed;
      inset: 0;
      background: rgba(15,10,40,0.52);
      z-index: 1210;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.24s;
    }
    .nav-overlay.open {
      opacity: 1;
      pointer-events: all;
    }

    /* ===== DRAWER ===== */
    .nav-drawer {
      position: fixed;
      top: 0;
      left: 0;
      width: 310px;
      max-width: 88vw;
      height: 100%;
      height: 100dvh;
      background: linear-gradient(170deg, #1e1b4b 0%, #312e81 50%, #1e3a5f 100%);
      z-index: 1220;
      transform: translateX(-100%);
      transition: transform 0.28s cubic-bezier(0.4,0,0.2,1);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .nav-drawer.open {
      transform: translateX(0);
    }
    .nav-drawer-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 14px;
      background: rgba(0,0,0,0.25);
      position: sticky;
      top: 0;
      flex-shrink: 0;
    }
    .nav-drawer-home {
      display: flex;
      align-items: center;
      gap: 9px;
      text-decoration: none;
      color: white;
      font-size: 0.95rem;
      font-weight: 900;
    }
    .nav-drawer-home:hover { opacity: 0.85; }
    .nav-close-btn {
      background: rgba(255,255,255,0.12);
      border: 1.5px solid rgba(255,255,255,0.25);
      color: white;
      border-radius: 8px;
      width: 34px;
      height: 34px;
      font-size: 1.1rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.15s;
      flex-shrink: 0;
      line-height: 1;
    }
    .nav-close-btn:hover { background: rgba(255,255,255,0.25); }

    .nav-body {
      overflow-y: auto;
      flex: 1;
      padding: 8px 0 24px;
    }
    .nav-body::-webkit-scrollbar { width: 4px; }
    .nav-body::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 2px; }

    /* Home link */
    .nav-home-item {
      margin: 6px 10px;
    }
    .nav-home-item a {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 12px;
      color: rgba(255,255,255,0.85);
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 800;
      border-radius: 10px;
      transition: background 0.15s, color 0.15s;
    }
    .nav-home-item a:hover,
    .nav-home-item a.active { background: rgba(255,255,255,0.15); color: white; }

    /* Category */
    .nav-cat {
      margin: 10px 10px 2px;
    }
    .nav-cat-btn {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      background: none;
      border: none;
      padding: 9px 12px;
      border-radius: 10px;
      cursor: pointer;
      transition: background 0.15s;
      gap: 8px;
    }
    .nav-cat-btn:hover { background: rgba(255,255,255,0.08); }
    .nav-cat-label {
      font-size: 0.82rem;
      font-weight: 900;
      letter-spacing: 0.4px;
      text-align: left;
      flex: 1;
    }
    .nav-cat-arrow {
      font-size: 0.75rem;
      color: rgba(255,255,255,0.5);
      transition: transform 0.22s;
      flex-shrink: 0;
    }
    .nav-cat.open .nav-cat-arrow { transform: rotate(180deg); }

    /* Pages list */
    .nav-pages {
      overflow: hidden;
      max-height: 0;
      transition: max-height 0.26s ease;
    }
    .nav-cat.open .nav-pages {
      max-height: 500px;
    }
    .nav-page-link {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 9px 12px 9px 22px;
      color: rgba(255,255,255,0.7);
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 700;
      border-radius: 8px;
      margin: 2px 8px;
      transition: background 0.15s, color 0.15s;
      line-height: 1.3;
    }
    .nav-page-link:hover { background: rgba(255,255,255,0.12); color: white; }
    .nav-page-link.active {
      background: rgba(255,255,255,0.18);
      color: white;
    }
    .nav-page-link.active::before {
      content: '';
      display: block;
      width: 3px;
      height: 100%;
      border-radius: 2px;
      position: absolute;
      left: 8px;
    }
    .nav-page-link { position: relative; }
    .nav-pg-emoji { font-size: 0.95rem; flex-shrink: 0; }

    /* Divider */
    .nav-divider {
      margin: 8px 14px;
      border: none;
      border-top: 1px solid rgba(255,255,255,0.1);
    }

    /* ===== PROFILE FOOTER ===== */
    .nav-profile-footer {
      flex-shrink: 0;
      border-top: 1px solid rgba(255,255,255,0.14);
      background: rgba(0,0,0,0.28);
    }
    .nav-profile-link {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      padding: 16px 16px 10px;
      text-decoration: none;
      color: white;
      transition: background 0.15s;
    }
    .nav-profile-link:hover { background: rgba(255,255,255,0.07); }
    .nav-profile-avatar {
      font-size: 2.8rem;
      flex-shrink: 0;
      line-height: 1;
      filter: drop-shadow(0 2px 6px rgba(0,0,0,0.3));
    }
    .nav-profile-info {
      flex: 1;
      min-width: 0;
      padding-top: 2px;
    }
    .nav-profile-name {
      font-size: 1.05rem;
      font-weight: 900;
      color: white;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 2px;
    }
    .nav-profile-level {
      font-size: 0.78rem;
      font-weight: 700;
      color: #c4b5fd;
      margin-bottom: 7px;
    }
    .nav-profile-xprow {
      display: flex;
      align-items: center;
      gap: 7px;
    }
    .nav-profile-xpbar {
      flex: 1;
      height: 7px;
      background: rgba(255,255,255,0.15);
      border-radius: 4px;
      overflow: hidden;
    }
    .nav-profile-xpfill {
      height: 100%;
      background: linear-gradient(90deg, #a78bfa, #60a5fa);
      border-radius: 4px;
      transition: width 0.5s ease;
    }
    .nav-profile-xpnum {
      font-size: 0.72rem;
      font-weight: 900;
      color: #a78bfa;
      white-space: nowrap;
      flex-shrink: 0;
    }
    .nav-profile-xpleft {
      font-size: 0.68rem;
      font-weight: 700;
      color: rgba(255,255,255,0.38);
      margin-top: 3px;
    }
    .nav-profile-stats {
      display: flex;
      border-top: 1px solid rgba(255,255,255,0.08);
      margin: 0 10px 10px;
    }
    .nav-profile-stat {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 10px 6px 8px;
      gap: 2px;
    }
    .nav-profile-stat-val {
      font-size: 1.1rem;
      font-weight: 900;
      color: white;
    }
    .nav-profile-stat-lbl {
      font-size: 0.65rem;
      font-weight: 700;
      color: rgba(255,255,255,0.45);
      text-transform: uppercase;
      letter-spacing: 0.3px;
      text-align: center;
    }

    /* ===== DESKTOP: menu bar ===== */
    @media (min-width: 768px) {
      /* Slightly bigger drawer on desktop */
      .nav-drawer { width: 300px; }
    }
  `;

  const styleEl = document.createElement('style');
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  // ── Build HTML ───────────────────────────────────────────────────
  // Toggle button
  const toggleBtn = document.createElement('button');
  toggleBtn.className = 'nav-toggle';
  toggleBtn.setAttribute('aria-label', 'Ouvrir le menu');
  toggleBtn.innerHTML = '☰';
  document.body.appendChild(toggleBtn);

  // Overlay
  const overlay = document.createElement('div');
  overlay.className = 'nav-overlay';
  document.body.appendChild(overlay);

  // Drawer
  const drawer = document.createElement('nav');
  drawer.className = 'nav-drawer';
  drawer.setAttribute('aria-label', 'Navigation');

  // Drawer header
  const drawerHeader = document.createElement('div');
  drawerHeader.className = 'nav-drawer-header';
  drawerHeader.innerHTML = `
    <a href="index.html" class="nav-drawer-home" onclick="closeNav()">
      <span>🌟</span><span>Les Maths de Clémence</span>
    </a>
    <button class="nav-close-btn" onclick="closeNav()" aria-label="Fermer">✕</button>
  `;
  drawer.appendChild(drawerHeader);

  // Drawer body
  const body = document.createElement('div');
  body.className = 'nav-body';

  // Home link
  const homeItem = document.createElement('div');
  homeItem.className = 'nav-home-item';
  homeItem.innerHTML = `
    <a href="index.html" ${current === 'index.html' ? 'class="active"' : ''}>
      🏠 Accueil — toutes les matières
    </a>
  `;
  body.appendChild(homeItem);

  const div0 = document.createElement('hr');
  div0.className = 'nav-divider';
  body.appendChild(div0);

  // Categories
  let activeCategory = null;
  NAV.forEach((cat, catIdx) => {
    const catDiv = document.createElement('div');
    catDiv.className = 'nav-cat';

    const hasActivePage = cat.pages.some(p => p.href === current);
    if (hasActivePage) catDiv.classList.add('open');

    catDiv.innerHTML = `
      <button class="nav-cat-btn" aria-expanded="${hasActivePage}">
        <span class="nav-cat-label" style="color: ${cat.color};">${cat.label}</span>
        <span class="nav-cat-arrow">▼</span>
      </button>
      <div class="nav-pages">
        ${cat.pages.map(p => `
          <a href="${p.href}"
             class="nav-page-link${p.href === current ? ' active' : ''}"
             onclick="closeNav()">
            <span class="nav-pg-emoji">${p.emoji}</span>
            <span>${p.title}</span>
          </a>
        `).join('')}
      </div>
    `;

    // Toggle accordion
    catDiv.querySelector('.nav-cat-btn').addEventListener('click', () => {
      const isOpen = catDiv.classList.contains('open');
      // Close all
      document.querySelectorAll('.nav-cat').forEach(c => c.classList.remove('open'));
      document.querySelectorAll('.nav-cat-btn').forEach(b => b.setAttribute('aria-expanded', 'false'));
      // Toggle
      if (!isOpen) {
        catDiv.classList.add('open');
        catDiv.querySelector('.nav-cat-btn').setAttribute('aria-expanded', 'true');
      }
    });

    body.appendChild(catDiv);
  });

  // ── Profile footer ────────────────────────────────────────────────
  const profileFooter = document.createElement('div');
  profileFooter.className = 'nav-profile-footer';

  function renderProfileFooter() {
    const gs = window.GS;
    if (!gs) {
      profileFooter.innerHTML = `<a href="profile.html" class="nav-profile-link" onclick="closeNav()">👤 Mon profil</a>`;
      return;
    }
    const p = gs.profile();
    const lv = gs.getLevel(p.xp);
    const nx = gs.getNextLevel(p.xp);
    const xpPct = nx ? Math.round(((p.xp - lv.xp) / (nx.xp - lv.xp)) * 100) : 100;
    const xpLeft = nx ? (nx.xp - p.xp) + ' XP pour le niveau suivant' : 'Niveau max atteint !';
    profileFooter.innerHTML = `
      <a href="profile.html" class="nav-profile-link" onclick="closeNav()">
        <span class="nav-profile-avatar">${p.avatar || '⭐'}</span>
        <div class="nav-profile-info">
          <div class="nav-profile-name">${p.name || 'Clémence'}</div>
          <div class="nav-profile-level">${lv.emoji} ${lv.title} &mdash; Niveau ${p.level}</div>
          <div class="nav-profile-xprow">
            <div class="nav-profile-xpbar"><div class="nav-profile-xpfill" style="width:${xpPct}%"></div></div>
            <span class="nav-profile-xpnum">${p.xp} XP</span>
          </div>
          <div class="nav-profile-xpleft">${xpLeft}</div>
        </div>
      </a>
      <div class="nav-profile-stats">
        <div class="nav-profile-stat"><span class="nav-profile-stat-val">${p.tot}</span><span class="nav-profile-stat-lbl">réponses</span></div>
        <div class="nav-profile-stat"><span class="nav-profile-stat-val">${p.badges.length}</span><span class="nav-profile-stat-lbl">badges</span></div>
        <div class="nav-profile-stat"><span class="nav-profile-stat-val">${p.maxStreak > 0 ? '🔥' : '—'}${p.maxStreak > 0 ? p.maxStreak : ''}</span><span class="nav-profile-stat-lbl">meilleure série</span></div>
      </div>
    `;
  }

  renderProfileFooter();

  drawer.appendChild(body);
  drawer.appendChild(profileFooter);
  document.body.appendChild(drawer);

  // ── Open / Close ─────────────────────────────────────────────────
  function openNav() {
    renderProfileFooter();
    drawer.classList.add('open');
    overlay.classList.add('open');
    toggleBtn.classList.add('is-open');
    toggleBtn.setAttribute('aria-label', 'Fermer le menu');
    document.body.style.overflow = 'hidden';
  }

  function closeNav() {
    drawer.classList.remove('open');
    overlay.classList.remove('open');
    toggleBtn.classList.remove('is-open');
    toggleBtn.setAttribute('aria-label', 'Ouvrir le menu');
    document.body.style.overflow = '';
  }

  // Expose closeNav globally (used in inline onclick)
  window.closeNav = closeNav;

  toggleBtn.addEventListener('click', () => {
    drawer.classList.contains('open') ? closeNav() : openNav();
  });
  overlay.addEventListener('click', closeNav);

  // Close on Escape
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeNav();
  });

})();
