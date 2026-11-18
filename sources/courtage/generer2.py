"""Les 5 publications de Claude, en deux ambiances alternées dans le feed :
bleu nuit (0 €, loi Lemoine) et sable et soleil (portrait, banque, pièces du dossier).
Écrit ../../medias/<slug>-<n>.jpg (mêmes noms que ceux déjà inscrits dans le CRM).

    python generer2.py
"""
import pathlib, subprocess, shutil
from PIL import Image
import illustrations as I

ICI = pathlib.Path(__file__).resolve().parent
R = ICI / "rendu2"; R.mkdir(exist_ok=True)
MEDIAS = ICI.parent.parent / "medias"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
LOGOS = pathlib.Path(r"C:\Users\elodi\OneDrive\Espace commun\Claude\logo-la-reference-courtage")
shutil.copy(LOGOS / "logo-la-reference-courtage.svg", R / "logo.svg")
shutil.copy(LOGOS / "logo-la-reference-courtage-fond-fonce.svg", R / "logo-fonce.svg")
shutil.copy(ICI / "portrait-mickael.jpg", R / "portrait-mickael.jpg")
CTA = ICI / "elodie" / "9.png"

BASE = """*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Arial,Helvetica,sans-serif;position:relative}
.logo{position:absolute;left:96px;top:92px;height:74px}
.page{position:absolute;right:96px;top:116px;font-size:28px;font-weight:700;letter-spacing:2px}
h1{font-size:84px;line-height:1.02;font-weight:700;letter-spacing:-1.5px}
.o{color:#F4801C}.barre{width:110px;height:9px;background:#F4801C;margin:34px 0}
.sous{font-size:40px;line-height:1.22}
.num{font-size:170px;font-weight:700;line-height:.85;letter-spacing:-5px;color:#4FB3D6}
h2{font-size:64px;line-height:1.05;font-weight:400;letter-spacing:-1px}h2 b{display:block;font-weight:700}
p{font-size:37px;line-height:1.22;margin-top:24px}
.ill{position:absolute}.ill svg{width:100%;height:100%;overflow:visible}
.rond{position:absolute;border-radius:50%}
ul{list-style:none;margin-top:34px}
li{font-size:38px;line-height:1.2;padding-left:36px;position:relative;margin-bottom:18px}
li:before{content:"";position:absolute;left:4px;top:16px;width:14px;height:14px;border-radius:50%;background:#F4801C}
"""
THEMES = {
    "nuit": dict(css="body{background:#15384E;color:#fff} .sous,p,li{color:#CFE3EE} .page{color:#7FA7BD}", logo="logo-fonce.svg"),
    "sable": dict(css="body{background:#FFF3E2;color:#1D5B78} .sous,p,li{color:#1D5B78} .page{color:#9A4E10}", logo="logo.svg"),
}

def decor(theme, x, y, t):
    if theme == "nuit":
        return f'<div class="rond" style="width:{t}px;height:{t}px;left:{x}px;top:{y}px;background:#1C4560"></div>'
    i = int(t * .73)
    return (f'<div class="rond" style="width:{t}px;height:{t}px;left:{x}px;top:{y}px;background:#FCE0C2"></div>'
            f'<div class="rond" style="width:{i}px;height:{i}px;left:{x+(t-i)//2}px;top:{y+(t-i)//2}px;background:#F9C08A"></div>')

def doc(theme, corps, page=""):
    th = THEMES[theme]
    pg = f'<div class="page">{page}</div>' if page else ""
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE}{th["css"]}</style></head><body>'
            f'{corps}<img class="logo" src="{th["logo"]}">{pg}</body></html>')

def couverture(theme, titre, sous, ill, page):
    d = decor(theme, 470, 560, 840) if theme == "sable" else decor(theme, 420, 500, 960)
    return doc(theme, f"""{d}
<div style="position:absolute;left:96px;top:300px;width:860px"><h1>{titre}</h1><div class="barre"></div><div class="sous" style="width:520px">{sous}</div></div>
<div class="ill" style="right:60px;bottom:100px;width:580px;height:500px">{ill}</div>""", page)

def point(theme, num, l1, l2, txt, ill, page):
    d = decor(theme, 560, -330, 820) if theme == "sable" else decor(theme, 560, -280, 760)
    return doc(theme, f"""{d}
<div class="ill" style="left:240px;top:230px;width:600px;height:520px">{ill}</div>
<div style="position:absolute;left:96px;top:820px;width:890px;display:flex;gap:44px;align-items:flex-start">
<div class="num">{num}</div><div><h2>{l1}<b>{l2}</b></h2><p>{txt}</p></div></div>""", page)

def liste(theme, num, titre, items, ill, page):
    d = decor(theme, 560, -330, 820) if theme == "sable" else decor(theme, 560, -280, 760)
    lis = "".join(f"<li>{i}</li>" for i in items)
    return doc(theme, f"""{d}
<div class="ill" style="left:300px;top:210px;width:480px;height:415px">{ill}</div>
<div style="position:absolute;left:96px;top:680px;width:890px">
<div style="display:flex;gap:36px;align-items:flex-end"><div class="num" style="font-size:140px">{num}</div><h2 style="padding-bottom:4px"><b>{titre}</b></h2></div>
<ul>{lis}</ul></div>""", page)

def zero():
    return doc("nuit", f"""{decor("nuit", 420, 500, 960)}
<div style="position:absolute;left:96px;top:290px;width:860px">
<div class="num" style="font-size:230px;color:#F4801C">0&nbsp;€</div><div class="barre"></div>
<h2>d'honoraires avant<b>le déblocage des fonds</b></h2>
<p style="width:520px">Nos honoraires ne sont dus qu'une fois votre financement obtenu et les fonds débloqués.</p></div>
<div class="ill" style="right:50px;bottom:90px;width:500px;height:432px">{I.CONTRAT}</div>""")

def portrait():
    return doc("sable", f"""{decor("sable", 420, 380, 900)}
<div style="position:absolute;right:96px;top:300px;width:430px;height:560px;border-radius:30px;overflow:hidden;border:10px solid #fff;box-shadow:0 30px 60px -30px rgba(29,91,120,.55)">
<img src="portrait-mickael.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 18%"></div>
<div style="position:absolute;left:96px;top:320px;width:420px">
<div style="font-size:26px;font-weight:700;letter-spacing:3px;color:#F4801C">VOTRE INTERLOCUTEUR</div>
<h1 style="margin-top:24px;font-size:96px">Mickael<br>Rigaud</h1><div class="barre"></div>
<div class="sous" style="font-size:36px">Fondateur de La Référence Courtage, dans le financement depuis 2014.</div></div>
<div style="position:absolute;left:96px;top:1000px;width:890px;font-size:40px;line-height:1.25;color:#1D5B78">
Un seul interlocuteur, <b>de votre premier appel jusqu'à la signature</b> chez le notaire.</div>""")

PUBLICATIONS = {
    "lrc-zero-honoraire": [zero()],
    "lrc-banque": [
        couverture("sable", 'Ce que la banque<br>regarde avant<br><span class="o">de dire oui</span>', "Six points qu'elle étudie sur chaque dossier de prêt immobilier.", I.BANQUE, "1/8"),
        point("sable", "01", "Le taux", "d'endettement", "Vos mensualités de crédit, assurance comprise, ne doivent pas dépasser 35&nbsp;% de vos revenus.", I.CAMEMBERT, "2/8"),
        point("sable", "02", "La durée", "du prêt", "25 ans maximum, jusqu'à 27 ans quand le projet comprend une construction ou des travaux importants.", I.CALENDRIER, "3/8"),
        point("sable", "03", "Votre", "apport", "En général, il couvre au moins les frais de notaire et de garantie, et montre votre capacité d'épargne.", I.TIRELIRE, "4/8"),
        point("sable", "04", "Le reste", "à vivre", "Ce qu'il vous reste chaque mois une fois le crédit et les charges payés.", I.PORTEFEUILLE, "5/8"),
        point("sable", "05", "Votre situation", "professionnelle", "Type de contrat, ancienneté, régularité des revenus : la banque regarde leur stabilité.", I.MALLETTE, "6/8"),
        point("sable", "06", "La tenue", "de vos comptes", "Découverts, crédits à la consommation en cours, capacité à mettre de côté.", I.RELEVE, "7/8"),
        CTA,
    ],
    "lrc-loi-lemoine": [
        couverture("nuit", 'Assurance<br>emprunteur :<br><span class="o">la loi Lemoine</span>', "Ce qu'elle change pour votre prêt, même s'il est déjà en cours.", I.BOUCLIER_MAISON, "1/5"),
        point("nuit", "01", "Changez-en", "à tout moment", "Depuis 2022, vous pouvez résilier votre assurance emprunteur quand vous voulez, sans frais.", I.ECHANGE, "2/5"),
        point("nuit", "02", "Des garanties", "équivalentes", "Le nouveau contrat doit offrir au moins les mêmes garanties. La banque a 10 jours ouvrés pour répondre.", I.EQUIVALENT, "3/5"),
        point("nuit", "03", "Sans questionnaire", "de santé", "Pour une part assurée jusqu'à 200&nbsp;000&nbsp;€ par personne, si le prêt se termine avant vos 60 ans.", I.SANTE, "4/5"),
        CTA,
    ],
    "lrc-pieces-dossier": [
        couverture("sable", 'Les pièces<br>de votre<br><span class="o">dossier de prêt</span>', "La liste à préparer pour gagner du temps dès le premier rendez-vous.", I.DOSSIER, "1/6"),
        liste("sable", "01", "Votre identité", ["Pièce d'identité en cours de validité", "Justificatif de domicile récent", "Livret de famille, contrat de mariage ou de PACS", "Jugement de divorce, le cas échéant"], I.IDENTITE, "2/6"),
        liste("sable", "02", "Vos revenus", ["3 derniers bulletins de salaire", "Bulletin de décembre de l'an dernier", "Contrat de travail", "2 derniers avis d'imposition"], I.BULLETIN, "3/6"),
        liste("sable", "03", "Vos comptes", ["3 derniers relevés de tous vos comptes", "Relevés de votre épargne et de votre apport", "Tableaux d'amortissement des crédits en cours"], I.RELEVES, "4/6"),
        liste("sable", "04", "Votre projet", ["Compromis ou promesse de vente", "Devis si travaux", "Contrat de réservation pour un achat sur plan", "Permis de construire et contrat de construction"], I.MAISON_CLE, "5/6"),
        CTA,
    ],
}

def main():
    for slug, diapos in PUBLICATIONS.items():
        for i, d in enumerate(diapos, 1):
            png = R / f"{slug}-{i}.png"
            if isinstance(d, pathlib.Path):
                Image.open(d).convert("RGB").save(png)
            else:
                h = png.with_suffix(".html"); h.write_text(d, encoding="utf-8")
                subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                                "--window-size=1080,1350", f"--screenshot={png}", h.as_uri()], check=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            Image.open(png).convert("RGB").save(MEDIAS / f"{slug}-{i}.jpg", quality=92)

if __name__ == "__main__":
    main()
