# Publication Instagram

Ce dépôt publie automatiquement sur Instagram, par l'API Meta, sans aucun service payant.

## Fonctionnement

- `publications/*.json` contient une publication par fichier.
- `medias/` contient les images et vidéos. Elles sont servies par GitHub Pages, ce qui leur donne l'adresse publique qu'exige Instagram.
- `comptes.json` contient les comptes Instagram et le nom du secret GitHub qui garde leur jeton.
- `.github/workflows/publier.yml` passe toutes les 15 minutes et publie ce qui est `valide` et dont la date est passée.

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
4. Ajoutez la ligne correspondante dans le bloc `env` de `publier.yml`.

## Obtenir un jeton de page qui n'expire pas

1. Dans l'Explorateur de l'API Graph (developers.facebook.com/tools/explorer), sélectionnez l'app « Publication Groupe ». Générez un jeton avec ces autorisations : `pages_show_list`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`, `business_management`.
2. Dans le Débogueur de jeton d'accès, cliquez sur « Extend Access Token ».
3. Revenez dans l'Explorateur avec ce jeton prolongé et lancez `me/accounts?fields=name,access_token,instagram_business_account`. Copiez l'`access_token` de la page voulue.
4. Vérifiez-le dans le débogueur : la ligne « Expires » doit indiquer « Never ». Collez-le dans le secret GitHub, sans retour à la ligne.

## Essai local

```bash
BASE_MEDIAS=https://compte.github.io/publication-instagram node scripts/publier.mjs --essai
```
