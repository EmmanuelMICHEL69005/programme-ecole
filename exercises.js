/* ============================================================
   exercises.js — Moteur d'exercices interactifs
   Site École Facile
   ============================================================ */

// ── Stockage des données par ID d'exercice ──────────────────
const _EX = {};
let _combo = 0;

// ── Utilitaires ─────────────────────────────────────────────
function shuffle(a) { return [...a].sort(() => Math.random() - 0.5); }
function rnd(a) { return a[Math.floor(Math.random() * a.length)]; }
function formatFrac(s) {
  if (s === null || s === undefined) return '';
  return String(s).replace(/(\d+)\/(\d+)/g,
    '<span class="f" role="img" aria-label="$1 sur $2"><span class="fn" aria-hidden="true">$1</span><span class="fd" aria-hidden="true">$2</span></span>');
}

// ── Messages ─────────────────────────────────────────────────
const BRAVO = [
  '✅ Parfait !','✅ Excellent !','✅ Bravo !','✅ Super !',
  '✅ Génial !','✅ Trop bien !','✅ Incroyable !','✅ Tu assures !'
];
const FIRE  = ['🔥 En feu !','🔥 Combo x'+0,'⚡ Incroyable !'];

// ── Animation XP flottante ───────────────────────────────────
function _xp(el) {
  if (!window.GS_HAS_PROFILE) return; // pas de faux XP pour un invité
  const label = _combo >= 5 ? '+10 XP 🔥🔥' : _combo >= 3 ? '+10 XP 🔥' : '+10 XP';
  const r = el.getBoundingClientRect();
  const f = document.createElement('div');
  f.className = '_xpf';
  f.textContent = label;
  f.style.cssText = `left:${r.left + r.width/2 - 30}px;top:${r.top + window.scrollY - 10}px`;
  document.body.appendChild(f);
  setTimeout(() => f.remove(), 950);
}

// ── Résultat correct / incorrect ─────────────────────────────
function _ok(el, fb, correct) {
  el.classList.add('ex-correct');
  fb.innerHTML = rnd(BRAVO);
  fb.className = 'feedback-line fb-ok';
  _combo++;
  _xp(el);
}
function _focusMsg(el) {
  if (!el) return;
  el.setAttribute('tabindex', '-1');
  try { el.focus({ preventScroll: true }); } catch (e) { el.focus(); }
}
function _lessonLink() {
  return window.EF_LESSON ? ` <a class="fb-lesson" href="${window.EF_LESSON}">📖 Revoir la leçon</a>` : '';
}
function _ko(el, fb, correct, expl) {
  el.classList.add('ex-wrong');
  fb.innerHTML = '❌ La bonne réponse : ' + formatFrac(correct) + (expl ? '. ' + expl : '') + _lessonLink();
  fb.className = 'feedback-line fb-ko';
  _combo = 0;
}

// ═══════════════════════════════════════════════════════════
// 1. QCM — Questionnaire à choix multiples
// ═══════════════════════════════════════════════════════════
function buildQCM(data, containerId) {
  const container = document.getElementById(containerId);
  data.forEach((item, i) => {
    const eid = `${containerId}__${i}`;
    _EX[eid] = item;
    const d = document.createElement('div');
    d.className = 'q-block';
    d.style.animationDelay = (i * 0.07) + 's';
    const card   = item.card   ? `<div class="ex-card">${formatFrac(item.card)}</div>` : '';
    const enonce = item.enonce ? `<div class="pb-enonce">${item.enonce}</div>` : '';
    const hint   = item.hint   ? `<div class="ex-hint">💡 ${item.hint}</div>` : '';
    const sh = shuffle(item.choices);
    d.innerHTML = `${card}${enonce}
      <div class="q-text">${formatFrac(item.q)}</div>
      <div class="qcm-row" id="${containerId}-r${i}">
        ${sh.map(c => `<button class="btn-choice" data-val="${c.replace(/"/g,'&quot;')}"
          onclick="_qcmCheck(this,'${containerId}-r${i}','${containerId}-f${i}','${eid}')"
        >${formatFrac(c)}</button>`).join('')}
      </div>
      <div class="retry-line" id="${containerId}-t${i}" aria-live="polite"></div>
      <div class="feedback-line" aria-live="polite" id="${containerId}-f${i}"></div>`;
    if (/^anglais-/.test(location.pathname.split('/').pop())) d.querySelectorAll('.btn-choice').forEach(b => b.lang = 'en');
    container.appendChild(d);
  });
}
window._qcmCheck = function(btn, rowId, fbId, eid) {
  const item = _EX[eid];
  const row = document.getElementById(rowId);
  const fb = document.getElementById(fbId);
  const retry = document.getElementById(fbId.replace(/-f(\d+)$/, '-t$1'));
  const nChoices = row.querySelectorAll('.btn-choice').length;
  if (btn.dataset.val !== item.correct && !row.dataset.tried && nChoices > 2) {
    // Premier essai raté : on barre ce choix et on laisse réessayer
    row.dataset.tried = '1';
    btn.disabled = true;
    btn.classList.add('tried');
    if (retry) retry.innerHTML = '🤔 Pas tout à fait. Réessaie !' + (item.hint ? ' <span class="retry-hint">💡 ' + item.hint + '</span>' : '');
    const other = [...row.querySelectorAll('.btn-choice')].find(b => !b.disabled);
    if (other) other.focus();
    return;
  }
  row.querySelectorAll('.btn-choice').forEach(b => b.disabled = true);
  if (retry) retry.innerHTML = '';
  if (btn.dataset.val === item.correct && row.dataset.tried) {
    btn.classList.add('correct');
    fb.innerHTML = '👍 Trouvé au deuxième essai !' + (item.expl ? ' ' + item.expl : '');
    fb.className = 'feedback-line fb-ok2';
    _combo = 0;
  } else if (btn.dataset.val === item.correct) {
    btn.classList.add('correct');
    _ok(btn, fb, item.correct);
  } else {
    btn.classList.add('wrong');
    row.querySelectorAll('.btn-choice').forEach(b => {
      if (b.dataset.val === item.correct) b.classList.add('correct');
    });
    _ko(btn, fb, item.correct, item.expl);
  }
  _focusMsg(fb);
};

// ═══════════════════════════════════════════════════════════
// 2. Vrai / Faux
// ═══════════════════════════════════════════════════════════
function buildVF(data, containerId) {
  const container = document.getElementById(containerId);
  data.forEach((item, i) => {
    const eid = `${containerId}__${i}`;
    _EX[eid] = item;
    const d = document.createElement('div');
    d.className = 'q-block';
    d.style.animationDelay = (i * 0.07) + 's';
    const card   = item.card   ? `<div class="ex-card">${formatFrac(item.card)}</div>` : '';
    const enonce = item.enonce ? `<div class="pb-enonce">${item.enonce}</div>` : '';
    d.innerHTML = `${card}${enonce}
      <div class="q-text">${formatFrac(item.q)}</div>
      <div class="qcm-row vf-row" id="${containerId}-r${i}" style="gap:16px">
        <button class="btn-choice btn-vrai" data-val="vrai"
          onclick="_vfCheck(this,'${containerId}-r${i}','${containerId}-f${i}','${eid}')">✓ Vrai</button>
        <button class="btn-choice btn-faux" data-val="faux"
          onclick="_vfCheck(this,'${containerId}-r${i}','${containerId}-f${i}','${eid}')">✗ Faux</button>
      </div>
      <div class="retry-line" id="${containerId}-t${i}" aria-live="polite"></div>
      <div class="feedback-line" aria-live="polite" id="${containerId}-f${i}"></div>`;
    container.appendChild(d);
  });
}
window._vfCheck = function(btn, rowId, fbId, eid) {
  const item = _EX[eid];
  document.getElementById(rowId).querySelectorAll('.btn-choice').forEach(b => b.disabled = true);
  const fb = document.getElementById(fbId);
  const expected = item.correct ? 'vrai' : 'faux';
  if (btn.dataset.val === expected) {
    btn.classList.add('correct');
    _ok(btn, fb, expected);
  } else {
    btn.classList.add('wrong');
    document.getElementById(rowId).querySelectorAll('.btn-choice').forEach(b => {
      if (b.dataset.val === expected) b.classList.add('correct');
    });
    const expl = item.expl ? `. ${item.expl}` : '';
    fb.innerHTML = '❌ C\'était ' + (item.correct ? 'Vrai' : 'Faux') + expl + _lessonLink();
    fb.className = 'feedback-line fb-ko';
    _combo = 0;
  }
  _focusMsg(fb);
};

// ═══════════════════════════════════════════════════════════
// 3. Ordre — Cliquer dans le bon ordre
// ═══════════════════════════════════════════════════════════
function buildOrdre(data, containerId) {
  const container = document.getElementById(containerId);
  data.forEach((item, i) => {
    const eid = `${containerId}__${i}`;
    _EX[eid] = item;
    const d = document.createElement('div');
    d.className = 'q-block';
    d.style.animationDelay = (i * 0.07) + 's';
    const poolId = `${containerId}-op${i}`;
    const zoneId = `${containerId}-oz${i}`;
    const sh = shuffle([...item.items]);
    d.innerHTML = `
      <div class="q-text">${item.q}</div>
      <div class="ordre-pool" id="${poolId}">
        ${sh.map(v => `<button class="ordre-item" data-val="${v.replace(/"/g,'&quot;')}"
          onclick="_ordreAdd(this,'${poolId}','${zoneId}')">${formatFrac(v)}</button>`).join('')}
      </div>
      <div class="ordre-hint">Touche les éléments dans le bon ordre ↓ (touche un élément placé pour l'enlever)</div>
      <div class="ordre-zone" id="${zoneId}"></div>
      <div class="ex-actions">
        <button class="btn-validate" onclick="_ordreCheck('${poolId}','${zoneId}','${containerId}-f${i}','${eid}')">Valider ✔</button>
        <button class="btn-reset" onclick="_ordreReset('${poolId}','${zoneId}')">↺ Recommencer</button>
      </div>
      <div class="retry-line" id="${containerId}-t${i}" aria-live="polite"></div>
      <div class="feedback-line" aria-live="polite" id="${containerId}-f${i}"></div>`;
    container.appendChild(d);
  });
}
window._ordreAdd = function(btn, poolId, zoneId) {
  if (btn.classList.contains('used') || btn.disabled) return;
  btn.classList.add('used');
  const zone = document.getElementById(zoneId);
  const chip = document.createElement('button');
  chip.className = 'ordre-chip';
  chip.dataset.val = btn.dataset.val;
  chip.innerHTML = btn.innerHTML;
  chip.onclick = () => { btn.classList.remove('used'); chip.remove(); };
  zone.appendChild(chip);
};
window._ordreCheck = function(poolId, zoneId, fbId, eid) {
  const item = _EX[eid];
  const zone = document.getElementById(zoneId);
  const chips = [...zone.querySelectorAll('.ordre-chip')];
  const chosen = chips.map(c => c.dataset.val);
  const fb = document.getElementById(fbId);
  const retry = document.getElementById(fbId.replace(/-f(\d+)$/, '-t$1'));
  if (chosen.length < item.items.length) {
    if (retry) retry.innerHTML = '⚠️ Place tous les éléments d\'abord !';
    return;
  }
  const ok = chosen.every((v, j) => v === item.items[j]);
  chips.forEach((c, j) => {
    const good = c.dataset.val === item.items[j];
    c.classList.toggle('ok', good); c.classList.toggle('ko', !good);
  });
  if (!ok && !zone.dataset.tried) {
    // 2e essai : on garde le début juste, on rend le reste à placer
    zone.dataset.tried = '1';
    const k = chosen.findIndex((v, j) => v !== item.items[j]);
    chips.slice(k).forEach(c => { if (c.onclick) c.onclick(); else c.remove(); });
    chips.slice(0, k).forEach(c => { c.classList.add('ok'); c.classList.remove('ko'); });
    if (retry) retry.innerHTML = k > 0
      ? '🤔 Le début est juste (✓). Replace la suite dans le bon ordre, puis valide.'
      : '🤔 Pas tout à fait. Recommence depuis le début, dans le bon ordre, puis valide.';
    return;
  }
  if (retry) retry.innerHTML = '';
  document.getElementById(poolId).querySelectorAll('.ordre-item').forEach(b => { b.disabled = true; b.onclick = null; });
  chips.forEach(c => c.onclick = null);
  if (ok && zone.dataset.tried) {
    fb.innerHTML = '👍 Trouvé au deuxième essai !';
    fb.className = 'feedback-line fb-ok2';
    _combo = 0;
  } else if (ok) {
    _ok(zone, fb, '');
    fb.innerHTML = rnd(BRAVO);
    fb.className = 'feedback-line fb-ok';
  } else {
    fb.innerHTML = '❌ Le bon ordre : ' + item.items.map(v => formatFrac(v)).join(' → ') + (item.expl ? '. ' + item.expl : '') + _lessonLink();
    fb.className = 'feedback-line fb-ko';
    _combo = 0;
  }
};
window._ordreReset = function(poolId, zoneId) {
  document.getElementById(poolId).querySelectorAll('.ordre-item').forEach(b => {
    b.classList.remove('used'); b.disabled = false;
  });
  document.getElementById(zoneId).innerHTML = '';
};

// ═══════════════════════════════════════════════════════════
// 4. Tri — Classer par catégorie (clic pour sélectionner, clic colonne pour placer)
// ═══════════════════════════════════════════════════════════
let _triSel = null;
let _triSelGrid = null;
function buildTri(data, containerId) {
  const container = document.getElementById(containerId);
  data.forEach((item, i) => {
    const eid = `${containerId}__${i}`;
    _EX[eid] = item;
    const d = document.createElement('div');
    d.className = 'q-block';
    d.style.animationDelay = (i * 0.07) + 's';
    const poolId = `${containerId}-tp${i}`;
    const gridId = `${containerId}-tg${i}`;
    const sh = shuffle([...item.items]);
    const colsHtml = item.cats.map((cat, ci) => `
      <div class="tri-col" data-cat="${cat}" role="button" tabindex="0" aria-label="Colonne ${cat.replace(/<[^>]+>/g,'')}"
           onclick="_triDrop('${poolId}','${containerId}-tc${i}-${ci}','${gridId}')"
           onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();this.click();}">
        <div class="tri-col-title">${cat}</div>
        <div class="tri-col-items" id="${containerId}-tc${i}-${ci}"></div>
      </div>`).join('');
    d.innerHTML = `
      <div class="q-text">${item.q}</div>
      <div class="tri-pool" id="${poolId}">
        ${sh.map(it => `<button class="tri-chip" data-val="${it.v.replace(/"/g,'&quot;')}" data-cat="${it.cat}"
          onclick="_triPick(this,'${gridId}')">${formatFrac(it.v)}</button>`).join('')}
      </div>
      <div class="tri-hint">Touche un élément, puis la colonne où il va</div>
      <div class="tri-grid" id="${gridId}">${colsHtml}</div>
      <div class="ex-actions">
        <button class="btn-validate" onclick="_triCheck('${poolId}','${gridId}','${containerId}-f${i}','${eid}')">Valider ✔</button>
      </div>
      <div class="retry-line" id="${containerId}-t${i}" aria-live="polite"></div>
      <div class="feedback-line" aria-live="polite" id="${containerId}-f${i}"></div>`;
    container.appendChild(d);
  });
}
window._triPick = function(btn, gridId) {
  if (btn.classList.contains('tri-used')) return;
  document.querySelectorAll('.tri-chip.tri-sel').forEach(b => b.classList.remove('tri-sel'));
  document.querySelectorAll('.tri-col.tri-target').forEach(c => c.classList.remove('tri-target'));
  _triSel = btn;
  _triSelGrid = gridId;
  btn.classList.add('tri-sel');
  document.getElementById(gridId).querySelectorAll('.tri-col').forEach(c => c.classList.add('tri-target'));
};
window._triDrop = function(poolId, colItemsId, gridId) {
  if (!_triSel || _triSelGrid !== gridId) return;
  const colItems = document.getElementById(colItemsId);
  const chip = document.createElement('div');
  chip.className = 'tri-placed';
  chip.innerHTML = formatFrac(_triSel.dataset.val);
  chip.dataset.val = _triSel.dataset.val;
  chip.dataset.cat = _triSel.dataset.cat;
  const src = _triSel;
  chip.onclick = (e) => { e.stopPropagation(); src.classList.remove('tri-used', 'tri-sel'); chip.remove(); };
  colItems.appendChild(chip);
  _triSel.classList.add('tri-used');
  _triSel.classList.remove('tri-sel');
  _triSel = null;
  document.getElementById(gridId).querySelectorAll('.tri-col').forEach(c => c.classList.remove('tri-target'));
};
window._triCheck = function(poolId, gridId, fbId, eid) {
  const item = _EX[eid];
  const grid = document.getElementById(gridId);
  const pool = document.getElementById(poolId);
  const fb = document.getElementById(fbId);
  const retry = document.getElementById(fbId.replace(/-f(\d+)$/, '-t$1'));
  if (grid.querySelectorAll('.tri-placed').length < item.items.length) {
    if (retry) retry.innerHTML = '⚠️ Place tous les éléments d\'abord !';
    return;
  }
  const bad = [];
  grid.querySelectorAll('.tri-col').forEach(col => {
    col.querySelectorAll('.tri-placed').forEach(chip => {
      const good = chip.dataset.cat === col.dataset.cat;
      chip.classList.toggle('ok', good); chip.classList.toggle('ko', !good);
      if (!good) bad.push(chip);
    });
  });
  if (bad.length && !grid.dataset.tried) {
    grid.dataset.tried = '1';
    if (retry) retry.innerHTML = '🤔 ' + (bad.length > 1
      ? bad.length + ' éléments sont mal placés (marqués ✗). Touche-les pour les reprendre, replace-les, puis valide.'
      : '1 élément est mal placé (marqué ✗). Touche-le pour le reprendre, replace-le, puis valide.');
    return;
  }
  if (retry) retry.innerHTML = '';
  grid.querySelectorAll('.tri-placed').forEach(c => c.onclick = null);
  pool.querySelectorAll('.tri-chip').forEach(b => { b.disabled = true; b.onclick = null; });
  grid.querySelectorAll('.tri-col').forEach(c => { c.onclick = null; c.classList.remove('tri-target'); });
  if (!bad.length && grid.dataset.tried) {
    fb.innerHTML = '👍 Trouvé au deuxième essai !'; fb.className = 'feedback-line fb-ok2'; _combo = 0;
  } else if (!bad.length) {
    _ok(grid, fb, ''); fb.innerHTML = rnd(BRAVO); fb.className = 'feedback-line fb-ok';
  } else {
    const answer = item.cats.map(c => '<b>' + c + '</b> : ' + item.items.filter(it => it.cat === c).map(it => formatFrac(it.v)).join(', ')).join(' · ');
    fb.innerHTML = '❌ La bonne réponse : ' + answer + '.' + _lessonLink();
    fb.className = 'feedback-line fb-ko'; _combo = 0;
  }
};


// ═══════════════════════════════════════════════════════════
// 5. Paires — Associer deux colonnes
// ═══════════════════════════════════════════════════════════
let _pairSel = null;
function buildPaires(data, containerId) {
  const container = document.getElementById(containerId);
  // Format court accepté : [{left, right}, …] = un seul tableau de paires
  if (data.length && !data[0].pairs && 'left' in data[0]) {
    data = [{ q: 'Relie chaque élément à celui qui lui correspond.', pairs: data.map(p => [p.left, p.right]) }];
  }
  data.forEach((item, i) => {
    const eid = `${containerId}__${i}`;
    _EX[eid] = item;
    const d = document.createElement('div');
    d.className = 'q-block';
    d.style.animationDelay = (i * 0.07) + 's';
    const wrapId = `${containerId}-pw${i}`;
    const lefts  = shuffle(item.pairs.map(p => p[0]));
    const rights = shuffle(item.pairs.map(p => p[1]));
    d.innerHTML = `
      <div class="q-text">${item.q}</div>
      <div class="tri-hint">Touche un élément à gauche, puis celui qui va avec à droite ↓</div>
      <div class="paires-wrap" id="${wrapId}">
        <div class="paires-col">
          ${lefts.map(v => `<button class="paires-btn" data-val="${v.replace(/"/g,'&quot;')}" data-side="L"
            onclick="_pairClick(this,'${wrapId}','${containerId}-f${i}','${eid}')">${formatFrac(v)}</button>`).join('')}
        </div>
        <div class="paires-col">
          ${rights.map(v => `<button class="paires-btn" data-val="${v.replace(/"/g,'&quot;')}" data-side="R"
            onclick="_pairClick(this,'${wrapId}','${containerId}-f${i}','${eid}')">${formatFrac(v)}</button>`).join('')}
        </div>
      </div>
      <div class="retry-line" id="${containerId}-t${i}" aria-live="polite"></div>
      <div class="feedback-line" aria-live="polite" id="${containerId}-f${i}"></div>`;
    container.appendChild(d);
  });
}
window._pairClick = function(btn, wrapId, fbId, eid) {
  if (btn.classList.contains('p-ok')) return;
  const item = _EX[eid];
  const wrap = document.getElementById(wrapId);
  if (btn.dataset.side === 'L') {
    document.querySelectorAll('.paires-btn.p-sel').forEach(b => b.classList.remove('p-sel'));
    _pairSel = btn; btn.classList.add('p-sel');
  } else {
    if (!_pairSel || !wrap.contains(_pairSel)) { _pairSel = null; return; }
    const lv = _pairSel.dataset.val, rv = btn.dataset.val;
    const matched = item.pairs.some(p => p[0] === lv && p[1] === rv);
    if (matched) {
      [_pairSel, btn].forEach(b => { b.classList.remove('p-sel'); b.classList.add('p-ok'); b.disabled = true; });
      _pairSel = null; _combo++; _xp(btn);
      const all = wrap.querySelectorAll('.paires-btn');
      if ([...all].every(b => b.classList.contains('p-ok'))) {
        const fb = document.getElementById(fbId);
        fb.innerHTML = rnd(BRAVO); fb.className = 'feedback-line fb-ok';
      }
    } else {
      [btn, _pairSel].forEach(b => b.classList.add('p-ko'));
      setTimeout(() => {
        [btn, _pairSel].forEach(b => b.classList.remove('p-ko'));
        _pairSel.classList.remove('p-sel'); _pairSel = null;
      }, 600);
      _combo = 0;
    }
  }
};

// ═══════════════════════════════════════════════════════════
// 6. Complétion — Choisir le nombre manquant (variante QCM visuelle)
// ═══════════════════════════════════════════════════════════
function buildCompletion(data, containerId) {
  buildQCM(data, containerId); // même moteur, la mise en valeur est dans item.q avec ☐
}
