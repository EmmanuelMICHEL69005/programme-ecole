#!/usr/bin/env python3
"""
École Facile : écrit dans le HTML ce que le JavaScript ajoute dans le navigateur,
pour que les moteurs de recherche voient le vrai contenu des pages.

Appelé par tools/build_site.py (ne pas lancer seul, sauf pour tester) :
- pages d'exercices : une introduction (compétences travaillées, liens leçon et programme),
  le corrigé complet des questions (bloc repliable « Corrigé pour les parents »),
  un titre et une meta description propres à la page ;
- toutes les pages qui chargent related.js : le bloc « Voir aussi » en HTML.

Les questions sont lues dans les scripts de chaque page par tools/extract_exercises.mjs
(Node.js). Sans Node, les blocs déjà écrits sont conservés tels quels.
Chaque bloc est encadré de commentaires <!-- ef:… --> et régénéré à l'identique.
"""
import html, json, re, shutil, subprocess

LEVEL_LABEL = {'cp': 'CP', 'ce1': 'CE1', 'ce2': 'CE2', 'cm1': 'CM1', 'cm2': 'CM2', '6e': '6e', '5e': '5e', '4e': '4e', '3e': '3e'}
SUBJECT_PHRASE = {'maths': 'de maths', 'francais': 'de français', 'histoire-geo': "d'histoire-géographie",
                  'anglais': "d'anglais", 'eps': "d'EPS"}
GENERIC_TITLES = {'vrai ou faux', 'qcm', 'quiz', 'mélange', 'bilan', 'révisions', 'révision', 'défi', 'défi final'}
# Premiers mots à garder avec leur majuscule (noms propres, sigles, anglais)
KEEP_CAP = {'athènes', 'rome', 'napoléon', 'louis', 'pythagore', 'thalès', "l'antiquité", "l'empire", "l'égypte",
            'xixe', 'cod', 'cc', 'pp', 'be', 'can', 'for', 'in', 'must', 'past', 'present', 'reported', 'so', 'some',
            'some-', 'there', 'too', 'used', 'was', 'who', 'will'}
OPS = {'add': '+', 'sub': '−', 'mul': '×', 'div': '÷'}


def level_phrase(p):
    if p['theme'] == 'eps-cycle2':
        return 'pour le cycle 2 (CP, CE1, CE2)'
    if p['theme'] == 'eps-cycle3':
        return 'pour le cycle 3 (CM1, CM2, 6e)'
    lvl = LEVEL_LABEL.get(p['level'] or '', '')
    if not lvl:
        return ''
    return ('en ' if lvl[0].isdigit() else 'au ') + lvl


def text(s):
    """Texte brut et échappé d'un champ (qui peut contenir un peu de HTML)."""
    if s is None:
        return ''
    if isinstance(s, bool):
        return 'Vrai' if s else 'Faux'
    s = re.sub(r'<br\s*/?>', ' ', str(s))
    s = html.unescape(re.sub(r'<[^>]+>', '', s))
    return html.escape(re.sub(r'\s+', ' ', s).strip(), quote=False)


def plain(s):
    """Texte brut (non échappé)."""
    s = re.sub(r'<br\s*/?>', ' ', str(s or ''))
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def block_title(h2_inner):
    t = re.sub(r'<span class="ex-badge"[^>]*>.*?</span>', '', h2_inner, flags=re.S)
    t = re.sub(r'<span style="margin-left:auto[^>]*>.*?</span>', '', t, flags=re.S)
    return plain(t)


def parse_blocks(page_html):
    """[(titre, {ids des conteneurs du bloc})] dans l'ordre de la page."""
    blocks = []
    parts = page_html.split('class="exercice-block"')[1:]
    for part in parts:
        h2 = re.search(r'<h2 class="ex-title"[^>]*>(.*?)</h2>', part, re.S)
        ids = set(re.findall(r'id="([^"]+)"', part.split('class="exercice-block"')[0][:4000]))
        blocks.append((block_title(h2.group(1)) if h2 else '', ids))
    return blocks


def join_q(*parts):
    """Énoncé, consigne puis support (« Calcule : 34 + 25 = ? »)."""
    out = ''
    for x in parts:
        if not x:
            continue
        if out:
            out += ' ' if out[-1] in '?:.!…»)' else ' : '
        out += x
    return out


def item_html(ex, it):
    t = ex['type']
    li = lambda q, a, extra='': f'<li>{q} <span class="cr-a">→ <strong>{a}</strong></span>{extra}</li>'
    if t in ('qcm', 'pb'):
        q = join_q(text(it.get('enonce')), text(it.get('formule')), text(it.get('q') or it.get('question')), text(it.get('card')))
        if it.get('tableau'):
            q += ' ' + text(it['tableau'])
        return li(q, text(it.get('correct')))
    if t == 'vf':
        expl = f' <span class="cr-x">{text(it["expl"])}</span>' if it.get('expl') else ''
        q = join_q(text(it.get('enonce')), text(it.get('q')), text(it.get('card')))
        return li(q, text(bool(it.get('correct'))), expl)
    if t == 'ordre':
        return li(text(it.get('q')), ' → '.join(text(v) for v in it.get('items', [])))
    if t == 'paires':
        pairs = it.get('pairs') or ([[it['left'], it['right']]] if 'left' in it else [])
        inner = ''.join(f'<li>{text(a)} ↔ <strong>{text(b)}</strong></li>' for a, b in pairs)
        return f'<li>{text(it.get("q")) or "Relie chaque élément à celui qui lui correspond."}<ul>{inner}</ul></li>'
    if t == 'tri':
        by_cat = {}
        for x in it.get('items', []):
            by_cat.setdefault(x.get('cat'), []).append(text(x.get('v')))
        inner = ''.join(f'<li><strong>{text(c)}</strong> : {", ".join(by_cat.get(c, []))}</li>' for c in it.get('cats', []))
        return f'<li>{text(it.get("q"))}<ul>{inner}</ul></li>'
    if t == 'op':
        return li(f'{it.get("a")} {OPS.get(ex.get("op"), "?")} {it.get("b")} = ?', text(it.get('result')))
    return ''


def short_paires(ex):
    # Format court de buildPaires : une liste de {left, right} = un seul exercice
    if ex['type'] == 'paires' and ex['items'] and 'left' in ex['items'][0]:
        return [{'q': 'Relie chaque élément à celui qui lui correspond.', 'pairs': [[i['left'], i['right']] for i in ex['items']]}]
    return ex['items']


def build_exercise_page(page_html, p, exs):
    blocks = parse_blocks(page_html)
    level = level_phrase(p)
    subj = SUBJECT_PHRASE.get(p['subject'], '')
    # Rattache chaque exercice extrait à son bloc (même conteneur, sinon même rang)
    keyed = []
    for k, ex in exs.items():
        idx = next((i for i, (_, ids) in enumerate(blocks) if k in ids), None)
        if idx is None:
            m = re.match(r'^(?:tab|ex)(\d+)', k)
            idx = int(m.group(1)) - 1 if m and int(m.group(1)) - 1 < len(blocks) else None
        keyed.append((idx if idx is not None else 999, k, ex))
    keyed.sort(key=lambda x: (x[0], x[1]))
    n_q = sum(len(short_paires(ex)) for _, _, ex in keyed)
    skills, seen = [], set()
    for title, _ in blocks:
        t = title.strip(' .')
        low = t.lower()
        if t and low not in GENERIC_TITLES and low not in seen:
            seen.add(low)
            first = low.split()[0].strip(',;:')
            keep = p['subject'] == 'anglais' or first in KEEP_CAP or t[:2].isupper()
            skills.append(t if keep else t[0].lower() + t[1:])
    n_ex = len(blocks)
    s = 's' if n_ex > 1 else ''
    q_part = f', soit {n_q} questions' if n_q > n_ex else ''
    skills_txt = html.escape(', '.join(skills[:8]) + ('…' if len(skills) > 8 else ''), quote=False)
    intro = (f'<p><strong>{n_ex} exercice{s} interactif{s} {subj} {level}</strong>{q_part}'
             + (f' : {skills_txt}.' if skills else '.')
             + ' Chaque réponse est corrigée tout de suite, avec une explication en cas d’erreur.'
             + ' Gratuit, sans inscription et sans publicité.</p>')
    links = []
    if p.get('lesson'):
        links.append(f'<a href="{p["lesson"]}">📖 Revoir la leçon</a>')
    if p['level'] and p['theme'] not in ('eps-cycle2', 'eps-cycle3'):
        links.append(f'<a href="programme-{p["level"]}.html">🗂️ Programme du {LEVEL_LABEL[p["level"]]}</a>')
    if keyed:
        links.append('<a href="#corrige">✅ Corrigé pour les parents</a>')
    intro_html = ('<!-- ef:intro --><section class="ex-intro">' + intro
                  + (f'<p class="ex-intro-links">{" · ".join(links)}</p>' if links else '')
                  + '</section><!-- /ef:intro -->')

    corrige_html = ''
    if keyed:
        parts = []
        for idx, k, ex in keyed:
            title = blocks[idx][0] if idx < len(blocks) else ''
            title = html.escape(title, quote=False)
            label = f'Ex {idx + 1}' + (f' · {title}' if title else '') if idx < len(blocks) else (title or 'Exercice')
            items = ''.join(item_html(ex, it) for it in short_paires(ex))
            if items:
                parts.append(f'<details><summary>{label}</summary><ol class="cr-list">{items}</ol></details>')
        corrige_html = ('<!-- ef:corrige --><section class="ex-corrige" id="corrige"><h2>Corrigé des exercices</h2>'
                        '<p>Pour les parents : toutes les questions de la page avec leur réponse, pour vérifier '
                        'ou refaire une séance sur papier. Ouvrez un exercice pour voir son corrigé.</p>'
                        + ''.join(parts) + '</section><!-- /ef:corrige -->')

    out = re.sub(r'\n?<!-- ef:intro -->.*?<!-- /ef:intro -->', '', page_html, flags=re.S)
    out = re.sub(r'<!-- ef:corrige -->.*?<!-- /ef:corrige -->\n?', '', out, flags=re.S)
    out = re.sub(r'(<main[^>]*>)\n{3,}', r'\1\n\n', out, count=1)
    out = re.sub(r'\n{3,}</main>', '\n\n</main>', out, count=1)
    out = re.sub(r'(<main[^>]*>)', lambda m: m.group(1) + '\n' + intro_html, out, count=1)
    if corrige_html:
        out = out.replace('</main>', corrige_html + '\n</main>', 1)

    # Titre et description propres à la page
    lvl = LEVEL_LABEL.get(p['level'] or '', '')
    h1 = plain(p['title'])
    if p['theme'] in ('eps-cycle2', 'eps-cycle3'):
        lvl = 'cycle ' + p['theme'][-1]
    name = h1 if (not lvl or lvl.lower() in h1.lower()) else f'{h1} {lvl}'
    title = f'{name} : exercices corrigés | École Facile'
    tail = f' {n_ex} exercice{s} interactif{s}, gratuit{s} et sans inscription.'
    desc = f'Exercices {subj} corrigés {level}.' + tail
    for k in range(min(4, len(skills)), 0, -1):
        cand = f'Exercices {subj} corrigés {level} : {", ".join(skills[:k])}' + ('.' if k == len(skills) else '…') + tail
        if len(cand) <= 160:
            desc = cand
            break
    desc = re.sub(r'\s+', ' ', desc).replace(' .', '.')
    attr = html.escape(desc, quote=False).replace('"', '&quot;')
    tattr = html.escape(title, quote=False).replace('"', '&quot;')
    out = re.sub(r'<title>.*?</title>', lambda m: f'<title>{html.escape(title, quote=False)}</title>', out, count=1, flags=re.S)
    out = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + attr + m.group(2), out, count=1)
    out = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + attr + m.group(2), out, count=1)
    out = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + tattr + m.group(2), out, count=1)
    return out


def node_json(script, files):
    if not files:
        return {}
    r = subprocess.run(['node', script, *files], capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-2000:])
    return json.loads(r.stdout)


def run(pages):
    """Met à jour les pages ; renvoie le nombre de fichiers modifiés (ou None sans Node)."""
    if not shutil.which('node'):
        print('· Node.js absent : contenu statique (corrigés, « Voir aussi ») non régénéré')
        return None
    ex_pages = [p for p in pages if p['kind'] == 'exercices']
    data = node_json('tools/extract_exercises.mjs', [p['href'] for p in ex_pages])
    import os
    with_related = [f for f in sorted(os.listdir('.')) if f.endswith('.html')
                    and 'src="related.js' in open(f, encoding='utf-8').read()]
    related = node_json('tools/render_related.mjs', with_related)
    changed = 0
    by_href = {p['href']: p for p in ex_pages}
    for f in sorted(set(by_href) | set(with_related)):
        src = open(f, encoding='utf-8').read()
        out = src
        if f in by_href:
            out = build_exercise_page(out, by_href[f], data.get(f, {}))
        out = re.sub(r'<!-- ef:related -->.*?<!-- /ef:related -->\n?', '', out, flags=re.S)
        if f in related:
            out = out.replace('</main>', '<!-- ef:related -->' + related[f] + '<!-- /ef:related -->\n</main>', 1)
        if out != src:
            open(f, 'w', encoding='utf-8').write(out)
            changed += 1
    return changed
