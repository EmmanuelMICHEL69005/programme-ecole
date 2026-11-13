# -*- coding: utf-8 -*-
"""Contenu des pages Guides parents et Aide élèves (généré par tools/build_guides.py).

Règles de rédaction :
- pyramide inversée : l'essentiel d'abord (encadré « L'essentiel »), puis le détail ;
- chaque chiffre et chaque citation a une source vérifiable listée en bas de page ;
- pas de chiffre inventé ; en cas de doute, on n'écrit pas ;
- tutoiement pour les élèves, vouvoiement pour les parents.
"""

UPDATED = '2026-11-13'
UPDATED_FR = '13 novembre 2026'

# ── Sources partagées (vérifiées le 13/11/2026) ──────────────────────
S = {
    'devoirs1956': ("Circonscription d'Oullins (académie de Lyon) — Historique de la suppression des devoirs à la maison (arrêté du 23 novembre 1956, circulaire du 29 décembre 1956, circulaire de 1994)",
                    'https://inspection-oullins.circo.ac-lyon.fr/spip/IMG/article_PDF/SUPPRESSION-DES-DEVOIRS-A-LA-MAISON_a76.pdf'),
    'devoirsfaits': ("Ministère de l'Éducation nationale — Devoirs faits : un temps d'étude accompagnée pour réaliser les devoirs",
                     'https://www.education.gouv.fr/devoirs-faits-un-temps-d-etude-accompagnee-pour-realiser-les-devoirs-7337'),
    'bo2023': ("Bulletin officiel n° 16 du 20 avril 2023 — Devoirs faits rendu obligatoire pour tous les élèves de 6e",
               'https://www.education.gouv.fr/bo/2023/Hebdo16/MENE2302487N'),
    'eduscoldf': ("Éduscol — Devoirs faits, un temps dédié pour accompagner les collégiens",
                  'https://eduscol.education.gouv.fr/5511/devoirs-faits-un-temps-dedie-pour-accompagner-les-collegiens-dans-la-realisation-de-leurs-devoirs'),
    'pisa': ("DEPP — PISA 2022 : la France ne fait pas exception à la baisse généralisée des performances en culture mathématique",
             'https://www.education.gouv.fr/depp/pisa-2022-la-france-ne-fait-pas-exception-la-baisse-generalisee-des-performances-en-culture-380205'),
    'sommeil': ("Santé.fr (Santé publique France) — Le sommeil de l'enfant",
                'https://www.sante.fr/le-sommeil-de-lenfant-0'),
    'mallette': ("Ministère de l'Éducation nationale — La Mallette des parents",
                 'https://mallettedesparents.education.gouv.fr/'),
    'roediger': ("Roediger H. L. & Karpicke J. D. (2006), « Test-Enhanced Learning », Psychological Science, 17(3) — communiqué de l'université Washington de Saint-Louis",
                 'https://source.washu.edu/2006/03/repeated-testtaking-better-for-retention-than-repeated-studying-research-shows/'),
    'cooper': ("Cooper H., Robinson J. C. & Patall E. A. (2006), « Does Homework Improve Academic Achievement? », Review of Educational Research, 76(1) — présentation par l'université Duke",
               'https://today.duke.edu/2006/03/homework.html'),
    'dehaene': ("Stanislas Dehaene (2018), Apprendre ! Les talents du cerveau, le défi des machines, Odile Jacob",
                'https://www.odilejacob.fr/catalogue/sciences/neurosciences/apprendre-_9782738145420.php'),
    'programmes': ("Éduscol — Programmes et ressources de l'école et du collège",
                   'https://eduscol.education.gouv.fr/'),
}

def stat(big, text, src):
    return f'<div class="g-stat"><b>{big}</b><span>{text}<small>Source : {src}</small></span></div>'

def quote(text, cite):
    return f'<blockquote class="g-quote">« {text} »<cite>— {cite}</cite></blockquote>'

ARTICLES = []

# ════════════════════════════════════════════════════════════════════
# CLUSTER PARENTS — ACCOMPAGNER LES DEVOIRS
# ════════════════════════════════════════════════════════════════════

ARTICLES.append(dict(
    slug='aider-son-enfant-a-faire-ses-devoirs', hub='parents', pillar=True, icon='🧭',
    kicker='Guide parents · Devoirs',
    title="Aider son enfant à faire ses devoirs : le guide complet (CP à la 3e)",
    seo_title="Aider son enfant à faire ses devoirs (CP à 3e)",
    description="Aider son enfant à faire ses devoirs sans conflit : rôle du parent, routine, durée selon l'âge, méthode, blocages. Conseils sourcés et fiches gratuites.",
    intro="Votre rôle n'est pas de refaire la classe, mais d'installer un cadre calme et régulier. Voici ce qui marche vraiment, ce que disent les textes officiels et la recherche, et des outils gratuits pour démarrer ce soir.",
    minutes=8,
    tldr=[
        "Votre rôle : un <strong>cadre</strong> (lieu, horaire, durée), de l'<strong>encouragement</strong> et des <strong>questions</strong>, pas les réponses.",
        "En primaire, les devoirs <strong>écrits</strong> à la maison sont interdits depuis 1956 : le soir, c'est surtout lire et apprendre ses leçons.",
        "Au collège, l'étude gratuite <strong>Devoirs faits</strong> existe dans chaque établissement ; elle est obligatoire en 6e depuis 2023.",
        "La méthode la plus efficace pour retenir : <strong>se tester</strong> plutôt que relire, et réviser en plusieurs petites séances.",
        "Si votre enfant bloque, on fait une pause, on découpe la tâche et on en parle à l'enseignant.",
    ],
    body=f"""
<h2>Quel est le vrai rôle d'un parent pendant les devoirs ?</h2>
<p>Le parent n'est pas un second professeur. Votre enfant a déjà un enseignant qui explique les notions. À la maison, ce qui l'aide le plus, c'est :</p>
<ul>
<li><strong>un cadre stable</strong> : toujours le même moment, le même endroit calme, sans écran allumé ;</li>
<li><strong>de l'intérêt</strong> : « Qu'as-tu appris aujourd'hui ? », « Explique-moi comment tu as fait » ;</li>
<li><strong>des questions plutôt que des réponses</strong> : « Que dit la consigne ? », « Où peux-tu trouver l'aide dans ta leçon ? » ;</li>
<li><strong>de la régularité</strong> : 15 minutes chaque soir valent mieux qu'une heure la veille du contrôle.</li>
</ul>
<p>Le neuroscientifique Stanislas Dehaene résume l'apprentissage en quatre « piliers » : l'<strong>attention</strong>, l'<strong>engagement actif</strong>, le <strong>retour sur l'erreur</strong> et la <strong>consolidation</strong> (notamment par le sommeil). Un bon accompagnement à la maison nourrit ces quatre piliers : peu de distractions, un enfant qui fait lui-même, des erreurs corrigées sans drame, et des révisions courtes et répétées.</p>

<h2>Ce que disent les règles officielles sur les devoirs</h2>
<h3>À l'école primaire (CP au CM2)</h3>
<p>C'est souvent une surprise pour les parents : les devoirs <strong>écrits</strong> à la maison sont interdits à l'école élémentaire depuis 1956. La circulaire du 29 décembre 1956 précise :</p>
{quote("Aucun devoir écrit, soit obligatoire, soit facultatif, ne sera demandé aux élèves hors de la classe.", "Circulaire du 29 décembre 1956, citée par la circonscription d'Oullins (académie de Lyon)")}
<p>Cette règle a été étendue au CP en 1964 et rappelée en 1994 : le travail du soir se limite à un <strong>travail oral</strong> ou à des <strong>leçons à apprendre</strong>. Dans la pratique, le soir, votre enfant lit, récite, révise ses mots ou ses tables. C'est précisément là que des exercices courts et corrigés tout de suite, comme ceux d'École Facile, sont utiles.</p>
<h3>Au collège (6e à 3e)</h3>
<p>Les devoirs écrits existent au collège. Pour que tous les élèves puissent les faire dans de bonnes conditions, le ministère a créé en 2017 <strong>Devoirs faits</strong>, un temps d'étude accompagnée et gratuit au collège.</p>
{stat("6e", "Depuis la rentrée 2023, Devoirs faits est obligatoire pour tous les élèves de 6e. Il reste proposé, sur inscription, aux autres niveaux.", "Bulletin officiel n° 16 du 20 avril 2023")}
<p>Renseignez-vous auprès du collège (professeur principal ou vie scolaire) : c'est souvent la meilleure solution quand les devoirs deviennent une source de conflit à la maison.</p>

<h2>Combien de temps de devoirs selon l'âge ?</h2>
<p>Il n'existe pas de durée officielle en France. La recherche apporte un repère utile : la grande synthèse de Harris Cooper et de ses collègues (université Duke, 2006) montre que le lien entre devoirs et réussite est <strong>bien plus fort au collège et au lycée qu'à l'école primaire</strong>. Pour les plus jeunes, faire plus longtemps n'apporte pas grand-chose : mieux vaut court et régulier.</p>
<p>Nous détaillons des repères par classe dans notre article <a href="combien-de-temps-de-devoirs-par-age.html">Combien de temps de devoirs selon l'âge</a>.</p>

<h2>Une routine en 5 étapes qui évite les conflits</h2>
<ol class="g-steps">
<li><strong>Goûter et pause</strong> (15-30 min) : l'enfant sort d'une longue journée. On ne commence pas en rentrant.</li>
<li><strong>On regarde l'agenda ensemble</strong> : qu'y a-t-il pour demain ? pour la semaine ? On commence par le plus difficile.</li>
<li><strong>L'enfant travaille seul</strong>, vous restez disponible à proximité. Vous intervenez à sa demande.</li>
<li><strong>On vérifie par des questions</strong> : « Récite-moi », « Montre-moi un exemple », « Fais-en un sans regarder ».</li>
<li><strong>On termine sur une réussite</strong> : un exercice réussi, un mot d'encouragement précis (« Tu as bien relu la consigne »).</li>
</ol>
<p>Pour vous aider, téléchargez notre <a href="ressources.html">planning de devoirs de la semaine et la checklist « Mes devoirs du soir »</a>, à imprimer gratuitement.</p>

<h2>Apprendre une leçon : la méthode qui marche</h2>
<p>Relire sa leçon trois fois donne une impression de maîtrise… qui s'efface vite. En 2006, les chercheurs Roediger et Karpicke ont comparé deux groupes d'étudiants : l'un relisait un texte, l'autre s'entraînait à le restituer de mémoire.</p>
{stat("61 % vs 40 %", "Une semaine plus tard, le groupe qui s'était testé retenait 61 % du texte, contre 40 % pour le groupe qui avait relu.", "Roediger &amp; Karpicke, Psychological Science, 2006")}
<p>Concrètement : on lit la leçon une fois, on cache, on essaie de la redire ou de refaire un exemple, puis on vérifie. Et on recommence le lendemain. Tout est expliqué pas à pas dans <a href="comment-apprendre-une-lecon.html">Comment apprendre une leçon efficacement</a>.</p>

<h2>Quand votre enfant dit « je n'y arrive pas »</h2>
<p>Pleurs, colère, « je suis nul » : c'est fréquent et ce n'est pas un échec de votre part. Trois réflexes : <strong>faire une pause</strong>, <strong>découper</strong> la tâche en une toute petite étape réussissable, et <strong>revenir à un exemple</strong> de la leçon. Si les blocages durent, parlez-en à l'enseignant. Notre article <a href="mon-enfant-n-y-arrive-pas.html">Mon enfant dit « je n'y arrive pas »</a> détaille quoi dire et quoi éviter.</p>

<h2>Le sommeil, premier allié des devoirs</h2>
<p>La consolidation des apprentissages se fait en grande partie pendant le sommeil. Santé publique France recommande <strong>9 à 11 heures de sommeil par nuit entre 6 et 11 ans</strong>, avec un coucher régulier. Des devoirs qui débordent tard le soir sont donc contre-productifs.</p>
""",
    faq=[
        ("Dois-je corriger les devoirs de mon enfant ?", "Pas systématiquement. L'enseignant a besoin de voir les vraies erreurs pour adapter son aide. Posez plutôt des questions qui poussent votre enfant à se relire : « Es-tu sûr de ce résultat ? Comment peux-tu vérifier ? »"),
        ("Mon enfant de CE1 a des exercices écrits à faire, est-ce normal ?", "Officiellement, les devoirs écrits à la maison ne doivent pas être donnés à l'école élémentaire (circulaires de 1956, 1964 et 1994). Dans les faits, certaines classes donnent de petits exercices. Si cela pose problème, parlez-en calmement avec l'enseignant."),
        ("Je ne comprends pas moi-même la leçon (maths de 4e, anglais…), comment l'aider ?", "Vous n'avez pas besoin de tout savoir. Demandez à votre enfant de vous expliquer la leçon : expliquer est une excellente façon d'apprendre. Au collège, orientez-le vers Devoirs faits, et utilisez les leçons et exercices corrigés d'École Facile."),
        ("Combien de temps doivent durer les devoirs en primaire ?", "Il n'y a pas de durée officielle. En pratique, de 10 à 20 minutes en CP-CE1 et de 20 à 30 minutes en CM suffisent largement, dès lors que c'est régulier."),
    ],
    cta=[('motiver-son-enfant-pour-les-devoirs.html', 'Motiver son enfant', '7 leviers concrets'),
         ('ressources.html', 'Ressources gratuites', 'Plannings, checklists, exercices à imprimer'),
         ('exercices-gratuits.html', 'Exercices gratuits', 'Du CP à la 3e, corrigés'),],
    sources=['devoirs1956', 'devoirsfaits', 'bo2023', 'cooper', 'roediger', 'dehaene', 'sommeil', 'mallette'],
))

ARTICLES.append(dict(
    slug='motiver-son-enfant-pour-les-devoirs', hub='parents', icon='🔥',
    kicker='Guide parents · Motivation',
    title="Comment motiver son enfant à faire ses devoirs : 7 leviers concrets",
    seo_title="Motiver son enfant à faire ses devoirs : 7 conseils",
    description="Votre enfant refuse ses devoirs ou traîne ? 7 leviers concrets pour le motiver sans crier : petits objectifs, choix, encouragements, routine.",
    intro="La motivation ne se commande pas, mais elle se cultive. Ces sept leviers reposent sur un principe simple : un enfant s'engage quand il se sent capable, un peu libre, et qu'il voit ses progrès.",
    minutes=6,
    tldr=[
        "Un enfant se motive quand il se sent <strong>capable</strong> : visez de petites réussites rapides.",
        "Donnez-lui des <strong>choix</strong> (ordre des exercices, lieu, pause) dans un cadre fixe.",
        "Félicitez l'<strong>effort et la stratégie</strong> (« tu as relu la consigne »), pas l'intelligence.",
        "Rendez les <strong>progrès visibles</strong> : tableau de réussites, séries, badges.",
        "Évitez le chantage et les récompenses matérielles systématiques.",
    ],
    body=f"""
<h2>Pourquoi mon enfant n'a-t-il pas envie de faire ses devoirs ?</h2>
<p>Avant de chercher « le truc », il vaut mieux comprendre la cause. Les plus fréquentes :</p>
<ul>
<li><strong>la fatigue</strong> : après 6 heures de classe, l'attention est épuisée ;</li>
<li><strong>le sentiment d'échec</strong> : « de toute façon, je n'y arrive pas » ;</li>
<li><strong>une tâche trop floue ou trop longue</strong> : « réviser le chapitre 3 » ne dit pas quoi faire ;</li>
<li><strong>la concurrence des écrans</strong>, bien plus gratifiants à court terme.</li>
</ul>
<p>Les leviers ci-dessous répondent chacun à une de ces causes.</p>

<h2>1. Commencer par une réussite facile</h2>
<p>Le premier exercice doit être réussi en moins de cinq minutes. Ce « démarrage » crée un élan. Sur École Facile, chaque page commence par des questions simples : c'est voulu.</p>

<h2>2. Découper en petites missions</h2>
<p>« Apprendre la leçon de géographie » devient : 1) lire le résumé, 2) cacher et redire les 3 mots clés, 3) répondre à 5 questions. Chaque mission terminée est cochée. Notre <a href="ressources.html">checklist « Mes devoirs du soir »</a> sert exactement à cela.</p>

<h2>3. Donner du choix dans un cadre fixe</h2>
<p>Le moment et la durée ne se négocient pas ; le reste, si. Votre enfant peut choisir par quoi il commence, s'il travaille à la table de la cuisine ou à son bureau, et quand il prend sa pause de 5 minutes. Se sentir un peu maître de son travail augmente fortement l'engagement.</p>

<h2>4. Féliciter l'effort et la stratégie, pas le « talent »</h2>
<p>« Tu es trop fort ! » est agréable mais fragile : au premier échec, l'enfant en conclut qu'il n'est plus « fort ». Préférez des encouragements <strong>précis</strong> sur ce qu'il a fait :</p>
<ul>
<li>« Tu as relu la consigne avant de répondre, c'est pour ça que c'est juste. »</li>
<li>« Tu t'es trompé, tu as cherché pourquoi et tu as corrigé : c'est comme ça qu'on apprend. »</li>
</ul>
<p>Cela rejoint le troisième pilier de l'apprentissage décrit par Stanislas Dehaene : le <strong>retour sur l'erreur</strong>. L'erreur est une information, pas une faute.</p>

<h2>5. Rendre les progrès visibles</h2>
<p>Un enfant voit rarement qu'il progresse. Montrez-le-lui : un tableau de réussites sur le frigo, une série de jours d'affilée, les points et badges gagnés sur École Facile. Téléchargez notre <a href="ressources.html">tableau de motivation à imprimer</a>.</p>

<h2>6. Donner du sens</h2>
<p>Reliez les apprentissages à la vie : les fractions dans une recette, les durées pour savoir à quelle heure part le train, l'anglais dans une chanson qu'il aime. « À quoi ça sert ? » est une vraie question qui mérite une vraie réponse.</p>

<h2>7. Protéger le temps de devoirs des écrans</h2>
<p>Téléphone dans une autre pièce, télévision éteinte, tablette rangée. Et si possible, l'écran récréatif <strong>après</strong> les devoirs plutôt qu'avant.</p>

<div class="g-warn"><strong>À éviter :</strong> le chantage (« pas de foot si… »), les comparaisons avec les frères et sœurs, les récompenses matérielles à chaque séance. Elles marchent quelques jours, puis l'enfant ne travaille plus que pour la récompense.</div>

<h2>Et si rien ne marche ?</h2>
<p>Si le refus est massif et durable, il cache souvent une difficulté (lecture, attention, anxiété) ou de la fatigue. Parlez-en à l'enseignant, et si besoin au médecin traitant. Lisez aussi <a href="mon-enfant-n-y-arrive-pas.html">Mon enfant dit « je n'y arrive pas » : que faire ?</a></p>
""",
    faq=[
        ("Faut-il récompenser son enfant quand il fait ses devoirs ?", "Les félicitations précises et un tableau de réussites suffisent la plupart du temps. Les récompenses matérielles systématiques finissent souvent par remplacer l'envie d'apprendre. Une petite récompense ponctuelle pour un gros effort reste possible."),
        ("Mon ado ne veut plus que je l'aide, que faire ?", "C'est normal au collège. Restez disponible sans surveiller : demandez son planning de la semaine, proposez Devoirs faits au collège, et intéressez-vous à ce qu'il apprend plutôt qu'à ses notes."),
        ("Mon enfant fait ses devoirs en traînant pendant des heures, que faire ?", "Fixez une durée maximale (par exemple 20 minutes en primaire) avec un minuteur, découpez en missions, et commencez par une tâche facile. Si cela persiste, parlez-en à l'enseignant : la quantité ou la difficulté est peut-être inadaptée."),
    ],
    cta=[('ressources.html', 'Tableau de motivation', 'À imprimer gratuitement'),
         ('aider-son-enfant-a-faire-ses-devoirs.html', 'Le guide complet des devoirs', 'Rôle du parent, routine, méthode'),
         ('index.html', 'Exercices interactifs', 'Points, badges, correction immédiate')],
    sources=['dehaene', 'mallette'],
))

ARTICLES.append(dict(
    slug='combien-de-temps-de-devoirs-par-age', hub='parents', icon='⏱️',
    kicker='Guide parents · Organisation',
    title="Combien de temps de devoirs selon l'âge ? Repères du CP à la 3e",
    seo_title="Combien de temps de devoirs selon l'âge ?",
    description="Combien de temps doivent durer les devoirs en CP, CE1, CM2, 6e ou 3e ? Repères par classe, règles officielles, ce que dit la recherche et une routine du soir à imprimer.",
    intro="Il n'existe pas de durée officielle en France. Voici des repères raisonnables par classe, fondés sur les textes officiels et la recherche, pour un temps de devoirs efficace qui laisse aussi la place au jeu et au sommeil.",
    minutes=5,
    tldr=[
        "Primaire : <strong>pas de devoirs écrits</strong> officiellement ; lecture et leçons, environ <strong>10 à 30 minutes</strong> selon la classe.",
        "Collège : environ <strong>30 minutes à 1 h 30</strong> selon le niveau et les jours, avec l'aide gratuite de Devoirs faits.",
        "Plus long n'est pas mieux, surtout pour les plus jeunes : la régularité compte plus que la durée.",
        "Le sommeil passe avant : 9 à 11 heures par nuit entre 6 et 11 ans.",
    ],
    body=f"""
<h2>Les repères par classe</h2>
<p>Ces durées sont des <strong>repères indicatifs</strong> établis par École Facile à partir des textes officiels (pas de devoirs écrits en primaire) et des travaux de recherche cités plus bas. Ils concernent le travail quotidien, hors révisions d'un contrôle.</p>
<div class="g-table-wrap"><table class="g-table">
<thead><tr><th>Classe</th><th>Durée indicative par soir</th><th>Contenu typique</th></tr></thead>
<tbody>
<tr><td>CP</td><td>10 à 15 min</td><td>Lecture à voix haute, mots à apprendre</td></tr>
<tr><td>CE1 - CE2</td><td>15 à 20 min</td><td>Lecture, leçons courtes, tables, mots</td></tr>
<tr><td>CM1 - CM2</td><td>20 à 30 min</td><td>Leçons, conjugaison, tables, lecture</td></tr>
<tr><td>6e - 5e</td><td>30 à 45 min</td><td>Exercices écrits, leçons, préparation des contrôles</td></tr>
<tr><td>4e - 3e</td><td>45 min à 1 h 30</td><td>Exercices, révisions, préparation du brevet en 3e</td></tr>
</tbody></table></div>
<p>Si votre enfant dépasse régulièrement ces durées en travaillant sérieusement, ce n'est pas forcément un problème de volonté : la tâche est peut-être trop difficile ou mal comprise. Parlez-en à l'enseignant.</p>

<h2>Ce que disent les textes officiels</h2>
<p>À l'école élémentaire, la circulaire du 29 décembre 1956 interdit les devoirs écrits hors de la classe ; cette règle a été étendue au CP en 1964 et rappelée en 1994, qui limite le travail du soir à un travail oral ou à des leçons à apprendre. Au collège, aucun texte ne fixe de durée, mais le ministère a mis en place <strong>Devoirs faits</strong> (2017), obligatoire pour tous les élèves de 6e depuis la rentrée 2023.</p>

<h2>Ce que dit la recherche</h2>
<p>La synthèse de référence de Harris Cooper, Jorgianne Robinson et Erika Patall (université Duke, 2006) observe un lien positif entre devoirs et réussite, <strong>nettement plus fort au collège et au lycée qu'à l'école primaire</strong>. Harris Cooper cite aussi un repère répandu aux États-Unis, la « règle des 10 minutes » : environ 10 minutes de devoirs par année de scolarité. C'est une règle empirique, pas une norme ; nos repères français, plus prudents en primaire, en restent proches.</p>

<h2>Une routine du soir type</h2>
<ol class="g-steps">
<li><strong>16 h 30 - 17 h</strong> : goûter, jeu dehors, décompression.</li>
<li><strong>17 h - 17 h 20</strong> (primaire) ou <strong>17 h - 18 h</strong> (collège) : devoirs, le plus difficile en premier.</li>
<li><strong>5 minutes</strong> : on prépare le cartable du lendemain avec la <a href="ressources.html">checklist cartable</a>.</li>
<li><strong>Le soir</strong> : 5 minutes de relecture rapide avant de dormir (une leçon, quelques mots), puis coucher à heure fixe.</li>
</ol>
<div class="g-tip"><strong>Astuce :</strong> utilisez un minuteur visible. L'enfant sait quand cela s'arrête, ce qui réduit beaucoup les négociations.</div>

<h2>Et le week-end ?</h2>
<p>En primaire, une petite séance de lecture ou de jeu éducatif suffit. Au collège, planifiez le travail long (exposé, révisions) sur la semaine plutôt que tout le dimanche soir : notre <a href="ressources.html">planning de devoirs de la semaine</a> aide à répartir.</p>

{stat("9 à 11 h", "de sommeil par nuit recommandées entre 6 et 11 ans, avec un coucher régulier.", "Santé publique France, via Santé.fr")}
""",
    faq=[
        ("Est-ce que les devoirs sont obligatoires en primaire ?", "Les devoirs écrits à la maison ne doivent pas être donnés à l'école élémentaire (circulaires de 1956, 1964 et 1994). Les leçons à apprendre et la lecture restent attendues."),
        ("Mon enfant de 6e travaille 2 heures par soir, est-ce trop ?", "C'est au-dessus des repères habituels. Vérifiez s'il travaille avec des distractions, s'il a compris les consignes, et parlez-en au professeur principal. Devoirs faits, obligatoire en 6e, permet aussi d'avancer au collège."),
        ("Faut-il faire des devoirs pendant les vacances ?", "Ce n'est pas obligatoire. Quelques minutes de lecture et des jeux de calcul gardent les acquis sans transformer les vacances en corvée. Nos exercices courts s'y prêtent bien."),
    ],
    cta=[('ressources.html', 'Planning de devoirs à imprimer', 'Semaine type, gratuit'),
         ('aider-son-enfant-a-faire-ses-devoirs.html', 'Aider son enfant à faire ses devoirs', 'Le guide complet'),
         ('entree-en-sixieme.html', "Réussir l'entrée en 6e", 'Organisation, Devoirs faits')],
    sources=['devoirs1956', 'devoirsfaits', 'bo2023', 'cooper', 'sommeil'],
))

ARTICLES.append(dict(
    slug='mon-enfant-n-y-arrive-pas', hub='parents', icon='🤝',
    kicker='Guide parents · Difficultés',
    title="Mon enfant dit « je n'y arrive pas » : que faire ?",
    seo_title="Enfant qui bloque : « je n'y arrive pas »",
    description="Pleurs, colère, « je suis nul » pendant les devoirs ? Les bons réflexes pour débloquer la situation, les phrases à dire et à éviter, et quand consulter.",
    intro="Un enfant qui bloque n'est ni paresseux ni « nul » : il est face à une tâche qui, à ce moment-là, lui paraît trop grande. Votre mission : la rendre plus petite.",
    minutes=6,
    tldr=[
        "D'abord <strong>calmer</strong> : pause de 5 minutes, verre d'eau, respiration.",
        "Ensuite <strong>découper</strong> : une seule petite étape réussissable.",
        "Revenir à un <strong>exemple</strong> de la leçon, puis faire un exercice presque identique.",
        "Remplacer « tu es nul » par « <strong>tu ne sais pas encore</strong> ».",
        "Si le blocage dure ou se répète, en parler à l'enseignant.",
    ],
    body=f"""
<h2>Pourquoi un enfant bloque-t-il ?</h2>
<p>Derrière « je n'y arrive pas », il y a souvent l'une de ces situations :</p>
<ul>
<li>il n'a <strong>pas compris la consigne</strong> (un mot inconnu suffit) ;</li>
<li>il lui <strong>manque une notion d'avant</strong> (par exemple les tables, pour la division) ;</li>
<li>il est <strong>fatigué</strong> ou <strong>stressé</strong>, et son attention s'effondre ;</li>
<li>il a peur de se tromper devant vous.</li>
</ul>

<h2>Les 5 réflexes qui débloquent</h2>
<ol class="g-steps">
<li><strong>Accueillir l'émotion</strong> : « Je vois que c'est difficile, on fait une pause et on reprend ensemble. » Un cerveau en colère ou en larmes n'apprend pas.</li>
<li><strong>Faire reformuler la consigne</strong> : « Explique-moi avec tes mots ce qu'on te demande. » Très souvent, le blocage est là.</li>
<li><strong>Revenir à la leçon</strong> : chercher ensemble un exemple résolu, le refaire en cachant la solution.</li>
<li><strong>Découper</strong> : « On fait seulement la première ligne. » Puis la suivante.</li>
<li><strong>Finir sur une réussite</strong>, même petite, et le dire : « Tu vois, tu as trouvé la méthode. »</li>
</ol>

<h2>Les phrases qui aident… et celles qui bloquent</h2>
<div class="g-table-wrap"><table class="g-table">
<thead><tr><th>À dire</th><th>À éviter</th></tr></thead>
<tbody>
<tr><td>« Tu ne sais pas <strong>encore</strong>. »</td><td>« C'est pourtant facile ! »</td></tr>
<tr><td>« Montre-moi où tu bloques. »</td><td>« Tu n'écoutes jamais en classe. »</td></tr>
<tr><td>« Qu'est-ce que tu as déjà essayé ? »</td><td>« Donne, je vais le faire. »</td></tr>
<tr><td>« L'erreur nous dit ce qu'il faut revoir. »</td><td>« Ta sœur, elle, y arrivait. »</td></tr>
</tbody></table></div>
<p>L'idée de « pas encore » est importante : elle montre que la compétence se construit. C'est aussi ce que décrit la recherche en sciences cognitives, pour laquelle le <strong>retour sur l'erreur</strong> est l'un des quatre piliers de l'apprentissage (Stanislas Dehaene).</p>

<h2>Et si je ne comprends pas moi-même l'exercice ?</h2>
<p>C'est fréquent au collège. Ce n'est pas grave, et c'est même une occasion : demandez à votre enfant de vous expliquer la leçon. Expliquer oblige à organiser ce qu'on sait. Vous pouvez aussi vous appuyer sur nos <a href="cours.html">leçons courtes</a> et nos pages d'aide pour les élèves, comme <a href="je-ne-comprends-pas-les-fractions.html">Je ne comprends pas les fractions</a> ou <a href="resoudre-un-probleme-de-maths.html">Je n'arrive pas à résoudre les problèmes</a>.</p>

<h2>Quand faut-il s'inquiéter ?</h2>
<p>Parlez-en à l'enseignant si :</p>
<ul>
<li>les blocages reviennent presque tous les soirs, sur des matières différentes ;</li>
<li>la lecture reste très lente ou très laborieuse au-delà du CE1 ;</li>
<li>votre enfant exprime une forte anxiété (maux de ventre avant l'école, refus d'y aller).</li>
</ul>
<p>L'enseignant pourra proposer une aide adaptée et, si besoin, orienter vers le médecin scolaire ou le médecin traitant. Le site officiel <a href="https://mallettedesparents.education.gouv.fr/" rel="noopener">La Mallette des parents</a> du ministère donne aussi des repères sur le dialogue avec l'école.</p>
""",
    faq=[
        ("Mon enfant pleure pendant les devoirs, est-ce que j'arrête ?", "Faites une vraie pause. Si les larmes reviennent, arrêtez pour ce soir et écrivez un mot à l'enseignant : « Il a essayé, il a bloqué à tel endroit. » C'est une information précieuse pour lui."),
        ("Faut-il faire les exercices à la place de l'enfant ?", "Non : l'enseignant ne verrait pas la difficulté. Mieux vaut un exercice inachevé mais honnête, accompagné d'un mot, qu'un exercice parfait fait par un adulte."),
        ("Les exercices en ligne peuvent-ils aider un enfant qui bloque ?", "Oui, s'ils sont courts et corrigés immédiatement : l'enfant voit tout de suite s'il a juste, sans attendre ni se sentir jugé. C'est le principe des exercices d'École Facile, du CP à la 3e."),
    ],
    cta=[('aide.html', "L'aide pour les élèves", 'Fractions, tables, problèmes…'),
         ('motiver-son-enfant-pour-les-devoirs.html', 'Motiver son enfant', '7 leviers concrets'),
         ('ressources.html', 'Fiches méthode à imprimer', 'Gratuites')],
    sources=['dehaene', 'mallette'],
))

ARTICLES.append(dict(
    slug='comment-apprendre-une-lecon', hub='parents', icon='🧠',
    kicker='Méthode · Apprendre',
    title="Comment apprendre une leçon efficacement : la méthode en 4 étapes",
    seo_title="Comment apprendre une leçon efficacement",
    description="Relire ne suffit pas. La méthode en 4 étapes pour retenir une leçon : comprendre, se tester, espacer, dormir. Fiche à imprimer.",
    intro="Relire sa leçon trois fois donne l'impression de la savoir. Mais une semaine plus tard, presque tout est oublié. La recherche montre une méthode bien plus efficace, et elle tient en 4 étapes.",
    minutes=6,
    tldr=[
        "<strong>Comprendre</strong> d'abord : reformuler avec ses mots, trouver un exemple.",
        "<strong>Se tester</strong> : cacher la leçon et la redire, plutôt que la relire.",
        "<strong>Espacer</strong> : plusieurs petites séances (aujourd'hui, demain, dans 3 jours).",
        "<strong>Dormir</strong> : le sommeil consolide ce qui a été appris.",
    ],
    body=f"""
<h2>Pourquoi relire ne suffit pas</h2>
<p>Quand on relit, tout paraît familier, et on croit savoir. C'est une illusion : reconnaître n'est pas se souvenir. Le jour du contrôle, il faut <strong>retrouver</strong> l'information seul, sans la leçon sous les yeux. C'est donc ce geste-là qu'il faut entraîner.</p>
{stat("61 % vs 40 %", "Une semaine après, des étudiants qui s'étaient entraînés à restituer un texte de mémoire en retenaient 61 %, contre 40 % pour ceux qui l'avaient relu.", "Roediger &amp; Karpicke, Psychological Science, 2006")}

<h2>La méthode en 4 étapes</h2>
<ol class="g-steps">
<li><strong>Comprendre.</strong> Lire la leçon une fois, lentement. Pour chaque paragraphe, se demander : « Qu'est-ce que ça veut dire ? Quel exemple je peux donner ? » Un mot inconnu ? On le cherche.</li>
<li><strong>Se tester.</strong> Cacher la leçon. Redire à voix haute, écrire les mots clés sur une feuille, refaire un exemple, ou répondre à des questions. Puis vérifier, et corriger ce qui manquait.</li>
<li><strong>Espacer.</strong> Recommencer le test le lendemain, puis quelques jours après. Trois séances de 10 minutes réparties valent mieux qu'une séance de 30 minutes la veille.</li>
<li><strong>Dormir.</strong> Une courte relecture-test avant le coucher, puis une vraie nuit : pendant le sommeil, le cerveau consolide ce qu'il a appris.</li>
</ol>
<p>Ces étapes correspondent aux quatre piliers de l'apprentissage décrits par Stanislas Dehaene : <strong>attention</strong> (étape 1), <strong>engagement actif</strong> et <strong>retour sur l'erreur</strong> (étape 2), <strong>consolidation</strong> (étapes 3 et 4).</p>

<h2>Adapter la méthode selon l'âge</h2>
<h3>En primaire (CP au CM2)</h3>
<ul>
<li>Le parent pose les questions : « Que veut dire… ? », « Donne-moi un exemple ».</li>
<li>Pour une poésie : un vers, puis deux, puis la strophe, en cachant à chaque fois.</li>
<li>Pour les mots ou les tables : petites cartes avec la question d'un côté et la réponse de l'autre.</li>
</ul>
<h3>Au collège (6e à 3e)</h3>
<ul>
<li>L'élève fabrique ses propres questions à partir de la leçon (5 questions par chapitre).</li>
<li>Il fait une carte mentale de mémoire, puis la compare avec le cours.</li>
<li>Il prévoit ses séances de révision dans un planning, plusieurs jours avant le contrôle.</li>
</ul>

<h2>Les exercices corrigés : la façon la plus simple de se tester</h2>
<p>Un exercice avec correction immédiate est un test : on cherche, on répond, on voit tout de suite si c'est juste. C'est l'idée des pages d'École Facile : <a href="cours.html">une leçon courte</a>, puis des <a href="index.html">exercices corrigés</a> sur le même thème, du CP à la 3e.</p>
<div class="g-tip"><strong>À imprimer :</strong> notre <a href="ressources.html">fiche méthode « Apprendre une leçon »</a> résume les 4 étapes pour l'avoir sous les yeux au bureau.</div>
""",
    faq=[
        ("Combien de fois faut-il réviser une leçon ?", "Au moins trois fois, de façon espacée : le jour même, le lendemain, et quelques jours plus tard. À chaque fois, en se testant plutôt qu'en relisant."),
        ("Les fiches de révision, ça marche ?", "Oui, si on s'en sert pour se tester (question d'un côté, réponse de l'autre). Recopier la leçon proprement prend du temps mais aide peu à retenir."),
        ("Mon enfant connaît sa leçon le soir et l'a oubliée le lendemain, pourquoi ?", "C'est l'oubli normal quand on apprend tout en une fois. Une séance courte de test le lendemain matin et quelques jours plus tard suffit à fixer la leçon."),
    ],
    cta=[('ressources.html', 'Fiche méthode à imprimer', 'Apprendre une leçon en 4 étapes'),
         ('cours.html', 'Toutes les leçons', 'Du CP à la 3e'),
         ('aider-son-enfant-a-faire-ses-devoirs.html', 'Le guide des devoirs', 'Pour les parents')],
    sources=['roediger', 'dehaene', 'sommeil'],
))

# ════════════════════════════════════════════════════════════════════
# CLUSTER PARENTS — PROGRAMME ET RESSOURCES
# ════════════════════════════════════════════════════════════════════

ARTICLES.append(dict(
    slug='exercices-gratuits', hub='parents', pillar=True, icon='🎁',
    kicker='Guide parents · Ressources gratuites',
    title="Exercices gratuits du CP à la 3e : conformes au programme et corrigés",
    seo_title="Exercices gratuits du CP à la 3e, corrigés",
    description="Exercices gratuits et corrigés du CP à la 3e, conformes au programme : maths, français, histoire-géo, anglais. Sans pub, sans inscription.",
    intro="École Facile propose gratuitement, sans publicité et sans inscription obligatoire, des exercices interactifs corrigés pour chaque classe du CP à la 3e, des leçons courtes et des fiches à imprimer.",
    minutes=4,
    tldr=[
        "Des exercices <strong>interactifs et corrigés immédiatement</strong> pour les 9 niveaux, du CP à la 3e.",
        "Maths, français, histoire-géographie, anglais (collège) et EPS, organisés selon le <strong>programme officiel</strong>.",
        "<strong>Gratuit, sans publicité</strong>, utilisable sans compte ; de nouveaux exercices sont ajoutés régulièrement.",
        "Des <strong>fiches à imprimer</strong> avec corrigé, des plannings et des checklists dans les ressources.",
    ],
    body="""
<h2>Choisir la classe de votre enfant</h2>
<p>Chaque page « programme » résume ce qu'il faut savoir en fin d'année et renvoie vers les leçons et les exercices correspondants.</p>
<div class="g-cta">
<a href="programme-cp.html">CP<small>Lire, compter jusqu'à 100</small></a>
<a href="programme-ce1.html">CE1<small>Nombres jusqu'à 1 000, premières tables</small></a>
<a href="programme-ce2.html">CE2<small>Tables, division, imparfait</small></a>
<a href="programme-cm1.html">CM1<small>Fractions, décimaux, impératif</small></a>
<a href="programme-cm2.html">CM2<small>Proportionnalité, phrase complexe</small></a>
<a href="programme-6e.html">6e<small>Fractions, nombres décimaux</small></a>
<a href="programme-5e.html">5e<small>Calcul littéral, puissances</small></a>
<a href="programme-4e.html">4e<small>Équations, Pythagore</small></a>
<a href="programme-3e.html">3e<small>Fonctions, préparation du brevet</small></a>
</div>

<h2>Comment sont conçus nos exercices</h2>
<ul>
<li><strong>Alignés sur le programme</strong> de l'Éducation nationale pour chaque classe et chaque thème.</li>
<li><strong>Correction immédiate</strong> : l'enfant voit tout de suite s'il a juste, ce qui en fait de véritables petits tests de mémoire, la méthode la plus efficace pour retenir.</li>
<li><strong>Courts</strong> : 4 à 5 questions par exercice, pour travailler 10 minutes sans se lasser.</li>
<li><strong>Vérifiés</strong> : une seule réponse juste par question ; pour les nouveaux exercices, chaque réponse calculable est recalculée par programme avant publication.</li>
<li><strong>Motivants</strong> : points d'expérience et badges pour rendre les progrès visibles.</li>
</ul>

<h2>Comment les utiliser à la maison</h2>
<ol class="g-steps">
<li>Lisez la <a href="cours.html">leçon courte</a> du thème avec votre enfant (2 à 3 minutes).</li>
<li>Laissez-le faire un exercice seul, puis regardez ensemble les erreurs.</li>
<li>Refaites le même thème quelques jours plus tard : c'est la répétition espacée qui fixe les connaissances.</li>
</ol>
<p>Pour la méthode complète, lisez <a href="aider-son-enfant-a-faire-ses-devoirs.html">Aider son enfant à faire ses devoirs</a> et <a href="comment-apprendre-une-lecon.html">Comment apprendre une leçon efficacement</a>.</p>

<h2>Des fiches gratuites à imprimer</h2>
<p>Pour travailler sans écran : tables de multiplication, calcul mental, fractions et conjugaison, chaque fois <strong>avec le corrigé</strong>, ainsi que des plannings et des checklists pour organiser la semaine. Tout est dans les <a href="ressources.html">ressources gratuites</a>.</p>

<h2>Votre enfant bloque sur une notion ?</h2>
<p>Nos pages d'aide expliquent simplement les notions qui posent le plus souvent problème : <a href="je-ne-comprends-pas-les-fractions.html">les fractions</a>, <a href="apprendre-les-tables-de-multiplication.html">les tables de multiplication</a>, <a href="resoudre-un-probleme-de-maths.html">les problèmes de maths</a>.</p>
""",
    faq=[
        ("Les exercices d'École Facile sont-ils vraiment gratuits ?", "Oui. Le site est gratuit et sans publicité. Créer un compte est facultatif : il sert seulement à garder ses points et sa progression."),
        ("Les exercices suivent-ils le programme officiel ?", "Oui, ils sont organisés par classe et par thème selon les programmes de l'Éducation nationale du cycle 2 (CP-CE2), du cycle 3 (CM1-6e) et du cycle 4 (5e-3e)."),
        ("Peut-on imprimer les exercices ?", "Les exercices interactifs se font à l'écran, mais des fiches PDF à imprimer, avec corrigé, sont disponibles dans la page Ressources."),
    ],
    cta=[('ressources.html', 'Fiches à imprimer', 'PDF gratuits avec corrigé'),
         ('cours.html', 'Toutes les leçons', 'Courtes et illustrées'),
         ('index.html', 'Commencer les exercices', 'Choisir sa classe')],
    sources=['programmes', 'roediger'],
))

ARTICLES.append(dict(
    slug='entree-en-sixieme', hub='parents', icon='🎒',
    kicker='Guide parents · Collège',
    title="Réussir l'entrée en 6e : organisation, devoirs et conseils pour les parents",
    seo_title="Entrée en 6e : aider son enfant à réussir",
    description="Plusieurs professeurs, agenda, Devoirs faits obligatoire : comment accompagner votre enfant à l'entrée en 6e. Conseils et checklist.",
    intro="L'entrée en 6e change beaucoup de choses : plusieurs professeurs, un emploi du temps qui varie, plus d'autonomie. Les élèves qui s'en sortent le mieux sont souvent ceux qui sont les mieux organisés.",
    minutes=6,
    tldr=[
        "Le défi principal de la 6e est l'<strong>organisation</strong> : agenda, cartable, emploi du temps.",
        "Depuis 2023, <strong>Devoirs faits</strong> est obligatoire et gratuit pour tous les élèves de 6e.",
        "Vérifiez l'agenda (ou l'ENT) <strong>avec</strong> votre enfant les premières semaines, puis laissez-le faire seul.",
        "Revoir les bases du CM2 (fractions, décimaux, conjugaison) sécurise le début d'année.",
    ],
    body=f"""
<h2>Ce qui change vraiment en 6e</h2>
<ul>
<li><strong>Un professeur par matière</strong>, avec ses propres habitudes et exigences.</li>
<li><strong>Un emploi du temps</strong> différent chaque jour, parfois avec des semaines A et B.</li>
<li><strong>Un agenda ou un cahier de textes en ligne</strong> (l'ENT) à consulter soi-même.</li>
<li><strong>Des devoirs écrits</strong>, et des contrôles annoncés à l'avance qu'il faut préparer sur plusieurs jours.</li>
</ul>

<h2>Devoirs faits : une aide gratuite à utiliser</h2>
{stat("Obligatoire", "Depuis la rentrée 2023, l'accompagnement aux devoirs Devoirs faits est rendu obligatoire pour tous les élèves de 6e.", "Bulletin officiel n° 16 du 20 avril 2023")}
<p>Ce temps d'étude, encadré au collège, permet à votre enfant de faire une partie de ses devoirs avec un adulte disponible pour l'aider. Demandez-lui ce qu'il y fait, et encouragez-le à y poser ses questions. Le ministère propose aussi <strong>Jules</strong>, un assistant numérique du CNED pour accompagner les collégiens dans le cadre de Devoirs faits.</p>

<h2>L'organisation en 5 habitudes</h2>
<ol class="g-steps">
<li><strong>Chaque soir</strong> : on regarde l'agenda pour le lendemain <em>et</em> pour la semaine.</li>
<li><strong>Le cartable se fait la veille</strong>, avec l'emploi du temps sous les yeux (notre <a href="ressources.html">checklist cartable</a> aide beaucoup).</li>
<li><strong>Un contrôle annoncé</strong> = trois petites séances de révision réparties, pas une seule la veille.</li>
<li><strong>Un endroit fixe</strong> pour les affaires de classe et un pour les devoirs.</li>
<li><strong>Le week-end</strong> : 10 minutes pour faire le point sur la semaine suivante.</li>
</ol>

<h2>Revoir les bases du CM2 avant et pendant la 6e</h2>
<p>La 6e appartient au même cycle que le CM1 et le CM2 (le cycle 3) : elle consolide ce qui a été vu à l'école. Revoir quelques notions clés rassure et fait gagner du temps :</p>
<div class="g-cta">
<a href="fractions-cm2.html">Fractions CM2<small>Exercices corrigés</small></a>
<a href="decimaux-cm2.html">Nombres décimaux CM2<small>Exercices corrigés</small></a>
<a href="conjugaison-cm2.html">Conjugaison CM2<small>Exercices corrigés</small></a>
<a href="programme-6e.html">Programme de 6e<small>Ce qu'il faut savoir</small></a>
</div>

<h2>Le rôle des parents en 6e</h2>
<p>Les premières semaines, faites <strong>avec</strong> votre enfant : regarder l'agenda, préparer le cartable, planifier les révisions. Puis, petit à petit, laissez-le faire seul et vérifiez seulement. L'objectif de l'année est qu'il devienne autonome.</p>
<p>Restez aussi en lien avec le collège : réunion de rentrée, professeur principal, carnet de liaison. Le site officiel <a href="https://mallettedesparents.education.gouv.fr/" rel="noopener">La Mallette des parents</a> explique le fonctionnement du collège.</p>
""",
    faq=[
        ("Devoirs faits est-il payant ?", "Non, Devoirs faits est gratuit. Il est obligatoire en 6e depuis la rentrée 2023 et proposé aux autres niveaux du collège selon l'organisation de chaque établissement."),
        ("Mon enfant oublie toujours ses affaires, que faire ?", "Préparez le cartable la veille avec l'emploi du temps et une checklist affichée près du bureau. Après quelques semaines, l'habitude s'installe."),
        ("Combien de temps de devoirs en 6e ?", "Comptez en moyenne 30 à 45 minutes par soir, plus les révisions avant un contrôle. Si c'est beaucoup plus, parlez-en au professeur principal."),
    ],
    cta=[('ressources.html', 'Checklist cartable et planning', 'À imprimer'),
         ('programme-6e.html', 'Le programme de 6e', 'Leçons et exercices'),
         ('combien-de-temps-de-devoirs-par-age.html', 'Temps de devoirs par âge', 'Repères CP-3e')],
    sources=['bo2023', 'devoirsfaits', 'eduscoldf', 'mallette'],
))

# ════════════════════════════════════════════════════════════════════
# CLUSTER ÉLÈVES — « JE NE COMPRENDS PAS… »
# ════════════════════════════════════════════════════════════════════

ARTICLES.append(dict(
    slug='je-ne-comprends-pas-les-fractions', hub='aide', icon='🍕',
    kicker='Aide élèves · Maths',
    title="Je ne comprends pas les fractions : l'explication simple",
    seo_title="Je ne comprends pas les fractions : explication",
    description="Les fractions expliquées simplement avec des pizzas : numérateur, dénominateur, comparer, additionner. Erreurs à éviter et exercices corrigés.",
    intro="Pas de panique : une fraction, c'est juste une façon de dire « combien de parts on prend » quand on a coupé quelque chose en parts égales. On reprend tout depuis le début.",
    minutes=5,
    tldr=[
        "Dans <strong>3/4</strong>, le 4 (en bas) dit en combien de parts égales on coupe, le 3 (en haut) combien de parts on prend.",
        "Même nombre en bas : la plus grande fraction est celle qui a <strong>le plus grand nombre en haut</strong>.",
        "Même nombre en haut : la plus grande est celle qui a <strong>le plus petit nombre en bas</strong> (les parts sont plus grosses).",
        "Pour additionner 2/5 + 1/5, on ajoute les nombres du haut : <strong>3/5</strong>. Le bas ne change pas.",
    ],
    body="""
<h2>C'est quoi, une fraction ?</h2>
<p>Imagine une pizza coupée en <strong>4 parts égales</strong>. Tu en manges <strong>3</strong>. Tu as mangé <strong>3/4</strong> de la pizza (on dit « trois quarts »).</p>
<ul>
<li>Le nombre <strong>du bas</strong> s'appelle le <strong>dénominateur</strong> : en combien de parts égales on a coupé (ici 4).</li>
<li>Le nombre <strong>du haut</strong> s'appelle le <strong>numérateur</strong> : combien de parts on prend (ici 3).</li>
</ul>
<div class="g-tip"><strong>Pour t'en souvenir :</strong> le <strong>D</strong>énominateur est en <strong>D</strong>essous.</div>
<p>Attention, les parts doivent être <strong>égales</strong>. Une pizza coupée en 4 morceaux de tailles différentes, ce ne sont pas des quarts.</p>

<h2>Comment lire une fraction ?</h2>
<div class="g-table-wrap"><table class="g-table">
<thead><tr><th>Fraction</th><th>On lit</th></tr></thead>
<tbody>
<tr><td>1/2</td><td>un demi</td></tr>
<tr><td>1/3</td><td>un tiers</td></tr>
<tr><td>3/4</td><td>trois quarts</td></tr>
<tr><td>2/5</td><td>deux cinquièmes</td></tr>
<tr><td>7/10</td><td>sept dixièmes</td></tr>
</tbody></table></div>

<h2>Comparer deux fractions</h2>
<h3>Cas 1 : le même nombre en bas</h3>
<p>Les parts ont la même taille. Celui qui en prend le plus a la plus grande fraction : <strong>3/8 &lt; 5/8</strong>.</p>
<h3>Cas 2 : le même nombre en haut</h3>
<p>C'est là que beaucoup d'élèves se trompent ! Compare <strong>1/3</strong> et <strong>1/4</strong>. Une pizza coupée en 3 donne des parts <strong>plus grosses</strong> qu'une pizza coupée en 4. Donc <strong>1/3 &gt; 1/4</strong>.</p>
<div class="g-warn"><strong>Erreur fréquente :</strong> penser que 1/4 est plus grand que 1/3 « parce que 4 est plus grand que 3 ». Plus on coupe en parts nombreuses, plus chaque part est petite.</div>
<h3>Cas 3 : comparer à 1</h3>
<p>Si le haut est plus petit que le bas, la fraction est plus petite que 1 (3/4 &lt; 1). Si le haut et le bas sont égaux, elle vaut 1 (4/4 = 1). Si le haut est plus grand, elle est plus grande que 1 (5/4 &gt; 1 : c'est une pizza entière et encore un quart).</p>

<h2>Des fractions égales</h2>
<p>La moitié d'une pizza, c'est 1/2. C'est aussi 2/4, ou 4/8 : la même quantité, coupée en plus de parts. Pour trouver une fraction égale, on <strong>multiplie (ou divise) le haut et le bas par le même nombre</strong> : 1/3 = 2/6 (on a fait × 2 en haut et en bas).</p>

<h2>Additionner des fractions (même dénominateur)</h2>
<p>On additionne les nombres du haut, et le nombre du bas <strong>ne change pas</strong> : 2/5 + 1/5 = 3/5.</p>
<div class="g-warn"><strong>Erreur fréquente :</strong> écrire 1/5 + 1/5 = 2/10. Non ! Deux parts de cinquième, ce sont 2 cinquièmes : <strong>2/5</strong>.</div>

<h2>Je m'entraîne</h2>
<p>Choisis ta classe. Commence par la leçon si tu as un doute, puis fais les exercices : la correction est immédiate.</p>
<div class="g-cta">
<a href="fractions-ce1.html">Fractions CE1<small>Partager en parts égales</small></a>
<a href="fiche1.html">Fractions CE2<small>Je découpe, je compare, je calcule</small></a>
<a href="fractions-cm1.html">Fractions CM1<small>Lire, comparer, additionner</small></a>
<a href="fractions-cm2.html">Fractions CM2<small>Fractions décimales</small></a>
<a href="fractions-6e.html">Fractions 6e<small>Quotients, fraction d'une quantité</small></a>
<a href="fractions-5e.html">Fractions 5e<small>Additionner, comparer</small></a>
</div>
<p>Leçons : <a href="cours-fractions-ce2.html">cours CE2</a> · <a href="cours-fractions-cm1.html">cours CM1</a> · <a href="cours-fractions-cm2.html">cours CM2</a> · <a href="cours-fractions-6e.html">cours 6e</a>. Et pour t'entraîner sur papier : la <a href="ressources.html">fiche d'exercices de fractions CM1 avec corrigé</a>.</p>
""",
    faq=[
        ("Quelle est la différence entre numérateur et dénominateur ?", "Le dénominateur (en bas) indique en combien de parts égales on partage. Le numérateur (en haut) indique combien de parts on prend."),
        ("Pourquoi 1/3 est plus grand que 1/4 ?", "Parce qu'en coupant une pizza en 3, chaque part est plus grosse qu'en la coupant en 4. Avec le même numérateur, plus le dénominateur est petit, plus la fraction est grande."),
        ("Comment savoir si une fraction est plus grande que 1 ?", "Si le numérateur (en haut) est plus grand que le dénominateur (en bas), la fraction est plus grande que 1. Par exemple, 7/4 > 1."),
    ],
    cta=[('fractions-cm1.html', 'Exercices fractions CM1', 'Corrigés tout de suite'),
         ('ressources.html', 'Fiche fractions à imprimer', 'Avec corrigé'),
         ('aide.html', "Toute l'aide aux élèves", 'Tables, problèmes…')],
    sources=['programmes'],
))

ARTICLES.append(dict(
    slug='apprendre-les-tables-de-multiplication', hub='aide', icon='✖️',
    kicker='Aide élèves · Maths',
    title="Je n'arrive pas à apprendre mes tables de multiplication : 6 astuces",
    seo_title="Apprendre les tables de multiplication : 6 astuces",
    description="Tu n'arrives pas à retenir tes tables ? Il n'y a que 36 résultats à apprendre. 6 astuces, 5 minutes par jour et des fiches gratuites.",
    intro="Bonne nouvelle : les tables, ce n'est pas 100 résultats à apprendre par cœur. Avec quelques astuces, il n'en reste que 36. Et 5 minutes par jour suffisent.",
    minutes=5,
    tldr=[
        "3 × 7 = 7 × 3 : grâce à cela, il ne reste que <strong>36 résultats</strong> à apprendre (tables de 2 à 9).",
        "Astuces : ×2 = double, ×4 = double du double, ×5 = moitié de ×10, ×9 = ×10 moins une fois.",
        "<strong>5 minutes par jour</strong> à se tester valent mieux qu'une heure le dimanche.",
        "On commence par les tables faciles (2, 5, 10), puis 3, 4, et on finit par 6, 7, 8, 9.",
    ],
    body="""
<h2>Il n'y a que 36 résultats à apprendre</h2>
<p>La table de 1 est facile (1 × 6 = 6) et celle de 10 aussi (10 × 6 = 60). Ensuite, <strong>l'ordre ne compte pas</strong> : 3 × 7 = 7 × 3 = 21. Si tu sais l'un, tu sais l'autre !</p>
<p>Pour les tables de 2 à 9, il ne reste donc que <strong>36 multiplications différentes</strong>. Et beaucoup se trouvent avec des astuces.</p>

<h2>6 astuces pour trouver le résultat</h2>
<h3>1. Table de 2 : le double</h3>
<p>2 × 8, c'est le double de 8 : 8 + 8 = <strong>16</strong>.</p>
<h3>2. Table de 4 : le double du double</h3>
<p>4 × 7 : le double de 7, c'est 14, et le double de 14, c'est <strong>28</strong>.</p>
<h3>3. Table de 5 : la moitié de la table de 10</h3>
<p>5 × 8 : 10 × 8 = 80, et la moitié de 80, c'est <strong>40</strong>. Les résultats finissent toujours par 0 ou 5.</p>
<h3>4. Table de 8 : le double de la table de 4</h3>
<p>8 × 6 : 4 × 6 = 24, et le double de 24, c'est <strong>48</strong>.</p>
<h3>5. Table de 9 : dix fois moins une fois</h3>
<p>9 × 7 : 10 × 7 = 70, puis 70 − 7 = <strong>63</strong>. Autre astuce : dans la table de 9 (de 9 × 2 à 9 × 10), les deux chiffres du résultat font toujours 9 quand on les additionne (6 + 3 = 9, 7 + 2 = 9).</p>
<h3>6. Table de 6 : cinq fois plus une fois</h3>
<p>6 × 7 : 5 × 7 = 35, puis 35 + 7 = <strong>42</strong>.</p>

<h2>La méthode des 5 minutes par jour</h2>
<ol class="g-steps">
<li><strong>Choisis une seule table</strong> (ou une moitié de table) pour la semaine.</li>
<li><strong>Récite-la</strong> une fois dans l'ordre, puis <strong>dans le désordre</strong> : c'est le désordre qui compte au contrôle.</li>
<li><strong>Teste-toi</strong> : cartes avec la multiplication d'un côté et le résultat de l'autre, ou exercices corrigés.</li>
<li><strong>Mets de côté</strong> les résultats que tu rates et revois-les le lendemain.</li>
<li><strong>Chaque jour</strong>, refais aussi deux minutes sur les tables des semaines d'avant.</li>
</ol>
<div class="g-tip"><strong>Pourquoi ça marche :</strong> se tester (plutôt que relire) et revoir un peu chaque jour sont les deux méthodes les plus efficaces pour retenir, d'après les recherches sur la mémoire.</div>

<h2>Dans quel ordre apprendre les tables ?</h2>
<p>D'abord les plus faciles : <strong>2, 5 et 10</strong>. Puis <strong>3 et 4</strong>. Enfin <strong>6, 7, 8 et 9</strong>, avec les astuces ci-dessus. La plus difficile est souvent celle de 7 : les autres tables t'en donnent déjà presque tous les résultats (7 × 2, 7 × 3…) !</p>

<h2>Je m'entraîne</h2>
<div class="g-cta">
<a href="tables-ce2.html">Tables de multiplication CE2<small>Exercices corrigés</small></a>
<a href="multiplication-ce1.html">Multiplication CE1<small>Comprendre la multiplication</small></a>
<a href="multiplication-division-ce2.html">Multiplication et division CE2<small>Exercices corrigés</small></a>
<a href="calcul-mental-cm1.html">Calcul mental CM1<small>Pour aller plus vite</small></a>
</div>
<p>Sur papier : imprime l'<a href="ressources.html">affiche des tables de multiplication</a> et la <a href="ressources.html">fiche de 40 multiplications avec corrigé</a>.</p>
""",
    faq=[
        ("Combien de temps faut-il pour apprendre les tables de multiplication ?", "Avec 5 minutes par jour et une table par semaine environ, la plupart des enfants les connaissent en quelques semaines. Ensuite, quelques minutes de révision régulières les gardent en mémoire."),
        ("En quelle classe apprend-on les tables ?", "On les commence en CE1 et on doit toutes les connaître à la fin du CE2, qui termine le cycle 2. Elles servent ensuite pour la division, les fractions et le calcul mental."),
        ("Quelle est la table la plus difficile ?", "Souvent celles de 7 et de 8. Mais grâce à l'ordre qui ne compte pas (7 × 3 = 3 × 7), presque tous leurs résultats se trouvent déjà dans les autres tables."),
    ],
    cta=[('tables-ce2.html', 'Exercices tables CE2', 'Corrigés tout de suite'),
         ('ressources.html', 'Affiche et fiche à imprimer', 'Gratuites'),
         ('aide.html', "Toute l'aide aux élèves", 'Fractions, problèmes…')],
    sources=['roediger', 'programmes'],
))

ARTICLES.append(dict(
    slug='resoudre-un-probleme-de-maths', hub='aide', icon='🔎',
    kicker='Aide élèves · Maths',
    title="Je n'arrive pas à résoudre les problèmes de maths : la méthode en 5 étapes",
    seo_title="Résoudre un problème de maths en 5 étapes",
    description="Quelle opération choisir ? La méthode en 5 étapes pour résoudre un problème de maths, avec exemples corrigés, pièges et exercices.",
    intro="Le plus difficile dans un problème, ce n'est pas le calcul : c'est de comprendre l'histoire. Avec ces 5 étapes, tu sauras toujours par où commencer.",
    minutes=6,
    tldr=[
        "<strong>1. Lire</strong> l'histoire et la redire avec tes mots.",
        "<strong>2. Trouver la question</strong> : que cherche-t-on ?",
        "<strong>3. Faire un schéma</strong> pour voir les nombres, puis choisir l'opération.",
        "<strong>4. Calculer</strong>, puis <strong>5. vérifier</strong> et écrire une phrase réponse.",
        "Attention : « de plus » ne veut pas toujours dire « addition » !",
    ],
    body="""
<h2>Les 5 étapes</h2>
<ol class="g-steps">
<li><strong>Je lis et je raconte.</strong> Lis le problème deux fois. Puis raconte l'histoire sans les nombres : « Quelqu'un achète des choses et on veut savoir combien il paie. »</li>
<li><strong>Je trouve la question.</strong> Souligne-la. Que cherche-t-on : un total ? une différence ? un partage ?</li>
<li><strong>Je fais un schéma.</strong> Dessine des barres, des paquets ou un tableau avec les nombres. Le schéma montre quelle opération faire.</li>
<li><strong>Je calcule.</strong> Pose l'opération si besoin.</li>
<li><strong>Je vérifie et je réponds.</strong> Est-ce que le résultat est logique ? Écris une phrase réponse avec l'unité (€, cm, minutes…).</li>
</ol>

<h2>Un exemple corrigé</h2>
<p><strong>Problème :</strong> Inès achète 3 cahiers à 2 € chacun et un stylo à 4 €. Combien paie-t-elle en tout ?</p>
<ul>
<li><strong>Je raconte :</strong> Inès achète des cahiers et un stylo, on cherche le prix total.</li>
<li><strong>La question :</strong> combien paie-t-elle en tout ? On cherche un total.</li>
<li><strong>Schéma :</strong> [2 €][2 €][2 €] + [4 €].</li>
<li><strong>Calcul :</strong> 3 × 2 = 6, puis 6 + 4 = 10.</li>
<li><strong>Phrase réponse :</strong> Inès paie 10 € en tout.</li>
</ul>

<h2>Le piège des « mots-indices »</h2>
<p>Beaucoup d'élèves cherchent un mot dans l'énoncé : « en tout » = addition, « de plus » = addition… Mais ça ne marche pas toujours !</p>
<p><strong>Exemple :</strong> Léa a 12 billes. Elle a 5 billes <strong>de plus</strong> que Tom. Combien Tom a-t-il de billes ?</p>
<p>Ici, il ne faut pas faire 12 + 5 ! Léa en a plus que Tom, donc Tom en a <strong>moins</strong> : 12 − 5 = <strong>7</strong>. Tom a 7 billes.</p>
<div class="g-warn"><strong>Retiens :</strong> ne cherche pas un mot, comprends l'histoire. Le schéma t'aide à ne pas tomber dans le piège.</div>

<h2>Quelle opération choisir ?</h2>
<div class="g-table-wrap"><table class="g-table">
<thead><tr><th>Dans l'histoire…</th><th>Opération</th><th>Exemple</th></tr></thead>
<tbody>
<tr><td>On réunit, on ajoute</td><td>Addition</td><td>8 filles et 7 garçons : 8 + 7 = 15 élèves</td></tr>
<tr><td>On enlève, on compare, on cherche un écart</td><td>Soustraction</td><td>Il avait 20 €, il dépense 6 € : 20 − 6 = 14 €</td></tr>
<tr><td>On répète la même quantité plusieurs fois</td><td>Multiplication</td><td>4 paquets de 6 œufs : 4 × 6 = 24 œufs</td></tr>
<tr><td>On partage en parts égales, ou on fait des groupes</td><td>Division</td><td>24 bonbons pour 4 enfants : 24 ÷ 4 = 6 bonbons chacun</td></tr>
</tbody></table></div>

<h2>Je vérifie mon résultat</h2>
<ul>
<li><strong>Ordre de grandeur :</strong> un enfant ne mesure pas 15 m, un trajet en bus ne dure pas 3 secondes.</li>
<li><strong>Opération inverse :</strong> si 24 ÷ 4 = 6, alors 6 × 4 doit faire 24.</li>
<li><strong>Relis la question :</strong> as-tu bien répondu à ce qu'on demande (et pas à une étape intermédiaire) ?</li>
</ul>

<h2>Je m'entraîne</h2>
<div class="g-cta">
<a href="problemes-cp.html">Problèmes CP<small>Ajouter, enlever</small></a>
<a href="problemes-ce1.html">Problèmes CE1<small>Plus, moins, partager</small></a>
<a href="problemes.html">Problèmes CE2<small>Plusieurs étapes</small></a>
<a href="problemes-cm1.html">Problèmes CM1<small>Combien de plus, de moins</small></a>
<a href="problemes-cm2.html">Problèmes CM2<small>Durées, proportionnalité</small></a>
</div>
<p>À imprimer : la <a href="ressources.html">fiche méthode « Résoudre un problème en 5 étapes »</a>, à garder dans ta trousse ou ton classeur.</p>
""",
    faq=[
        ("Comment savoir quelle opération faire dans un problème ?", "Raconte l'histoire avec tes mots et fais un schéma. On additionne quand on réunit, on soustrait quand on enlève ou qu'on compare, on multiplie quand on répète la même quantité, on divise quand on partage en parts égales."),
        ("Pourquoi faut-il écrire une phrase réponse ?", "Elle oblige à vérifier qu'on a bien répondu à la question posée, avec la bonne unité. C'est aussi ce que demande l'enseignant."),
        ("Mon enfant comprend les calculs mais pas les problèmes, que faire ?", "C'est très fréquent : la difficulté est souvent la lecture de l'énoncé. Faites-lui raconter l'histoire sans les nombres, puis dessiner un schéma, avant tout calcul."),
    ],
    cta=[('problemes-cm1.html', 'Exercices problèmes CM1', 'Corrigés tout de suite'),
         ('ressources.html', 'Fiche méthode à imprimer', 'Gratuite'),
         ('aide.html', "Toute l'aide aux élèves", 'Fractions, tables…')],
    sources=['programmes'],
))

# ── Pages hub ─────────────────────────────────────────────────────────
HUBS = {
    'parents': dict(
        slug='parents', icon='👪', kicker='Espace parents',
        title="Espace parents : accompagner son enfant du CP à la 3e",
        seo_title="Espace parents : devoirs, méthode, motivation",
        description="Guides gratuits pour les parents : devoirs, motivation, organisation, blocages, entrée en 6e. Sources officielles et fiches à imprimer.",
        intro="Des guides courts et sourcés pour accompagner votre enfant sans stress : devoirs, méthode, motivation, programme. Et des outils gratuits à imprimer.",
    ),
    'aide': dict(
        slug='aide', icon='🆘', kicker='Aide élèves',
        title="Je n'y arrive pas ! L'aide des élèves, du CP à la 3e",
        seo_title="Je n'y arrive pas : l'aide des élèves (CP à 3e)",
        description="Fractions, tables, problèmes : tu bloques ? Des explications simples, les erreurs à éviter et des exercices corrigés.",
        intro="Tu bloques sur une notion ? Choisis-la : on t'explique simplement, on te montre les erreurs à éviter, puis tu t'entraînes avec des exercices corrigés.",
    ),
}
