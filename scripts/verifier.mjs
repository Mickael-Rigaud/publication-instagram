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

for (const [cle, compte] of Object.entries(comptes)) {
  const jeton = (process.env[compte.secret] || '').trim();
  if (!jeton) { console.error(`${cle} : secret ${compte.secret} absent`); process.exitCode = 1; continue; }
  try {
    const profil = await lire(`/${compte.ig_user_id}`, { fields: 'username,name,media_count,followers_count' }, jeton);
    console.log(`${cle} : @${profil.username} (${profil.name}) — ${profil.media_count} publications, ${profil.followers_count} abonnés`);
    // Quota de publication : n'est accessible qu'avec l'autorisation instagram_content_publish.
    const quota = await lire(`/${compte.ig_user_id}/content_publishing_limit`, { fields: 'quota_usage,config' }, jeton);
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
