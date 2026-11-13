#!/usr/bin/env python3
"""
École Facile : génère les pages Guides parents, Aide élèves, Ressources et À propos.

    python3 tools/build_ressources.py   # (re)crée les PDF dans ressources/ et tools/ressources.json
    python3 tools/build_guides.py       # (re)crée les pages HTML à partir de tools/guides_content.py
    python3 tools/build_site.py         # met à jour les ?v= des CSS/JS

Le contenu se modifie dans tools/guides_content.py, jamais dans les .html générés.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from guides_content import ARTICLES, HUBS, S, UPDATED, UPDATED_FR  # noqa: E402

BASE = 'https://ecolefacile.fr'
RES = json.load(open('tools/ressources.json', encoding='utf-8')) if os.path.exists('tools/ressources.json') else []

CLUSTERS = [
    ('parents', 'Accompagner les devoirs', ['aider-son-enfant-a-faire-ses-devoirs', 'motiver-son-enfant-pour-les-devoirs',
                                            'combien-de-temps-de-devoirs-par-age', 'mon-enfant-n-y-arrive-pas', 'comment-apprendre-une-lecon']),
    ('parents', 'Programme et ressources gratuites', ['exercices-gratuits', 'entree-en-sixieme']),
    ('parents', 'Méthode et révisions', ['reviser-un-controle', 'reviser-pendant-les-vacances']),
    ('aide', 'Maths', ['je-ne-comprends-pas-les-fractions', 'apprendre-les-tables-de-multiplication', 'resoudre-un-probleme-de-maths',
                       'poser-une-division', 'proportionnalite-explication', 'theoreme-de-pythagore']),
    ('aide', 'Français', ['homophones-a-a-et-est-son-sont', 'accord-du-participe-passe']),
]
BY_SLUG = {a['slug']: a for a in ARTICLES}

FOOTER = ('<footer class="site-footer">Fait avec ❤️ pour Clémence<div class="footer-levels">'
          + ' · '.join(f'<a href="programme-{l}.html">{L}</a>' for l, L in
                       [('cp', 'CP'), ('ce1', 'CE1'), ('ce2', 'CE2'), ('cm1', 'CM1'), ('cm2', 'CM2'), ('6e', '6e'), ('5e', '5e'), ('4e', '4e'), ('3e', '3e')])
          + '</div><div class="footer-levels"><a href="parents.html">Espace parents</a> · <a href="aide.html">Aide élèves</a> · '
          '<a href="ressources.html">Ressources gratuites</a> · <a href="a-propos.html">À propos</a></div></footer>')

SCRIPTS = '\n'.join(f'<script src="{s}"></script>' for s in
                    ['sync.js', 'firebase-keys.js', 'auth.js', 'pages.js', 'gamification.js', 'nav.js', 'related.js', 'seo.js'])

def esc(s):
    return html.escape(s, quote=True)

def strip_tags(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s))

def tabs(active):
    items = [('parents.html', '👪 Espace parents', 'parents'), ('aide.html', '🆘 Aide élèves', 'aide'),
             ('ressources.html', '📥 Ressources gratuites', 'ressources'), ('index.html', '✏️ Exercices', 'ex')]
    cur = ' aria-current="page"'
    return '<nav class="g-tabs" aria-label="Rubriques">' + ''.join(
        '<a href="' + h + '"' + (cur if k == active else '') + '>' + t + '</a>' for h, t, k in items) + '</nav>'

NBSP = '\u00a0'
def typo(text):
    """Espaces insécables de la typographie française, hors balises et scripts."""
    parts = re.split(r'(<script.*?</script>|<[^>]+>)', text, flags=re.S)
    for i in range(0, len(parts), 2):
        t = parts[i]
        t = re.sub(r' ([:;?!»])', NBSP + r'\1', t)
        t = t.replace('« ', '«' + NBSP)
        parts[i] = t
    return ''.join(parts)

def page(slug, seo_title, description, kicker, h1, intro, active, main, schemas, og_type='article'):
    h1, intro, main = typo(h1), typo(intro), typo(main)
    url = f'{BASE}/{slug}.html'
    ld = '\n'.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="canonical" href="{url}">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(seo_title)} | École Facile</title>
<meta name="description" content="{esc(description)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(seo_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{BASE}/og-image.png">
<meta property="og:site_name" content="École Facile">
<meta property="og:locale" content="fr_FR">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="guides.css">
{ld}
</head>
<body class="g-page">
<header class="g-header">
  <div class="g-kicker">{esc(kicker)}</div>
  <h1>{h1}</h1>
  <p>{intro}</p>
  {tabs(active)}
</header>
<main class="g-main">
{main}
</main>
{FOOTER}
{SCRIPTS}
</body>
</html>
'''

def sources_html(keys):
    return ('<section class="g-sources"><h2>Sources</h2><ol>' +
            ''.join(f'<li>{esc(S[k][0])} — <a href="{S[k][1]}" rel="noopener" target="_blank">{esc(S[k][1].split("/")[2])}</a></li>' for k in keys) +
            '</ol></section>')

AUTHOR = ('<aside class="g-author"><span class="g-av">📚</span><div><strong>Rédigé par l\'équipe École Facile</strong>, '
          'site gratuit et sans publicité d\'exercices du CP à la 3e. Nos guides s\'appuient sur les textes officiels de '
          'l\'Éducation nationale et sur des travaux de recherche publiés, cités en sources. '
          f'Mis à jour le {UPDATED_FR}. <a href="a-propos.html">Notre méthode de rédaction</a>.</div></aside>')

def card(href, icon, title, text, extra=''):
    return f'<a class="g-card" href="{href}"><span class="g-ico">{icon}</span><strong>{title}</strong><span>{text}</span>{extra}</a>'

def article_cards(slugs):
    return '<div class="g-cards">' + ''.join(
        card(f'{s}.html', BY_SLUG[s]['icon'], BY_SLUG[s]['title'], BY_SLUG[s]['description'][:150].rsplit(' ', 1)[0] + '…') for s in slugs) + '</div>'

def build_article(a):
    hub = HUBS[a['hub']]
    siblings = [s for c in CLUSTERS for s in c[2] if a['slug'] in c[2] and s != a['slug']]
    words = len(strip_tags(a['body']).split())
    main = (f'<div class="g-meta"><span>Par <strong>l\'équipe École Facile</strong></span><span>Mis à jour le <time datetime="{UPDATED}">{UPDATED_FR}</time></span>'
            f'<span>Lecture : {a["minutes"]} min</span></div>'
            '<section class="g-tldr"><h2>L\'essentiel en 30 secondes</h2><ul>' + ''.join(f'<li>{t}</li>' for t in a['tldr']) + '</ul></section>'
            + a['body'] +
            '<h2>Questions fréquentes</h2><div class="g-faq">' +
            ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(r)}</p></details>' for q, r in a['faq']) + '</div>'
            '<h2>Pour aller plus loin</h2><div class="g-cta">' +
            ''.join(f'<a href="{h}">{esc(t)}<small>{esc(sm)}</small></a>' for h, t, sm in a['cta']) + '</div>'
            + (('<h2>Dans le même dossier</h2>' + article_cards(siblings)) if siblings else '')
            + sources_html(a['sources']) + AUTHOR)
    schemas = [
        {'@context': 'https://schema.org', '@type': 'Article', 'headline': strip_tags(a['title']), 'description': a['description'],
         'inLanguage': 'fr', 'datePublished': UPDATED, 'dateModified': UPDATED, 'wordCount': words,
         'mainEntityOfPage': f'{BASE}/{a["slug"]}.html', 'image': f'{BASE}/og-image.png',
         'author': {'@type': 'Organization', 'name': 'École Facile', 'url': BASE + '/'},
         'publisher': {'@type': 'Organization', 'name': 'École Facile', 'url': BASE + '/', 'logo': {'@type': 'ImageObject', 'url': f'{BASE}/favicon.svg'}},
         'audience': {'@type': 'Audience', 'audienceType': 'Parents' if a['hub'] == 'parents' else 'Élèves'},
         'isPartOf': {'@type': 'CollectionPage', 'name': hub['title'], 'url': f'{BASE}/{hub["slug"]}.html'},
         'citation': [S[k][1] for k in a['sources']]},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': r}} for q, r in a['faq']]},
    ]
    return page(a['slug'], a['seo_title'], a['description'], a['kicker'], a['title'], a['intro'], a['hub'], main, schemas)

def build_hub(key):
    h = HUBS[key]
    parts = []
    for hub, name, slugs in CLUSTERS:
        if hub == key:
            parts.append(f'<h2>{name}</h2>' + article_cards(slugs))
    if key == 'parents':
        parts.append('<h2>Ressources gratuites à imprimer</h2><p>Plannings, checklists, fiches méthode et exercices avec corrigé, en PDF.</p>'
                     '<div class="g-cards">' + ''.join(card('ressources.html', r['icon'], r['title'], r['public']) for r in RES[:6]) + '</div>'
                     '<p><a href="ressources.html">Voir toutes les ressources →</a></p>')
        parts.append('<h2>Le programme de chaque classe</h2><div class="g-cta">' + ''.join(
            f'<a href="programme-{l}.html">Programme {L}<small>Leçons et exercices</small></a>' for l, L in
            [('cp', 'CP'), ('ce1', 'CE1'), ('ce2', 'CE2'), ('cm1', 'CM1'), ('cm2', 'CM2'), ('6e', '6e'), ('5e', '5e'), ('4e', '4e'), ('3e', '3e')]) + '</div>')
        parts.append('<h2>Votre enfant bloque sur une notion ?</h2><p>Envoyez-le sur l\'<a href="aide.html">aide aux élèves</a> : '
                     'explications simples, erreurs fréquentes et exercices corrigés.</p>')
    else:
        parts.append('<h2>Je m\'entraîne</h2><p>Une fois que tu as compris, le meilleur moyen de retenir, c\'est de t\'entraîner : '
                     '<a href="index.html">choisis ta classe</a> et fais des exercices corrigés tout de suite. Tu préfères le papier ? '
                     'Les <a href="ressources.html">fiches à imprimer</a> ont un corrigé.</p>'
                     '<div class="g-tip"><strong>Parents :</strong> vous trouverez des conseils pour accompagner votre enfant dans '
                     'l\'<a href="parents.html">espace parents</a>.</div>')
    slugs = [s for c in CLUSTERS if c[0] == key for s in c[2]]
    schemas = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': h['title'], 'description': h['description'],
                'url': f'{BASE}/{h["slug"]}.html', 'inLanguage': 'fr',
                'hasPart': [{'@type': 'Article', 'headline': BY_SLUG[s]['title'], 'url': f'{BASE}/{s}.html'} for s in slugs]}]
    return page(h['slug'], h['seo_title'], h['description'], h['kicker'], h['title'], h['intro'], key, ''.join(parts), schemas, 'website')

def build_ressources():
    groups = {}
    for r in RES:
        groups.setdefault(r['group'], []).append(r)
    parts = ['<section class="g-tldr"><h2>Comment ça marche</h2><ul>'
             '<li>Tous les fichiers sont <strong>gratuits</strong>, en PDF, au format A4, sans inscription.</li>'
             '<li>Les fiches d\'exercices contiennent <strong>le corrigé</strong> en dernière page : imprimez-la à part.</li>'
             '<li>Usage libre à la maison et en classe. Merci de ne pas les revendre.</li></ul></section>']
    for g, items in groups.items():
        parts.append(f'<h2>{g}</h2><div class="g-cards">')
        for r in items:
            size = f'{max(1, round(r["bytes"] / 1024))} Ko'
            extra = (f'<span style="margin-top:6px">{"".join(f"<span class=g-pill>{esc(t)}</span>" for t in r["tags"])}</span>'
                     f'<span class="g-dl">⬇ Télécharger le PDF ({r["pages"]} p., {size})</span>')
            parts.append(f'<a class="g-card" href="ressources/{r["file"]}" download><span class="g-ico">{r["icon"]}</span>'
                         f'<strong>{esc(r["title"])}</strong><span>{esc(r["desc"])}</span>{extra}</a>')
        parts.append('</div>')
    parts.append('<h2>Pour aller plus loin</h2><div class="g-cta">'
                 '<a href="aider-son-enfant-a-faire-ses-devoirs.html">Aider son enfant à faire ses devoirs<small>Le guide complet</small></a>'
                 '<a href="comment-apprendre-une-lecon.html">Comment apprendre une leçon<small>La méthode en 4 étapes</small></a>'
                 '<a href="index.html">Exercices interactifs<small>Corrigés tout de suite</small></a></div>')
    parts.append(AUTHOR)
    schemas = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Ressources gratuites à imprimer',
                'url': f'{BASE}/ressources.html', 'inLanguage': 'fr',
                'hasPart': [{'@type': 'DigitalDocument', 'name': r['title'], 'encodingFormat': 'application/pdf',
                             'url': f'{BASE}/ressources/{r["file"]}', 'isAccessibleForFree': True,
                             'educationalLevel': ', '.join(r['tags'])} for r in RES]}]
    return page('ressources', 'Fiches gratuites à imprimer du CP à la 3e',
                'Fiches PDF gratuites du CP à la 3e : exercices corrigés, tables de multiplication, planning de devoirs, checklists, fiches méthode.',
                'Ressources gratuites', 'Ressources gratuites à imprimer',
                'Des fiches PDF pour les enfants et les parents : exercices avec corrigé, plannings, checklists et fiches méthode. Gratuit, sans inscription.',
                'ressources', ''.join(parts), schemas, 'website')

def build_apropos():
    main = f'''
<section class="g-tldr"><h2>En bref</h2><ul>
<li>École Facile est un site <strong>gratuit et sans publicité</strong> d'exercices interactifs du CP à la 3e.</li>
<li>Les exercices suivent les <strong>programmes officiels</strong> de l'Éducation nationale.</li>
<li>Nos guides citent leurs <strong>sources</strong> et sont datés.</li></ul></section>
<h2>Pourquoi ce site ?</h2>
<p>École Facile est né d'un besoin simple : permettre à un enfant de s'entraîner seul à la maison, avec des exercices courts, corrigés tout de suite et adaptés à sa classe, sans publicité ni abonnement.</p>
<h2>Comment nous créons les exercices</h2>
<ul>
<li>Chaque exercice est rattaché à une classe et à un thème du programme officiel (cycles 2, 3 et 4).</li>
<li>Chaque question a <strong>une seule bonne réponse</strong>, et les mauvaises réponses proposées correspondent à des erreurs fréquentes des élèves.</li>
<li>Avant publication des nouveaux exercices, les réponses calculables sont <strong>recalculées par programme</strong>, et chaque page est testée dans un navigateur.</li>
<li>De nouveaux exercices sont ajoutés régulièrement aux pages existantes.</li>
</ul>
<h2>Comment nous rédigeons les guides</h2>
<ul>
<li><strong>L'essentiel d'abord</strong> : chaque guide commence par un résumé, puis détaille.</li>
<li><strong>Des sources vérifiables</strong> : textes officiels (Bulletin officiel, education.gouv.fr, Éduscol), sites publics d'information et recherches publiées dans des revues scientifiques. Elles sont listées en bas de chaque page.</li>
<li><strong>Pas de chiffre sans source.</strong> Quand une recommandation est un repère de notre part (par exemple une durée de devoirs), nous le disons.</li>
<li><strong>Une date de mise à jour</strong> sur chaque guide ; nous corrigeons dès qu'une règle change.</li>
</ul>
<h2>Ce que nous ne faisons pas</h2>
<p>Pas de publicité, pas de vente de données, pas d'abonnement. Un compte est facultatif et sert seulement à garder sa progression.</p>
{AUTHOR}
'''
    schemas = [{'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'À propos d\'École Facile', 'url': f'{BASE}/a-propos.html',
                'inLanguage': 'fr', 'about': {'@type': 'Organization', 'name': 'École Facile', 'url': BASE + '/'}}]
    return page('a-propos', 'À propos : notre méthode pour les exercices et les guides',
                'Qui sommes-nous et comment nous créons les exercices et les guides d\'École Facile : programme officiel, vérification, sources, gratuité, sans publicité.',
                'À propos', 'À propos d\'École Facile', 'Un site gratuit, sans publicité, pour s\'entraîner du CP à la 3e. Voici comment nous travaillons.',
                None, main, schemas, 'website')

def update_sitemap(slugs):
    sm = open('sitemap.xml', encoding='utf-8').read()
    add = ''.join(f'  <url><loc>{BASE}/{s}.html</loc><lastmod>{UPDATED}</lastmod><priority>{p}</priority><changefreq>monthly</changefreq></url>\n'
                  for s, p in slugs if f'{BASE}/{s}.html<' not in sm)
    if add:
        sm = sm.replace('</urlset>', '\n' + add + '</urlset>')
        open('sitemap.xml', 'w', encoding='utf-8').write(sm)
    return add.count('<url>')

if __name__ == '__main__':
    out = {}
    for a in ARTICLES:
        out[a['slug']] = build_article(a)
    for k in HUBS:
        out[HUBS[k]['slug']] = build_hub(k)
    out['ressources'] = build_ressources()
    out['a-propos'] = build_apropos()
    for slug, text in out.items():
        open(f'{slug}.html', 'w', encoding='utf-8').write(text)
    n = update_sitemap([(s, '0.8' if s in ('parents', 'aide', 'ressources') or BY_SLUG.get(s, {}).get('pillar') else '0.7') for s in out])
    print(f'{len(out)} pages écrites · {n} URL ajoutées au sitemap')
