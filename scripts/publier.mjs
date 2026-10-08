// Publie sur Instagram les publications validées dont l'heure est venue.
// Lancé toutes les 15 minutes par .github/workflows/publier.yml.
// Usage local : node scripts/publier.mjs [--essai]   (--essai : n'appelle pas Meta)

import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const GRAPH = 'https://graph.facebook.com/v23.0';
const RACINE = new URL('..', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1');
const ESSAI = process.argv.includes('--essai');

// Adresse publique des médias, servie par GitHub Pages (ex. https://compte.github.io/publication-instagram)
const BASE_MEDIAS = (process.env.BASE_MEDIAS || '').replace(/\/$/, '');

const comptes = JSON.parse(readFileSync(join(RACINE, 'comptes.json'), 'utf8'));
const dossier = join(RACINE, 'publications');

const pause = ms => new Promise(r => setTimeout(r, ms));

async function graph(methode, chemin, params, jeton) {
  const url = new URL(GRAPH + chemin);
  const corps = new URLSearchParams({ ...params, access_token: jeton });
  const rep = methode === 'GET'
    ? await fetch(url + '?' + corps)
    : await fetch(url, { method: 'POST', body: corps });
  const json = await rep.json();
  if (json.error) throw new Error(`${json.error.message} (code ${json.error.code})`);
  return json;
}

function urlMedia(fichier) {
  if (/^https?:\/\//.test(fichier)) return fichier;
  if (!BASE_MEDIAS) throw new Error('BASE_MEDIAS non défini');
  return `${BASE_MEDIAS}/${fichier.replace(/^\//, '')}`;
}

// GitHub Pages met une minute ou deux à servir un fichier poussé : on attend le prochain passage.
async function accessible(url) {
  try { return (await fetch(url, { method: 'HEAD' })).ok; } catch { return false; }
}

const estVideo = f => /\.(mp4|mov)$/i.test(f);

// Meta traite les médias de façon asynchrone : il faut attendre FINISHED avant de publier.
async function attendreConteneur(id, jeton) {
  for (let i = 0; i < 60; i++) {
    const { status_code } = await graph('GET', `/${id}`, { fields: 'status_code' }, jeton);
    if (status_code === 'FINISHED') return;
    if (status_code === 'ERROR' || status_code === 'EXPIRED') throw new Error(`conteneur ${id} : ${status_code}`);
    await pause(5000);
  }
  throw new Error(`conteneur ${id} : toujours en traitement après 5 minutes`);
}

async function creerConteneur(igId, pub, jeton) {
  const urls = pub.medias.map(urlMedia);
  const legende = pub.type === 'story' ? {} : { caption: pub.legende || '' };

  if (pub.type === 'carrousel') {
    const enfants = [];
    for (const u of urls) {
      const p = estVideo(u) ? { media_type: 'VIDEO', video_url: u } : { image_url: u };
      const { id } = await graph('POST', `/${igId}/media`, { ...p, is_carousel_item: 'true' }, jeton);
      await attendreConteneur(id, jeton);
      enfants.push(id);
    }
    return (await graph('POST', `/${igId}/media`, { media_type: 'CAROUSEL', children: enfants.join(','), ...legende }, jeton)).id;
  }

  const u = urls[0];
  if (pub.type === 'reel') {
    return (await graph('POST', `/${igId}/media`, { media_type: 'REELS', video_url: u, share_to_feed: 'true', ...legende }, jeton)).id;
  }
  if (pub.type === 'story') {
    const p = estVideo(u) ? { video_url: u } : { image_url: u };
    return (await graph('POST', `/${igId}/media`, { media_type: 'STORIES', ...p }, jeton)).id;
  }
  return (await graph('POST', `/${igId}/media`, { image_url: u, ...legende }, jeton)).id;
}

async function publier(fichier) {
  const chemin = join(dossier, fichier);
  const pub = JSON.parse(readFileSync(chemin, 'utf8'));
  if (pub.statut !== 'valide') return;
  if (new Date(pub.date) > new Date()) return;

  const compte = comptes[pub.compte];
  if (!compte) throw new Error(`${fichier} : compte inconnu « ${pub.compte} »`);

  for (const f of pub.medias) {
    const u = urlMedia(f);
    if (!(await accessible(u))) { console.log(`${fichier} : ${u} pas encore en ligne, au prochain passage`); return; }
  }

  console.log(`${fichier} → ${compte.nom} (${pub.type})`);
  if (ESSAI) { console.log('  essai : rien envoyé'); return; }

  const jeton = (process.env[compte.secret] || '').trim();
  if (!jeton) throw new Error(`secret ${compte.secret} absent`);

  // Le statut passe à « en_cours » avant l'appel : si le passage plante, on ne republie pas en double.
  pub.statut = 'en_cours';
  writeFileSync(chemin, JSON.stringify(pub, null, 2) + '\n');

  try {
    const conteneur = await creerConteneur(compte.ig_user_id, pub, jeton);
    await attendreConteneur(conteneur, jeton);
    const { id } = await graph('POST', `/${compte.ig_user_id}/media_publish`, { creation_id: conteneur }, jeton);
    const { permalink } = await graph('GET', `/${id}`, { fields: 'permalink' }, jeton);
    Object.assign(pub, { statut: 'publie', media_id: id, lien: permalink, publie_le: new Date().toISOString() });
    delete pub.erreur;
    console.log(`  publié : ${permalink}`);
  } catch (e) {
    Object.assign(pub, { statut: 'erreur', erreur: e.message });
    console.error(`  erreur : ${e.message}`);
    process.exitCode = 1;
  }
  writeFileSync(chemin, JSON.stringify(pub, null, 2) + '\n');
}

for (const f of readdirSync(dossier).filter(f => f.endsWith('.json')).sort()) {
  try { await publier(f); } catch (e) { console.error(`${f} : ${e.message}`); process.exitCode = 1; }
}
