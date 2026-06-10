(function () {
  'use strict';

  // ── Navigation data ──────────────────────────────────────────────
  const NAV_LEVELS = {
    CP: {
      label: '🌱 CP',
      color: '#86efac',
      cats: [
        { label: '🔢 Nombres et calculs', color: '#86efac', pages: [
          { emoji: '🔢', title: 'Les nombres (jusqu\'à 100)', href: 'nombres-cp.html' },
          { emoji: '➕', title: 'Addition et soustraction',   href: 'calcul-cp.html' },
          { emoji: '⚡', title: 'Calcul mental',              href: 'calcul-mental-cp.html' },
        ]},
        { label: '📐 Mesures & géométrie', color: '#86efac', pages: [
          { emoji: '📏', title: 'Mesures & monnaie',          href: 'mesures-cp.html' },
          { emoji: '🔷', title: 'Les formes',                 href: 'geometrie-cp.html' },
          { emoji: '📊', title: 'Données',                    href: 'donnees-cp.html' },
          { emoji: '🧩', title: 'Résolution de problèmes',   href: 'problemes-cp.html' },
        ]},
        { label: '🏛️ Histoire & Géographie', color: '#86efac', pages: [
          { emoji: '🌍', title: 'Histoire & Géographie',      href: 'histoire-geo-cp.html' },
        ]},
        { label: '🏃 EPS', color: '#86efac', pages: [
          { emoji: '🏃', title: 'EPS — Éducation Physique',   href: 'eps-cycle2.html' },
        ]},
      ],
    },
    CE1: {
      label: '🌿 CE1',
      color: '#6ee7b7',
      cats: [
        { label: '🔢 Nombres et calculs', color: '#6ee7b7', pages: [
          { emoji: '🔢', title: 'Les nombres (jusqu\'à 1000)', href: 'nombres-ce1.html' },
          { emoji: '✂️', title: 'Introduction aux fractions',  href: 'fractions-ce1.html' },
          { emoji: '➕', title: 'Les opérations',              href: 'calcul-ce1.html' },
          { emoji: '⚡', title: 'Calcul mental',               href: 'calcul-mental-ce1.html' },
          { emoji: '🖊️', title: 'Opérations posées',           href: 'operations-posees-ce1.html' },
          { emoji: '✖️', title: 'Sens de la multiplication',   href: 'multiplication-ce1.html' },
        ]},
        { label: '📐 Mesures & géométrie', color: '#6ee7b7', pages: [
          { emoji: '📏', title: 'Mesures',                     href: 'mesures-ce1.html' },
          { emoji: '🔷', title: 'Géométrie',                   href: 'geometrie-ce1.html' },
          { emoji: '📊', title: 'Données',                     href: 'donnees-ce1.html' },
          { emoji: '🧩', title: 'Résolution de problèmes',    href: 'problemes-ce1.html' },
        ]},
        { label: '🏛️ Histoire & Géographie', color: '#6ee7b7', pages: [
          { emoji: '🏛️', title: 'Histoire & Géographie',      href: 'histoire-geo-ce1.html' },
        ]},
        { label: '🏃 EPS', color: '#6ee7b7', pages: [
          { emoji: '🏃', title: 'EPS — Éducation Physique',   href: 'eps-cycle2.html' },
        ]},
      ],
    },
    CE2: {
      label: '📚 CE2',
      color: '#a78bfa',
      cats: [
        { label: '🔢 Nombres et calculs', color: '#a78bfa', pages: [
          { emoji: '🔢', title: 'Les nombres entiers',        href: 'nombres.html' },
          { emoji: '🔣', title: 'Nombres décimaux',           href: 'decimaux-ce2.html' },
          { emoji: '✂️', title: 'Fractions — Je découpe',     href: 'fiche1.html' },
          { emoji: '📏', title: 'Fractions — Je compare',     href: 'fiche2.html' },
          { emoji: '🍎', title: 'Fractions — Je calcule',     href: 'fiche3.html' },
          { emoji: '➕', title: 'Les opérations',             href: 'calcul.html' },
          { emoji: '⚡', title: 'Calcul mental',              href: 'calcul-mental.html' },
          { emoji: '🧩', title: 'Problèmes',                  href: 'problemes.html' },
          { emoji: '🖊️', title: 'Opérations posées',          href: 'operations-posees-ce2.html' },
          { emoji: '✖️', title: 'Multiplication et division',  href: 'multiplication-division-ce2.html' },
          { emoji: '➗', title: 'Division euclidienne',         href: 'division-ce2.html' },
          { emoji: '🔢', title: 'Tables de multiplication',    href: 'tables-ce2.html' },
        ]},
        { label: '📐 Grandeurs et mesures', color: '#93c5fd', pages: [
          { emoji: '📏', title: 'Longueurs, masses, contenances', href: 'mesures.html' },
          { emoji: '🕐', title: 'Le temps et la monnaie',         href: 'temps.html' },
        ]},
        { label: '🔷 Espace et géométrie', color: '#6ee7b7', pages: [
          { emoji: '🔷', title: 'Géométrie plane', href: 'geometrie.html' },
          { emoji: '🎲', title: 'Les solides',     href: 'solides.html' },
          { emoji: '🪞', title: 'Symétrie axiale',  href: 'symetrie-ce2.html' },
        ]},
        { label: '📊 Organisation des données', color: '#fcd34d', pages: [
          { emoji: '📊', title: 'Tableaux et graphiques', href: 'donnees.html' },
        ]},
        { label: '🏛️ Histoire & Géographie', color: '#a78bfa', pages: [
          { emoji: '🏰', title: 'Histoire & Géographie',      href: 'histoire-geo-ce2.html' },
        ]},
        { label: '🏃 EPS', color: '#a78bfa', pages: [
          { emoji: '🏃', title: 'EPS — Éducation Physique',   href: 'eps-cycle2.html' },
        ]},
      ],
    },
    CM1: {
      label: '🎯 CM1',
      color: '#93c5fd',
      cats: [
        { label: '🔢 Nombres et calculs', color: '#93c5fd', pages: [
          { emoji: '🔢', title: 'Grands nombres (≤ 999 999)', href: 'nombres-cm1.html' },
          { emoji: '🔣', title: 'Nombres décimaux',           href: 'decimaux-cm1.html' },
          { emoji: '✂️', title: 'Fractions',                  href: 'fractions-cm1.html' },
          { emoji: '➕', title: 'Les 4 opérations',           href: 'calcul-cm1.html' },
          { emoji: '⚡', title: 'Calcul mental',              href: 'calcul-mental-cm1.html' },
          { emoji: '🖊️', title: 'Opérations posées',          href: 'calcul-pose-cm1.html' },
        ]},
        { label: '📐 Mesures & géométrie', color: '#93c5fd', pages: [
          { emoji: '📐', title: 'Périmètres et aires',        href: 'mesures-cm1.html' },
          { emoji: '⏱️', title: 'Durées et conversions',      href: 'temps-cm1.html' },
          { emoji: '🔷', title: 'Géométrie — angles',         href: 'geometrie-cm1.html' },
          { emoji: '📐', title: 'Les angles',                 href: 'angles-cm1.html' },
          { emoji: '🧊', title: 'Les solides',                href: 'solides-cm1.html' },
          { emoji: '📊', title: 'Données & statistiques',     href: 'donnees-cm1.html' },
          { emoji: '⚖️', title: 'Proportionnalité',           href: 'proportionnalite-cm1.html' },
          { emoji: '🧩', title: 'Résolution de problèmes',   href: 'problemes-cm1.html' },
        ]},
        { label: '🏛️ Histoire & Géographie', color: '#93c5fd', pages: [
          { emoji: '🏛️', title: 'Histoire & Géographie',      href: 'histoire-geo-cm1.html' },
        ]},
        { label: '🏃 EPS', color: '#93c5fd', pages: [
          { emoji: '🏆', title: 'EPS — Éducation Physique',   href: 'eps-cycle3.html' },
        ]},
      ],
    },
    CM2: {
      label: '🏆 CM2',
      color: '#fcd34d',
      cats: [
        { label: '🔢 Nombres et calculs', color: '#fcd34d', pages: [
          { emoji: '🔢', title: 'Très grands nombres',         href: 'nombres-cm2.html' },
          { emoji: '🔣', title: 'Décimaux avancés',            href: 'decimaux-cm2.html' },
          { emoji: '✂️', title: 'Fractions avancées',           href: 'fractions-cm2.html' },
          { emoji: '➕', title: 'Les 4 opérations avancées',   href: 'calcul-cm2.html' },
          { emoji: '⚡', title: 'Calcul mental',               href: 'calcul-mental-cm2.html' },
          { emoji: '🖊️', title: 'Opérations posées décimaux',  href: 'calcul-pose-cm2.html' },
          { emoji: '🧩', title: 'Problèmes',                   href: 'problemes-cm2.html' },
        ]},
        { label: '📐 Mesures & géométrie', color: '#fcd34d', pages: [
          { emoji: '📐', title: 'Aires et volumes',            href: 'mesures-cm2.html' },
          { emoji: '⏳', title: 'Durées et conversions',      href: 'temps-cm2.html' },
          { emoji: '🔷', title: 'Géométrie avancée',           href: 'geometrie-cm2.html' },
          { emoji: '📊', title: 'Statistiques & probabilités', href: 'donnees-cm2.html' },
          { emoji: '⚖️', title: 'Proportionnalité & %',        href: 'proportionnalite-cm2.html' },
        ]},
        { label: '🏛️ Histoire & Géographie', color: '#fcd34d', pages: [
          { emoji: '⚜️', title: 'Histoire & Géographie',      href: 'histoire-geo-cm2.html' },
        ]},
        { label: '🏃 EPS', color: '#fcd34d', pages: [
          { emoji: '🏆', title: 'EPS — Éducation Physique',   href: 'eps-cycle3.html' },
        ]},
      ],
    },
    '6e': {
      label: '⭐ 6ème',
      color: '#f9a8d4',
      cats: [
        { label: '🔢 Nombres et calculs', color: '#f9a8d4', pages: [
          { emoji: '🔢', title: 'Nombres et relatifs',         href: 'nombres-6e.html' },
          { emoji: '✂️', title: 'Fractions & quotients',        href: 'fractions-6e.html' },
          { emoji: '📘', title: 'Algèbre — introduction',       href: 'algebre-6e.html' },
          { emoji: '⚡', title: 'Calcul mental',               href: 'calcul-mental-6e.html' },
          { emoji: '🎲', title: 'Probabilités',                href: 'probabilites-6e.html' },
        ]},
        { label: '📐 Mesures & géométrie', color: '#f9a8d4', pages: [
          { emoji: '🔷', title: 'Géométrie',                   href: 'geometrie-6e.html' },
          { emoji: '📐', title: 'Aires et volumes',            href: 'mesures-6e.html' },
          { emoji: '📊', title: 'Statistiques',                href: 'donnees-6e.html' },
          { emoji: '⚖️', title: 'Proportionnalité & %',        href: 'proportionnalite-6e.html' },
        ]},
        { label: '🏛️ Histoire & Géographie', color: '#f9a8d4', pages: [
          { emoji: '🌍', title: 'Histoire & Géographie',      href: 'histoire-geo-6e.html' },
        ]},
        { label: '🏃 EPS', color: '#f9a8d4', pages: [
          { emoji: '🏆', title: 'EPS — Éducation Physique',   href: 'eps-cycle3.html' },
        ]},
      ],
    },
  };

  const LEVEL_ORDER = ['CP','CE1','CE2','CM1','CM2','6e'];

  const current = window.location.pathname.split('/').pop() || 'index.html';

  // detect which level the current page belongs to
  function detectCurrentLevel() {
    for (const lvKey of LEVEL_ORDER) {
      for (const cat of NAV_LEVELS[lvKey].cats) {
        if (cat.pages.some(p => p.href === current)) return lvKey;
      }
    }
    return null;
  }

  // get user's profile level (from GS if loaded)
  function getUserLevel() {
    try {
      const gs = window.GS;
      if (gs) {
        const cl = gs.profile().classe;
        if (LEVEL_ORDER.includes(cl)) return cl;
      }
    } catch(e) {}
    return 'CE2';
  }

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

    /* ===== LEVEL TABS ===== */
    .nav-level-tabs {
      display: flex;
      gap: 5px;
      padding: 8px 10px 6px;
      overflow-x: auto;
      flex-shrink: 0;
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .nav-level-tabs::-webkit-scrollbar { display: none; }
    .nav-level-tab {
      flex-shrink: 0;
      background: rgba(255,255,255,0.07);
      border: 1.5px solid rgba(255,255,255,0.15);
      border-radius: 20px;
      padding: 5px 11px;
      font-size: 0.72rem;
      font-weight: 900;
      color: rgba(255,255,255,0.6);
      cursor: pointer;
      transition: background 0.15s, color 0.15s, border-color 0.15s;
      font-family: inherit;
      white-space: nowrap;
    }
    .nav-level-tab:hover { background: rgba(255,255,255,0.15); color: white; }
    .nav-level-tab.active {
      background: rgba(255,255,255,0.22);
      border-color: rgba(255,255,255,0.45);
      color: white;
    }
    .nav-level-section { display: none; }
    .nav-level-section.visible { display: block; }

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
      <span>🌟</span><span>École Facile</span>
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

  // ── Level tabs ─────────────────────────────────────────────────────
  const pageLevel = detectCurrentLevel();
  let activeLevel = pageLevel || getUserLevel();

  const tabsRow = document.createElement('div');
  tabsRow.className = 'nav-level-tabs';
  LEVEL_ORDER.forEach(lvKey => {
    const tab = document.createElement('button');
    tab.className = 'nav-level-tab' + (lvKey === activeLevel ? ' active' : '');
    tab.textContent = NAV_LEVELS[lvKey].label;
    tab.style.setProperty('border-color', lvKey === activeLevel ? NAV_LEVELS[lvKey].color : '');
    tab.style.setProperty('color', lvKey === activeLevel ? NAV_LEVELS[lvKey].color : '');
    tab.addEventListener('click', () => selectLevel(lvKey));
    tabsRow.appendChild(tab);
  });
  body.appendChild(tabsRow);

  // ── Level sections ─────────────────────────────────────────────────
  const levelSections = {};
  LEVEL_ORDER.forEach(lvKey => {
    const lvData = NAV_LEVELS[lvKey];
    const section = document.createElement('div');
    section.className = 'nav-level-section' + (lvKey === activeLevel ? ' visible' : '');
    section.dataset.level = lvKey;

    lvData.cats.forEach(cat => {
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

      catDiv.querySelector('.nav-cat-btn').addEventListener('click', () => {
        const isOpen = catDiv.classList.contains('open');
        section.querySelectorAll('.nav-cat').forEach(c => c.classList.remove('open'));
        section.querySelectorAll('.nav-cat-btn').forEach(b => b.setAttribute('aria-expanded', 'false'));
        if (!isOpen) {
          catDiv.classList.add('open');
          catDiv.querySelector('.nav-cat-btn').setAttribute('aria-expanded', 'true');
        }
      });

      section.appendChild(catDiv);
    });

    levelSections[lvKey] = section;
    body.appendChild(section);
  });

  function selectLevel(lvKey) {
    activeLevel = lvKey;
    tabsRow.querySelectorAll('.nav-level-tab').forEach((tab, i) => {
      const k = LEVEL_ORDER[i];
      const isActive = k === lvKey;
      tab.classList.toggle('active', isActive);
      tab.style.setProperty('border-color', isActive ? NAV_LEVELS[k].color : '');
      tab.style.setProperty('color', isActive ? NAV_LEVELS[k].color : '');
    });
    Object.entries(levelSections).forEach(([k, s]) => {
      s.classList.toggle('visible', k === lvKey);
    });
  }

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
    // re-sync level tab to user's profile if no page-based level detected
    if (!pageLevel) {
      const ul = getUserLevel();
      if (ul !== activeLevel) selectLevel(ul);
    }
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
