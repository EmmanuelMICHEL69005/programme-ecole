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
