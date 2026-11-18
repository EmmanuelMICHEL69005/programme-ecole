#!/usr/bin/env node
// Calcule, pour chaque page, le bloc « Voir aussi » que related.js injecte dans le navigateur,
// afin de l'écrire directement dans le HTML (liens visibles par les moteurs sans JavaScript).
// Usage : node tools/render_related.mjs page1.html … > related.json   →  { "page.html": "<section …>" }
import fs from 'node:fs';
import vm from 'node:vm';

const code = fs.readFileSync('related.js', 'utf8');
const result = {};
for (const file of process.argv.slice(2)) {
  let html = '';
  const main = { insertAdjacentHTML(pos, h) { html = h; } };
  const ctx = {
    window: { location: { pathname: '/' + file } },
    document: {
      head: { insertAdjacentHTML() {} },
      querySelector(sel) { return sel === 'main' ? main : null; },
    },
  };
  ctx.window.document = ctx.document;
  vm.createContext(ctx);
  try { vm.runInContext(code, ctx, { timeout: 2000 }); } catch (e) { /* page sans bloc */ }
  if (html) result[file] = html;
}
process.stdout.write(JSON.stringify(result));
