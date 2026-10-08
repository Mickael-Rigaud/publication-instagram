# -*- coding: utf-8 -*-
"""Crée les fiches publications/*.json d'un mois et son récapitulatif visuel.

    python sources/programme.py novembre      # un mois
    python sources/programme.py               # tous les mois

Les fiches sortent en brouillon ; une fiche existante garde son statut
(validée, publiée…) : relancer ce script ne déprogramme jamais rien.

Fil en colonnes : Expertise (gauche) · Réseau (milieu) · AMO (droite).
Instagram place la plus récente en haut à gauche : chaque série se publie
donc AMO, puis Réseau, puis Expertise.
"""

import datetime
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
sys.path.insert(0, ICI)
from planning import PLANNING  # noqa: E402
from planning_novembre import NOVEMBRE  # noqa: E402

MOIS = {
    "octobre": (PLANNING, "Du lundi 12 au vendredi 30 octobre 2026", "30 octobre"),
    "novembre": (NOVEMBRE, "Du lundi 2 au vendredi 27 novembre 2026", "27 novembre"),
}
NOMS = {"expertise": "Expertise", "reseau": "Réseau", "amo": "AMO"}
JOURS = ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."]


def jour(date):
    d = datetime.date.fromisoformat(date)
    return "%s %02d/%02d" % (JOURS[d.weekday()], d.day, d.month)


def heure(date, theme):
    """Réseau à 12h15 (les indépendants consultent à la pause), le reste à 18h30.
    Heure d'été jusqu'au 25/10/2026, heure d'hiver ensuite : toujours l'heure de Paris."""
    horaire = "12:15" if theme == "reseau" else "18:30"
    return "T%s:00%s" % (horaire, "+02:00" if date < "2026-10-25" else "+01:00")


def fiches(entrees):
    for date, slug, n, theme, legende in entrees:
        assert len(legende) <= 2200, slug
        assert "590" not in legende, slug
        for k in range(1, n + 1):
            assert os.path.exists(os.path.join(RACINE, "medias", "%s-%d.jpg" % (slug, k))), (slug, k)
        chemin = os.path.join(RACINE, "publications", "%s.json" % slug)
        fiche = {"compte": "btp_expertise", "type": "carrousel", "theme": theme,
                 "date": date + heure(date, theme), "statut": "brouillon", "legende": legende,
                 "medias": ["medias/%s-%d.jpg" % (slug, k) for k in range(1, n + 1)]}
        if os.path.exists(chemin):
            with open(chemin, encoding="utf-8") as f:
                ancienne = json.load(f)
            for cle in ("statut", "media_id", "lien", "publie_le", "erreur"):
                if cle in ancienne:
                    fiche[cle] = ancienne[cle]
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(json.dumps(fiche, ensure_ascii=False, indent=2) + "\n")


def recap(mois):
    entrees, periode, fin = MOIS[mois]
    lignes = []
    for k, (date, slug, n, theme, legende) in enumerate(entrees):
        if k % 3 == 0:
            lignes.append('<h2 class="semaine">Semaine %d</h2>' % (k // 3 + 1))
        vignettes = "".join('<img src="../medias/%s-%d.jpg">' % (slug, i) for i in range(1, n + 1))
        texte = legende.replace("&", "&amp;").replace("<", "&lt;").replace("\n", "<br>")
        lignes.append('<section class="post %s"><div class="quand"><b>%s</b><span>%s</span><em>%s</em></div>'
                      '<div class="contenu"><div class="vignettes">%s</div><p>%s</p></div></section>'
                      % (theme, jour(date), "12h15" if theme == "reseau" else "18h30", NOMS[theme], vignettes, texte))
    # Fil en fin de mois : la plus récente en haut à gauche, les semaines précédentes en grisé.
    tout = sorted((p for m in MOIS.values() for p in m[0] if p[0] <= entrees[-1][0]),
                  key=lambda p: p[0], reverse=True)
    grille = ""
    for p in tout[:len(entrees) + 6]:
        grille += '<img%s src="../medias/%s-1.jpg">' % ("" if p in entrees else ' class="ancien"', p[1])
    if mois == "octobre":
        grille += "".join('<img class="ancien" src="photos/ancien-%d.jpg">' % i for i in range(1, 7))
    with open(os.path.join(ICI, "recap-gabarit.html"), encoding="utf-8") as f:
        html = f.read()
    html = (html.replace("{{POSTS}}", "\n".join(lignes)).replace("{{GRILLE}}", grille)
                .replace("{{PERIODE}}", periode).replace("{{FIN}}", fin).replace("{{NOMBRE}}", str(len(entrees))))
    sortie = os.path.join(ICI, "recap-%s.html" % mois)
    with open(sortie, "w", encoding="utf-8") as f:
        f.write(html)
    return sortie


if __name__ == "__main__":
    for mois in sys.argv[1:] or list(MOIS):
        fiches(MOIS[mois][0])
        print(mois, ":", len(MOIS[mois][0]), "fiches (statut existant conservé) ->", recap(mois))
