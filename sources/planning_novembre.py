# -*- coding: utf-8 -*-
"""Planning de novembre 2026 : légendes et dates (voir programme.py).

Le 11 novembre est férié : le Réseau de la semaine 2 passe au mardi 10.
Prix relus sur btpexpertise.fr/reglement/ le 2026-10-08.
"""

from planning import CONTACT, TAGS_AMO, TAGS_EXPERTISE, TAGS_RESEAU

PRIX_DESORDRES_TXT = "Expertise désordres et malfaçons à partir de 1 200 € TTC, devis établi avant toute intervention."
PRIX_AMO_TXT = "Honoraires AMO : 5 à 8 % du montant HT des travaux, minimum 3 500 € HT."
CANDIDATURE_TXT = "Candidature sur btpexpertise.fr/rejoignez-nous, premier échange téléphonique sans engagement."

NOVEMBRE = [
    # --- Semaine 1
    ("2026-11-02", "2026-11-amo-cadrage", 6, "amo",
     "Le projet commence avant le premier devis.\n\n"
     "Sans cadrage, chaque entreprise chiffre un projet différent : l'une imagine une cuisine ouverte, l'autre non ; l'une prévoit la dépose, l'autre l'oublie. Résultat : trois devis impossibles à comparer.\n\n"
     "L'étude du projet pose les bonnes questions : objectifs, contraintes, priorités, enveloppe. La définition des travaux décrit ensuite les prestations, pour que chaque entreprise chiffre le même projet.\n\n"
     "Vous restez décisionnaire, et vous contractez directement avec l'entreprise de votre choix.\n\n"
     + PRIX_AMO_TXT + "\n" + CONTACT + "\n\n" + TAGS_AMO),
    ("2026-11-04", "2026-11-reseau-economiste", 5, "reseau",
     "Profil recherché : économiste de la construction.\n\n"
     "Estimer des travaux poste par poste, analyser et comparer des devis, éclairer le choix des entreprises : une compétence au cœur des missions d'assistance à maîtrise d'ouvrage.\n\n"
     "Le réseau BTP Expertise réunit des professionnels indépendants sur les Alpes-Maritimes et le Var. Vous gardez votre structure et votre responsabilité professionnelle.\n\n"
     + CANDIDATURE_TXT + "\n\n" + TAGS_RESEAU + " #economistedelaconstruction"),
    ("2026-11-06", "2026-10-27-pied-de-mur", 6, "expertise",
     "Le bas du mur s'effrite.\n\n"
     "Salpêtre, peinture qui cloque, plinthes qui gonflent : l'humidité monte peut-être du sol. Ou pas. Remontées capillaires, infiltration latérale, fuite ou condensation : les traces se ressemblent, les traitements n'ont rien à voir.\n\n"
     "À éviter : l'enduit étanche sur un mur ancien, le doublage collé qui cache le problème, le traitement choisi au hasard.\n\n"
     "Le bon ordre : constater, identifier la cause, choisir le traitement, vérifier la reprise.\n\n"
     + PRIX_DESORDRES_TXT + "\n" + CONTACT + "\n\n" + TAGS_EXPERTISE + " #humidite #salpetre"),
    # --- Semaine 2
    ("2026-11-09", "2026-11-amo-budget", 6, "amo",
     "Votre budget va déraper. Voici pourquoi.\n\n"
     "Rarement à cause d'un seul poste. Souvent à cause de ce qui n'était pas écrit : postes oubliés, quantités floues, surprises du bâti existant, avenants en cours de route.\n\n"
     "Avant les travaux, on estime poste par poste, on hiérarchise, on prévoit une marge pour les aléas et on compare les devis sur un même périmètre. Pendant les travaux, chaque avenant se discute : comprendre, vérifier, puis décider.\n\n"
     "L'AMO éclaire vos décisions ; elle ne promet ni budget ni délai. La décision reste la vôtre.\n\n"
     + PRIX_AMO_TXT + "\n" + CONTACT + "\n\n" + TAGS_AMO + " #budgettravaux"),
    ("2026-11-10", "2026-11-reseau-rapport", 5, "reseau",
     "Ce qui fait un rapport qui tient.\n\n"
     "Constater : situer, mesurer, photographier avec un repère d'échelle.\n"
     "Analyser : examiner les hypothèses une à une, s'appuyer sur les DTU et les règles de l'art, conclure sur la cause probable et son degré de certitude.\n"
     "Préconiser : les priorités, les investigations nécessaires, et les limites de la mission, écrites noir sur blanc.\n\n"
     "C'est l'exigence que nous partageons avec les professionnels indépendants du réseau. Vous la partagez aussi ?\n\n"
     + CANDIDATURE_TXT + "\n\n" + TAGS_RESEAU + " #rapportdexpertise"),
    ("2026-11-13", "2026-10-29-avant-achat", 6, "expertise",
     "Coup de cœur. Offre ce soir ?\n\n"
     "Les diagnostics obligatoires protègent le vendeur : amiante, plomb, termites, électricité, gaz, DPE, risques. Ils ne disent presque rien de l'état réel du bâtiment.\n\n"
     "L'expertise avant achat regarde la structure, l'humidité, la couverture, les travaux antérieurs, la copropriété. Et elle chiffre : des travaux à prévoir changent la discussion sur le prix. Le meilleur moment, c'est avant le compromis.\n\n"
     "Expertise avant achat à partir de 900 € TTC, devis établi avant toute intervention.\n" + CONTACT + "\n\n" + TAGS_EXPERTISE + " #avantachat #immobilier"),
    # --- Semaine 3
    ("2026-11-16", "2026-11-amo-visite", 6, "amo",
     "Ce qu'une visite de chantier vérifie vraiment.\n\n"
     "L'avancement au regard du planning, la qualité apparente des travaux, les points de vigilance avant qu'ils soient cachés : réseaux avant la fermeture des cloisons, supports et pentes avant le carrelage.\n\n"
     "Après chaque visite, un compte rendu écrit : photographies datées, observations, recommandations.\n\n"
     "La visite AMO observe, alerte et conseille. Elle ne dirige pas les travaux : vous restez maître de votre projet.\n\n"
     + PRIX_AMO_TXT + "\n" + CONTACT + "\n\n" + TAGS_AMO + " #chantier"),
    ("2026-11-18", "2026-11-reseau-couverture", 5, "reseau",
     "Profil recherché : spécialiste couverture et étanchéité.\n\n"
     "Avec les pluies d'automne, les dossiers d'infiltration se multiplient : relevés d'étanchéité, évacuations pluviales, raccords d'extensions et de vérandas, souches de cheminée.\n\n"
     "Le réseau BTP Expertise réunit des professionnels indépendants sur les Alpes-Maritimes et le Var. Les toitures, c'est votre terrain ?\n\n"
     + CANDIDATURE_TXT + "\n\n" + TAGS_RESEAU + " #couverture #etancheite"),
    ("2026-11-20", "2026-11-03-malfacon", 6, "expertise",
     "Ça ne me plaît pas. Est-ce une malfaçon ?\n\n"
     "Une finition qui déplaît, une tolérance admise, un choix discutable mais conforme : tout ce qui dérange n'est pas reprochable à l'entreprise. Et inversement.\n\n"
     "L'analyse se fait au regard de règles, pas d'un ressenti : DTU, règles de l'art, pièces du marché, notices des fabricants. Avant de contester, documentez : photos datées, devis, échanges écrits. Et ne faites rien reprendre avant le constat.\n\n"
     + PRIX_DESORDRES_TXT + "\n" + CONTACT + "\n\n" + TAGS_EXPERTISE + " #malfacons #travaux"),
    # --- Semaine 4
    ("2026-11-23", "2026-11-amo-sinistre", 6, "amo",
     "Après un sinistre, refaire… mais comment ?\n\n"
     "L'expert de l'assurance travaille pour son mandant, les entreprises proposent chacune leur solution, et vous devez décider vite.\n\n"
     "Avant de reconstruire : constater l'étendue, comprendre l'origine pour ne pas reconstruire sur la même faiblesse, décrire les reprises, consulter les entreprises sur un même périmètre. Et éviter les pièges de l'urgence : nettoyer avant de photographier, signer le premier devis, refaire à l'identique.\n\n"
     + PRIX_AMO_TXT + "\n" + CONTACT + "\n\n" + TAGS_AMO + " #sinistre"),
    ("2026-11-25", "2026-11-reseau-thermicien", 5, "reseau",
     "Profil recherché : thermicien du bâtiment.\n\n"
     "Moisissures, condensation, inconfort : des dossiers où la thermique fait la différence. Trouver le point froid, vérifier la continuité de l'isolation, comprendre un circuit de ventilation.\n\n"
     "Le réseau BTP Expertise réunit des professionnels indépendants sur les Alpes-Maritimes et le Var. Vous gardez votre structure et votre responsabilité professionnelle.\n\n"
     + CANDIDATURE_TXT + "\n\n" + TAGS_RESEAU + " #thermique"),
    ("2026-11-27", "2026-11-fuite-encastree", 6, "expertise",
     "Une facture d'eau qui grimpe. Et rien ne coule.\n\n"
     "Une fuite encastrée se voit rarement : elle se devine. Compteur qui tourne robinets fermés, tache qui s'étend, carrelage qui sonne creux, odeur d'humidité persistante.\n\n"
     "Le test simple : tout fermer, relever l'index du compteur, attendre une à deux heures sans tirer d'eau, comparer.\n\n"
     "Et surtout, ne pas casser au hasard : on localise avant de réparer.\n\n"
     + PRIX_DESORDRES_TXT + "\n" + CONTACT + "\n\n" + TAGS_EXPERTISE + " #fuite #plomberie"),
]
