/* ============================================================
   SYNC — Synchronisation multi-appareils (Firebase)

   CONFIGURATION FIREBASE :
   1. Aller sur https://console.firebase.google.com
   2. Créer un projet (ex: "ecole-facile")
   3. Ajouter une application Web
   4. Activer Realtime Database (mode test)
   5. Copier les valeurs de config ci-dessous
   ============================================================ */

window.EF_SYNC = (function () {
  'use strict';

  // ── Config Firebase — À REMPLIR ──────────────────────────────
  const FB_CONFIG = {
    apiKey:      window.EF_FIREBASE_API_KEY      || '',
    databaseURL: window.EF_FIREBASE_DATABASE_URL || '',
    projectId:   window.EF_FIREBASE_PROJECT_ID   || '',
  };
  // Les valeurs peuvent aussi être définies dans firebase-keys.js
  // (fichier non versionné, à créer localement)

  const ENABLED = !!(FB_CONFIG.apiKey && FB_CONFIG.databaseURL);

  let _db = null;
  let _initialized = false;

  // ── Initialise Firebase (chargement dynamique du SDK) ────────
  function init(cb) {
    if (!ENABLED) { if (cb) cb(null); return; }
    if (_initialized) { if (cb) cb(_db); return; }

    function loadScript(src, onload) {
      const s = document.createElement('script');
      s.src = src; s.onload = onload;
      document.head.appendChild(s);
    }

    loadScript('https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js', function () {
      loadScript('https://www.gstatic.com/firebasejs/9.23.0/firebase-database-compat.js', function () {
        try {
          if (!firebase.apps.length) firebase.initializeApp(FB_CONFIG);
          _db = firebase.database();
          _initialized = true;
          if (cb) cb(_db);
        } catch (e) {
          console.warn('[EF Sync] Firebase init error:', e);
          if (cb) cb(null);
        }
      });
    });
  }

  // ── Sauvegarder un profil ─────────────────────────────────────
  function saveProfile(syncCode, profileData, cb) {
    if (!ENABLED || !syncCode) { if (cb) cb(false); return; }
    init(function (db) {
      if (!db) { if (cb) cb(false); return; }
      const clean = JSON.parse(JSON.stringify(profileData));
      delete clean.id; // on n'expose pas l'ID local
      db.ref('profiles/' + syncCode).set({
        ...clean,
        _savedAt: Date.now(),
      }).then(function () {
        if (cb) cb(true);
      }).catch(function () {
        if (cb) cb(false);
      });
    });
  }

  // ── Charger un profil par code ────────────────────────────────
  function loadProfile(syncCode, cb) {
    if (!ENABLED || !syncCode) { if (cb) cb(null); return; }
    init(function (db) {
      if (!db) { if (cb) cb(null); return; }
      db.ref('profiles/' + syncCode).once('value').then(function (snap) {
        if (cb) cb(snap.exists() ? snap.val() : null);
      }).catch(function () {
        if (cb) cb(null);
      });
    });
  }

  // ── Générer un code de sync ───────────────────────────────────
  function generateCode() {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    let code = '';
    for (let i = 0; i < 6; i++) {
      code += chars[Math.floor(Math.random() * chars.length)];
    }
    return code;
  }

  // ── API publique ──────────────────────────────────────────────
  return {
    enabled: ENABLED,
    saveProfile: saveProfile,
    loadProfile: loadProfile,
    generateCode: generateCode,
  };
})();
