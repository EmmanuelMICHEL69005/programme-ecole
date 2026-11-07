#!/usr/bin/env python3
"""
École Facile : une seule source pour la liste des pages + versions automatiques.

    python3 tools/build_site.py           # régénère pages.js et les ?v= des fichiers
    python3 tools/build_site.py --check   # signale seulement les incohérences

- pages.js     : window.EF_PAGES, généré depuis les pages elles-mêmes
                 (niveau, matière, titre, leçon associée). Utilisé par le menu,
                 le lien « Revoir la leçon » et le lien « Faire les exercices ».
- ?v=...       : empreinte du contenu de chaque fichier CSS/JS. Plus de numéros
                 à incrémenter à la main, et un conflit de version se règle en
                 relançant simplement ce script.
"""
import hashlib, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

LEVELS = ['cp', 'ce1', 'ce2', 'cm1', 'cm2', '6e', '5e', '4e', '3e']
LEVEL_LABEL = {'cp': 'CP', 'ce1': 'CE1', 'ce2': 'CE2', 'cm1': 'CM1', 'cm2': 'CM2', '6e': '6e', '5e': '5e', '4e': '4e', '3e': '3e'}
LEGACY_CE2 = {'nombres', 'calcul', 'calcul-mental', 'problemes', 'mesures', 'temps', 'geometrie', 'solides', 'donnees', 'fiche1', 'fiche2', 'fiche3'}
SUBJECT = {
    'francais': {'conjugaison', 'grammaire', 'orthographe', 'vocabulaire'},
    'histoire-geo': {'histoire-geo', 'geographie', 'moyen-age', 'histoire-contemporaine', 'antiquite'},
    'anglais': {'anglais'},
    'eps': {'eps-cycle2', 'eps-cycle3'},
}
SKIP = {'index', 'cours', 'profile', '404'}

def subject_of(theme):
    for sub, themes in SUBJECT.items():
        if theme in themes:
            return sub
    return 'maths'

def split_name(base):
    m = re.match(r'^(.*)-(' + '|'.join(LEVELS) + r')$', base)
    if m:
        return m.group(1), m.group(2)
    if base in LEGACY_CE2:
        return base, 'ce2'
    if base == 'eps-cycle2':
        return base, 'cp'
    if base == 'eps-cycle3':
        return base, 'cm1'
    return base, None

def h1_of(text):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''

def build_registry():
    pages, lessons_from_programme = [], {}
    for f in sorted(os.listdir('.')):
        if not f.endswith('.html'):
            continue
        text = open(f, encoding='utf-8').read()
        if f.startswith('programme-'):
            for links in re.findall(r'<div class="pil-links">(.*?)</div>', text):
                ex = re.search(r'href="([^"]+)" class="pil-ex"', links)
                co = re.search(r'href="([^"]+)" class="pil-cours"', links)
                if ex and co:
                    lessons_from_programme[ex.group(1)] = co.group(1)
    for f in sorted(os.listdir('.')):
        if not f.endswith('.html'):
            continue
        base = f[:-5]
        if base in SKIP or base.startswith('programme-'):
            continue
        text = open(f, encoding='utf-8').read()
        kind = 'cours' if base.startswith('cours-') else ('exercices' if 'exercice-block' in text else None)
        if not kind:
            continue
        theme, level = split_name(base[6:] if kind == 'cours' else base)
        pages.append({'href': f, 'kind': kind, 'level': level, 'subject': subject_of(theme), 'theme': theme, 'title': h1_of(text)})
    by_href = {p['href']: p for p in pages}
    for p in pages:
        if p['kind'] != 'exercices':
            continue
        lesson = lessons_from_programme.get(p['href']) or ('cours-' + p['href'] if ('cours-' + p['href']) in by_href else None)
        if lesson and lesson in by_href:
            p['lesson'] = lesson
    return pages

def write_pages_js(pages):
    body = '[\n' + ',\n'.join(json.dumps(p, ensure_ascii=False, separators=(',', ':')) for p in pages) + '\n]'
    out = ('/* Généré par tools/build_site.py — ne pas modifier à la main. */\n'
           'window.EF_PAGES = ' + body + ';\n')
    old = open('pages.js', encoding='utf-8').read() if os.path.exists('pages.js') else ''
    if old != out:
        open('pages.js', 'w', encoding='utf-8').write(out)
        return True
    return False

def stamp_versions():
    assets = {}
    for f in os.listdir('.'):
        if f.endswith(('.js', '.css')) and f != 'sw.js':
            assets[f] = hashlib.sha1(open(f, 'rb').read()).hexdigest()[:8]
    pattern = re.compile(r'((?:src|href)=")(' + '|'.join(re.escape(a) for a in assets) + r')(?:\?v=[^"]*)?(")')
    changed = 0
    for f in os.listdir('.'):
        if not f.endswith('.html'):
            continue
        text = open(f, encoding='utf-8').read()
        new = pattern.sub(lambda m: f'{m.group(1)}{m.group(2)}?v={assets[m.group(2)]}{m.group(3)}', text)
        if new != text:
            open(f, 'w', encoding='utf-8').write(new)
            changed += 1
    return changed

def check(pages):
    issues = []
    index = open('index.html', encoding='utf-8').read()
    nav = open('nav.js', encoding='utf-8').read()
    for p in pages:
        if p['kind'] != 'exercices':
            continue
        if f'href="{p["href"]}"' not in index:
            issues.append(f"absente de l'accueil (carte ajoutée automatiquement via pages.js) : {p['href']}")
        if p['href'] not in nav and p['subject'] != 'francais':
            issues.append(f"absente du menu (ajoutée automatiquement via pages.js) : {p['href']}")
        if not p['level']:
            issues.append(f"niveau inconnu : {p['href']}")
    return issues

if __name__ == '__main__':
    pages = build_registry()
    issues = check(pages)
    if '--check' not in sys.argv:
        wrote = write_pages_js(pages)
        changed = stamp_versions()   # après pages.js, pour que son empreinte soit à jour
        print(f"pages.js : {len(pages)} pages{' (mis à jour)' if wrote else ''} · versions mises à jour dans {changed} fichiers HTML")
    for i in issues:
        print('·', i)
