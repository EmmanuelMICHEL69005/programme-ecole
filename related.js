(function(){
  'use strict';

  // Maillage interne : pour chaque page, liste de pages suggérées
  // Format : { label, href, level }
  var RELATED = {
    /* ── CP ── */
    'nombres-cp.html':      [{h:'calcul-cp.html',l:'Addition et soustraction CP'},{h:'calcul-mental-cp.html',l:'Calcul mental CP'},{h:'nombres-ce1.html',l:'Les nombres CE1 — étape suivante'}],
    'calcul-cp.html':       [{h:'nombres-cp.html',l:'Les nombres CP'},{h:'calcul-mental-cp.html',l:'Calcul mental CP'},{h:'problemes-cp.html',l:'Résolution de problèmes CP'},{h:'calcul-ce1.html',l:'Opérations CE1 — étape suivante'}],
    'calcul-mental-cp.html':[{h:'calcul-cp.html',l:'Addition et soustraction CP'},{h:'nombres-cp.html',l:'Les nombres CP'},{h:'calcul-mental-ce1.html',l:'Calcul mental CE1 — étape suivante'}],
    'mesures-cp.html':      [{h:'geometrie-cp.html',l:'Géométrie CP'},{h:'mesures-ce1.html',l:'Mesures CE1 — étape suivante'}],
    'geometrie-cp.html':    [{h:'mesures-cp.html',l:'Mesures CP'},{h:'geometrie-ce1.html',l:'Géométrie CE1 — étape suivante'}],
    'donnees-cp.html':      [{h:'donnees-ce1.html',l:'Données CE1 — étape suivante'},{h:'problemes-cp.html',l:'Résolution de problèmes CP'}],
    'problemes-cp.html':    [{h:'calcul-cp.html',l:'Addition et soustraction CP'},{h:'mesures-cp.html',l:'Mesures CP'},{h:'problemes-ce1.html',l:'Problèmes CE1 — étape suivante'}],
    'histoire-geo-cp.html': [{h:'histoire-geo-ce1.html',l:'Histoire-Géo CE1 — étape suivante'},{h:'eps-cycle2.html',l:'EPS Cycle 2'}],

    /* ── CE1 ── */
    'nombres-ce1.html':     [{h:'calcul-ce1.html',l:'Les opérations CE1'},{h:'fractions-ce1.html',l:'Introduction aux fractions CE1'},{h:'nombres-cp.html',l:'Les nombres CP — révision'},{h:'nombres-ce2.html',l:'Les nombres CE2 — étape suivante'}],
    'fractions-ce1.html':   [{h:'nombres-ce1.html',l:'Les nombres CE1'},{h:'fiche1.html',l:'Fractions CE2 — Je découpe'},{h:'fractions-cm1.html',l:'Fractions CM1 — étape suivante'}],
    'calcul-ce1.html':      [{h:'nombres-ce1.html',l:'Les nombres CE1'},{h:'calcul-mental-ce1.html',l:'Calcul mental CE1'},{h:'operations-posees-ce1.html',l:'Opérations posées CE1'},{h:'multiplication-ce1.html',l:'Multiplication CE1'}],
    'calcul-mental-ce1.html':[{h:'calcul-ce1.html',l:'Les opérations CE1'},{h:'calcul-mental-cp.html',l:'Calcul mental CP — révision'},{h:'calcul-mental.html',l:'Calcul mental CE2 — étape suivante'}],
    'operations-posees-ce1.html':[{h:'calcul-ce1.html',l:'Les opérations CE1'},{h:'operations-posees-ce2.html',l:'Opérations posées CE2 — étape suivante'}],
    'multiplication-ce1.html':[{h:'calcul-ce1.html',l:'Les opérations CE1'},{h:'calcul-mental-ce1.html',l:'Calcul mental CE1'},{h:'multiplication-division-ce2.html',l:'Multiplication et division CE2 — étape suivante'}],
    'mesures-ce1.html':     [{h:'mesures-cp.html',l:'Mesures CP — révision'},{h:'mesures-ce2.html',l:'Mesures CE2 — étape suivante'},{h:'geometrie-ce1.html',l:'Géométrie CE1'}],
    'geometrie-ce1.html':   [{h:'geometrie-cp.html',l:'Géométrie CP — révision'},{h:'geometrie-ce2.html',l:'Géométrie CE2 — étape suivante'},{h:'symetrie-ce2.html',l:'Symétrie CE2'}],
    'donnees-ce1.html':     [{h:'donnees-cp.html',l:'Données CP — révision'},{h:'donnees.html',l:'Données CE2 — étape suivante'}],
    'problemes-ce1.html':   [{h:'calcul-ce1.html',l:'Les opérations CE1'},{h:'problemes-cp.html',l:'Problèmes CP — révision'},{h:'problemes.html',l:'Problèmes CE2 — étape suivante'}],
    'histoire-geo-ce1.html':[{h:'histoire-geo-cp.html',l:'Histoire-Géo CP — révision'},{h:'histoire-geo-ce2.html',l:'Histoire-Géo CE2 — étape suivante'},{h:'eps-cycle2.html',l:'EPS Cycle 2'}],

    /* ── CE2 ── */
    'nombres-ce2.html':     [{h:'decimaux-ce2.html',l:'Nombres décimaux CE2'},{h:'calcul.html',l:'Les opérations CE2'},{h:'nombres-ce1.html',l:'Les nombres CE1 — révision'},{h:'nombres-cm1.html',l:'Grands nombres CM1 — étape suivante'}],
    'decimaux-ce2.html':    [{h:'nombres-ce2.html',l:'Les nombres CE2'},{h:'fiche1.html',l:'Fractions CE2'},{h:'decimaux-cm1.html',l:'Décimaux CM1 — étape suivante'}],
    'fiche1.html':          [{h:'fiche2.html',l:'Fractions — Je compare'},{h:'fiche3.html',l:'Fractions — Je calcule'},{h:'fractions-ce1.html',l:'Fractions CE1 — révision'},{h:'fractions-cm1.html',l:'Fractions CM1 — étape suivante'}],
    'fiche2.html':          [{h:'fiche1.html',l:'Fractions — Je découpe'},{h:'fiche3.html',l:'Fractions — Je calcule'},{h:'decimaux-ce2.html',l:'Nombres décimaux CE2'}],
    'fiche3.html':          [{h:'fiche1.html',l:'Fractions — Je découpe'},{h:'fiche2.html',l:'Fractions — Je compare'},{h:'fractions-cm1.html',l:'Fractions CM1 — étape suivante'}],
    'calcul.html':          [{h:'nombres-ce2.html',l:'Les nombres CE2'},{h:'calcul-mental.html',l:'Calcul mental CE2'},{h:'operations-posees-ce2.html',l:'Opérations posées CE2'},{h:'calcul-cm1.html',l:'Les 4 opérations CM1 — étape suivante'}],
    'calcul-mental.html':   [{h:'calcul.html',l:'Les opérations CE2'},{h:'calcul-mental-ce1.html',l:'Calcul mental CE1 — révision'},{h:'calcul-mental-cm1.html',l:'Calcul mental CM1 — étape suivante'}],
    'operations-posees-ce2.html':[{h:'calcul.html',l:'Les opérations CE2'},{h:'multiplication-division-ce2.html',l:'Multiplication et division CE2'},{h:'operations-posees-ce1.html',l:'Opérations posées CE1 — révision'},{h:'calcul-pose-cm1.html',l:'Opérations posées CM1 — étape suivante'}],
    'multiplication-division-ce2.html':[{h:'division-ce2.html',l:'Division euclidienne CE2'},{h:'calcul.html',l:'Les opérations CE2'},{h:'multiplication-ce1.html',l:'Multiplication CE1 — révision'},{h:'calcul-cm1.html',l:'Les 4 opérations CM1 — étape suivante'}],
    'division-ce2.html':    [{h:'multiplication-division-ce2.html',l:'Multiplication et division CE2'},{h:'calcul.html',l:'Les opérations CE2'},{h:'problemes.html',l:'Problèmes CE2'},{h:'calcul-cm1.html',l:'Les 4 opérations CM1 — étape suivante'}],
    'mesures-ce2.html':     [{h:'mesures.html',l:'Longueurs, masses CE2'},{h:'temps.html',l:'Temps et monnaie CE2'},{h:'mesures-ce1.html',l:'Mesures CE1 — révision'},{h:'mesures-cm1.html',l:'Mesures CM1 — étape suivante'}],
    'mesures.html':         [{h:'mesures-ce2.html',l:'Mesures CE2'},{h:'temps.html',l:'Temps et monnaie CE2'},{h:'mesures-cm1.html',l:'Mesures CM1 — étape suivante'}],
    'temps.html':           [{h:'mesures.html',l:'Longueurs, masses CE2'},{h:'mesures-ce2.html',l:'Mesures CE2'},{h:'temps-cm1.html',l:'Durées CM1 — étape suivante'}],
    'geometrie-ce2.html':   [{h:'symetrie-ce2.html',l:'Symétrie axiale CE2'},{h:'geometrie.html',l:'Géométrie plane CE2'},{h:'geometrie-ce1.html',l:'Géométrie CE1 — révision'},{h:'geometrie-cm1.html',l:'Géométrie CM1 — étape suivante'}],
    'geometrie.html':       [{h:'geometrie-ce2.html',l:'Géométrie CE2'},{h:'symetrie-ce2.html',l:'Symétrie axiale CE2'},{h:'solides.html',l:'Les solides CE2'}],
    'symetrie-ce2.html':    [{h:'geometrie-ce2.html',l:'Géométrie CE2'},{h:'geometrie.html',l:'Géométrie plane CE2'},{h:'geometrie-ce1.html',l:'Géométrie CE1 — révision'},{h:'geometrie-cm1.html',l:'Géométrie CM1 — étape suivante'}],
    'solides.html':         [{h:'geometrie.html',l:'Géométrie plane CE2'},{h:'geometrie-ce2.html',l:'Géométrie CE2'},{h:'solides-cm1.html',l:'Solides CM1 — étape suivante'}],
    'donnees.html':         [{h:'donnees-ce1.html',l:'Données CE1 — révision'},{h:'donnees-cm1.html',l:'Données CM1 — étape suivante'}],
    'problemes.html':       [{h:'calcul.html',l:'Les opérations CE2'},{h:'division-ce2.html',l:'Division euclidienne CE2'},{h:'problemes-ce1.html',l:'Problèmes CE1 — révision'},{h:'problemes-cm1.html',l:'Problèmes CM1 — étape suivante'}],
    'histoire-geo-ce2.html':[{h:'histoire-geo-ce1.html',l:'Histoire-Géo CE1 — révision'},{h:'eps-cycle2.html',l:'EPS Cycle 2'}],

    /* ── CM1 ── */
    'nombres-cm1.html':     [{h:'decimaux-cm1.html',l:'Nombres décimaux CM1'},{h:'fractions-cm1.html',l:'Fractions CM1'},{h:'nombres-ce2.html',l:'Les nombres CE2 — révision'},{h:'nombres-cm2.html',l:'Très grands nombres CM2 — étape suivante'}],
    'decimaux-cm1.html':    [{h:'nombres-cm1.html',l:'Les nombres CM1'},{h:'fractions-cm1.html',l:'Fractions CM1'},{h:'decimaux-ce2.html',l:'Décimaux CE2 — révision'},{h:'decimaux-cm2.html',l:'Décimaux CM2 — étape suivante'}],
    'fractions-cm1.html':   [{h:'decimaux-cm1.html',l:'Décimaux CM1'},{h:'fiche1.html',l:'Fractions CE2 — révision'},{h:'fractions-cm2.html',l:'Fractions CM2 — étape suivante'},{h:'fractions-6e.html',l:'Fractions 6e — étape suivante'}],
    'calcul-cm1.html':      [{h:'calcul-mental-cm1.html',l:'Calcul mental CM1'},{h:'calcul-pose-cm1.html',l:'Opérations posées CM1'},{h:'calcul.html',l:'Opérations CE2 — révision'},{h:'calcul-cm2.html',l:'Opérations CM2 — étape suivante'}],
    'calcul-mental-cm1.html':[{h:'calcul-cm1.html',l:'Les 4 opérations CM1'},{h:'calcul-mental.html',l:'Calcul mental CE2 — révision'},{h:'calcul-mental-cm2.html',l:'Calcul mental CM2 — étape suivante'}],
    'calcul-pose-cm1.html': [{h:'calcul-cm1.html',l:'Les 4 opérations CM1'},{h:'operations-posees-ce2.html',l:'Opérations posées CE2 — révision'},{h:'calcul-pose-cm2.html',l:'Opérations posées CM2 — étape suivante'}],
    'mesures-cm1.html':     [{h:'temps-cm1.html',l:'Durées CM1'},{h:'geometrie-cm1.html',l:'Géométrie CM1'},{h:'mesures-ce2.html',l:'Mesures CE2 — révision'},{h:'mesures-cm2.html',l:'Mesures CM2 — étape suivante'}],
    'temps-cm1.html':       [{h:'mesures-cm1.html',l:'Mesures CM1'},{h:'temps.html',l:'Temps CE2 — révision'},{h:'temps-cm2.html',l:'Durées CM2 — étape suivante'}],
    'geometrie-cm1.html':   [{h:'solides-cm1.html',l:'Solides CM1'},{h:'symetrie-ce2.html',l:'Symétrie CE2 — révision'},{h:'geometrie-cm2.html',l:'Géométrie CM2 — étape suivante'}],
    'solides-cm1.html':     [{h:'geometrie-cm1.html',l:'Géométrie CM1'},{h:'solides.html',l:'Solides CE2 — révision'}],
    'donnees-cm1.html':     [{h:'proportionnalite-cm1.html',l:'Proportionnalité CM1'},{h:'donnees.html',l:'Données CE2 — révision'},{h:'donnees-cm2.html',l:'Statistiques CM2 — étape suivante'}],
    'proportionnalite-cm1.html':[{h:'decimaux-cm1.html',l:'Décimaux CM1'},{h:'fractions-cm1.html',l:'Fractions CM1'},{h:'proportionnalite-cm2.html',l:'Proportionnalité CM2 — étape suivante'}],
    'problemes-cm1.html':   [{h:'calcul-cm1.html',l:'Les 4 opérations CM1'},{h:'proportionnalite-cm1.html',l:'Proportionnalité CM1'},{h:'problemes.html',l:'Problèmes CE2 — révision'},{h:'problemes-cm2.html',l:'Problèmes CM2 — étape suivante'}],

    /* ── CM2 ── */
    'nombres-cm2.html':     [{h:'decimaux-cm2.html',l:'Décimaux CM2'},{h:'fractions-cm2.html',l:'Fractions CM2'},{h:'nombres-cm1.html',l:'Grands nombres CM1 — révision'},{h:'nombres-6e.html',l:'Nombres 6e — étape suivante'}],
    'decimaux-cm2.html':    [{h:'nombres-cm2.html',l:'Très grands nombres CM2'},{h:'fractions-cm2.html',l:'Fractions CM2'},{h:'decimaux-cm1.html',l:'Décimaux CM1 — révision'}],
    'fractions-cm2.html':   [{h:'decimaux-cm2.html',l:'Décimaux CM2'},{h:'fractions-cm1.html',l:'Fractions CM1 — révision'},{h:'fractions-6e.html',l:'Fractions 6e — étape suivante'}],
    'calcul-cm2.html':      [{h:'calcul-mental-cm2.html',l:'Calcul mental CM2'},{h:'calcul-pose-cm2.html',l:'Opérations posées CM2'},{h:'calcul-cm1.html',l:'4 opérations CM1 — révision'}],
    'calcul-mental-cm2.html':[{h:'calcul-cm2.html',l:'Les 4 opérations CM2'},{h:'calcul-mental-cm1.html',l:'Calcul mental CM1 — révision'},{h:'calcul-mental-6e.html',l:'Calcul mental 6e — étape suivante'}],
    'calcul-pose-cm2.html': [{h:'calcul-cm2.html',l:'Les 4 opérations CM2'},{h:'calcul-pose-cm1.html',l:'Opérations posées CM1 — révision'}],
    'problemes-cm2.html':   [{h:'calcul-cm2.html',l:'Les 4 opérations CM2'},{h:'proportionnalite-cm2.html',l:'Proportionnalité CM2'},{h:'problemes-cm1.html',l:'Problèmes CM1 — révision'}],
    'mesures-cm2.html':     [{h:'temps-cm2.html',l:'Durées CM2'},{h:'geometrie-cm2.html',l:'Géométrie CM2'},{h:'mesures-cm1.html',l:'Mesures CM1 — révision'},{h:'mesures-6e.html',l:'Mesures 6e — étape suivante'}],
    'temps-cm2.html':       [{h:'mesures-cm2.html',l:'Mesures CM2'},{h:'temps-cm1.html',l:'Durées CM1 — révision'}],
    'geometrie-cm2.html':   [{h:'mesures-cm2.html',l:'Mesures CM2'},{h:'geometrie-cm1.html',l:'Géométrie CM1 — révision'},{h:'geometrie-6e.html',l:'Géométrie 6e — étape suivante'}],
    'donnees-cm2.html':     [{h:'proportionnalite-cm2.html',l:'Proportionnalité CM2'},{h:'donnees-cm1.html',l:'Données CM1 — révision'},{h:'donnees-6e.html',l:'Statistiques 6e — étape suivante'}],
    'proportionnalite-cm2.html':[{h:'fractions-cm2.html',l:'Fractions CM2'},{h:'proportionnalite-cm1.html',l:'Proportionnalité CM1 — révision'},{h:'proportionnalite-6e.html',l:'Proportionnalité 6e — étape suivante'}],

    /* ── 6e ── */
    'nombres-6e.html':      [{h:'fractions-6e.html',l:'Fractions 6e'},{h:'algebre-6e.html',l:'Algèbre 6e'},{h:'nombres-cm2.html',l:'Très grands nombres CM2 — révision'}],
    'fractions-6e.html':    [{h:'nombres-6e.html',l:'Nombres 6e'},{h:'calcul-mental-6e.html',l:'Calcul mental 6e'},{h:'fractions-cm2.html',l:'Fractions CM2 — révision'}],
    'algebre-6e.html':      [{h:'nombres-6e.html',l:'Nombres 6e'},{h:'proportionnalite-6e.html',l:'Proportionnalité 6e'}],
    'calcul-mental-6e.html':[{h:'fractions-6e.html',l:'Fractions 6e'},{h:'nombres-6e.html',l:'Nombres 6e'},{h:'calcul-mental-cm2.html',l:'Calcul mental CM2 — révision'}],
    'probabilites-6e.html': [{h:'donnees-6e.html',l:'Statistiques 6e'},{h:'donnees-cm2.html',l:'Données CM2 — révision'}],
    'geometrie-6e.html':    [{h:'mesures-6e.html',l:'Mesures 6e'},{h:'geometrie-cm2.html',l:'Géométrie CM2 — révision'}],
    'mesures-6e.html':      [{h:'geometrie-6e.html',l:'Géométrie 6e'},{h:'mesures-cm2.html',l:'Mesures CM2 — révision'}],
    'donnees-6e.html':      [{h:'probabilites-6e.html',l:'Probabilités 6e'},{h:'proportionnalite-6e.html',l:'Proportionnalité 6e'},{h:'donnees-cm2.html',l:'Données CM2 — révision'}],
    'proportionnalite-6e.html':[{h:'fractions-6e.html',l:'Fractions 6e'},{h:'algebre-6e.html',l:'Algèbre 6e'},{h:'proportionnalite-cm2.html',l:'Proportionnalité CM2 — révision'}],

    /* ── EPS ── */
    'eps-cycle2.html':      [{h:'eps-cycle3.html',l:'EPS Cycle 3 — CM1/CM2/6e'},{h:'histoire-geo-cp.html',l:'Histoire-Géo CP'},{h:'histoire-geo-ce1.html',l:'Histoire-Géo CE1'},{h:'histoire-geo-ce2.html',l:'Histoire-Géo CE2'}],
    'eps-cycle3.html':      [{h:'eps-cycle2.html',l:'EPS Cycle 2 — CP/CE1/CE2'}],
  };

  var cur = window.location.pathname.split('/').pop() || 'index.html';
  var links = RELATED[cur];
  if (!links || !links.length) return;

  var css = '<style>.related-section{margin:32px 0 0;padding:18px 16px 14px;background:#f8f7ff;border-top:3px solid #e0e7ff;}.related-title{font-size:0.78rem;font-weight:900;text-transform:uppercase;letter-spacing:1.5px;color:#6b7280;margin-bottom:10px;}.related-links{display:flex;flex-wrap:wrap;gap:8px;}.related-link{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1.5px solid #e0e7ff;border-radius:20px;padding:6px 14px;font-size:0.8rem;font-weight:800;color:#4f46e5;text-decoration:none;transition:background 0.15s,border-color 0.15s;}.related-link:hover{background:#eef2ff;border-color:#a5b4fc;color:#3730a3;}.related-link-arrow{font-size:0.7rem;opacity:0.5;}</style>';
  document.head.insertAdjacentHTML('beforeend', css);

  var html = '<section class="related-section"><div class="related-title">📚 Voir aussi</div><div class="related-links">';
  links.forEach(function(lk){
    html += '<a href="' + lk.h + '" class="related-link"><span>' + lk.l + '</span><span class="related-link-arrow">›</span></a>';
  });
  html += '</div></section>';

  var main = document.querySelector('main');
  if (main) main.insertAdjacentHTML('beforeend', html);
})();
