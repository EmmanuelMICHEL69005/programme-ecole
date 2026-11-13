#!/usr/bin/env python3
"""
École Facile : génère les fiches PDF gratuites de ressources/ (+ tools/ressources.json).

    python3 tools/build_ressources.py

Nécessite Node + Playwright (Chromium) pour l'impression en PDF.
Les réponses des fiches d'exercices sont calculées par programme puis revérifiées
indépendamment (assertions) avant l'impression : une fiche fausse n'est jamais écrite.
"""
import json, os, random, re, subprocess, sys, tempfile
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
OUT = 'ressources'
os.makedirs(OUT, exist_ok=True)

CSS = '''
@page { size: A4; margin: 14mm 14mm 18mm; }
* { box-sizing: border-box; }
body { font-family: "DejaVu Sans", "Liberation Sans", Arial, sans-serif; color: #1e1b4b; font-size: 12.5pt; margin: 0; }
h1 { font-size: 21pt; margin: 0 0 4px; color: #1f3c88; }
h2 { font-size: 14pt; margin: 16px 0 6px; color: #172d66; }
.sub { color: #4b5060; margin: 0 0 10px; }
.top { display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 3px solid #1f3c88; padding-bottom: 8px; margin-bottom: 12px; }
.brand { font-weight: 800; color: #1f3c88; font-size: 11pt; text-align: right; }
.brand small { display: block; font-weight: 400; color: #5f6472; }
.name { display: flex; gap: 30px; margin: 4px 0 12px; font-size: 11.5pt; }
.name span { flex: 1; border-bottom: 1.5px dotted #888; padding-bottom: 2px; }
.grid { display: grid; gap: 10px 18px; }
.c2 { grid-template-columns: 1fr 1fr; } .c3 { grid-template-columns: 1fr 1fr 1fr; } .c4 { grid-template-columns: repeat(4, 1fr); }
.q { font-size: 14pt; padding: 6px 0; border-bottom: 1px solid #e5e7eb; white-space: nowrap; }
.q b { color: #1f3c88; font-size: 10pt; margin-right: 6px; }
.blank { display: inline-block; min-width: 56px; border-bottom: 1.5px solid #333; }
.ans { color: #15803d; font-weight: 800; }
.box { border: 2px solid #1f3c88; border-radius: 10px; padding: 10px 14px; margin: 10px 0; }
.tip { border: 2px solid #22c55e; background: #ecfdf5; border-radius: 10px; padding: 8px 12px; margin: 10px 0; font-size: 11.5pt; }
.steps { counter-reset: s; list-style: none; padding: 0; margin: 0; }
.steps li { counter-increment: s; position: relative; padding: 9px 10px 9px 52px; margin: 9px 0; border: 2px solid #e0e7ff; border-radius: 12px; min-height: 48px; }
.steps li::before { content: counter(s); position: absolute; left: 10px; top: 8px; width: 30px; height: 30px; border-radius: 50%; background: #1f3c88; color: #fff; font-weight: 800; display: flex; align-items: center; justify-content: center; }
.steps li strong { font-size: 13.5pt; }
table { border-collapse: collapse; width: 100%; }
td, th { border: 1.5px solid #9aa3c7; padding: 6px; vertical-align: top; }
th { background: #eef2ff; font-size: 11pt; }
.mt td, .mt th { text-align: center; font-size: 12pt; padding: 4px; }
.mt th { background: #1f3c88; color: #fff; }
.mt td.sq { background: #fff3c4; font-weight: 800; }
.check li { list-style: none; margin: 11px 0; font-size: 14.5pt; }
.check li::before { content: "☐  "; font-size: 15pt; color: #1f3c88; }
.check { padding-left: 4px; }
.pb { break-before: page; }
.frac { display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 3px; line-height: 1.05; font-size: 13pt; }
.frac .n { border-bottom: 1.5px solid #1e1b4b; padding: 0 3px; }
.small { font-size: 10.5pt; color: #4b5060; }
'''

FOOT_TXT = 'École Facile — ecolefacile.fr — Fiche gratuite. Reproduction libre pour un usage personnel ou en classe, non commercial.'

def doc(title, sub, body, name=False):
    head = (f'<div class="top"><div><h1>{title}</h1><p class="sub">{sub}</p></div>'
            '<div class="brand">École Facile<small>ecolefacile.fr</small></div></div>')
    nm = '<div class="name"><span>Prénom :</span><span>Date :</span></div>' if name else ''
    return f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{head}{nm}{body}</body></html>'

def frac(n, d):
    return f'<span class="frac"><span class="n">{n}</span><span>{d}</span></span>'

RES = []
def add(file, html_text, **meta):
    RES.append(dict(file=file, html=html_text, **meta))

# ── 1. Tables de multiplication : 40 calculs + corrigé ─────────────────
rng = random.Random(20261113)
pairs = []
while len(pairs) < 40:
    a, b = rng.randint(2, 9), rng.randint(2, 10)
    if (a, b) not in pairs:
        pairs.append((a, b))
qs = [f'{a} × {b} =' for a, b in pairs]
answers = [a * b for a, b in pairs]
for q, r in zip(qs, answers):  # vérification indépendante : on relit la chaîne affichée
    x, y = map(int, re.findall(r'\d+', q))
    assert x * y == r
body = '<div class="grid c4">' + ''.join(f'<div class="q"><b>{i+1}.</b>{q} <span class="blank"></span></div>' for i, q in enumerate(qs)) + '</div>'
body += '<div class="tip">Astuce : 3 × 7 = 7 × 3. Si tu bloques, cherche le calcul « à l\'envers » dans une table que tu connais mieux.</div>'
body += '<div class="pb"></div><h2>Corrigé</h2><div class="grid c4">' + ''.join(f'<div class="q"><b>{i+1}.</b>{q} <span class="ans">{r}</span></div>' for i, (q, r) in enumerate(zip(qs, answers))) + '</div>'
add('exercices-tables-de-multiplication-ce2-corrige.pdf', doc('Tables de multiplication', '40 calculs dans le désordre, tables de 2 à 9 — CE2 / CM1', body, True),
    title='40 multiplications à imprimer (avec corrigé)', desc='Les tables de 2 à 9 dans le désordre, pour s\'entraîner sur papier. Corrigé en page 2.',
    public='Exercices de tables CE2-CM1 avec corrigé', icon='✖️', tags=['CE2', 'CM1', 'Maths'], group='Exercices à imprimer, avec corrigé')

# ── 2. Calcul mental CE1 : additions et soustractions jusqu'à 100 ──────
rng = random.Random(1311)
items = []
while len(items) < 30:
    if len(items) % 2 == 0:
        a, b = rng.randint(10, 69), rng.randint(2, 30)
        if a + b > 99: continue
        items.append((f'{a} + {b} =', a + b))
    else:
        a, b = rng.randint(20, 99), rng.randint(2, 19)
        if a - b < 0: continue
        items.append((f'{a} − {b} =', a - b))
for q, r in items:
    x, op, y = re.match(r'(\d+) ([+−]) (\d+)', q).groups()
    assert (int(x) + int(y) if op == '+' else int(x) - int(y)) == r and 0 <= r <= 99
body = '<div class="grid c3">' + ''.join(f'<div class="q"><b>{i+1}.</b>{q} <span class="blank"></span></div>' for i, (q, _) in enumerate(items)) + '</div>'
body += '<div class="tip">Astuce : pour 47 + 8, fais d\'abord 47 + 3 = 50, puis 50 + 5 = 55.</div>'
body += '<div class="pb"></div><h2>Corrigé</h2><div class="grid c3">' + ''.join(f'<div class="q"><b>{i+1}.</b>{q} <span class="ans">{r}</span></div>' for i, (q, r) in enumerate(items)) + '</div>'
add('exercices-calcul-mental-ce1-corrige.pdf', doc('Calcul mental', '30 additions et soustractions jusqu\'à 100 — CE1', body, True),
    title='30 calculs mentaux CE1 (avec corrigé)', desc='Additions et soustractions jusqu\'à 100, avec une astuce de calcul. Corrigé en page 2.',
    public='Calcul mental CE1 avec corrigé', icon='🧮', tags=['CE1', 'CE2', 'Maths'], group='Exercices à imprimer, avec corrigé')

# ── 3. Fractions CM1 ────────────────────────────────────────────────
def bar(n, d):
    w = 220 / d
    cells = ''.join(f'<rect x="{1 + i*w:.1f}" y="1" width="{w:.1f}" height="26" fill="{"#7c3aed" if i < n else "#fff"}" stroke="#1e1b4b" stroke-width="1.5"/>' for i in range(d))
    return f'<svg width="224" height="28" viewBox="0 0 224 28">{cells}</svg>'
shade = [(3, 4), (2, 5), (5, 8), (1, 3), (7, 10), (4, 6)]
compare = [((3, 8), (5, 8)), ((1, 3), (1, 4)), ((7, 10), (3, 10)), ((2, 5), (2, 3)), ((4, 4), (1, 1)), ((5, 4), (3, 4)), ((1, 2), (2, 4)), ((2, 7), (2, 9))]
adds = [((2, 5), (1, 5)), ((3, 8), (4, 8)), ((1, 6), (4, 6)), ((5, 10), (3, 10)), ((2, 9), (5, 9)), ((1, 4), (2, 4))]
def sign(p, q):
    a, b = Fraction(*p), Fraction(*q)
    return '<' if a < b else '>' if a > b else '='
cmp_ans = [sign(p, q) for p, q in compare]
add_ans = [(p[0] + q[0], p[1]) for p, q in adds]
for (p, q), (n, d) in zip(adds, add_ans):
    assert p[1] == q[1] and Fraction(n, d) == Fraction(*p) + Fraction(*q)
assert cmp_ans == ['<', '>', '>', '<', '=', '>', '=', '>']
b1 = '<h2>1. Quelle fraction est coloriée ?</h2><div class="grid c2">' + ''.join(
    f'<div class="q"><b>{chr(97+i)}.</b>{bar(n, d)} &nbsp;→ <span class="blank"></span></div>' for i, (n, d) in enumerate(shade)) + '</div>'
b2 = '<h2>2. Compare avec &lt;, &gt; ou =</h2><div class="grid c2">' + ''.join(
    f'<div class="q"><b>{chr(97+i)}.</b>{frac(*p)} <span class="blank" style="min-width:30px"></span> {frac(*q)}</div>' for i, (p, q) in enumerate(compare)) + '</div>'
b3 = '<h2>3. Calcule</h2><div class="grid c3">' + ''.join(
    f'<div class="q"><b>{chr(97+i)}.</b>{frac(*p)} + {frac(*q)} = <span class="blank"></span></div>' for i, (p, q) in enumerate(adds)) + '</div>'
tip = '<div class="tip">Rappel : le nombre du bas (dénominateur) dit en combien de parts égales on coupe ; le nombre du haut (numérateur), combien on en prend. Pour additionner deux fractions qui ont le même dénominateur, on additionne les numérateurs et on garde le dénominateur.</div>'
c1 = '<h2>Corrigé</h2><p><strong>1.</strong> ' + ' · '.join(f'{chr(97+i)}. {frac(n, d)}' for i, (n, d) in enumerate(shade)) + '</p>'
c2 = '<p><strong>2.</strong> ' + ' · '.join(f'{chr(97+i)}. {frac(*p)} <span class="ans">{s}</span> {frac(*q)}' for i, ((p, q), s) in enumerate(zip(compare, cmp_ans))) + '</p>'
c3 = '<p><strong>3.</strong> ' + ' · '.join(f'{chr(97+i)}. {frac(*p)} + {frac(*q)} = <span class="ans">{frac(n, d)}</span>' for i, ((p, q), (n, d)) in enumerate(zip(adds, add_ans))) + '</p>'
c3 += '<p class="small">Pour le 2.b : une pizza coupée en 3 donne des parts plus grosses qu\'une pizza coupée en 4, donc 1/3 &gt; 1/4. Pour le 2.g : 1/2 et 2/4 représentent la même quantité.</p>'
add('exercices-fractions-cm1-corrige.pdf', doc('Les fractions', 'Lire, comparer et additionner des fractions — CM1', tip + b1 + b2 + b3 + '<div class="pb"></div>' + c1 + c2 + c3, True),
    title='Fiche fractions CM1 (avec corrigé)', desc='Lire une fraction coloriée, comparer, additionner des fractions de même dénominateur. Corrigé en page 2.',
    public='Fractions CM1 avec corrigé', icon='🍕', tags=['CM1', 'CM2', 'Maths'], group='Exercices à imprimer, avec corrigé')

# ── 4. Conjugaison : présent des verbes en -er ────────────────────────
VERBS = ['chanter', 'jouer', 'parler', 'danser', 'regarder', 'marcher', 'aimer', 'écouter', 'arriver', 'habiter']
PRON = [('je', 'e'), ('tu', 'es'), ('il', 'e'), ('elle', 'e'), ('on', 'e'), ('nous', 'ons'), ('vous', 'ez'), ('ils', 'ent'), ('elles', 'ent')]
rng = random.Random(42)
conj = []
for v in VERBS:
    for _ in range(2):
        p, e = rng.choice(PRON)
        form = v[:-2] + e
        subj = ("j'" if p == 'je' and form[0] in 'aeéèêiouh' else p + ' ')
        conj.append((v, p, subj + form))
# vérification : terminaisons régulières et élision correcte
for v, p, full in conj:
    assert v.endswith('er') and not v.endswith(('ger', 'cer', 'yer', 'eler', 'eter'))
    assert full.endswith(dict(PRON)[p]) and (full.startswith("j'") == (p == 'je' and v[0] in 'aeéèêiouh'))
def subj_of(v, p):
    return "j'" if p == 'je' and v[0] in 'aeéèêiouh' else p + ' '
qs = ['(' + v + ') ' + subj_of(v, p) + '…………………' for v, p, _ in conj]
body = ('<div class="tip">Au présent, les verbes en -er prennent les terminaisons : je -e, tu -es, il/elle/on -e, nous -ons, vous -ez, ils/elles -ent. '
        'Devant une voyelle ou un h muet, « je » devient « j\' » (j\'aime, j\'habite).</div>'
        '<h2>Conjugue le verbe au présent</h2><div class="grid c2">' + ''.join(f'<div class="q"><b>{i+1}.</b>{q}</div>' for i, q in enumerate(qs)) + '</div>'
        '<div class="pb"></div><h2>Corrigé</h2><div class="grid c2">' + ''.join(f'<div class="q"><b>{i+1}.</b>({v}) <span class="ans">{full}</span></div>' for i, (v, p, full) in enumerate(conj)) + '</div>')
add('exercices-conjugaison-present-ce2-corrige.pdf', doc('Le présent des verbes en -er', '20 formes à conjuguer (10 verbes) — CE2', body, True),
    title='Présent des verbes en -er (avec corrigé)', desc='20 formes à conjuguer au présent (10 verbes : chanter, jouer, aimer, habiter…). Corrigé en page 2.',
    public='Conjugaison CE2 avec corrigé', icon='✍️', tags=['CE2', 'CM1', 'Français'], group='Exercices à imprimer, avec corrigé')

# ── 5. Affiche des tables ────────────────────────────────────────────
rows = ''.join('<tr><th>' + str(i) + '</th>' + ''.join(f'<td class="{"sq" if i == j else ""}">{i*j}</td>' for j in range(1, 11)) + '</tr>' for i in range(1, 11))
grid = '<table class="mt"><tr><th>×</th>' + ''.join(f'<th>{j}</th>' for j in range(1, 11)) + '</tr>' + rows + '</table>'
lists = '<div class="grid c4" style="margin-top:12px">' + ''.join(
    '<div class="box" style="padding:6px 10px;font-size:10.5pt"><strong>Table de ' + str(t) + '</strong><br>' + '<br>'.join(f'{t} × {k} = {t*k}' for k in range(1, 11)) + '</div>' for t in range(2, 10)) + '</div>'
assert all(f'{t} × {k} = {t*k}' in lists for t in range(2, 10) for k in range(1, 11))
add('affiche-tables-de-multiplication.pdf', doc('Les tables de multiplication', 'Affiche à garder au bureau. En jaune : les carrés (2 × 2, 3 × 3…).', grid + lists +
    '<div class="tip">Astuces : × 4 = double du double · × 5 = moitié de × 10 · × 9 = × 10 moins une fois · 3 × 7 = 7 × 3.</div>'),
    title='Affiche des tables de multiplication', desc='Le tableau de Pythagore et les tables de 2 à 9, avec les astuces pour les retenir.',
    public='Affiche des tables de 1 à 10', icon='📋', tags=['CE1', 'CE2', 'CM1'], group='Affiches et fiches méthode')

# ── 6. Fiche méthode : résoudre un problème ───────────────────────────
add('fiche-methode-resoudre-un-probleme.pdf', doc('Résoudre un problème en 5 étapes', 'Fiche méthode — du CE1 à la 6e', '''
<ol class="steps">
<li><strong>Je lis et je raconte.</strong><br>Je lis deux fois. Je raconte l'histoire avec mes mots, sans les nombres.</li>
<li><strong>Je trouve la question.</strong><br>Je la souligne. Qu'est-ce qu'on cherche : un total ? un écart ? un partage ?</li>
<li><strong>Je fais un schéma.</strong><br>Barres, paquets, tableau : le dessin m'aide à choisir l'opération.</li>
<li><strong>Je calcule.</strong><br>Je pose l'opération si besoin.</li>
<li><strong>Je vérifie et je réponds.</strong><br>Mon résultat est-il logique ? J'écris une phrase réponse avec l'unité (€, cm, min…).</li>
</ol>
<h2>Quelle opération ?</h2>
<table><tr><th>Dans l'histoire…</th><th>Opération</th></tr>
<tr><td>On réunit, on ajoute</td><td>Addition +</td></tr>
<tr><td>On enlève, on compare, on cherche un écart</td><td>Soustraction −</td></tr>
<tr><td>On répète plusieurs fois la même quantité</td><td>Multiplication ×</td></tr>
<tr><td>On partage en parts égales, on fait des groupes</td><td>Division ÷</td></tr></table>
<div class="tip"><strong>Attention au piège :</strong> « Léa a 12 billes, c'est 5 de plus que Tom. Combien Tom a-t-il de billes ? » → 12 − 5 = 7. « De plus » ne veut pas toujours dire « + » : je comprends l'histoire !</div>'''),
    title='Fiche méthode : résoudre un problème', desc='Les 5 étapes, le tableau « quelle opération ? » et le piège des mots-indices.',
    public='Méthode en 5 étapes, CE1 à 6e', icon='🔎', tags=['CE1', 'CM2', '6e'], group='Affiches et fiches méthode')
assert 12 - 5 == 7

# ── 7. Fiche méthode : apprendre une leçon ────────────────────────────
add('fiche-methode-apprendre-une-lecon.pdf', doc('Apprendre une leçon en 4 étapes', 'Fiche méthode — primaire et collège', '''
<ol class="steps">
<li><strong>Je comprends.</strong><br>Je lis lentement. Pour chaque partie : qu'est-ce que ça veut dire ? Quel exemple je peux donner ?</li>
<li><strong>Je me teste.</strong><br>Je cache la leçon. Je redis, j'écris les mots clés, je refais un exemple. Puis je vérifie et je corrige.</li>
<li><strong>J'espace.</strong><br>Je recommence le test demain, puis dans quelques jours. 3 × 10 minutes valent mieux que 30 minutes la veille.</li>
<li><strong>Je dors.</strong><br>Un petit test avant de dormir, puis une vraie nuit : le cerveau range ce que j'ai appris.</li>
</ol>
<h2>Mes séances de révision</h2>
<table><tr><th>Leçon</th><th>Jour 1</th><th>Jour 2</th><th>Jour 4 ou 5</th><th>Contrôle le…</th></tr>
<tr><td style="height:34px"></td><td></td><td></td><td></td><td></td></tr><tr><td style="height:34px"></td><td></td><td></td><td></td><td></td></tr>
<tr><td style="height:34px"></td><td></td><td></td><td></td><td></td></tr><tr><td style="height:34px"></td><td></td><td></td><td></td><td></td></tr></table>
<div class="tip">Relire, ce n'est pas apprendre : se tester, c'est apprendre. (Roediger &amp; Karpicke, 2006 : une semaine après, 61 % retenu en se testant contre 40 % en relisant.)</div>'''),
    title='Fiche méthode : apprendre une leçon', desc='Comprendre, se tester, espacer, dormir : la méthode qui marche, avec un tableau de révisions.',
    public='Méthode en 4 étapes, primaire et collège', icon='🧠', tags=['Primaire', 'Collège'], group='Affiches et fiches méthode')

# ── 8. Planning de devoirs de la semaine ──────────────────────────────
days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
rows = ''.join(f'<tr><th style="width:16%">{d}</th><td style="height:{"58" if d not in ("Samedi", "Dimanche") else "40"}px"></td><td></td><td style="width:12%"></td><td style="width:7%"></td></tr>' for d in days)
add('planning-devoirs-semaine.pdf', doc('Mon planning de devoirs', 'Semaine du ………………… au …………………', f'''
<table><tr><th></th><th>Ce que je dois faire (matière, exercice, leçon)</th><th>Pour quand ?</th><th>Durée</th><th>✓</th></tr>{rows}</table>
<div class="tip">Je commence par le plus difficile. Un contrôle annoncé = 3 petites révisions réparties dans la semaine, pas une seule la veille.</div>''', True),
    title='Planning de devoirs de la semaine', desc='Un tableau du lundi au dimanche pour noter et cocher ses devoirs, et répartir les révisions.',
    public='Planning hebdomadaire à remplir', icon='🗓️', tags=['Primaire', 'Collège', 'Parents'], group='Organisation et motivation')

# ── 9. Checklist « Mes devoirs du soir » ──────────────────────────────
add('checklist-devoirs-du-soir.pdf', doc('Mes devoirs du soir', 'Checklist à afficher au bureau', '''
<h2>Avant de commencer</h2><ul class="check">
<li>J'ai goûté et je me suis reposé(e) un peu.</li><li>J'ai rangé mon bureau, l'écran est éteint.</li>
<li>J'ai regardé mon agenda : pour demain ET pour la semaine.</li><li>J'ai tout ce qu'il me faut : cahiers, trousse, leçon.</li></ul>
<h2>Pendant</h2><ul class="check">
<li>Je commence par le plus difficile.</li><li>Je lis la consigne jusqu'au bout et je la redis avec mes mots.</li>
<li>Pour une leçon : je cache et je me teste.</li><li>Je bloque ? Je relis un exemple de la leçon, puis je demande de l'aide.</li></ul>
<h2>À la fin</h2><ul class="check">
<li>J'ai tout fait ? Je coche dans mon agenda.</li><li>Je prépare mon cartable pour demain avec l'emploi du temps.</li>
<li>Avant de dormir : 5 minutes pour me tester encore une fois.</li></ul>'''),
    title='Checklist « Mes devoirs du soir »', desc='Les bons réflexes avant, pendant et après les devoirs, à afficher au bureau.',
    public='Routine du soir à afficher', icon='✅', tags=['Primaire', 'Collège'], group='Organisation et motivation')

# ── 10. Checklist cartable ─────────────────────────────────────────────
add('checklist-cartable.pdf', doc('Mon cartable est prêt !', 'À cocher chaque soir avec l\'emploi du temps', '''
<div class="grid c2"><div><h2>Tous les jours</h2><ul class="check">
<li>Agenda ou cahier de textes</li><li>Trousse complète (stylos, crayon, gomme, colle, ciseaux)</li><li>Règle et ardoise / équerre</li>
<li>Cahier de liaison / carnet de correspondance</li><li>Devoirs faits et rangés</li><li>Gourde et goûter</li></ul></div>
<div><h2>Selon l'emploi du temps de demain</h2><ul class="check">
<li>Cahiers et livres des matières de demain</li><li>Affaires de sport (EPS)</li><li>Matériel spécial (compas, calculatrice, flûte…)</li>
<li>Papier signé à rendre</li><li>Carte de cantine / de transport</li><li>Tenue adaptée à la météo</li></ul></div></div>
<h2>Mes matières de la semaine</h2>
<table><tr><th>Lundi</th><th>Mardi</th><th>Mercredi</th><th>Jeudi</th><th>Vendredi</th></tr><tr><td style="height:150px"></td><td></td><td></td><td></td><td></td></tr></table>'''),
    title='Checklist cartable', desc='Tout ce qu\'il faut vérifier la veille, plus un emploi du temps simplifié à remplir.',
    public='À cocher chaque soir', icon='🎒', tags=['Primaire', '6e'], group='Organisation et motivation')

# ── 11. Tableau de motivation ──────────────────────────────────────────
wk = ''.join(f'<tr><th>Semaine {i}</th>' + ''.join('<td style="height:56px"></td>' for _ in range(7)) + '</tr>' for i in range(1, 5))
add('tableau-de-motivation.pdf', doc('Mon tableau de réussites', 'Une étoile ou un autocollant à chaque séance de travail réussie', f'''
<table><tr><th></th>{''.join(f'<th>{d[:3]}.</th>' for d in days)}</tr>{wk}</table>
<h2>Mon objectif du mois</h2><div class="box" style="height:70px"></div>
<h2>Ce dont je suis fier / fière</h2><div class="box" style="height:90px"></div>
<div class="tip"><strong>Pour les parents :</strong> félicitez l'effort et la méthode (« tu as relu la consigne »), pas seulement le résultat. Évitez de transformer chaque étoile en récompense matérielle.</div>'''),
    title='Tableau de motivation', desc='4 semaines d\'étoiles à colorier, un objectif du mois et un espace « je suis fier(e) ».',
    public='4 semaines d\'étoiles à colorier', icon='⭐', tags=['Primaire', 'Parents'], group='Organisation et motivation')

# ── 12. Checklist entrée en 6e (parents) ───────────────────────────────
add('checklist-entree-en-sixieme.pdf', doc('Entrée en 6e : la checklist des parents', 'Les premières semaines de collège', '''
<h2>Avant la rentrée</h2><ul class="check">
<li>Activer les identifiants de l'ENT (cahier de textes, notes, messagerie)</li><li>Acheter les fournitures de la liste du collège</li>
<li>Repérer le trajet et l'horaire du bus</li><li>Revoir quelques bases du CM2 (fractions, décimaux, conjugaison)</li></ul>
<h2>Les premières semaines</h2><ul class="check">
<li>Regarder l'agenda / l'ENT avec mon enfant chaque soir</li><li>Afficher l'emploi du temps (semaines A et B s'il y en a)</li>
<li>Préparer le cartable la veille ensemble</li><li>Demander comment se passe Devoirs faits (obligatoire en 6e depuis 2023)</li>
<li>Noter le nom du professeur principal et du CPE</li><li>Aller à la réunion de rentrée</li></ul>
<h2>Ensuite</h2><ul class="check">
<li>Laisser mon enfant faire seul, et vérifier seulement</li><li>Planifier les révisions des contrôles sur plusieurs jours</li>
<li>Garder un temps de sommeil suffisant (9 à 11 h entre 6 et 13 ans)</li><li>En cas de difficulté : contacter le professeur principal</li></ul>'''),
    title='Checklist entrée en 6e', desc='Pour les parents : avant la rentrée, les premières semaines, puis l\'autonomie.',
    public='Pour les parents de futurs 6e', icon='🏫', tags=['CM2', '6e', 'Parents'], group='Organisation et motivation')

# ════════════════ VAGUE 2 ════════════════
from decimal import Decimal
import math

def fr_num(x):
    """Écriture française d'un nombre (virgule décimale, signe moins typographique)."""
    s = format(x, 'f') if isinstance(x, Decimal) else str(x)
    if '.' in s:
        s = s.rstrip('0').rstrip('.') if isinstance(x, Decimal) and '.' in s else s
    return s.replace('-', '−').replace('.', ',')

def corr_grid(items, cols='c3'):
    return f'<div class="grid {cols}">' + ''.join(f'<div class="q"><b>{i+1}.</b>{q} <span class="ans">{r}</span></div>' for i, (q, r) in enumerate(items)) + '</div>'

def ex_grid(items, cols='c3', blank=True):
    return f'<div class="grid {cols}">' + ''.join(f'<div class="q"><b>{i+1}.</b>{q} {"<span class=blank></span>" if blank else ""}</div>' for i, (q, _) in enumerate(items)) + '</div>'

# ── 13. CP : additions et soustractions jusqu'à 20 ────────────────────
rng = random.Random(2026)
cp = []
while len(cp) < 24:
    if len(cp) % 2 == 0:
        a, b = rng.randint(1, 12), rng.randint(1, 9)
        if a + b > 20 or (f'{a} + {b} =', a + b) in cp: continue
        cp.append((f'{a} + {b} =', a + b))
    else:
        a, b = rng.randint(5, 20), rng.randint(1, 9)
        if a - b < 0 or (f'{a} − {b} =', a - b) in cp: continue
        cp.append((f'{a} − {b} =', a - b))
for q, r in cp:
    x, op, y = re.match(r'(\d+) ([+−]) (\d+)', q).groups()
    assert (int(x) + int(y) if op == '+' else int(x) - int(y)) == r and 0 <= r <= 20
add('exercices-calcul-cp-corrige.pdf', doc('Je calcule jusqu\'à 20', '24 additions et soustractions — CP',
    '<div class="tip">Astuce : pour 8 + 5, je fais 8 + 2 = 10, puis 10 + 3 = 13.</div>' + ex_grid(cp, 'c3') +
    '<div class="pb"></div><h2>Corrigé</h2>' + corr_grid(cp, 'c3'), True),
    title='24 calculs jusqu\'à 20 pour le CP (avec corrigé)', desc='Additions et soustractions jusqu\'à 20, en gros caractères, avec l\'astuce du passage à 10. Corrigé en page 2.',
    public='Calcul CP avec corrigé', icon='🔢', tags=['CP', 'CE1', 'Maths'], group='Exercices à imprimer, avec corrigé')

# ── 14. Homophones CE2 ────────────────────────────────────────────────
HOMO = [
    ('Lina ___ un chat.', 'a / à', 'a', 'Lina avait un chat.'),
    ('Nous allons ___ la plage.', 'a / à', 'à', '« avait » ne marche pas.'),
    ('Il ___ mangé une pomme.', 'a / à', 'a', 'Il avait mangé.'),
    ('Je pense ___ toi.', 'a / à', 'à', '« avait » ne marche pas.'),
    ('Le ciel ___ bleu.', 'et / est', 'est', 'Le ciel était bleu.'),
    ("J'aime les pommes ___ les poires.", 'et / est', 'et', 'et puis les poires.'),
    ('Mon frère ___ malade.', 'et / est', 'est', 'Mon frère était malade.'),
    ('Il court ___ il saute.', 'et / est', 'et', 'Il court et puis il saute.'),
    ('Les fleurs ___ jolies.', 'son / sont', 'sont', 'Les fleurs étaient jolies.'),
    ('Tom range ___ vélo.', 'son / sont', 'son', 'Tom range mon vélo.'),
    ('Ils ___ en retard.', 'son / sont', 'sont', 'Ils étaient en retard.'),
    ('Elle cherche ___ livre.', 'son / sont', 'son', 'Elle cherche mon livre.'),
    ('___ va au cinéma ce soir.', 'On / Ont', 'On', 'Il va au cinéma.'),
    ('Les enfants ___ faim.', 'on / ont', 'ont', 'Les enfants avaient faim.'),
    ('Mes parents ___ une voiture rouge.', 'on / ont', 'ont', 'Mes parents avaient une voiture.'),
    ('Demain, ___ jouera au foot.', 'on / ont', 'on', 'Demain, il jouera au foot.'),
    ('___ est ma trousse ?', 'Ou / Où', 'Où', 'On parle d\'un lieu.'),
    ('Tu préfères le lait ___ le jus ?', 'ou / où', 'ou', 'le lait ou bien le jus.'),
]
for s_, ch, ans, why in HOMO:
    assert s_.count('___') == 1 and ans in [c.strip() for c in ch.split('/')]
hq = ''.join(f'<div class="q" style="white-space:normal"><b>{i+1}.</b>{s_.replace("___", "<span class=blank></span>")} <span class="small">({ch})</span></div>' for i, (s_, ch, _, _) in enumerate(HOMO))
hc = ''.join(f'<div class="q" style="white-space:normal"><b>{i+1}.</b>{s_.replace("___", "<span class=ans>" + ans + "</span>")} <span class="small">— {why}</span></div>' for i, (s_, _, ans, why) in enumerate(HOMO))
add('exercices-homophones-ce2-corrige.pdf', doc('Les homophones', 'a/à, et/est, son/sont, on/ont, ou/où — CE2', '''
<div class="tip">Je remplace : <strong>a</strong> → avait · <strong>est</strong> → était · <strong>et</strong> → et puis · <strong>sont</strong> → étaient · <strong>son</strong> → mon · <strong>ont</strong> → avaient · <strong>on</strong> → il · <strong>ou</strong> → ou bien · <strong>où</strong> → un lieu ou un moment.</div>
<h2>Complète avec le bon mot</h2><div class="grid c2">''' + hq + '</div><div class="pb"></div><h2>Corrigé</h2><div class="grid c2">' + hc + '</div>', True),
    title='Fiche homophones CE2 (avec corrigé)', desc='18 phrases à compléter : a/à, et/est, son/sont, on/ont, ou/où. Le corrigé explique le test à faire.',
    public='Homophones CE1-CM1 avec corrigé', icon='🔤', tags=['CE1', 'CE2', 'CM1', 'Français'], group='Exercices à imprimer, avec corrigé')

# ── 15. Divisions CM1 ────────────────────────────────────────────────
DIVS = [(157, 6), (845, 4), (618, 3), (96, 8), (734, 5), (1209, 3), (508, 7), (365, 9), (1000, 8), (842, 2), (713, 6), (2525, 5)]
divq = [(f'{a} ÷ {b}', divmod(a, b)) for a, b in DIVS]
for (q, (qu, re_)), (a, b) in zip(divq, DIVS):
    assert b * qu + re_ == a and 0 <= re_ < b
dq = ''.join(f'<div class="box" style="height:225px;margin:0;font-size:13pt"><b style="color:#1f3c88">{i+1}.</b> {q}<div style="margin-top:165px;font-size:11pt">q = <span class="blank" style="min-width:44px"></span> r = <span class="blank" style="min-width:30px"></span></div></div>' for i, (q, _) in enumerate(divq))
dc = ''.join(f'<div class="q"><b>{i+1}.</b>{q} → q = <span class="ans">{qu}</span>, r = <span class="ans">{r}</span> <span class="small">({b} × {qu} + {r} = {a})</span></div>' for i, ((q, (qu, r)), (a, b)) in enumerate(zip(divq, DIVS)))
add('exercices-divisions-cm1-corrige.pdf', doc('La division posée', '12 divisions par un nombre à un chiffre : trouve le quotient (q) et le reste (r) — CM1 / CM2', '''
<div class="tip">À chaque étape : combien de fois ? → je multiplie → je soustrais → j'abaisse. Le reste est toujours plus petit que le diviseur. Après avoir abaissé un chiffre, si le diviseur ne « rentre » pas, j'écris 0 au quotient (au tout début, je prends plutôt un chiffre de plus).
Pour vérifier : diviseur × quotient + reste = dividende.</div><div class="grid c4" style="gap:8px">''' + dq + '</div><div class="pb"></div><h2>Corrigé</h2><div class="grid c2">' + dc + '</div>', True),
    title='12 divisions posées (avec corrigé)', desc='Quotient et reste, dont des divisions avec un 0 au quotient. Le corrigé montre la vérification.',
    public='Divisions CM1-CM2 avec corrigé', icon='➗', tags=['CM1', 'CM2', '6e', 'Maths'], group='Exercices à imprimer, avec corrigé')

# ── 16. Nombres décimaux CM2 ─────────────────────────────────────────
D = Decimal
CMP = [('3.5', '3.15'), ('2.7', '2.70'), ('0.9', '0.12'), ('12.08', '12.8'), ('5.45', '5.405'), ('7', '6.99'), ('0.5', '0.50'), ('4.1', '4.09')]
cmpd = [(D(a), D(b), '<' if D(a) < D(b) else '>' if D(a) > D(b) else '=') for a, b in CMP]
assert [c for _, _, c in cmpd] == ['>', '=', '>', '<', '>', '>', '=', '>']
OPS = [('2.5', '+', '1.25'), ('3.7', '+', '4.6'), ('10', '−', '2.4'), ('6.05', '+', '0.9'), ('8.3', '−', '1.75'), ('12.5', '+', '7.5'), ('5', '−', '0.01'), ('0.25', '+', '0.75')]
opd = [(D(a), op, D(b), D(a) + D(b) if op == '+' else D(a) - D(b)) for a, op, b in OPS]
assert [str(r.normalize()) for *_, r in opd] == ['3.75', '8.3', '7.6', '6.95', '6.55', '2E+1', '4.99', '1']
def fd(x):
    s = format(x.normalize(), 'f')
    return s.replace('.', ',')
c1 = ''.join(f'<div class="q"><b>{chr(97+i)}.</b>{sa.replace(".", ",")} <span class="blank" style="min-width:30px"></span> {sb.replace(".", ",")}</div>' for i, (sa, sb) in enumerate(CMP))
c2 = ''.join(f'<div class="q"><b>{chr(97+i)}.</b>{fd(a)} {op} {fd(b)} = <span class="blank"></span></div>' for i, (a, op, b, _) in enumerate(opd))
k1 = ''.join(f'<div class="q"><b>{chr(97+i)}.</b>{sa.replace(".", ",")} <span class="ans">{c}</span> {sb.replace(".", ",")}</div>' for i, ((sa, sb), (_, _, c)) in enumerate(zip(CMP, cmpd)))
k2 = ''.join(f'<div class="q"><b>{chr(97+i)}.</b>{fd(a)} {op} {fd(b)} = <span class="ans">{fd(r)}</span></div>' for i, (a, op, b, r) in enumerate(opd))
add('exercices-nombres-decimaux-cm2-corrige.pdf', doc('Les nombres décimaux', 'Comparer, additionner et soustraire — CM2', '''
<div class="tip">Pour comparer, j'écris les deux nombres avec autant de chiffres après la virgule : 3,5 = 3,50 et 3,50 &gt; 3,15. Pour additionner ou soustraire, j'aligne les virgules.</div>
<h2>1. Compare avec &lt;, &gt; ou =</h2><div class="grid c2">''' + c1 + '</div><h2>2. Calcule</h2><div class="grid c2">' + c2 +
    '</div><div class="pb"></div><h2>Corrigé</h2><h2>1.</h2><div class="grid c2">' + k1 + '</div><h2>2.</h2><div class="grid c2">' + k2 + '</div>', True),
    title='Fiche nombres décimaux CM2 (avec corrigé)', desc='Comparer des décimaux (les pièges comme 3,5 et 3,15), additionner et soustraire. Corrigé en page 2.',
    public='Décimaux CM2-6e avec corrigé', icon='🔟', tags=['CM2', '6e', 'Maths'], group='Exercices à imprimer, avec corrigé')

# ── 17. Nombres relatifs 5e ──────────────────────────────────────────
rng = random.Random(55)
rel = []
def wr(n):  # écriture d'un relatif dans un calcul
    return f'(−{abs(n)})' if n < 0 else str(n)
while len(rel) < 20:
    a, b = rng.randint(-15, 15), rng.randint(-15, 15)
    if a == 0 or b == 0 or (a > 0 and b > 0): continue
    if len(rel) % 2 == 0:
        q, r = f'{wr(a)} + {wr(b)} =', a + b
    else:
        q, r = f'{wr(a)} − {wr(b)} =', a - b
    if any(q == x for x, _ in rel): continue
    rel.append((q, r))
for q, r in rel:
    expr = q.rstrip(' =').replace('−', '-')
    assert eval(expr) == r
relr = [(q, fr_num(r)) for q, r in rel]
add('exercices-nombres-relatifs-5e-corrige.pdf', doc('Les nombres relatifs', '20 additions et soustractions — 5e', '''
<div class="tip">Additionner : même signe → j'ajoute les distances à zéro et je garde le signe ; signes contraires → je soustrais les distances à zéro et je prends le signe de celui qui est le plus loin de zéro.
Soustraire un nombre, c'est ajouter son opposé : 5 − (−3) = 5 + 3 = 8.</div>''' + ex_grid(relr, 'c3') + '<div class="pb"></div><h2>Corrigé</h2>' + corr_grid(relr, 'c3'), True),
    title='20 calculs avec des nombres relatifs (avec corrigé)', desc='Additions et soustractions de nombres relatifs, avec les règles d\'addition et de soustraction rappelées. Corrigé en page 2.',
    public='Relatifs 5e avec corrigé', icon='➖', tags=['5e', '4e', 'Maths'], group='Exercices à imprimer, avec corrigé')
assert 5 - (-3) == 8

# ── 18. Pythagore 4e ─────────────────────────────────────────────────
PY = []
for ab, ac in [(3, 4), (6, 8), (5, 12), (8, 15)]:
    bc = math.isqrt(ab * ab + ac * ac); assert bc * bc == ab * ab + ac * ac
    PY.append((f'ABC est rectangle en A, AB = {ab} cm et AC = {ac} cm. Calcule BC.',
               f'ABC est rectangle en A, donc d\'après le théorème de Pythagore : BC² = AB² + AC² = {ab*ab} + {ac*ac} = {ab*ab+ac*ac}, donc BC = √{ab*ab+ac*ac} = <span class="ans">{bc} cm</span>'))
for bc, ab in [(13, 5), (10, 6), (25, 7)]:
    ac2 = bc * bc - ab * ab; ac = math.isqrt(ac2); assert ac * ac == ac2
    PY.append((f'ABC est rectangle en A, BC = {bc} cm et AB = {ab} cm. Calcule AC.',
               f'ABC est rectangle en A, donc d\'après le théorème de Pythagore : BC² = AB² + AC², d\'où AC² = BC² − AB² = {bc*bc} − {ab*ab} = {ac2}, donc AC = √{ac2} = <span class="ans">{ac} cm</span>'))
v = math.sqrt(13); assert round(v, 1) == 3.6
PY.append(('ABC est rectangle en A, AB = 2 cm et AC = 3 cm. Calcule BC, arrondi au dixième.',
           'ABC est rectangle en A, donc d\'après le théorème de Pythagore : BC² = 4 + 9 = 13, donc BC = √13 ≈ <span class="ans">3,6 cm</span>'))
for (a, b, c), (P, Q, R) in [((9, 12, 15), 'DEF'), ((5, 6, 8), 'GHI')]:
    rect = a * a + b * b == c * c
    PY.append((f'Le triangle {P}{Q}{R} a pour côtés {P}{Q} = {a} cm, {Q}{R} = {b} cm et {P}{R} = {c} cm. Est-il rectangle ?',
               f'Le plus grand côté est [{P}{R}]. {P}{R}² = {c*c} et {P}{Q}² + {Q}{R}² = {a*a} + {b*b} = {a*a+b*b}. ' +
               (f'C\'est égal, donc d\'après la réciproque du théorème de Pythagore, <span class="ans">le triangle {P}{Q}{R} est rectangle en {Q}</span>.' if rect
                else f'Ce n\'est pas égal, donc d\'après la contraposée du théorème de Pythagore, <span class="ans">le triangle {P}{Q}{R} n\'est pas rectangle</span>.')))
assert 9*9+12*12 == 15*15 and 5*5+6*6 != 8*8
pq = ''.join(f'<div class="q" style="white-space:normal;padding:6px 0 30px"><b>{i+1}.</b>{q}</div>' for i, (q, _) in enumerate(PY))
pc = ''.join(f'<div class="q" style="white-space:normal"><b>{i+1}.</b>{a}</div>' for i, (_, a) in enumerate(PY))
add('exercices-pythagore-4e-corrige.pdf', doc('Le théorème de Pythagore', 'Calculer une longueur et prouver qu\'un triangle est rectangle — 4e', '''
<div class="tip">Dans un triangle ABC rectangle en A, l'hypoténuse est [BC] (en face de l'angle droit) et BC² = AB² + AC². Pour trouver une longueur, je n'oublie pas la racine carrée.</div>''' + pq + '<div class="pb"></div><h2>Corrigé</h2>' + pc, True),
    title='Fiche théorème de Pythagore 4e (avec corrigé)', desc='Hypoténuse, côté de l\'angle droit, valeur arrondie et réciproque : 10 exercices avec un corrigé rédigé (justifications comprises).',
    public='Pythagore 4e avec corrigé', icon='📐', tags=['4e', '3e', 'Maths'], group='Exercices à imprimer, avec corrigé')

# ── 19. Proportionnalité CM2 ─────────────────────────────────────────
P = []
# tableau : coefficient 3
tab = [(2, 6), (5, None), (7, None), (None, 30)]
k = Fraction(6, 2)
tab_ans = [(x if x is not None else int(y / k), y if y is not None else int(x * k)) for x, y in tab]
assert tab_ans == [(2, 6), (5, 15), (7, 21), (10, 30)]
recette = Fraction(200, 4) * 6; assert recette == 300
stylo = Decimal('4') / 5 * 8; assert stylo == Decimal('6.4')
pct = [(10, 70, 7), (25, 40, 10), (50, 18, 9), (20, 150, 30)]
for p_, n, r in pct: assert Fraction(p_ * n, 100) == r
ech = 3 * 100000 / 100000; assert ech == 3
row1 = ''.join(f'<td>{x if x is not None else ""}</td>' for x, _ in tab)
row2 = ''.join(f'<td>{y if y is not None else ""}</td>' for _, y in tab)
body = f'''
<div class="tip">Deux grandeurs sont proportionnelles si on passe de l'une à l'autre en multipliant toujours par le même nombre. Passage à l'unité : je calcule pour 1, puis pour ce qu'on demande.</div>
<h2>1. Complète le tableau de proportionnalité</h2>
<table style="width:70%"><tr><th>Nombre de paquets</th>{row1}</tr><tr><th>Nombre de gâteaux</th>{row2}</tr></table>
<h2>2. Recette</h2><p>Pour 4 personnes, il faut 200 g de farine. Combien en faut-il pour 6 personnes ? <span class="blank"></span></p>
<h2>3. Passage à l'unité</h2><p>5 stylos coûtent 4 €. Combien coûtent 8 stylos ? <span class="blank"></span></p>
<h2>4. Pourcentages</h2><div class="grid c2">{''.join(f'<div class="q">{p_} % de {n} = <span class="blank"></span></div>' for p_, n, _ in pct)}</div>
<h2>5. Échelle</h2><p>Sur une carte à l'échelle 1/100 000, deux villages sont à 3 cm l'un de l'autre. Quelle est la distance réelle ? <span class="blank"></span></p>
<h2>6. Proportionnel ou pas ?</h2><p>a. Le prix payé et le nombre de baguettes achetées (même prix pour chaque baguette). <span class="blank"></span><br>b. La taille d'un enfant et son âge. <span class="blank"></span></p>
<div class="pb"></div><h2>Corrigé</h2>
<p><strong>1.</strong> On multiplie par 3 : 5 → <span class="ans">15</span> ; 7 → <span class="ans">21</span> ; 30 ÷ 3 = <span class="ans">10</span>.</p>
<p><strong>2.</strong> Pour 1 personne : 200 ÷ 4 = 50 g. Pour 6 : 6 × 50 = <span class="ans">300 g</span>.</p>
<p><strong>3.</strong> 1 stylo : 4 ÷ 5 = 0,80 €. 8 stylos : 8 × 0,80 = <span class="ans">6,40 €</span>.</p>
<p><strong>4.</strong> {' · '.join(f'{p_} % de {n} = <span class="ans">{r}</span>' for p_, n, r in pct)}</p>
<p><strong>5.</strong> 1 cm représente 100 000 cm = 1 km, donc 3 cm représentent <span class="ans">3 km</span>.</p>
<p><strong>6.</strong> a. <span class="ans">Oui</span> : 2 fois plus de baguettes coûtent 2 fois plus cher. b. <span class="ans">Non</span> : à 10 ans, on ne mesure pas le double de sa taille à 5 ans.</p>'''
add('exercices-proportionnalite-cm2-corrige.pdf', doc('La proportionnalité', 'Tableau, recette, passage à l\'unité, pourcentages, échelle — CM2 / 6e', body, True),
    title='Fiche proportionnalité CM2 (avec corrigé)', desc='Tableau, recette, passage à l\'unité, pourcentages et échelle, avec un corrigé détaillé.',
    public='Proportionnalité CM2-6e avec corrigé', icon='⚖️', tags=['CM2', '6e', 'Maths'], group='Exercices à imprimer, avec corrigé')


# ── Impression PDF via Playwright ──────────────────────────────────────
tmp = tempfile.mkdtemp(prefix='ef_res_')
jobs = []
for r in RES:
    hp = os.path.join(tmp, r['file'].replace('.pdf', '.html'))
    open(hp, 'w', encoding='utf-8').write(r['html'])
    jobs.append([hp, os.path.abspath(os.path.join(OUT, r['file']))])
js = os.path.join(tmp, 'print.js')
open(js, 'w').write('''
const {chromium}=require('playwright'); const jobs=JSON.parse(process.argv[2]); const FOOT=process.argv[3];
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const [h,o] of jobs){await p.goto('file://'+h);await p.pdf({path:o,format:'A4',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="width:100%;text-align:center;font-size:8px;color:#6b7080;font-family:DejaVu Sans,sans-serif">'+FOOT+' · <span class="pageNumber"></span>/<span class="totalPages"></span></div>'});}
await b.close();})().catch(e=>{console.error(e);process.exit(1)});''')
subprocess.run(['node', js, json.dumps(jobs), FOOT_TXT], check=True)

meta = []
for r in RES:
    path = os.path.join(OUT, r['file'])
    data = open(path, 'rb').read()
    pages = len(re.findall(rb'/Type\s*/Page[^s]', data))
    meta.append({k: v for k, v in r.items() if k != 'html'} | {'bytes': len(data), 'pages': pages})
json.dump(meta, open('tools/ressources.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'{len(meta)} PDF écrits dans {OUT}/ :', ', '.join(f"{m['file']} ({m['pages']} p.)" for m in meta))
