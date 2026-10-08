# -*- coding: utf-8 -*-
"""Fabrique les carrousels BTP Expertise à partir de carrousels.py.

    python sources/generer.py              # tous les carrousels
    python sources/generer.py 2026-10-13-toiture

Chaque carrousel sort en HTML dans sources/<slug>/ et en JPEG 1080x1350 dans
medias/<slug>-N.jpg, plus un aperçu sources/<slug>/apercu.jpg.

Trois thématiques (champ "theme" du carrousel) : expertise, amo, reseau.
Le gabarit les distingue tout seul : étiquette dans l'en-tête, bandeau de
couleur en haut de chaque visuel, couleur dominante (voir gabarit.css).

Les prix ne s'écrivent JAMAIS de mémoire : les relire sur btpexpertise.fr/reglement/
au moment de rédiger (voir README).
"""

import os
import re
import subprocess
import sys

from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
sys.path.insert(0, ICI)
from carrousels import CARROUSELS  # noqa: E402

THEMES = {"expertise": "EXPERTISE", "amo": "AMO", "reseau": "RÉSEAU"}

ICONES = {
    "x": '<path d="M7 7l10 10M17 7 7 17" stroke-width="2.6"/>',
    "ok": '<path d="M5 12.5l4.5 4.5L19 7.5" stroke-width="2.6"/>',
    "alerte": '<path d="M12 4 3 20h18L12 4z"/><path d="M12 10v4.5M12 17.5v.1" stroke-width="2.4"/>',
    "loupe": '<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5 5"/>',
    "barres": '<path d="M5 19V13M12 19V8M19 19V4"/>',
    "doc": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/>',
    "goutte": '<path d="M12 3C9 7.5 6 11 6 14.5a6 6 0 0 0 12 0C18 11 15 7.5 12 3z"/>',
    "maison": '<path d="M4 11 12 4l8 7v9H4z"/><path d="M10 20v-5h4v5"/>',
    "pente": '<path d="M3 19h18L3 9z"/>',
    "ajout": '<rect x="3" y="9" width="10" height="11"/><path d="M13 13h8v7h-8M3 9l5-5 5 5"/>',
    "photo": '<rect x="3" y="7" width="18" height="13" rx="2"/><circle cx="12" cy="13.5" r="3.5"/><path d="M8 7l1.5-3h5L16 7"/>',
    "euro": '<path d="M17 6.5A7 7 0 1 0 17 17.5M4 10.5h9M4 13.5h9"/>',
    "cal": '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/>',
    "reseau": '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="18" r="2.5"/><circle cx="19" cy="18" r="2.5"/>'
              '<path d="M12 7.5v4M12 11.5 6.5 16M12 11.5l5.5 4.5"/>',
}


def icone(nom, couleur="o"):
    return ('<div class="icone ic-%s"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" '
            'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">%s</svg></div>'
            % (couleur, ICONES[nom]))


def entete(n, total, theme):
    return ('<header><img src="../logo-principal.png" alt=""><div class="sep"></div>'
            "<div><b>EXPERTISE BÂTIMENT</b><span>ASSISTANCE À MAÎTRISE D'OUVRAGE</span></div>"
            '<div class="theme">%s</div><div class="compteur">%02d / %02d</div></header>'
            % (THEMES[theme], n, total))


def tete(s):
    h = ""
    if s.get("etiquette"):
        h += '<div class="etiquette %s">%s</div>' % (s.get("etiquette_couleur", ""), s["etiquette"])
    if s.get("surtitre"):
        h += '<div class="surtitre">%s</div>' % s["surtitre"]
    h += "<h2>%s</h2>" % s["titre"]
    if s.get("chapo"):
        h += '<p class="chapo">%s</p>' % s["chapo"]
    return h


def pied(s):
    h = ""
    if s.get("encadre"):
        h += '<div class="encadre">%s</div>' % s["encadre"]
    if s.get("cle"):
        h += '<div class="cle">%s</div>' % s["cle"]
    return h


def insecables(texte):
    """Espace insécable avant ? ! : ; comme en typographie française."""
    return re.sub(r" ([?!:;])", r"&nbsp;\1", texte)


def diapo(s, n, total, theme):
    s = {k: insecables(v) if isinstance(v, str) and k in ("titre", "chapo") else v for k, v in s.items()}
    t = s["type"]

    # Couverture sans photo, sur feuille : étiquette, titre fin, liste à tirets, note
    if t == "titre":
        tirets = "".join("<li>%s</li>" % x for x in s.get("items", []))
        corps = ('<div class="label">%s</div><h1>%s</h1><ul class="tirets">%s</ul><p class="chapo">%s</p>'
                 % (s["label"], s["titre"], tirets, s["chapo"]))
        return ('<section class="slide couv-titre">%s<div class="corps">%s</div></section>'
                % (entete(n, total, theme), corps))

    if t in ("couverture", "contact"):
        fond = ('<div class="fond" style="background-image:url(../photos/%s);background-position:%s"></div>'
                % (s["photo"], s.get("cadrage", "center")) if s.get("photo") else "")
        classe = "couv" if t == "couverture" else "fin"
        corps = '<div class="pastille">%s</div>' % s["pastille"]
        if t == "couverture":
            corps += '<h1 style="font-size:%dpx">%s</h1><p class="chapo">%s</p>' % (s.get("taille", 88), s["titre"], s["chapo"])
            corps += s.get("visuel", "")
            style = ""
        else:
            corps += '<h1 style="font-size:%dpx">%s</h1><p class="chapo">%s</p>' % (s.get("taille", 80), s["titre"], s["chapo"])
            boutons = s.get("boutons", ("06 81 65 15 91", "btpexpertise.fr"))
            corps += ('<div class="boutons"><div class="bouton or">%s</div><div class="bouton bl">%s</div></div>'
                      '<div class="villes"><span>Nice</span><span>Cannes</span><span>Antibes</span>'
                      '<span>Toulon</span><span>Fréjus</span><span>Draguignan</span></div>' % tuple(boutons))
            corps += '<p class="prix">%s</p>' % s["prix"]
            style = ' style="justify-content:center"'
        return ('<section class="slide photo %s">%s<div class="voile"></div>%s<div class="corps"%s>%s</div></section>'
                % (classe, fond, entete(n, total, theme), style, corps))

    gris = " gris" if s.get("gris") else ""
    h = tete(s)
    if t == "frise":
        h += '<div class="frise %s">' % s.get("couleur", "")
        for k, (titre, texte) in enumerate(s["items"], 1):
            h += ('<div class="etape"><div class="rond">%02d</div><div class="carte"><h3>%s</h3><p>%s</p></div></div>'
                  % (k, titre, texte))
        h += "</div>"
    elif t == "cartes":
        bleu = " bleu" if s.get("couleur") == "bleu" else ""
        h += '<div class="pile">'
        for ic, titre, texte in s["items"]:
            couleur = "n" if bleu else "o"
            h += ('<div class="carte ligne%s">%s<div><h3>%s</h3><p>%s</p></div></div>'
                  % (bleu, icone(ic, couleur), titre, texte))
        h += "</div>"
    elif t == "liste":
        h += '<div class="coches">' + "".join("<span>%s</span>" % x for x in s["items"]) + "</div>"
    elif t == "duo":
        h += '<div class="duo">'
        for k, (ic, titre, texte) in enumerate(s["items"]):
            couleur = "bleu" if k == 1 else ""
            h += ('<div class="carte %s">%s<h3>%s</h3><p>%s</p></div>'
                  % (couleur, icone(ic, "b" if k == 1 else "o"), titre, texte))
        h += "</div>"
    h += pied(s)
    large = " large" if t != "liste" and len(s.get("items", [])) <= 3 else ""
    return ('<section class="slide%s">%s<div class="corps%s">%s</div></section>'
            % (gris, entete(n, total, theme), large, h))


def page(c):
    total = len(c["diapos"])
    theme = c.get("theme", "expertise")
    corps = "\n".join(diapo(s, k, total, theme) for k, s in enumerate(c["diapos"], 1))
    return ("<!doctype html><html lang=\"fr\"><head><meta charset=\"utf-8\"><title>%s</title>"
            "<link href=\"https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800"
            "&family=Poppins:wght@300;400;500;600&display=swap\" rel=\"stylesheet\">"
            "<link rel=\"stylesheet\" href=\"../gabarit.css\"></head><body class=\"theme-%s\">\n%s\n"
            "<script>const n=+(new URLSearchParams(location.search).get('n')||1);"
            "document.querySelectorAll('.slide')[n-1].classList.add('actif');</script>"
            "</body></html>" % (c["slug"], theme, corps))


def rendre(c):
    dossier = os.path.join(ICI, c["slug"])
    os.makedirs(dossier, exist_ok=True)
    html = os.path.join(dossier, "carrousel.html")
    with open(html, "w", encoding="utf-8") as f:
        f.write(page(c))
    url = "file:///" + html.replace("\\", "/")
    images = []
    for n in range(1, len(c["diapos"]) + 1):
        png = os.path.join(dossier, "s%d.png" % n)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1080,1350", "--virtual-time-budget=8000",
                        "--screenshot=" + png, "%s?n=%d" % (url, n)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        im = Image.open(png).convert("RGB")
        os.remove(png)
        jpg = os.path.join(RACINE, "medias", "%s-%d.jpg" % (c["slug"], n))
        im.save(jpg, quality=92, optimize=True)
        images.append(im)
    w, h = 432, 540
    apercu = Image.new("RGB", (w * len(images) + 8 * (len(images) - 1), h), "#9a9a9a")
    for k, im in enumerate(images):
        apercu.paste(im.resize((w, h), Image.LANCZOS), (k * (w + 8), 0))
    apercu.save(os.path.join(dossier, "apercu.jpg"), quality=86)
    print(c["slug"], c.get("theme", "expertise"), len(images), "diapos")


if __name__ == "__main__":
    voulus = sys.argv[1:]
    for c in CARROUSELS:
        if not voulus or c["slug"] in voulus:
            rendre(c)
