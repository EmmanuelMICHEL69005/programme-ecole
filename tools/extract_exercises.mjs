#!/usr/bin/env node
// Extrait les données des exercices de chaque page (questions, choix, bonne réponse)
// en exécutant ses scripts dans un bac à sable, sans navigateur.
// Usage : node tools/extract_exercises.mjs page1.html page2.html … > exercices.json
// Sortie : { "page.html": { "ex1": {"type": "qcm", "items": [...]}, ... }, ... }
import fs from 'node:fs';
import vm from 'node:vm';

const TYPES = {
  buildQCM: 'qcm', buildVF: 'vf', buildOrdre: 'ordre', buildTri: 'tri', buildPaires: 'paires',
  buildQBlock: 'qblock', buildPbBlocks: 'pb', buildOpCards: 'op', buildOrdreSets: 'ordresets',
};

function stubEl() {
  const el = new Proxy(function () {}, {
    get(t, k) {
      if (k === Symbol.toPrimitive) return () => '';
      if (k === 'style' || k === 'dataset' || k === 'classList') return el;
      if (k === 'querySelectorAll' || k === 'getElementsByTagName' || k === 'getElementsByClassName') return () => [];
      if (k === 'length') return 0;
      if (k === 'innerHTML' || k === 'textContent' || k === 'value' || k === 'id' || k === 'className') return '';
      return el;
    },
    set() { return true; },
    apply() { return el; },
    construct() { return el; },
  });
  return el;
}

function extract(file) {
  const src = fs.readFileSync(file, 'utf8');
  const scripts = [...src.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)]
    .map(m => m[1]).filter(s => !/application\/ld\+json/.test(s) && s.trim());
  const out = {};
  const el = stubEl();
  const ctx = {
    console: { log() {}, warn() {}, error() {} },
    document: new Proxy({}, { get(t, k) {
      if (k === 'getElementById' || k === 'querySelector' || k === 'createElement') return () => el;
      if (k === 'querySelectorAll') return () => [];
      if (k === 'addEventListener') return () => {};
      return el;
    } }),
    location: { pathname: '/' + file, href: 'https://ecolefacile.fr/' + file, search: '', hash: '' },
    localStorage: { getItem() { return null; }, setItem() {}, removeItem() {} },
    setTimeout() {}, setInterval() {}, clearTimeout() {}, requestAnimationFrame() {},
    addEventListener() {},
    navigator: { userAgent: 'node' },
    shuffle: a => [...a], formatFrac: s => s, _EX: {},
    Math, JSON, Array, Object, String, Number, Date,
  };
  const clone = x => JSON.parse(JSON.stringify(x));
  for (const [fn, type] of Object.entries(TYPES)) {
    ctx[fn] = (data, id, ...rest) => {
      if (typeof id === 'string' && Array.isArray(data)) {
        out[id] = { type, items: clone(data) };
        if (type === 'op' && typeof rest[2] === 'string') out[id].op = rest[2];
      } else if (data && typeof data === 'object' && !Array.isArray(data) && typeof rest[0] === 'string') {
        // buildQBlock(item, conteneur, 'tab1-0') : une question à la fois, regroupées par préfixe
        const key = rest[0].replace(/-\d+$/, '');
        (out[key] = out[key] || { type: 'qcm', items: [] }).items.push(clone(data));
      }
    };
  }
  ctx.window = ctx;
  vm.createContext(ctx);
  // Les fonctions de capture doivent gagner sur une éventuelle redéfinition dans la page.
  const guard = Object.keys(TYPES).map(fn => `try{ ${fn} = __cap_${fn}; }catch(e){}`).join('\n');
  for (const fn of Object.keys(TYPES)) ctx['__cap_' + fn] = ctx[fn];
  for (const s of scripts) {
    // On neutralise les redéfinitions locales des moteurs communs (function buildQCM(…) { … })
    const code = s.replace(/function\s+(buildQCM|buildVF|buildOrdre|buildTri|buildPaires)\s*\(/g, 'function __local_$1(');
    try { vm.runInContext(guard + '\n' + code, ctx, { timeout: 2000 }); } catch (e) { /* script non essentiel : ignoré */ }
  }
  return out;
}

const result = {};
for (const f of process.argv.slice(2)) result[f] = extract(f);
process.stdout.write(JSON.stringify(result));
