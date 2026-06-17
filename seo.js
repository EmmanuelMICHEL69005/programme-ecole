(function () {
  'use strict';

  var BASE = 'https://ecolefacile.fr';
  var fname = location.pathname.split('/').pop() || 'index.html';

  // ── Breadcrumb mapping ────────────────────────────────────────
  var LEVELS = {
    'cp': 'CP', 'ce1': 'CE1', 'ce2': 'CE2',
    'cm1': 'CM1', 'cm2': 'CM2', '6e': '6ème'
  };
  function detectLevel(f) {
    for (var l in LEVELS) {
      if (f.indexOf('-' + l + '.') > -1 || f.indexOf('-' + l + '-') > -1 ||
          f.endsWith('-' + l + '.html') || f.startsWith(l + '-')) return l;
    }
    if (f.startsWith('fiche')) return 'ce2';
    if (/^(calcul|mesures|geometrie|temps|donnees|problemes|tables|symetrie|solides|nombres|division|multiplication)\.html$/.test(f)) return 'ce2';
    return null;
  }
  var isCours = fname.startsWith('cours-');
  var level = detectLevel(fname);

  // ── Inject JSON-LD breadcrumb ────────────────────────────────
  function addSchema(obj) {
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.text = JSON.stringify(obj);
    document.head.appendChild(s);
  }

  var items = [{ '@type': 'ListItem', 'position': 1, 'name': 'Accueil', 'item': BASE + '/' }];
  if (level) {
    items.push({ '@type': 'ListItem', 'position': 2, 'name': LEVELS[level], 'item': BASE + '/programme-' + level + '.html' });
  }
  var pageTitle = document.title.replace(' | École Facile', '').replace('— École Facile', '').trim();
  items.push({ '@type': 'ListItem', 'position': items.length + 1, 'name': pageTitle, 'item': BASE + '/' + fname });

  addSchema({ '@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items });

  // ── EducationalResource schema ────────────────────────────────
  var desc = (document.querySelector('meta[name="description"]') || {}).content || '';
  if (fname !== 'index.html') {
    var type = isCours ? 'Course' : 'Quiz';
    addSchema({
      '@context': 'https://schema.org',
      '@type': type,
      'name': pageTitle,
      'description': desc,
      'url': BASE + '/' + fname,
      'inLanguage': 'fr',
      'provider': { '@type': 'Organization', 'name': 'École Facile', 'url': BASE },
      'educationalLevel': level ? LEVELS[level] : 'Primaire',
      'teaches': pageTitle,
      'isAccessibleForFree': true
    });
  }

  // ── Visual breadcrumb bar ────────────────────────────────────
  if (fname === 'index.html') return;
  var bar = document.createElement('nav');
  bar.setAttribute('aria-label', 'Fil d\'Ariane');
  bar.style.cssText = 'padding:4px 18px 8px;font-size:.72rem;font-weight:800;color:#9ca3af;display:flex;align-items:center;gap:5px;flex-wrap:wrap';
  var crumbs = [{ label: 'Accueil', href: 'index.html' }];
  if (level) crumbs.push({ label: LEVELS[level], href: 'programme-' + level + '.html' });
  if (isCours) crumbs.push({ label: 'Cours', href: 'programme-' + level + '.html' });
  crumbs.push({ label: pageTitle.split('—')[0].trim(), href: null });

  bar.innerHTML = crumbs.map(function (c, i) {
    var sep = i > 0 ? '<span style="color:#c4b5fd">›</span>' : '';
    if (c.href) return sep + '<a href="' + c.href + '" style="color:#7c3aed;text-decoration:none;font-weight:900">' + c.label + '</a>';
    return sep + '<span style="color:#1e1b4b">' + c.label + '</span>';
  }).join('');

  var header = document.querySelector('.site-header, .cours-header');
  if (header && header.nextSibling) {
    header.parentNode.insertBefore(bar, header.nextSibling);
  } else {
    document.body.insertBefore(bar, document.body.firstChild);
  }
})();
