// Vérifie, sans rien publier, que chaque jeton atteint bien son compte Instagram
// et sa page Facebook, avec les autorisations de publication.
// Lancé à la main depuis l'onglet Actions (workflow « Vérifier les comptes »).

import { readFileSync } from 'node:fs';

const GRAPH = 'https://graph.facebook.com/v23.0';
const comptes = JSON.parse(readFileSync(new URL('../comptes.json', import.meta.url), 'utf8'));

async function lire(chemin, params, jeton) {
  const rep = await fetch(`${GRAPH}${chemin}?` + new URLSearchParams({ ...params, access_token: jeton }));
  const json = await rep.json();
  if (json.error) throw new Error(`${json.error.message} (code ${json.error.code})`);
  return json;
}

// Le compte Instagram d'une page. `ig_user_id` peut manquer dans comptes.json
// (RGD Renova, 12/10/2026) : la page le connaît, et son jeton suffit à le lire.
// On ne le recopie donc pas à la main, une faute de chiffre ne se verrait
// qu'au premier post refusé.
const IG_DE = new Map();
async function igDe(compte, jeton) {
  if (compte.ig_user_id) return compte.ig_user_id;
  if (!IG_DE.has(compte.fb_page_id)) {
    const p = await lire(`/${compte.fb_page_id}`, { fields: 'instagram_business_account' }, jeton);
    if (!p.instagram_business_account?.id) throw new Error(`aucun compte Instagram professionnel relié à la page ${compte.fb_page_id}`);
    IG_DE.set(compte.fb_page_id, p.instagram_business_account.id);
  }
  return IG_DE.get(compte.fb_page_id);
}

for (const [cle, compte] of Object.entries(comptes)) {
  const jeton = (process.env[compte.secret] || '').trim();
  if (!jeton) { console.error(`${cle} : secret ${compte.secret} absent`); process.exitCode = 1; continue; }
  try {
    const igId = await igDe(compte, jeton);
    const profil = await lire(`/${igId}`, { fields: 'username,name,media_count,followers_count' }, jeton);
    console.log(`${cle} : @${profil.username} (${profil.name}) — ${profil.media_count} publications, ${profil.followers_count} abonnés`);
    // Quota de publication : n'est accessible qu'avec l'autorisation instagram_content_publish.
    const quota = await lire(`/${igId}/content_publishing_limit`, { fields: 'quota_usage,config' }, jeton);
    const q = quota.data?.[0];
    console.log(`  publication Instagram autorisée : ${q?.quota_usage ?? 0} / ${q?.config?.quota_total ?? '?'} sur 24 h`);

    // Un jeton de page répond à /me par la page elle-même.
    const page = await lire('/me', { fields: 'id,name' }, jeton);
    console.log(`  page Facebook : ${page.name} (${page.id})`);
    // debug_token accepte le jeton de page pour s'examiner lui-même.
    const info = (await lire('/debug_token', { input_token: jeton }, jeton)).data || {};
    const scopes = info.scopes || [];
    const expire = info.expires_at ? new Date(info.expires_at * 1000).toISOString().slice(0, 10) : 'jamais';
    console.log(`  jeton : type ${info.type || '?'}, expire ${expire}`);
    console.log(`  autorisations : ${scopes.join(', ') || '(illisibles)'}`);
    for (const requise of ['instagram_content_publish', 'pages_manage_posts']) {
      if (scopes.length && !scopes.includes(requise)) {
        console.error(`  MANQUE ${requise}`);
        process.exitCode = 1;
      }
    }
  } catch (e) {
    console.error(`${cle} : ${e.message}`);
    process.exitCode = 1;
  }
}
