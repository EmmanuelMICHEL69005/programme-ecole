/* ============================================================
   AUTH — Firebase Authentication (email + mot de passe)
   Un compte peut porter PLUSIEURS profils (un par enfant) :
     users/{uid}/profiles/{pid}   → chaque profil
     users/{uid}/activeProfile    → pid du profil actif
   L'ancien users/{uid}/profile (profil unique) est migré automatiquement
   vers users/{uid}/profiles/main au premier chargement.

   CONFIG dans firebase-keys.js (non versionné) ou via window.* :
     window.EF_FIREBASE_API_KEY
     window.EF_FIREBASE_AUTH_DOMAIN
     window.EF_FIREBASE_DATABASE_URL
     window.EF_FIREBASE_PROJECT_ID
   ============================================================ */

window.EF_AUTH = (function () {
  'use strict';

  const FB_CONFIG = {
    apiKey:      window.EF_FIREBASE_API_KEY      || '',
    authDomain:  window.EF_FIREBASE_AUTH_DOMAIN  || '',
    databaseURL: window.EF_FIREBASE_DATABASE_URL || '',
    projectId:   window.EF_FIREBASE_PROJECT_ID   || '',
  };

  const ENABLED = !!(FB_CONFIG.apiKey && FB_CONFIG.authDomain && FB_CONFIG.databaseURL);

  let _auth = null, _db = null;
  let _user = null;
  let _profile = null;          // profil actif (rétro-compatible)
  let _profiles = {};           // { pid: profil } — plusieurs profils par compte
  let _activeId = null;         // pid du profil actif
  let _loadedUid = null;        // uid pour lequel _profiles a été chargé
  let _ready = false;
  let _readyCbs = [];
  let _changeCbs = [];

  const AVATARS = ['🌟','⭐','🦋','🌈','🦄','🐱','🐼','🐸','🦊','🐢','🌺','🍭','🎀','🚀','⚡','🎯','🏆','💎','🌙','🦸‍♀️'];
  const CLASSES = ['CP','CE1','CE2','CM1','CM2','6e','5e','4e','3e'];

  // ── SDK loading ───────────────────────────────────────────────
  function loadScript(src, cb) {
    const s = document.createElement('script');
    s.src = src;
    s.onload = cb;
    s.onerror = () => { console.warn('[EF Auth] Impossible de charger', src); cb(); };
    document.head.appendChild(s);
  }

  function initFirebase(cb) {
    if (!ENABLED) { cb(false); return; }
    const base = 'https://www.gstatic.com/firebasejs/9.23.0/';
    loadScript(base + 'firebase-app-compat.js', function () {
      loadScript(base + 'firebase-auth-compat.js', function () {
        loadScript(base + 'firebase-database-compat.js', function () {
          try {
            if (!window.firebase) { cb(false); return; }
            if (!firebase.apps.length) firebase.initializeApp(FB_CONFIG);
            _auth = firebase.auth();
            _db   = firebase.database();
            cb(true);
          } catch (e) {
            console.warn('[EF Auth] Erreur init Firebase :', e);
            cb(false);
          }
        });
      });
    });
  }

  // ── Profils DB (plusieurs profils par compte) ────────────────
  function genPid() {
    return 'p_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
  }

  function blankProfile(uid, data) {
    data = data || {};
    return {
      id: uid, pid: data.pid || genPid(),
      name: data.name || '', avatar: data.avatar || '🌟', classe: data.classe || 'CE2',
      xp: 0, level: 1, badges: [], tot: 0, streak: 0, maxStreak: 0,
      pages: {}, days: [], completedPages: {}, createdAt: Date.now(),
    };
  }

  function profilesList() {
    return Object.keys(_profiles)
      .map(pid => Object.assign({}, _profiles[pid], { pid }))
      .sort((a, b) => (a.createdAt || 0) - (b.createdAt || 0));
  }

  // Charge tous les profils du compte + migre l'ancien profil unique si besoin
  function loadAll(uid, cb) {
    _db.ref('users/' + uid).once('value').then(function (snap) {
      const root = snap.val() || {};
      let profiles = (root.profiles && typeof root.profiles === 'object') ? root.profiles : null;
      let activeId = root.activeProfile || null;

      if (!profiles || !Object.keys(profiles).length) {
        if (root.profile && root.profile.name) {
          // Migration : l'ancien profil unique devient le profil "principal"
          const migrated = Object.assign({}, root.profile, { pid: 'main' });
          profiles = { main: migrated };
          activeId = 'main';
          _db.ref('users/' + uid + '/profiles/main').set(migrated).catch(() => {});
          _db.ref('users/' + uid + '/activeProfile').set('main').catch(() => {});
        } else {
          profiles = {};
          activeId = null;
        }
      }
      if (!activeId || !profiles[activeId]) activeId = Object.keys(profiles)[0] || null;

      _profiles  = profiles;
      _activeId  = activeId;
      _profile   = activeId ? Object.assign({}, profiles[activeId], { pid: activeId }) : null;
      _loadedUid = uid;
      cb();
    }).catch(function () {
      _profiles = {}; _activeId = null; _profile = null; _loadedUid = uid;
      cb();
    });
  }

  // Écrit le profil actif dans users/{uid}/profiles/{activeId}
  function writeActive(data, cb) {
    if (!_user || !_db || !_activeId) { if (cb) cb(false); return; }
    const clean = JSON.parse(JSON.stringify(data));
    clean.pid = _activeId;
    clean._updatedAt = Date.now();
    _profiles[_activeId] = clean;
    _profile = Object.assign({}, clean);
    _db.ref('users/' + _user.uid + '/profiles/' + _activeId).set(clean)
      .then(() => { if (cb) cb(true); })
      .catch(() => { if (cb) cb(false); });
  }

  // ── State ─────────────────────────────────────────────────────
  function fireReady() {
    _ready = true;
    _readyCbs.slice().forEach(cb => cb(_user, _profile));
    _readyCbs = [];
  }

  function fireChange() {
    _changeCbs.slice().forEach(cb => cb(_user, _profile));
  }

  // ── Firebase setup ────────────────────────────────────────────
  function setup() {
    initFirebase(function (ok) {
      if (!ok) { fireReady(); return; }

      _auth.onAuthStateChanged(function (user) {
        _user = user;
        if (user) {
          // Profils déjà chargés pour cet utilisateur (ex : inscription qui vient d'avoir lieu)
          if (_loadedUid === user.uid) {
            if (!_ready) fireReady(); else fireChange();
            return;
          }
          loadAll(user.uid, function () {
            if (!_ready) fireReady(); else fireChange();
          });
        } else {
          _profiles = {}; _activeId = null; _profile = null; _loadedUid = null;
          if (!_ready) fireReady(); else fireChange();
        }
      });
    });
  }

  // ── CSS ───────────────────────────────────────────────────────
  function injectCSS() {
    if (document.getElementById('ef-auth-css')) return;
    const s = document.createElement('style');
    s.id = 'ef-auth-css';
    s.textContent = `
      .ef-auth-overlay {
        position: fixed; inset: 0; z-index: 9999;
        background: rgba(10,5,30,0.78);
        display: flex; align-items: center; justify-content: center;
        padding: 16px; animation: efFadeIn 0.2s ease;
        backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px);
      }
      @keyframes efFadeIn { from { opacity:0 } to { opacity:1 } }
      .ef-auth-card {
        background: #172d66;
        border: 1.5px solid rgba(183,196,240,0.3);
        border-radius: 24px; padding: 28px 24px 24px;
        width: 100%; max-width: 390px; color: white;
        box-shadow: 0 24px 64px rgba(0,0,0,0.55);
        animation: efSlideUp 0.26s cubic-bezier(0.4,0,0.2,1);
        max-height: 92vh; overflow-y: auto;
        scrollbar-width: thin; scrollbar-color: rgba(255,255,255,0.2) transparent;
      }
      @keyframes efSlideUp { from { transform:translateY(18px); opacity:0 } to { transform:translateY(0); opacity:1 } }
      .ef-auth-logo  { text-align:center; font-size:2.2rem; margin-bottom:6px; }
      .ef-auth-title { text-align:center; font-size:1.25rem; font-weight:900; margin-bottom:3px; }
      .ef-auth-sub   { text-align:center; font-size:0.8rem; opacity:0.6; margin-bottom:20px; line-height:1.4; }
      .ef-auth-tabs  { display:flex; gap:7px; margin-bottom:20px; }
      .ef-auth-tab {
        flex:1; padding:9px 6px; border-radius:11px;
        border:2px solid rgba(255,255,255,0.15);
        background:transparent; color:rgba(255,255,255,0.5);
        font-family:inherit; font-weight:800; font-size:0.85rem;
        cursor:pointer; transition:all 0.15s;
      }
      .ef-auth-tab.active { background:rgba(183,196,240,0.22); border-color:#b7c4f0; color:white; }
      .ef-auth-field { margin-bottom:13px; }
      .ef-auth-label {
        display:block; font-size:0.7rem; font-weight:900;
        text-transform:uppercase; letter-spacing:0.8px;
        color:rgba(255,255,255,0.5); margin-bottom:6px;
      }
      .ef-auth-input {
        width:100%; box-sizing:border-box;
        background:rgba(255,255,255,0.1); border:2px solid rgba(255,255,255,0.18);
        border-radius:11px; padding:11px 13px; color:white;
        font-family:inherit; font-size:0.92rem; font-weight:700;
        outline:none; transition:border-color 0.15s;
      }
      .ef-auth-input:focus { border-color:#b7c4f0; }
      .ef-auth-input::placeholder { color:rgba(255,255,255,0.3); }
      .ef-auth-sep {
        text-align:center; color:rgba(255,255,255,0.28);
        font-size:0.73rem; margin:14px 0 10px;
      }
      .ef-auth-avatar-grid { display:flex; flex-wrap:wrap; gap:5px; }
      .ef-auth-avatar-btn {
        width:36px; height:36px; border-radius:9px;
        border:2px solid rgba(255,255,255,0.1);
        background:rgba(255,255,255,0.07); font-size:1.25rem;
        cursor:pointer; display:flex; align-items:center; justify-content:center;
        transition:all 0.12s; line-height:1;
      }
      .ef-auth-avatar-btn.selected { border-color:#b7c4f0; background:rgba(183,196,240,0.25); }
      .ef-auth-classe-row { display:flex; gap:5px; flex-wrap:wrap; }
      .ef-auth-classe-btn {
        padding:6px 12px; border-radius:9px;
        border:2px solid rgba(255,255,255,0.14);
        background:rgba(255,255,255,0.06); color:rgba(255,255,255,0.65);
        font-family:inherit; font-size:0.8rem; font-weight:900;
        cursor:pointer; transition:all 0.12s;
      }
      .ef-auth-classe-btn.selected { border-color:#b7c4f0; background:rgba(183,196,240,0.22); color:white; }
      .ef-auth-btn {
        width:100%; padding:13px; border-radius:13px; border:none;
        background:#fff;
        color:#172d66; font-family:inherit; font-size:0.98rem; font-weight:900;
        cursor:pointer; margin-top:4px;
        transition:opacity 0.15s, transform 0.15s;
        box-shadow:0 4px 0 rgba(0,0,0,0.28);
      }
      .ef-auth-btn:hover { opacity:0.92; transform:translateY(-1px); }
      .ef-auth-btn:disabled { opacity:0.45; cursor:default; transform:none; }
      .ef-auth-error {
        background:rgba(239,68,68,0.18); border:1.5px solid rgba(239,68,68,0.38);
        border-radius:10px; padding:9px 13px; font-size:0.8rem; font-weight:700;
        color:#fca5a5; margin-top:11px; display:none; line-height:1.4;
      }
      .ef-auth-error.show { display:block; }
      .ef-auth-forgot {
        display:block; text-align:center; margin-top:12px;
        color:rgba(255,255,255,0.35); font-size:0.75rem; font-weight:700;
        text-decoration:none; cursor:pointer;
      }
      .ef-auth-forgot:hover { color:rgba(255,255,255,0.6); }
    `;
    document.head.appendChild(s);
  }

  // ── Auth modal ────────────────────────────────────────────────
  function showAuthModal(onSignedIn, defaultTab) {
    injectCSS();

    let tab = defaultTab || 'login';
    let selAvatar = '🌟';
    let selClasse = 'CE2';

    const overlay = document.createElement('div');
    overlay.className = 'ef-auth-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'ef-auth-title');
    document.body.appendChild(overlay);

    // Toujours une sortie : ✕, Échap, clic à côté ; le clavier reste dans la fenêtre
    const prevFocus = document.activeElement;
    function closeModal() {
      overlay.remove();
      document.removeEventListener('keydown', onKey);
      if (prevFocus && prevFocus.focus) prevFocus.focus();
    }
    function onKey(e) {
      if (!document.body.contains(overlay)) { document.removeEventListener('keydown', onKey); return; }
      if (e.key === 'Escape') { closeModal(); return; }
      if (e.key !== 'Tab') return;
      const f = [...overlay.querySelectorAll('button, input, a')].filter(x => !x.disabled && x.offsetParent !== null);
      if (!f.length) return;
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
    document.addEventListener('keydown', onKey);
    overlay.addEventListener('mousedown', function (e) { if (e.target === overlay) closeModal(); });

    function showError(msg) {
      const el = overlay.querySelector('.ef-auth-error');
      if (!el) return;
      el.textContent = msg;
      el.classList.add('show');
    }

    function setLoading(on) {
      const btn = overlay.querySelector('.ef-auth-btn');
      if (!btn) return;
      btn.disabled = on;
      btn.textContent = on ? '⏳ Chargement…' : (tab === 'signup' ? "C'est parti ! →" : "Se connecter →");
    }

    function friendlyError(err) {
      const msgs = {
        'auth/email-already-in-use': 'Cette adresse e-mail est déjà utilisée.',
        'auth/invalid-email':        'Adresse e-mail invalide.',
        'auth/weak-password':        'Mot de passe trop court (6 caractères minimum).',
        'auth/user-not-found':       'Aucun compte avec cette adresse e-mail.',
        'auth/wrong-password':       'Mot de passe incorrect.',
        'auth/invalid-credential':        'E-mail ou mot de passe incorrect.',
        'auth/invalid-login-credentials': 'E-mail ou mot de passe incorrect.',
        'auth/too-many-requests':    'Trop de tentatives. Réessaie dans quelques minutes.',
        'auth/network-request-failed': 'Erreur réseau — vérifie ta connexion.',
      };
      return msgs[err.code] || ('Erreur : ' + (err.message || err.code));
    }

    function doSignup() {
      if (!ENABLED) { showError('Firebase non configuré — vérifie firebase-keys.js.'); return; }
      if (!_auth)   { showError('Connexion Firebase impossible. Vérifie ta connexion Internet et réessaie.'); return; }
      const name     = (overlay.querySelector('#ef-name')?.value || '').trim();
      const email    = (overlay.querySelector('#ef-email')?.value || '').trim();
      const password =  overlay.querySelector('#ef-password')?.value || '';
      if (!name)              { showError('Entre ton prénom !'); return; }
      if (!email)             { showError('Entre ton adresse e-mail !'); return; }
      if (password.length < 6){ showError('Le mot de passe doit avoir au moins 6 caractères.'); return; }
      setLoading(true);
      _auth.createUserWithEmailAndPassword(email, password)
        .then(function (cred) {
          const pid = 'main';
          const profile = {
            id: cred.user.uid, pid, name, avatar: selAvatar, classe: selClasse,
            xp: 0, level: 1, badges: [], tot: 0, streak: 0, maxStreak: 0,
            pages: {}, days: [], completedPages: {}, createdAt: Date.now(),
          };
          _profiles  = { main: profile };
          _activeId  = pid;
          _profile   = profile;
          _loadedUid = cred.user.uid;
          const updates = {};
          updates['users/' + cred.user.uid + '/profiles/' + pid] = profile;
          updates['users/' + cred.user.uid + '/activeProfile']   = pid;
          _db.ref().update(updates).then(function () {
            cred.user.sendEmailVerification().catch(function () {});
            overlay.remove();
            onSignedIn(cred.user, profile);
          }).catch(function () {
            setLoading(false);
            showError('Compte créé mais erreur de sauvegarde. Réessaie ou vérifie les règles Firebase Database.');
          });
        })
        .catch(function (err) {
          setLoading(false);
          showError(friendlyError(err));
        });
    }

    function doLogin() {
      if (!ENABLED) { showError('Firebase non configuré — vérifie firebase-keys.js.'); return; }
      if (!_auth)   { showError('Connexion Firebase impossible. Vérifie ta connexion Internet et réessaie.'); return; }
      const email    = (overlay.querySelector('#ef-email')?.value || '').trim();
      const password =  overlay.querySelector('#ef-password')?.value || '';
      if (!email || !password) { showError('Remplis tous les champs.'); return; }
      setLoading(true);
      _auth.signInWithEmailAndPassword(email, password)
        .then(function (cred) {
          loadAll(cred.user.uid, function () {
            overlay.remove();
            onSignedIn(cred.user, _profile);
          });
        })
        .catch(function (err) {
          setLoading(false);
          showError(friendlyError(err));
        });
    }

    function doForgot() {
      if (!_auth) { showError('Connexion Firebase impossible. Vérifie ta connexion Internet et réessaie.'); return; }
      const email = (overlay.querySelector('#ef-email')?.value || '').trim();
      if (!email) { showError('Entre ton e-mail pour réinitialiser le mot de passe.'); return; }
      _auth.sendPasswordResetEmail(email)
        .then(function () { showError('✅ E-mail de réinitialisation envoyé !'); })
        .catch(function (err) { showError(friendlyError(err)); });
    }

    function render() {
      overlay.innerHTML = `
        <div class="ef-auth-card">
          <button type="button" class="ef-auth-close" aria-label="Fermer">✕</button>
          <div class="ef-auth-title" id="ef-auth-title">${tab === 'signup' ? 'Créer un compte' : 'Se connecter'}</div>
          <div class="ef-auth-sub">À faire avec un adulte : le compte garde les résultats de chaque enfant, sur tous les appareils.</div>
          <div class="ef-auth-tabs">
            <button class="ef-auth-tab ${tab==='signup'?'active':''}" data-tab="signup">Créer un compte</button>
            <button class="ef-auth-tab ${tab==='login'?'active':''}"  data-tab="login">Se connecter</button>
          </div>
          ${tab === 'signup' ? `
            <div class="ef-auth-field">
              <label class="ef-auth-label">Ton prénom</label>
              <input class="ef-auth-input" id="ef-name" type="text" placeholder="Ex : Clémence" autocomplete="name" maxlength="30">
            </div>
            <div class="ef-auth-field">
              <label class="ef-auth-label">Ton avatar</label>
              <div class="ef-auth-avatar-grid">
                ${AVATARS.map(a => `<button class="ef-auth-avatar-btn${a===selAvatar?' selected':''}" data-avatar="${a}">${a}</button>`).join('')}
              </div>
            </div>
            <div class="ef-auth-field">
              <label class="ef-auth-label">Ta classe</label>
              <div class="ef-auth-classe-row">
                ${CLASSES.map(c => `<button class="ef-auth-classe-btn${c===selClasse?' selected':''}" data-classe="${c}">${c}</button>`).join('')}
              </div>
            </div>
            <div class="ef-auth-sep">── Compte ──</div>
            <div class="ef-auth-field">
              <label class="ef-auth-label">Adresse e-mail</label>
              <input class="ef-auth-input" id="ef-email" type="email" placeholder="exemple@mail.com" autocomplete="email">
            </div>
            <div class="ef-auth-field">
              <label class="ef-auth-label">Mot de passe</label>
              <input class="ef-auth-input" id="ef-password" type="password" placeholder="6 caractères minimum" autocomplete="new-password">
            </div>
            <button class="ef-auth-btn">C'est parti ! →</button>
          ` : `
            <div class="ef-auth-field">
              <label class="ef-auth-label">Adresse e-mail</label>
              <input class="ef-auth-input" id="ef-email" type="email" placeholder="exemple@mail.com" autocomplete="email">
            </div>
            <div class="ef-auth-field">
              <label class="ef-auth-label">Mot de passe</label>
              <input class="ef-auth-input" id="ef-password" type="password" placeholder="Ton mot de passe" autocomplete="current-password">
            </div>
            <button class="ef-auth-btn">Se connecter →</button>
            <a class="ef-auth-forgot" id="ef-forgot">Mot de passe oublié ?</a>
          `}
          <div class="ef-auth-error"></div>
        </div>
      `;

      overlay.querySelector('.ef-auth-close').addEventListener('click', closeModal);
      const firstInput = overlay.querySelector('.ef-auth-input');
      if (firstInput) firstInput.focus();

      // Tab switching
      overlay.querySelectorAll('.ef-auth-tab').forEach(function (btn) {
        btn.addEventListener('click', function () {
          tab = btn.dataset.tab;
          render();
        });
      });

      // Avatar selection
      overlay.querySelectorAll('.ef-auth-avatar-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          selAvatar = btn.dataset.avatar;
          overlay.querySelectorAll('.ef-auth-avatar-btn').forEach(b => b.classList.remove('selected'));
          btn.classList.add('selected');
        });
      });

      // Classe selection
      overlay.querySelectorAll('.ef-auth-classe-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          selClasse = btn.dataset.classe;
          overlay.querySelectorAll('.ef-auth-classe-btn').forEach(b => b.classList.remove('selected'));
          btn.classList.add('selected');
        });
      });

      // Submit
      const submitBtn = overlay.querySelector('.ef-auth-btn');
      if (submitBtn) submitBtn.addEventListener('click', tab === 'signup' ? doSignup : doLogin);

      // Enter key
      overlay.querySelectorAll('.ef-auth-input').forEach(function (inp) {
        inp.addEventListener('keydown', function (e) {
          if (e.key === 'Enter') { if (tab === 'signup') doSignup(); else doLogin(); }
        });
      });

      // Forgot password
      const forgot = overlay.querySelector('#ef-forgot');
      if (forgot) forgot.addEventListener('click', function (e) { e.preventDefault(); doForgot(); });

      // Focus first field
      setTimeout(function () {
        const first = overlay.querySelector(tab === 'signup' ? '#ef-name' : '#ef-email');
        if (first) first.focus();
      }, 80);
    }

    render();
  }

  // ── Init ─────────────────────────────────────────────────────
  setup();

  // ── Public API ────────────────────────────────────────────────
  return {
    enabled: ENABLED,

    onReady: function (cb) {
      if (_ready) { cb(_user, _profile); } else { _readyCbs.push(cb); }
    },

    onChange: function (cb) {
      _changeCbs.push(cb);
    },

    getUser:    function () { return _user; },
    getProfile: function () { return _profile; },

    // ── Plusieurs profils par compte ──────────────────────────
    getProfiles:  function () { return profilesList(); },
    getActivePid: function () { return _activeId; },

    switchProfile: function (pid, cb) {
      if (!_user || !_db || !_profiles[pid]) { if (cb) cb(null); return; }
      _activeId = pid;
      _profile  = Object.assign({}, _profiles[pid], { pid });
      _db.ref('users/' + _user.uid + '/activeProfile').set(pid).catch(function () {});
      fireChange();
      if (cb) cb(_profile);
    },

    createProfile: function (data, cb) {
      if (!_user || !_db) { if (cb) cb(null); return; }
      const profile = blankProfile(_user.uid, data);
      const pid = profile.pid;
      _profiles[pid] = profile;
      _activeId = pid;
      _profile  = profile;
      const updates = {};
      updates['users/' + _user.uid + '/profiles/' + pid] = profile;
      updates['users/' + _user.uid + '/activeProfile']   = pid;
      _db.ref().update(updates)
        .then(function () { fireChange(); if (cb) cb(profile); })
        .catch(function () { if (cb) cb(null); });
    },

    deleteProfile: function (pid, cb) {
      if (!_user || !_db || !_profiles[pid]) { if (cb) cb(false, 'introuvable'); return; }
      if (Object.keys(_profiles).length <= 1) { if (cb) cb(false, 'dernier'); return; }
      delete _profiles[pid];
      const updates = {};
      updates['users/' + _user.uid + '/profiles/' + pid] = null;
      if (_activeId === pid) {
        _activeId = Object.keys(_profiles)[0];
        _profile  = Object.assign({}, _profiles[_activeId], { pid: _activeId });
        updates['users/' + _user.uid + '/activeProfile'] = _activeId;
      }
      _db.ref().update(updates)
        .then(function () { fireChange(); if (cb) cb(true, _activeId); })
        .catch(function () { if (cb) cb(false, 'erreur'); });
    },

    saveProfile: function (data, cb) {
      if (!_user || !_db || !_activeId) { if (cb) cb(false); return; }
      clearTimeout(window._efSaveTimer);
      window._efSaveTimer = setTimeout(function () {
        writeActive(data, cb);
      }, 1200);
    },

    saveProfileNow: function (data, cb) {
      writeActive(data, cb);
    },

    showAuthModal: showAuthModal,

    signOut: function () {
      if (_auth) {
        _auth.signOut().then(function () {
          _user = null;
          _profile = null;
          window.location.reload();
        });
      }
    },

    // deleteAccount(password, cb) — le mot de passe sert à se ré-authentifier
    // (Firebase exige une connexion récente pour supprimer un compte).
    // Ancienne signature deleteAccount(cb) encore acceptée.
    deleteAccount: function (password, cb) {
      if (typeof password === 'function') { cb = password; password = null; }
      if (!_auth || !_auth.currentUser) { if (cb) cb(false, 'non-connecté'); return; }
      const user = _auth.currentUser;
      const uid  = user.uid;

      function finish() {
        _user = null; _profile = null; _profiles = {}; _activeId = null; _loadedUid = null;
        if (cb) cb(true);
      }

      function wipeThenDelete() {
        // On efface les données pendant qu'on est encore authentifié,
        // puis on supprime le compte Auth.
        function deleteAuthUser() {
          user.delete()
            .then(finish)
            .catch(function (err) { if (cb) cb(false, err.code || 'delete-failed'); });
        }
        if (_db) {
          _db.ref('users/' + uid).remove().then(deleteAuthUser).catch(deleteAuthUser);
        } else {
          deleteAuthUser();
        }
      }

      if (password && user.email && window.firebase &&
          firebase.auth && firebase.auth.EmailAuthProvider) {
        const cred = firebase.auth.EmailAuthProvider.credential(user.email, password);
        user.reauthenticateWithCredential(cred)
          .then(wipeThenDelete)
          .catch(function (err) {
            const bad = err.code === 'auth/wrong-password' ||
                        err.code === 'auth/invalid-credential' ||
                        err.code === 'auth/invalid-login-credentials';
            if (cb) cb(false, bad ? 'mauvais-mot-de-passe' : (err.code || 'reauth-failed'));
          });
      } else {
        wipeThenDelete();
      }
    },
  };
})();
