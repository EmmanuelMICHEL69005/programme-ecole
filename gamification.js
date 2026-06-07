/* ============================================================
   GAMIFICATION — Les Maths de Clémence
   XP · Niveaux · Badges · Toasts · Confetti
   Multi-profils · Classes scolaires · Leçon suivante
   ============================================================ */
(function () {
  'use strict';

  // ── Config ───────────────────────────────────────────────────────
  const STORE_KEY  = 'clemence_maths_v2';
  const LEGACY_KEY = 'clemence_maths_v1';
  const XP_CORRECT = 10;

  const PAGE_SEQUENCE = [
    // CP
    'nombres-cp.html','calcul-cp.html','calcul-mental-cp.html','mesures-cp.html','geometrie-cp.html','donnees-cp.html',
    // CE1
    'nombres-ce1.html','fractions-ce1.html','calcul-ce1.html','calcul-mental-ce1.html','mesures-ce1.html','geometrie-ce1.html','donnees-ce1.html',
    // CE2
    'nombres.html','fiche1.html','fiche2.html','fiche3.html',
    'calcul.html','calcul-mental.html','problemes.html',
    'mesures.html','temps.html','geometrie.html','solides.html','donnees.html',
    // CM1
    'nombres-cm1.html','decimaux-cm1.html','fractions-cm1.html','calcul-cm1.html','calcul-mental-cm1.html','calcul-pose-cm1.html','mesures-cm1.html','geometrie-cm1.html','donnees-cm1.html','proportionnalite-cm1.html',
    // CM2
    'nombres-cm2.html','decimaux-cm2.html','fractions-cm2.html','calcul-cm2.html','calcul-mental-cm2.html','calcul-pose-cm2.html','mesures-cm2.html','geometrie-cm2.html','donnees-cm2.html','proportionnalite-cm2.html','problemes-cm2.html',
    // 6e
    'nombres-6e.html','fractions-6e.html','algebre-6e.html','geometrie-6e.html','mesures-6e.html','donnees-6e.html','proportionnalite-6e.html',
  ];
  const NEXT_LESSON_THRESHOLD = 5;
  const CLASSE_LIST = ['CP','CE1','CE2','CM1','CM2','6e'];
  const AVATARS = ['🌟','⭐','🦋','🌈','🦄','🐱','🐼','🐸','🦊','🐢','🌺','🍭','🎀','🚀','⚡','🎯','🏆','💎','🌙','🦸‍♀️'];

  const LEVELS = [
    { n:1, xp:0,    title:'Apprentie',       emoji:'🌱' },
    { n:2, xp:120,  title:'Exploratrice',    emoji:'🔭' },
    { n:3, xp:350,  title:'Calculatrice',    emoji:'🧮' },
    { n:4, xp:750,  title:'Géomètre',        emoji:'📐' },
    { n:5, xp:1400, title:'Mathématicienne', emoji:'🏆' },
    { n:6, xp:2300, title:'Experte',         emoji:'⭐' },
    { n:7, xp:3500, title:'Championne',      emoji:'🥇' },
    { n:8, xp:5000, title:'Légende',         emoji:'🌟' },
  ];

  const BADGES = [
    { id:'first',     emoji:'👣', name:'Premier pas !',      desc:'1ère bonne réponse',              check: p => p.tot >= 1 },
    { id:'hot3',      emoji:'🔥', name:'En feu !',           desc:'3 bonnes réponses de suite',      check: p => p.maxStreak >= 3 },
    { id:'hot5',      emoji:'⚡', name:'Inarrêtable !',      desc:'5 de suite',                      check: p => p.maxStreak >= 5 },
    { id:'hot10',     emoji:'🌪️',name:'Tornade !',          desc:'10 de suite',                     check: p => p.maxStreak >= 10 },
    { id:'c10',       emoji:'🚀', name:'Décollage !',        desc:'10 bonnes réponses',              check: p => p.tot >= 10 },
    { id:'c25',       emoji:'💪', name:'Costaude !',         desc:'25 bonnes réponses',              check: p => p.tot >= 25 },
    { id:'c50',       emoji:'🦸‍♀️',name:'Super héroïne',   desc:'50 bonnes réponses',              check: p => p.tot >= 50 },
    { id:'c100',      emoji:'💯', name:'Centenaire !',       desc:'100 bonnes réponses',             check: p => p.tot >= 100 },
    { id:'lv3',       emoji:'🧮', name:'Calculatrice',       desc:'Niveau 3 atteint',                check: p => p.level >= 3 },
    { id:'lv5',       emoji:'🏆', name:'Mathématicienne',    desc:'Niveau 5 atteint',                check: p => p.level >= 5 },
    { id:'fractions', emoji:'🍕', name:'Reine des fractions',desc:'Terminer les 3 fiches fractions', check: p => ['fiche1.html','fiche2.html','fiche3.html'].every(f => (p.pages[f]||0) >= 3) },
    { id:'geometry',  emoji:'🔷', name:'Architecte',         desc:'Compléter géométrie + solides',   check: p => (p.pages['geometrie.html']||0) >= 3 && (p.pages['solides.html']||0) >= 3 },
    { id:'allTopics', emoji:'🌈', name:'Programme complet !',desc:'Visiter 10 thèmes différents',    check: p => Object.keys(p.pages).filter(k => (p.pages[k]||0) >= 1).length >= 10 },
    { id:'mentalMath',emoji:'🧠', name:'Calcul éclair',      desc:'20 bonnes en calcul mental',      check: p => (p.pages['calcul-mental.html']||0) >= 20 },
    { id:'earlyBird', emoji:'🌅', name:'Lève-tôt',           desc:'Réviser avant 8h',                check: () => new Date().getHours() < 8 },
    { id:'nightOwl',  emoji:'🦉', name:'Chouette studieuse', desc:'Réviser après 21h',               check: () => new Date().getHours() >= 21 },
    { id:'consistent',emoji:'📅', name:'Assidue !',          desc:'Revenir 3 jours différents',      check: p => (p.days||[]).length >= 3 },
  ];

  const PAGE_LABELS = {
    'index.html':                  { title:'Accueil',                      emoji:'🏠' },
    // CP
    'nombres-cp.html':             { title:'Nombres CP',                   emoji:'🔢' },
    'calcul-cp.html':              { title:'Calcul CP',                    emoji:'➕' },
    'calcul-mental-cp.html':       { title:'Calcul mental CP',             emoji:'⚡' },
    'mesures-cp.html':             { title:'Mesures CP',                   emoji:'📏' },
    'geometrie-cp.html':           { title:'Géométrie CP',                 emoji:'🔷' },
    'donnees-cp.html':             { title:'Données CP',                   emoji:'📊' },
    // CE1
    'nombres-ce1.html':            { title:'Nombres CE1',                  emoji:'🔢' },
    'fractions-ce1.html':          { title:'Fractions CE1',                emoji:'✂️' },
    'calcul-ce1.html':             { title:'Calcul CE1',                   emoji:'➕' },
    'calcul-mental-ce1.html':      { title:'Calcul mental CE1',            emoji:'⚡' },
    'mesures-ce1.html':            { title:'Mesures CE1',                  emoji:'📏' },
    'geometrie-ce1.html':          { title:'Géométrie CE1',                emoji:'🔷' },
    'donnees-ce1.html':            { title:'Données CE1',                  emoji:'📊' },
    // CE2
    'nombres.html':                { title:'Nombres entiers CE2',          emoji:'🔢' },
    'fiche1.html':                 { title:'Fractions — découpe',          emoji:'✂️' },
    'fiche2.html':                 { title:'Fractions — compare',          emoji:'📏' },
    'fiche3.html':                 { title:'Fractions — calcule',          emoji:'🍎' },
    'calcul.html':                 { title:'Les opérations CE2',           emoji:'➕' },
    'calcul-mental.html':          { title:'Calcul mental CE2',            emoji:'⚡' },
    'problemes.html':              { title:'Problèmes CE2',                emoji:'🧩' },
    'mesures.html':                { title:'Mesures CE2',                  emoji:'📏' },
    'temps.html':                  { title:'Temps & monnaie CE2',          emoji:'🕐' },
    'geometrie.html':              { title:'Géométrie plane CE2',          emoji:'🔷' },
    'solides.html':                { title:'Les solides CE2',              emoji:'🎲' },
    'donnees.html':                { title:'Données CE2',                  emoji:'📊' },
    // CM1
    'nombres-cm1.html':            { title:'Nombres CM1',                  emoji:'🔢' },
    'decimaux-cm1.html':           { title:'Décimaux CM1',                 emoji:'🔣' },
    'fractions-cm1.html':          { title:'Fractions CM1',                emoji:'✂️' },
    'calcul-cm1.html':             { title:'Calcul CM1',                   emoji:'➕' },
    'calcul-mental-cm1.html':      { title:'Calcul mental CM1',            emoji:'⚡' },
    'calcul-pose-cm1.html':        { title:'Opérations posées CM1',        emoji:'🖊️' },
    'mesures-cm1.html':            { title:'Périmètres & Aires CM1',       emoji:'📐' },
    'geometrie-cm1.html':          { title:'Géométrie CM1',                emoji:'🔷' },
    'donnees-cm1.html':            { title:'Données CM1',                  emoji:'📊' },
    'proportionnalite-cm1.html':   { title:'Proportionnalité CM1',         emoji:'⚖️' },
    // CM2
    'nombres-cm2.html':            { title:'Nombres CM2',                  emoji:'🔢' },
    'decimaux-cm2.html':           { title:'Décimaux CM2',                 emoji:'🔣' },
    'fractions-cm2.html':          { title:'Fractions CM2',                emoji:'✂️' },
    'calcul-cm2.html':             { title:'Calcul CM2',                   emoji:'➕' },
    'calcul-mental-cm2.html':      { title:'Calcul mental CM2',            emoji:'⚡' },
    'calcul-pose-cm2.html':        { title:'Opérations posées CM2',        emoji:'🖊️' },
    'mesures-cm2.html':            { title:'Aires & Volumes CM2',          emoji:'📐' },
    'geometrie-cm2.html':          { title:'Géométrie CM2',                emoji:'🔷' },
    'donnees-cm2.html':            { title:'Statistiques CM2',             emoji:'📊' },
    'proportionnalite-cm2.html':   { title:'Proportionnalité CM2',         emoji:'⚖️' },
    'problemes-cm2.html':          { title:'Problèmes CM2',                emoji:'🧩' },
    // 6e
    'nombres-6e.html':             { title:'Nombres 6e',                   emoji:'🔢' },
    'fractions-6e.html':           { title:'Fractions 6e',                 emoji:'✂️' },
    'algebre-6e.html':             { title:'Algèbre 6e',                   emoji:'📘' },
    'geometrie-6e.html':           { title:'Géométrie 6e',                 emoji:'🔷' },
    'mesures-6e.html':             { title:'Aires & Volumes 6e',           emoji:'📐' },
    'donnees-6e.html':             { title:'Statistiques 6e',              emoji:'📊' },
    'proportionnalite-6e.html':    { title:'Proportionnalité 6e',          emoji:'⚖️' },
  };

  // ── Store helpers ────────────────────────────────────────────────
  function genId() {
    return 'p' + Date.now().toString(36) + Math.random().toString(36).slice(2,6);
  }

  function blank(name, avatar, classe) {
    const id = genId();
    return {
      id, name: name||'', avatar: avatar||'🌟', classe: classe||'CE2',
      xp:0, level:1, badges:[], tot:0, streak:0, maxStreak:0,
      pages:{}, days:[], createdAt: Date.now()
    };
  }

  let store;
  let P;

  function loadStore() {
    try {
      const raw = localStorage.getItem(STORE_KEY);
      if (raw) {
        store = JSON.parse(raw);
        P = store.profiles[store.active] || null;
        if (!P) {
          const ids = Object.keys(store.profiles||{});
          if (ids.length) { store.active = ids[0]; P = store.profiles[ids[0]]; }
        }
        return;
      }
    } catch(e) {}
    // Migrate v1
    try {
      const oldRaw = localStorage.getItem(LEGACY_KEY);
      if (oldRaw) {
        const old = JSON.parse(oldRaw);
        const p = blank(old.name||'Clémence', old.avatar||'🌟', 'CE2');
        Object.assign(p, {
          xp: old.xp||0, level: old.level||1, badges: old.badges||[],
          tot: old.tot||0, streak: old.streak||0, maxStreak: old.maxStreak||0,
          pages: old.pages||{}, days: old.days||[]
        });
        store = { active: p.id, profiles: { [p.id]: p } };
        saveStore();
        P = p;
        return;
      }
    } catch(e) {}
    store = { active: null, profiles: {} };
    P = null;
  }

  function saveStore() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(store)); } catch(e) {}
  }

  function save() {
    if (!P) return;
    const today = new Date().toISOString().slice(0,10);
    if (!P.days) P.days = [];
    if (!P.days.includes(today)) P.days.push(today);
    saveStore();
  }

  // ── Level helpers ─────────────────────────────────────────────────
  function getLevel(xp) {
    let cur = LEVELS[0];
    for (const l of LEVELS) { if (xp >= l.xp) cur = l; else break; }
    return cur;
  }
  function getNextLevel(xp) {
    for (const l of LEVELS) { if (xp < l.xp) return l; }
    return null;
  }
  function pct(xp) {
    const cur = getLevel(xp), nxt = getNextLevel(xp);
    if (!nxt) return 100;
    return Math.min(100, Math.round((xp - cur.xp) / (nxt.xp - cur.xp) * 100));
  }

  // ── Core: award XP ───────────────────────────────────────────────
  const page = window.location.pathname.split('/').pop() || 'index.html';
  let pageSessionCorrect = 0;
  let pageSessionAnswered = 0;
  let nextLessonShown = false;

  function award(xp) {
    if (!P) return;
    const oldLevel = getLevel(P.xp);
    P.xp  += xp;
    P.tot += 1;
    P.streak++;
    if (P.streak > P.maxStreak) P.maxStreak = P.streak;
    P.pages[page] = (P.pages[page] || 0) + 1;
    P.level = getLevel(P.xp).n;
    pageSessionCorrect++;
    pageSessionAnswered++;

    save();
    const newBadges = checkBadges();
    const newLevel  = getLevel(P.xp);

    showXPToast(xp, P.streak);
    renderHeaderChip();

    if (newLevel.n > oldLevel.n) setTimeout(() => showLevelUp(newLevel), 900);
    if ([3,5,10,20].includes(P.streak)) setTimeout(() => showStreakToast(P.streak), 500);
    newBadges.forEach((b, i) => setTimeout(() => showBadgeToast(b), 1400 + i * 2200));
  }

  function wrongAnswer() {
    if (!P) return;
    pageSessionAnswered++;
    P.streak = 0;
    save();
    renderHeaderChip();
  }

  // ── Badge check ──────────────────────────────────────────────────
  function checkBadges() {
    if (!P) return [];
    const fresh = [];
    BADGES.forEach(b => {
      if (!P.badges.includes(b.id) && b.check(P)) {
        P.badges.push(b.id);
        fresh.push(b);
      }
    });
    if (fresh.length) save();
    return fresh;
  }

  // ── CSS ──────────────────────────────────────────────────────────
  function injectCSS() {
    const s = document.createElement('style');
    s.textContent = `
      /* ===== HEADER CHIP ===== */
      .gs-header-chip {
        position: absolute;
        top: 12px; left: 12px;
        z-index: 100;
        display: flex; align-items: center; gap: 7px;
        background: rgba(255,255,255,0.18);
        border: 2px solid rgba(255,255,255,0.35);
        border-radius: 30px;
        padding: 6px 13px 6px 6px;
        cursor: pointer; color: white;
        font-family: inherit; font-weight: 800;
        transition: background 0.15s, transform 0.15s;
        backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
        max-width: calc(55vw - 24px);
        text-align: left; line-height: 1.2;
      }
      .gs-header-chip:hover { background: rgba(255,255,255,0.28); transform: scale(1.02); }
      .gs-chip-avatar { font-size: 1.6rem; line-height: 1; flex-shrink: 0; }
      .gs-chip-info   { display: flex; flex-direction: column; min-width: 0; }
      .gs-chip-name   { font-size: 0.84rem; font-weight: 900; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
      .gs-chip-meta   { font-size: 0.66rem; font-weight: 700; color: rgba(255,255,255,0.78); white-space: nowrap; }

      /* ===== XP TOAST ===== */
      .gs-xp-toast {
        position: fixed; top: 68px; left: 14px; z-index: 9800;
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        color: white; border-radius: 20px; padding: 7px 16px;
        font-size: 0.95rem; font-weight: 900; pointer-events: none;
        box-shadow: 0 4px 18px rgba(124,58,237,0.5);
        animation: gsXpPop 1.9s ease forwards;
      }
      @keyframes gsXpPop {
        0%   { opacity:0; transform: translateY(-10px) scale(0.8); }
        18%  { opacity:1; transform: translateY(0) scale(1.12); }
        38%  { transform: scale(1); }
        70%  { opacity:1; }
        100% { opacity:0; transform: translateY(-40px) scale(0.9); }
      }

      /* ===== STREAK TOAST ===== */
      .gs-streak-toast {
        position: fixed; top: 110px; left: 14px; z-index: 9801;
        background: linear-gradient(135deg, #dc2626, #f97316);
        color: white; border-radius: 20px; padding: 8px 18px;
        font-size: 1rem; font-weight: 900; pointer-events: none;
        box-shadow: 0 4px 18px rgba(239,68,68,0.5);
        animation: gsXpPop 2.5s ease forwards;
      }

      /* ===== BADGE TOAST ===== */
      .gs-badge-toast {
        position: fixed; bottom: 16px; right: 14px; z-index: 9802;
        background: linear-gradient(135deg, #065f46, #059669);
        color: white; border-radius: 18px; padding: 12px 18px;
        display: flex; align-items: center; gap: 12px;
        box-shadow: 0 6px 24px rgba(5,150,105,0.45);
        animation: gsBadgePop 3.5s ease forwards;
        pointer-events: none; max-width: 260px;
      }
      .gs-badge-toast-icon  { font-size: 2rem; flex-shrink: 0; }
      .gs-badge-toast-label { font-size: 0.7rem; font-weight: 700; opacity: 0.8; text-transform: uppercase; letter-spacing: 0.5px; }
      .gs-badge-toast-name  { font-size: 0.92rem; font-weight: 900; }
      @keyframes gsBadgePop {
        0%   { opacity:0; transform: translateX(60px) scale(0.8); }
        12%  { opacity:1; transform: translateX(0) scale(1.06); }
        25%  { transform: scale(1); }
        75%  { opacity:1; }
        100% { opacity:0; transform: translateX(40px); }
      }

      /* ===== LEVEL-UP MODAL ===== */
      .gs-levelup-overlay {
        position: fixed; inset: 0;
        background: rgba(10,5,30,0.75); z-index: 9900;
        display: flex; align-items: center; justify-content: center;
        animation: gsFadeIn 0.25s ease; backdrop-filter: blur(4px);
      }
      .gs-levelup-card {
        background: linear-gradient(150deg, #1e1b4b, #4c1d95 50%, #1e3a5f);
        color: white; border-radius: 28px; padding: 44px 32px 36px;
        text-align: center; max-width: 340px; width: 88%;
        box-shadow: 0 24px 80px rgba(124,58,237,0.6), 0 0 0 1px rgba(167,139,250,0.3);
        animation: gsCardPop 0.45s cubic-bezier(0.175,0.885,0.32,1.275);
        position: relative; overflow: hidden;
      }
      .gs-levelup-card::before {
        content: ''; position: absolute; top: -40%; left: -40%;
        width: 180%; height: 180%;
        background: radial-gradient(ellipse, rgba(167,139,250,0.12) 0%, transparent 65%);
        pointer-events: none;
      }
      .gs-levelup-emoji { font-size: 4.5rem; display: block; margin-bottom: 10px; animation: gsBounce 0.6s 0.4s ease both; }
      .gs-levelup-sup   { font-size: 0.82rem; font-weight: 700; color: #a78bfa; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px; }
      .gs-levelup-title { font-size: 2.2rem; font-weight: 900; margin-bottom: 4px; }
      .gs-levelup-sub   { font-size: 1.1rem; color: #c4b5fd; font-weight: 700; margin-bottom: 16px; }
      .gs-levelup-msg   { font-size: 0.95rem; color: rgba(255,255,255,0.75); margin-bottom: 28px; line-height: 1.5; }
      .gs-levelup-btn {
        background: linear-gradient(135deg, #7c3aed, #a855f7); color: white; border: none;
        border-radius: 24px; padding: 13px 36px; font-size: 1.05rem; font-weight: 900;
        cursor: pointer; font-family: inherit; transition: transform 0.15s, box-shadow 0.15s;
        box-shadow: 0 4px 16px rgba(124,58,237,0.4);
      }
      .gs-levelup-btn:hover { transform: scale(1.04); box-shadow: 0 6px 24px rgba(124,58,237,0.5); }

      @keyframes gsFadeIn  { from { opacity:0 } to { opacity:1 } }
      @keyframes gsCardPop { from { opacity:0; transform:scale(0.7) } to { opacity:1; transform:scale(1) } }
      @keyframes gsBounce  { 0% { transform:scale(0.5); opacity:0 } 70% { transform:scale(1.2) } 100% { transform:scale(1); opacity:1 } }

      /* ===== CONFETTI ===== */
      .gs-confetti {
        position: fixed; top: -10px; z-index: 9999;
        pointer-events: none; border-radius: 3px;
        animation: gsFall linear forwards;
      }
      @keyframes gsFall {
        0%   { transform: translateY(0) rotate(0deg); opacity: 1; }
        80%  { opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
      }

      /* ===== STARS on pages ===== */
      .gs-page-stars { display: flex; align-items: center; gap: 3px; font-size: 1.1rem; }

      /* ===== NEXT LESSON PANEL ===== */
      .gs-next-overlay {
        position: fixed; inset: 0; z-index: 5000;
        background: rgba(10,5,30,0.72);
        display: flex; align-items: flex-end; justify-content: center;
        animation: gsFadeIn 0.3s ease;
        backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px);
      }
      .gs-next-panel {
        background: linear-gradient(160deg, #1e1b4b 0%, #312e81 45%, #1e3a5f 100%);
        color: white; width: 100%; max-width: 560px;
        border-radius: 28px 28px 0 0;
        padding: 32px 24px 44px;
        box-shadow: 0 -12px 60px rgba(124,58,237,0.55);
        animation: gsNextSlideUp 0.45s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
        position: relative; overflow: hidden;
      }
      .gs-next-panel::before {
        content: ''; position: absolute; top: -50%; left: -20%;
        width: 140%; height: 100%;
        background: radial-gradient(ellipse, rgba(167,139,250,0.12) 0%, transparent 65%);
        pointer-events: none;
      }
      @keyframes gsNextSlideUp {
        from { transform: translateY(100%); opacity: 0; }
        to   { transform: translateY(0);    opacity: 1; }
      }
      .gs-next-close {
        position: absolute; top: 14px; right: 14px;
        background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2);
        color: rgba(255,255,255,0.7); border-radius: 50%; width: 34px; height: 34px;
        font-size: 0.85rem; cursor: pointer; display: flex; align-items: center; justify-content: center;
        transition: background 0.15s; font-family: inherit;
      }
      .gs-next-close:hover { background: rgba(255,255,255,0.25); color: white; }
      .gs-next-stars { font-size: 2.6rem; text-align: center; margin-bottom: 10px; letter-spacing: 6px; animation: gsBounce 0.5s 0.1s ease both; }
      .gs-next-star-empty { opacity: 0.25; }
      .gs-next-bravo { font-size: 1.8rem; font-weight: 900; text-align: center; margin-bottom: 4px; }
      .gs-next-sub   { font-size: 0.9rem; text-align: center; color: rgba(255,255,255,0.6); margin-bottom: 18px; }
      .gs-next-xp-badge {
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        border-radius: 30px; padding: 9px 24px; font-size: 1.15rem; font-weight: 900;
        text-align: center; margin: 0 auto 12px; display: table;
        box-shadow: 0 4px 18px rgba(124,58,237,0.4);
        animation: gsBounce 0.5s 0.25s ease both;
      }
      .gs-next-streak { text-align: center; font-size: 0.9rem; font-weight: 800; color: #fcd34d; margin-bottom: 16px; }
      .gs-next-main-btn {
        display: flex; align-items: center; gap: 14px;
        background: linear-gradient(135deg, #059669, #10b981);
        border-radius: 20px; padding: 17px 20px; text-decoration: none; color: white;
        margin-bottom: 14px; box-shadow: 0 6px 24px rgba(5,150,105,0.4);
        transition: transform 0.15s, box-shadow 0.15s;
        animation: gsBounce 0.5s 0.35s ease both;
      }
      .gs-next-main-btn:hover { transform: scale(1.02); box-shadow: 0 8px 32px rgba(5,150,105,0.55); }
      .gs-next-main-btn--gold { background: linear-gradient(135deg, #d97706, #f59e0b); box-shadow: 0 6px 24px rgba(217,119,6,0.4); }
      .gs-next-main-btn--gold:hover { box-shadow: 0 8px 32px rgba(217,119,6,0.55); }
      .gs-next-main-emoji { font-size: 2.2rem; flex-shrink: 0; }
      .gs-next-main-info  { flex: 1; }
      .gs-next-main-label { font-size: 0.72rem; font-weight: 700; opacity: 0.85; text-transform: uppercase; letter-spacing: 0.6px; }
      .gs-next-main-title { font-size: 1.15rem; font-weight: 900; }
      .gs-next-main-arrow { font-size: 1.5rem; font-weight: 900; opacity: 0.75; }
      .gs-next-actions { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
      .gs-next-secondary-btn {
        background: rgba(255,255,255,0.1); border: 1.5px solid rgba(255,255,255,0.22);
        border-radius: 24px; padding: 10px 20px; color: rgba(255,255,255,0.85); text-decoration: none;
        font-size: 0.87rem; font-weight: 800; transition: background 0.15s;
      }
      .gs-next-secondary-btn:hover { background: rgba(255,255,255,0.2); }
      .gs-next-continue {
        background: none; border: 1.5px solid rgba(255,255,255,0.18);
        border-radius: 24px; padding: 10px 20px; color: rgba(255,255,255,0.45);
        font-size: 0.87rem; font-weight: 700; cursor: pointer;
        transition: color 0.15s, border-color 0.15s; font-family: inherit;
      }
      .gs-next-continue:hover { color: rgba(255,255,255,0.8); border-color: rgba(255,255,255,0.35); }

      /* ===== PROFILE CREATION ===== */
      .gs-create-overlay {
        position: fixed; inset: 0; z-index: 9950;
        background: linear-gradient(160deg, #0f0c29, #302b63, #24243e);
        display: flex; align-items: center; justify-content: center;
        padding: 16px; overflow-y: auto;
      }
      .gs-create-panel {
        background: rgba(255,255,255,0.07);
        border: 1.5px solid rgba(255,255,255,0.18);
        border-radius: 28px; padding: 36px 26px 32px;
        width: 100%; max-width: 440px; color: white;
        animation: gsCardPop 0.45s cubic-bezier(0.175,0.885,0.32,1.275);
        max-height: 90vh; overflow-y: auto;
      }
      .gs-create-hero { font-size: 3rem; text-align: center; display: block; margin-bottom: 10px; animation: gsBounce 0.6s ease both; }
      .gs-create-title { font-size: 1.7rem; font-weight: 900; text-align: center; margin-bottom: 4px; }
      .gs-create-sub   { font-size: 0.9rem; text-align: center; color: rgba(255,255,255,0.6); margin-bottom: 28px; }
      .gs-create-field { margin-bottom: 22px; }
      .gs-create-label { display: block; font-size: 0.78rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.8px; color: rgba(255,255,255,0.65); margin-bottom: 8px; }
      .gs-create-input {
        width: 100%; background: rgba(255,255,255,0.1);
        border: 2px solid rgba(255,255,255,0.25); border-radius: 14px;
        padding: 12px 16px; font-size: 1.1rem; font-weight: 800; color: white;
        font-family: inherit; outline: none;
        transition: border-color 0.15s, background 0.15s;
      }
      .gs-create-input::placeholder { color: rgba(255,255,255,0.35); }
      .gs-create-input:focus { border-color: #a78bfa; background: rgba(167,139,250,0.12); }
      .gs-create-input.gs-input-error { border-color: #ef4444; animation: gsShake 0.35s ease; }
      @keyframes gsShake {
        0%,100% { transform: translateX(0); }
        20%,60% { transform: translateX(-6px); }
        40%,80% { transform: translateX(6px); }
      }
      .gs-avatar-grid { display: flex; flex-wrap: wrap; gap: 7px; }
      .gs-avatar-btn {
        font-size: 1.6rem; background: rgba(255,255,255,0.08);
        border: 2px solid transparent; border-radius: 12px;
        width: 48px; height: 48px; cursor: pointer;
        transition: background 0.15s, border-color 0.15s, transform 0.1s;
        display: flex; align-items: center; justify-content: center; line-height: 1;
      }
      .gs-avatar-btn:hover  { background: rgba(255,255,255,0.18); transform: scale(1.1); }
      .gs-avatar-btn.selected { border-color: #a78bfa; background: rgba(167,139,250,0.25); transform: scale(1.1); }
      .gs-classe-row { display: flex; gap: 8px; flex-wrap: wrap; }
      .gs-classe-btn {
        flex: 1; min-width: 56px; padding: 10px 6px; font-size: 0.9rem; font-weight: 900;
        background: rgba(255,255,255,0.08); border: 2px solid rgba(255,255,255,0.2);
        border-radius: 12px; color: white; cursor: pointer;
        transition: background 0.15s, border-color 0.15s, transform 0.1s;
        font-family: inherit; text-align: center;
      }
      .gs-classe-btn:hover  { background: rgba(255,255,255,0.18); transform: scale(1.04); }
      .gs-classe-btn.selected { background: rgba(167,139,250,0.3); border-color: #a78bfa; transform: scale(1.04); }
      .gs-create-btn {
        width: 100%; padding: 16px; font-size: 1.15rem; font-weight: 900;
        background: linear-gradient(135deg, #7c3aed, #a855f7); color: white; border: none;
        border-radius: 18px; cursor: pointer; font-family: inherit;
        box-shadow: 0 6px 24px rgba(124,58,237,0.45);
        transition: transform 0.15s, box-shadow 0.15s; margin-top: 6px;
      }
      .gs-create-btn:hover { transform: scale(1.02); box-shadow: 0 8px 32px rgba(124,58,237,0.55); }

      /* ===== PROFILE PICKER ===== */
      .gs-picker-overlay {
        position: fixed; inset: 0; z-index: 9940;
        background: rgba(10,5,30,0.72);
        display: flex; align-items: flex-end; justify-content: center;
        animation: gsFadeIn 0.25s ease;
        backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px);
      }
      .gs-picker-panel {
        background: linear-gradient(160deg, #1e1b4b, #312e81);
        width: 100%; max-width: 480px;
        border-radius: 28px 28px 0 0; padding: 24px 20px 36px;
        box-shadow: 0 -8px 40px rgba(124,58,237,0.45);
        animation: gsNextSlideUp 0.35s cubic-bezier(0.175,0.885,0.32,1.275);
        color: white; max-height: 80vh; overflow-y: auto;
      }
      .gs-picker-header {
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 18px;
      }
      .gs-picker-title { font-size: 1.1rem; font-weight: 900; }
      .gs-picker-close {
        background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2);
        color: rgba(255,255,255,0.7); border-radius: 50%; width: 32px; height: 32px;
        font-size: 0.82rem; cursor: pointer; display: flex; align-items: center; justify-content: center;
        font-family: inherit; transition: background 0.15s;
      }
      .gs-picker-close:hover { background: rgba(255,255,255,0.25); }
      .gs-picker-list { display: flex; flex-direction: column; gap: 8px; margin-bottom: 14px; }
      .gs-picker-item {
        display: flex; align-items: center; gap: 12px;
        background: rgba(255,255,255,0.07); border: 2px solid rgba(255,255,255,0.1);
        border-radius: 16px; padding: 12px 14px; cursor: pointer;
        color: white; font-family: inherit; text-align: left; width: 100%;
        transition: background 0.15s, border-color 0.15s;
      }
      .gs-picker-item:hover  { background: rgba(255,255,255,0.14); }
      .gs-picker-item.active { border-color: #a78bfa; background: rgba(167,139,250,0.15); }
      .gs-picker-avatar { font-size: 2.2rem; flex-shrink: 0; }
      .gs-picker-info   { flex: 1; min-width: 0; }
      .gs-picker-name   { font-size: 1rem; font-weight: 900; }
      .gs-picker-meta   { font-size: 0.75rem; font-weight: 700; color: rgba(255,255,255,0.6); margin-top: 2px; }
      .gs-picker-check  { font-size: 1.1rem; color: #a78bfa; font-weight: 900; flex-shrink: 0; }
      .gs-picker-add {
        width: 100%; padding: 12px; font-size: 0.95rem; font-weight: 800;
        background: rgba(255,255,255,0.1); border: 2px dashed rgba(255,255,255,0.25);
        border-radius: 16px; color: rgba(255,255,255,0.85); cursor: pointer;
        font-family: inherit; margin-bottom: 10px; transition: background 0.15s;
      }
      .gs-picker-add:hover { background: rgba(255,255,255,0.18); }
      .gs-picker-full {
        display: block; text-align: center; color: rgba(255,255,255,0.5);
        font-size: 0.85rem; font-weight: 700; text-decoration: none;
        padding: 6px; transition: color 0.15s;
      }
      .gs-picker-full:hover { color: rgba(255,255,255,0.85); }
    `;
    document.head.appendChild(s);
  }

  // ── Header chip ───────────────────────────────────────────────────
  let headerChipEl;

  function createHeaderProfile() {
    const header = document.querySelector('.site-header');
    if (!header) return;
    headerChipEl = document.createElement('button');
    headerChipEl.className = 'gs-header-chip';
    headerChipEl.setAttribute('title', 'Changer de profil');
    headerChipEl.addEventListener('click', showProfilePicker);
    renderHeaderChip();
    header.appendChild(headerChipEl);
  }

  function renderHeaderChip() {
    if (!headerChipEl) return;
    if (!P) {
      headerChipEl.innerHTML = `<span class="gs-chip-avatar">👤</span><div class="gs-chip-info"><span class="gs-chip-name">Créer un profil</span></div>`;
      return;
    }
    const lv = getLevel(P.xp);
    const streakStr = P.streak >= 3 ? ` 🔥${P.streak}` : '';
    headerChipEl.innerHTML = `
      <span class="gs-chip-avatar">${P.avatar}</span>
      <div class="gs-chip-info">
        <span class="gs-chip-name">${P.name}</span>
        <span class="gs-chip-meta">${lv.emoji} Niv.${P.level} · ${P.xp} XP${streakStr}</span>
      </div>
    `;
  }

  // ── Profile creation modal ────────────────────────────────────────
  function showCreateProfileModal(onDone) {
    const overlay = document.createElement('div');
    overlay.className = 'gs-create-overlay';

    let selAvatar = AVATARS[0];
    let selClasse = 'CE2';

    overlay.innerHTML = `
      <div class="gs-create-panel">
        <span class="gs-create-hero">✨</span>
        <h2 class="gs-create-title">Bienvenue !</h2>
        <p class="gs-create-sub">Crée ton profil pour commencer à gagner des points</p>
        <div class="gs-create-field">
          <label class="gs-create-label">Ton prénom</label>
          <input class="gs-create-input" id="gs-name-input" type="text" placeholder="Ex : Clémence" maxlength="20" autocomplete="off">
        </div>
        <div class="gs-create-field">
          <label class="gs-create-label">Ton avatar</label>
          <div class="gs-avatar-grid">
            ${AVATARS.map((a,i) => `<button class="gs-avatar-btn${i===0?' selected':''}" data-avatar="${a}" onclick="window._gsPickAvatar(this,'${a}')">${a}</button>`).join('')}
          </div>
        </div>
        <div class="gs-create-field">
          <label class="gs-create-label">Ta classe</label>
          <div class="gs-classe-row">
            ${CLASSE_LIST.map(c => `<button class="gs-classe-btn${c==='CE2'?' selected':''}" onclick="window._gsPickClasse(this,'${c}')">${c}</button>`).join('')}
          </div>
        </div>
        <button class="gs-create-btn" onclick="window._gsSubmitCreate()">C'est parti ! →</button>
      </div>
    `;

    document.body.appendChild(overlay);
    setTimeout(() => document.getElementById('gs-name-input')?.focus(), 350);

    window._gsPickAvatar = (btn, avatar) => {
      selAvatar = avatar;
      overlay.querySelectorAll('.gs-avatar-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
    };
    window._gsPickClasse = (btn, classe) => {
      selClasse = classe;
      overlay.querySelectorAll('.gs-classe-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
    };
    window._gsSubmitCreate = () => {
      const input = document.getElementById('gs-name-input');
      const name = (input?.value || '').trim();
      if (!name) {
        if (input) { input.classList.add('gs-input-error'); input.placeholder = '⚠️ Entre ton prénom !'; input.focus(); }
        return;
      }
      const p = blank(name, selAvatar, selClasse);
      store.profiles[p.id] = p;
      store.active = p.id;
      P = p;
      saveStore();
      overlay.remove();
      onDone(p);
    };

    const input = document.getElementById('gs-name-input');
    if (input) input.addEventListener('keydown', e => { if (e.key === 'Enter') window._gsSubmitCreate(); });
  }

  // ── Profile picker modal ──────────────────────────────────────────
  function showProfilePicker() {
    const overlay = document.createElement('div');
    overlay.className = 'gs-picker-overlay';

    function buildItems() {
      return Object.values(store.profiles||{}).map(p => {
        const lv = getLevel(p.xp);
        const active = p.id === store.active;
        return `
          <button class="gs-picker-item${active?' active':''}" onclick="window._gsActivate('${p.id}')">
            <span class="gs-picker-avatar">${p.avatar}</span>
            <div class="gs-picker-info">
              <div class="gs-picker-name">${p.name}</div>
              <div class="gs-picker-meta">${p.classe} · ${lv.emoji} Niv.${p.level} · ${p.xp} XP · ${p.tot} réponses</div>
            </div>
            ${active ? '<span class="gs-picker-check">✓</span>' : ''}
          </button>
        `;
      }).join('');
    }

    overlay.innerHTML = `
      <div class="gs-picker-panel">
        <div class="gs-picker-header">
          <span class="gs-picker-title">👤 Profils</span>
          <button class="gs-picker-close" onclick="this.closest('.gs-picker-overlay').remove()">✕</button>
        </div>
        <div class="gs-picker-list">${buildItems()}</div>
        <button class="gs-picker-add" onclick="window._gsNewProfile()">+ Nouveau profil</button>
        <a href="profile.html" class="gs-picker-full" onclick="this.closest('.gs-picker-overlay').remove()">Voir le profil complet →</a>
      </div>
    `;

    overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
    document.body.appendChild(overlay);

    window._gsActivate = id => {
      if (id === store.active) { overlay.remove(); return; }
      store.active = id;
      P = store.profiles[id];
      saveStore();
      location.reload();
    };
    window._gsNewProfile = () => {
      overlay.remove();
      showCreateProfileModal(p => {
        renderHeaderChip();
        checkBadges();
        save();
      });
    };
  }

  // ── Toasts ───────────────────────────────────────────────────────
  function showXPToast(xp, streak) {
    const el = document.createElement('div');
    el.className = 'gs-xp-toast';
    const bonus = streak >= 5 ? ' 🔥' : streak >= 3 ? ' 🌡️' : '';
    el.textContent = `+${xp} XP${bonus}`;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2000);
  }

  function showStreakToast(n) {
    const msgs = { 3:'🔥 En feu — 3 de suite !', 5:'⚡ Inarrêtable — 5 de suite !', 10:'🌪️ Tornade — 10 de suite !', 20:'💥 Légendaire — 20 de suite !' };
    const el = document.createElement('div');
    el.className = 'gs-streak-toast';
    el.textContent = msgs[n] || `🔥 ${n} de suite !`;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2600);
  }

  function showBadgeToast(badge) {
    const el = document.createElement('div');
    el.className = 'gs-badge-toast';
    el.innerHTML = `
      <div class="gs-badge-toast-icon">${badge.emoji}</div>
      <div>
        <div class="gs-badge-toast-label">Badge débloqué !</div>
        <div class="gs-badge-toast-name">${badge.name}</div>
      </div>
    `;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 3600);
  }

  // ── Level-up modal ───────────────────────────────────────────────
  function showLevelUp(lvl) {
    spawnConfetti();
    const overlay = document.createElement('div');
    overlay.className = 'gs-levelup-overlay';
    overlay.innerHTML = `
      <div class="gs-levelup-card">
        <span class="gs-levelup-emoji">${lvl.emoji}</span>
        <div class="gs-levelup-sup">Nouveau niveau !</div>
        <div class="gs-levelup-title">Niveau ${lvl.n}</div>
        <div class="gs-levelup-sub">${lvl.title}</div>
        <p class="gs-levelup-msg">Bravo ${P ? P.name : ''} ! Tu progresses super vite ! Continue comme ça 🎉</p>
        <button class="gs-levelup-btn" onclick="this.closest('.gs-levelup-overlay').remove()">Super ! →</button>
      </div>
    `;
    overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
    document.body.appendChild(overlay);
  }

  // ── Next lesson panel ────────────────────────────────────────────
  function showNextLessonPanel() {
    const curIdx   = PAGE_SEQUENCE.indexOf(page);
    const nextPage = curIdx >= 0 && curIdx < PAGE_SEQUENCE.length - 1 ? PAGE_SEQUENCE[curIdx + 1] : null;
    const nextInfo = nextPage ? PAGE_LABELS[nextPage] : null;
    const totalQ   = document.querySelectorAll('.feedback-line').length || pageSessionAnswered;
    const pct      = totalQ > 0 ? Math.round((pageSessionCorrect / totalQ) * 100) : 0;
    const stars    = pct === 100 ? 3 : pct >= 70 ? 2 : 1;
    const xpEarned = pageSessionCorrect * XP_CORRECT;
    const bravoMsg = pct === 100 ? 'Parfait ! 🎯' : pct >= 70 ? 'Très bien !' : 'Continue comme ça !';

    spawnConfetti();

    const overlay = document.createElement('div');
    overlay.className = 'gs-next-overlay';
    overlay.innerHTML = `
      <div class="gs-next-panel">
        <button class="gs-next-close" onclick="this.closest('.gs-next-overlay').remove()">✕</button>
        <div class="gs-next-stars">
          ${'⭐'.repeat(stars)}<span class="gs-next-star-empty">${'☆'.repeat(3 - stars)}</span>
        </div>
        <div class="gs-next-bravo">${bravoMsg}</div>
        <div class="gs-next-sub">${pageSessionCorrect} / ${totalQ} bonnes réponses</div>
        <div class="gs-next-xp-badge">+${xpEarned} XP 🎉</div>
        ${P && P.streak >= 3 ? `<div class="gs-next-streak">🔥 Série de ${P.streak} bonnes réponses !</div>` : ''}
        ${nextPage ? `
          <a href="${nextPage}" class="gs-next-main-btn">
            <span class="gs-next-main-emoji">${nextInfo.emoji}</span>
            <div class="gs-next-main-info">
              <div class="gs-next-main-label">Leçon suivante</div>
              <div class="gs-next-main-title">${nextInfo.title}</div>
            </div>
            <span class="gs-next-main-arrow">→</span>
          </a>
        ` : `
          <a href="profile.html" class="gs-next-main-btn gs-next-main-btn--gold">
            <span class="gs-next-main-emoji">🏆</span>
            <div class="gs-next-main-info">
              <div class="gs-next-main-label">Programme terminé !</div>
              <div class="gs-next-main-title">Voir mon profil</div>
            </div>
            <span class="gs-next-main-arrow">→</span>
          </a>
        `}
        <div class="gs-next-actions">
          <a href="index.html" class="gs-next-secondary-btn">🏠 Toutes les leçons</a>
          <button class="gs-next-continue" onclick="this.closest('.gs-next-overlay').remove()">Continuer à pratiquer</button>
        </div>
      </div>
    `;
    overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
    document.body.appendChild(overlay);
  }

  // ── Confetti ─────────────────────────────────────────────────────
  function spawnConfetti() {
    const colors = ['#f97316','#22c55e','#3b82f6','#7c3aed','#ffd84d','#ef4444','#ec4899','#06b6d4'];
    for (let i = 0; i < 70; i++) {
      const el = document.createElement('div');
      el.className = 'gs-confetti';
      const dur = 1.2 + Math.random() * 1.4;
      el.style.cssText = `left:${Math.random()*100}vw;background:${colors[Math.floor(Math.random()*colors.length)]};width:${6+Math.random()*8}px;height:${4+Math.random()*5}px;animation-delay:${Math.random()*0.6}s;animation-duration:${dur}s;transform:rotate(${Math.random()*360}deg);border-radius:${Math.random()>0.5?'50%':'2px'};`;
      document.body.appendChild(el);
      setTimeout(() => el.remove(), (dur + 0.7) * 1000);
    }
  }

  // ── Page complete detection ───────────────────────────────────────
  function checkPageComplete() {
    if (nextLessonShown) return;
    if (!PAGE_SEQUENCE.includes(page)) return;
    const lines = [...document.querySelectorAll('.feedback-line')];
    if (lines.length === 0) return;
    const answered = lines.filter(el => el.textContent.trim() !== '');
    if (answered.length >= lines.length) {
      nextLessonShown = true;
      setTimeout(showNextLessonPanel, 800);
    }
  }

  // ── Observer: detect correct/wrong answers on any page ───────────
  function setupObserver() {
    const FEEDBACK_CLASSES = new Set([
      'feedback-line','pizza-feedback','droite-feedback','figure-feedback',
      'tri-feedback','choix-feedback','pb-qcm-fb','flash-score'
    ]);

    function process(el) {
      if (!el || !el.classList) return;
      if (![...el.classList].some(c => FEEDBACK_CLASSES.has(c))) return;
      const txt = el.textContent || '';
      if (txt.includes('✅') && !el.dataset.gsOk) {
        el.dataset.gsOk = '1'; delete el.dataset.gsWrong;
        award(XP_CORRECT);
      } else if (txt.includes('❌') && !el.dataset.gsWrong) {
        el.dataset.gsWrong = '1'; delete el.dataset.gsOk;
        wrongAnswer();
      }
    }

    function handleNode(node) {
      if (!node || node.nodeType !== 1) return;
      process(node);
      let el = node.parentElement;
      for (let i = 0; i < 2 && el; i++, el = el.parentElement) process(el);
    }

    const obs = new MutationObserver(muts => {
      muts.forEach(m => {
        if (m.type === 'characterData') handleNode(m.target.parentElement);
        else {
          m.addedNodes.forEach(n => handleNode(n));
          if (m.type === 'childList') handleNode(m.target);
        }
      });
      checkPageComplete();
    });
    obs.observe(document.body, { subtree: true, characterData: true, childList: true });
  }

  // ── Init ─────────────────────────────────────────────────────────
  loadStore();

  function init() {
    injectCSS();
    if (!P) {
      showCreateProfileModal(() => {
        createHeaderProfile();
        setupObserver();
        checkBadges();
        save();
      });
    } else {
      createHeaderProfile();
      setupObserver();
      checkBadges();
      save();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // ── Public API ───────────────────────────────────────────────────
  window.GS = {
    profile:    () => P,
    store:      () => store,
    save,
    LEVELS, BADGES, PAGE_LABELS, CLASSE_LIST, AVATARS,
    getLevel, getNextLevel, pct,
    award, wrongAnswer,
    spawnConfetti,
    showProfilePicker,
    showCreateProfileModal,
    setName:   name   => { if (P) { P.name   = name;   save(); renderHeaderChip(); } },
    setAvatar: avatar => { if (P) { P.avatar = avatar; save(); renderHeaderChip(); } },
    setClasse: classe => { if (P) { P.classe = classe; save(); } },
    deleteProfile: id => {
      if (!store.profiles[id]) return;
      delete store.profiles[id];
      if (store.active === id) {
        const ids = Object.keys(store.profiles);
        store.active = ids[0] || null;
        P = ids.length ? store.profiles[store.active] : null;
      }
      saveStore();
      if (!P) showCreateProfileModal(() => { createHeaderProfile(); setupObserver(); checkBadges(); save(); });
      else { renderHeaderChip(); location.reload(); }
    },
    resetAll: () => {
      if (!P) return;
      const id = P.id;
      const fresh = blank(P.name, P.avatar, P.classe);
      fresh.id = id;
      store.profiles[id] = fresh;
      P = fresh;
      saveStore();
      location.reload();
    },
  };

})();
