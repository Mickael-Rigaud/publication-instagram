# Publication Instagram

Ce dépôt publie automatiquement sur Instagram, par l'API Meta, sans aucun service payant.

## Fonctionnement

**Depuis le 8 octobre 2026, ce qui est publié se décide dans le CRM Groupe**, pas ici : BTP Expertise → Communication → Calendrier réseaux sociaux.

- `.github/workflows/publier.yml` passe toutes les 15 minutes. Il demande au CRM (Edge Function `communication-publication`, secret `CRM_PUB_TOKEN`) les contenus au statut **Programmé**, cochés **Instagram**, dont la date et l'heure (heure de Paris, 9 h si vide) sont passées, et les publie.
- Le résultat est écrit dans le CRM : **Publié** avec le lien du post, ou **Erreur d'envoi** avec le motif. Pendant l'envoi le contenu est **Envoi en cours** : s'il y reste, vérifier sur Instagram avant de le remettre en Programmé, sinon il sortira deux fois.
- Date, heure, légende et visuels se changent donc dans le CRM et partent tels quels.
- `comptes.json` relie une structure du CRM (`activite`) à son compte Instagram et au secret qui garde son jeton.
- `medias/` reste servi par GitHub Pages : les diapos fabriquées ici y sont déposées, et le CRM pointe dessus. Une image déposée dans le CRM fonctionne aussi (stockage public). **JPEG uniquement** pour les images.
- `publications/*.json` et `sources/` ne servent plus qu'à **fabriquer** les diapos et la légende. Leur `statut` et leur `date` ne publient plus rien : une nouvelle publication s'ajoute au calendrier du CRM.

## Une publication

```json
{
  "compte": "btp_expertise",
  "type": "image",
  "date": "2026-10-10T09:00:00+02:00",
  "statut": "brouillon",
  "legende": "Texte de la publication",
  "medias": ["medias/2026-10-10-chantier.jpg"]
}
```

- `type` : `image`, `carrousel` (2 à 10 médias), `reel` (vidéo) ou `story`.
- `statut` : `brouillon`, puis `valide` pour autoriser l'envoi. Le script écrit ensuite `en_cours`, puis `publie` (avec le lien) ou `erreur` (avec le message).
- Les images doivent être en **JPEG**, au format portrait 4:5 jusqu'à paysage 1.91:1, et peser 8 Mo maximum.

Si une publication reste bloquée en `en_cours`, le passage s'est interrompu en plein envoi. Vérifiez sur Instagram si elle est partie avant de la remettre en `valide`.

## Ajouter un compte (par exemple RGD Renova)

1. Récupérez un jeton de page Meta en suivant la procédure ci-dessous, avec la page et le compte Instagram du nouveau compte.
2. Ajoutez une entrée dans `comptes.json` avec son `ig_user_id` et le nom de son secret.
3. Créez ce secret dans GitHub (Settings, puis Secrets and variables, puis Actions).
4. Ajoutez la ligne correspondante dans le bloc `env` de `publier.yml`, et la structure dans `PUBLICATION_AUTO` de `js/data/communication.js` du CRM.

## Obtenir un jeton de page qui n'expire pas

1. Dans l'Explorateur de l'API Graph (developers.facebook.com/tools/explorer), sélectionnez l'app « Publication Groupe ». Générez un jeton avec ces autorisations : `pages_show_list`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`, `business_management`.
2. Dans le Débogueur de jeton d'accès, cliquez sur « Extend Access Token ».
3. Revenez dans l'Explorateur avec ce jeton prolongé et lancez `me/accounts?fields=name,access_token,instagram_business_account`. Copiez l'`access_token` de la page voulue.
4. Vérifiez-le dans le débogueur : la ligne « Expires » doit indiquer « Never ». Collez-le dans le secret GitHub, sans retour à la ligne.

## Essai local

```bash
CRM_PUB_URL=https://qnidmkufauzguultdmky.supabase.co/functions/v1/communication-publication CRM_PUB_TOKEN=… node scripts/publier.mjs --essai
```

`--essai` lit le CRM et dit ce qui partirait, sans rien réserver ni envoyer à Meta.
