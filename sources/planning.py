# -*- coding: utf-8 -*-
"""Planning des publications : crée les fiches publications/*.json en brouillon
et le récapitulatif visuel sources/recap.html.

Fil en colonnes : Expertise (gauche) · Réseau (milieu) · AMO (droite).
Instagram place la plus récente en haut à gauche : chaque série se publie
donc AMO, puis Réseau, puis Expertise.

    python sources/planning.py
"""

import json
import os

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
HEURE = "T18:30:00+02:00"

TAGS_EXPERTISE = "#expertisebatiment #expertbatiment #nice #cannes #antibes #var #alpesmaritimes #cotedazur"
TAGS_AMO = "#amo #assistancemaitrisedouvrage #travaux #renovation #nice #var #alpesmaritimes #cotedazur"
TAGS_RESEAU = "#reseau #independant #batiment #expertbatiment #alpesmaritimes #var #cotedazur"
CONTACT = "06 81 65 15 91 · btpexpertise.fr"

PLANNING = [
    # --- Semaine 1
    ("2026-10-12", "2026-10-15-amo-devis", 6, "amo",
     "Trois devis. Trois prix. Lequel choisir ?\n\n"
     "Le moins cher n'est pas toujours le bon. Le plus cher non plus. Le piège, c'est de comparer des prix au lieu de comparer des prestations : un devis compte la dépose, l'autre l'oublie ; l'un détaille les quantités, l'autre écrit « forfait ».\n\n"
     "En assistance à maîtrise d'ouvrage, on lit chaque devis ligne par ligne : périmètre, quantités, matériaux, assurances, délais et paiements. Vous restez décisionnaire, et vous contractez directement avec les entreprises.\n\n"
     "Des devis à comparer ? " + CONTACT + "\n\n" + TAGS_AMO + " #devis"),
    ("2026-10-14", "reseau-rejoindre", 6, "reseau",
     "Indépendant du bâtiment ? Travaillons ensemble.\n\n"
     "BTP Expertise développe un réseau de professionnels indépendants, pour mobiliser la bonne compétence sur chaque dossier : expertise, structure, humidité, thermique, économie de la construction, électricité, plomberie, couverture…\n\n"
     "Vous gardez votre structure et votre responsabilité professionnelle. Prérequis : statut indépendant, expérience terrain, RC professionnelle à jour, secteur Alpes-Maritimes et/ou Var.\n\n"
     "Présentez-nous votre profil sur btpexpertise.fr/rejoignez-nous : premier échange téléphonique, sans engagement.\n\n" + TAGS_RESEAU),
    ("2026-10-16", "2026-10-13-toiture", 6, "expertise",
     "Une heure de pluie. Un mois d'eau.\n\n"
     "Sur la Côte d'Azur, un épisode méditerranéen peut déverser en une heure ce que la région reçoit parfois en un mois. Toitures-terrasses, terrains en pente, extensions : le bâti local a ses points faibles.\n\n"
     "Dans ce carrousel :\n→ ce que vous pouvez vérifier depuis le sol\n→ là où l'eau passe le plus souvent\n→ les 3 gestes qui comptent si l'eau est entrée\n\n"
     "Vérifier avant coûte le prix d'une visite. Constater après coûte le prix des travaux.\n\n"
     "Expertise désordres et malfaçons à partir de 1 200 € TTC, devis établi avant toute intervention.\n" + CONTACT + "\n\n" + TAGS_EXPERTISE + " #etancheite #toiture"),
    # --- Semaine 2
    ("2026-10-19", "2026-10-22-reception", 6, "amo",
     "Le jour de la réception, tout se joue.\n\n"
     "Signer le procès-verbal transfère la garde de l'ouvrage, fait partir les garanties (parfait achèvement 1 an, bon fonctionnement 2 ans, décennale 10 ans) et rend le solde exigible. Un défaut apparent que vous ne signalez pas ce jour-là est réputé accepté.\n\n"
     "Une réserve utile est située, décrite et photographiée. Et attention à la réception tacite : emménager et régler le solde peut valoir réception, sans aucune réserve.\n\n"
     "Assistance à réception de travaux à partir de 750 € TTC, devis établi avant toute intervention.\n" + CONTACT + "\n\n" + TAGS_AMO + " #receptiondetravaux"),
    ("2026-10-21", "reseau-competences", 4, "reseau",
     "Un dossier, la bonne compétence.\n\n"
     "Une fissure appelle un regard structure, une infiltration un spécialiste de l'étanchéité, un projet de travaux un accompagnement AMO. C'est le principe du réseau BTP Expertise : mobiliser le profil adapté à chaque dossier.\n\n"
     "Ingénieur structure, thermicien, économiste de la construction, spécialiste électricité, plomberie, couverture, assainissement… votre spécialité manque peut-être.\n\n"
     "Candidature sur btpexpertise.fr/rejoignez-nous, premier échange sans engagement.\n\n" + TAGS_RESEAU),
    ("2026-10-23", "2026-10-fissures-v3", 7, "expertise",
     "Cette fissure s'élargit chaque été… et se referme presque l'hiver.\n\n"
     "Dans le 06 et le 83, ce n'est souvent pas le mur qui pose problème : c'est le sol. Le retrait-gonflement des argiles fait travailler les fondations au rythme des saisons.\n\n"
     "Dans ce carrousel :\n→ le mécanisme, en deux saisons\n→ les signes qui doivent alerter\n→ les réflexes qui aggravent le dossier\n→ ce que vous pouvez faire dès aujourd'hui\n\n"
     "Le bon réflexe : ne pas reboucher tout de suite. Photographier, dater, mesurer. Et faire analyser avant de réparer.\n\n"
     "Expertise désordres et malfaçons à partir de 1 200 € TTC, devis établi avant toute intervention.\n" + CONTACT + "\n\n" + TAGS_EXPERTISE + " #fissures #retraitgonflementargiles"),
    # --- Semaine 3
    ("2026-10-26", "2026-11-05-amo-chantier", 6, "amo",
     "Le chantier dérape. Qui défend vos intérêts ?\n\n"
     "Avenants qui s'enchaînent, planning qui glisse, travaux différents du devis, acomptes qui devancent l'avancement : seul face aux entreprises, difficile de savoir quoi accepter.\n\n"
     "L'assistance à maîtrise d'ouvrage, c'est un regard technique à vos côtés : visites sur site, contrôle visuel de la qualité apparente, comptes rendus, assistance à réception. Nous conseillons, nous alertons ; vous décidez.\n\n"
     "Honoraires AMO : 5 à 8 % du montant HT des travaux, minimum 3 500 € HT.\n" + CONTACT + "\n\n" + TAGS_AMO + " #chantier"),
    ("2026-10-28", "reseau-expert", 5, "reseau",
     "La pathologie du bâti, c'est votre terrain ?\n\n"
     "Fissures et structure, humidité et infiltrations, malfaçons et litiges travaux : le cabinet cherche des experts bâtiment indépendants sur les Alpes-Maritimes et le Var.\n\n"
     "Le profil : une formation bâtiment, de l'expérience terrain, et des rapports écrits clairs, qui tiennent face à une entreprise, un assureur ou un juge. Statut indépendant, RC professionnelle à jour.\n\n"
     "Votre parcours nous intéresse : btpexpertise.fr/rejoignez-nous\n\n" + TAGS_RESEAU),
    ("2026-10-30", "2026-10-20-facade", 6, "expertise",
     "Après l'orage, le mur pleure.\n\n"
     "Coulures sous un débord, auréoles en pied de mur, traces autour des fenêtres : chaque trace a son origine, et la façade raconte par où l'eau est passée.\n\n"
     "Repeindre par-dessus ne soigne rien : la trace revient, la cause reste. Le bon ordre, c'est observer, comprendre, puis réparer au bon endroit.\n\n"
     "Expertise désordres et malfaçons à partir de 1 200 € TTC, devis établi avant toute intervention.\n" + CONTACT + "\n\n" + TAGS_EXPERTISE + " #infiltration #facade"),
]

