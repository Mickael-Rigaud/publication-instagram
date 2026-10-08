// Publie sur Instagram les contenus programmés du calendrier de communication
// du CRM Groupe dont l'heure est venue.
// Lancé toutes les 15 minutes par .github/workflows/publier.yml.
// Usage local : CRM_PUB_URL=… CRM_PUB_TOKEN=… node scripts/publier.mjs [--essai]
//   (--essai : lit le CRM mais n'envoie rien à Meta et ne réserve rien)
//
// ⚠ DEPUIS LE 08/10/2026 LA SOURCE EST LE CRM, PLUS `publications/*.json`.
// Une date, une légende ou un visuel changé dans le CRM (BTP Expertise →
// Communication → Calendrier réseaux sociaux) part tel quel. Les fichiers JSON
// restent la trace de fabrication des diapos ; ils ne publient plus rien.
//
// Le CRM n'est joint que par l'Edge Function `communication-publication` et
// son jeton : ce script n'a aucun autre accès à la base.

import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const GRAPH = 'https://graph.facebook.com/v23.0';
const RACINE = new URL('..', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1');
const ESSAI = process.argv.includes('--essai');
const CRM_URL = (process.env.CRM_PUB_URL || '').trim();
const CRM_TOKEN = (process.env.CRM_PUB_TOKEN || '').trim();

const comptes = JSON.parse(readFileSync(join(RACINE, 'comptes.json'), 'utf8'));
// La structure du CRM → le compte Instagram qui publie pour elle.
const COMPTE_DE = Object.fromEntries(Object.entries(comptes)
  .filter(([, c]) => c.activite).map(([cle, c]) => [c.activite, cle]));

const pause = ms => new Promise(r => setTimeout(r, ms));

async function crm(corps) {
  const r = await fetch(CRM_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-publication-token': CRM_TOKEN },
    body: JSON.stringify(corps),
  });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`CRM : ${d.erreur || 'HTTP ' + r.status}`);
  return d;
}

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

// GitHub Pages ou le stockage du CRM peuvent mettre un instant à servir un
// fichier tout juste déposé : on attend le prochain passage.
// Deux essais : un HEAD isolé échoue parfois sans raison (constaté à l'essai
// du 08/10 sur une image servie depuis des heures).
async function accessible(url) {
  for (let i = 0; i < 2; i++) {
    try { if ((await fetch(url, { method: 'HEAD' })).ok) return true; } catch { /* on réessaie */ }
    await pause(1500);
  }
  return false;
}

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

// Le format du CRM → le type de publication Instagram.
const TYPE = { post: 'image', carrousel: 'carrousel', reel: 'reel', story: 'story' };

// Ce qui se voit d'avance, avant de réserver quoi que ce soit chez Meta.
function probleme(c, medias) {
  const type = TYPE[c.format || 'post'];
  if (!type) return `format « ${c.format} » non publiable sur Instagram`;
  if (!medias.length) return 'aucun visuel (image ou vidéo) à publier';
  if (type === 'carrousel' && (medias.length < 2 || medias.length > 10)) return `un carrousel demande 2 à 10 visuels (${medias.length})`;
  if (type === 'reel' && medias[0].type !== 'video') return 'un reel demande une vidéo';
  const pasJpeg = medias.find(m => m.type === 'image' && !/\.jpe?g(\?|$)/i.test(m.url));
  if (pasJpeg) return `Instagram n'accepte que des images JPEG (${pasJpeg.nom || pasJpeg.url})`;
  return null;
}

async function creerConteneur(igId, type, medias, legende, jeton) {
  const cap = type === 'story' ? {} : { caption: legende || '' };
  if (type === 'carrousel') {
    const enfants = [];
    for (const m of medias) {
      const p = m.type === 'video' ? { media_type: 'VIDEO', video_url: m.url } : { image_url: m.url };
      const { id } = await graph('POST', `/${igId}/media`, { ...p, is_carousel_item: 'true' }, jeton);
      await attendreConteneur(id, jeton);
      enfants.push(id);
    }
    return (await graph('POST', `/${igId}/media`, { media_type: 'CAROUSEL', children: enfants.join(','), ...cap }, jeton)).id;
  }
  const m = medias[0];
  if (type === 'reel') {
    return (await graph('POST', `/${igId}/media`, { media_type: 'REELS', video_url: m.url, share_to_feed: 'true', ...cap }, jeton)).id;
  }
  if (type === 'story') {
    const p = m.type === 'video' ? { video_url: m.url } : { image_url: m.url };
    return (await graph('POST', `/${igId}/media`, { media_type: 'STORIES', ...p }, jeton)).id;
  }
  return (await graph('POST', `/${igId}/media`, { image_url: m.url, ...cap }, jeton)).id;
}

async function publier(c) {
  const cle = COMPTE_DE[c.activity];
  const compte = comptes[cle];
  const nom = `${c.date_prevue} ${c.heure || ''} « ${c.titre || c.id} »`;
  const medias = (c.visuels || []).filter(v => v.type === 'image' || v.type === 'video');
  const type = TYPE[c.format || 'post'];

  const souci = probleme(c, medias);
  if (souci) {
    // Rien n'est parti : on réserve pour pouvoir écrire l'erreur dans le CRM,
    // où elle se voit. Sans ça, le post resterait « Programmé » sans un mot.
    console.error(`${nom} : ${souci}`);
    if (!ESSAI && (await crm({ action: 'reserver', id: c.id })).ok) {
      await crm({ action: 'resultat', id: c.id, ok: false, erreur: souci });
    }
    process.exitCode = 1;
    return;
  }
  for (const m of medias) {
    if (!(await accessible(m.url))) { console.log(`${nom} : ${m.url} pas encore en ligne, au prochain passage`); return; }
  }

  console.log(`${nom} → ${compte.nom} (${type}, ${medias.length} média${medias.length > 1 ? 's' : ''})`);
  if (ESSAI) { console.log('  essai : rien envoyé'); return; }

  const jeton = (process.env[compte.secret] || '').trim();
  if (!jeton) throw new Error(`secret ${compte.secret} absent`);

  // ⚠ RÉSERVÉ AVANT L'APPEL À META : si le passage plante au milieu, le post
  // reste « en cours » dans le CRM et ne repart pas en double.
  if (!(await crm({ action: 'reserver', id: c.id })).ok) {
    console.log('  déjà pris par un autre passage, ou modifié entre-temps');
    return;
  }
  try {
    const conteneur = await creerConteneur(compte.ig_user_id, type, medias, c.texte, jeton);
    await attendreConteneur(conteneur, jeton);
    const { id } = await graph('POST', `/${compte.ig_user_id}/media_publish`, { creation_id: conteneur }, jeton);
    const { permalink } = await graph('GET', `/${id}`, { fields: 'permalink' }, jeton);
    await crm({ action: 'resultat', id: c.id, ok: true, media_id: id, lien: permalink });
    console.log(`  publié : ${permalink}`);
  } catch (e) {
    await crm({ action: 'resultat', id: c.id, ok: false, erreur: e.message }).catch(() => {});
    console.error(`  erreur : ${e.message}`);
    process.exitCode = 1;
  }
}

if (!CRM_URL || !CRM_TOKEN) {
  console.error('CRM_PUB_URL ou CRM_PUB_TOKEN absent : rien ne peut être lu');
  process.exit(1);
}
const activites = Object.keys(COMPTE_DE);
const { contenus } = await crm({ action: 'a_publier', reseau: 'instagram', activites });
console.log(`${contenus.length} contenu${contenus.length > 1 ? 's' : ''} à publier (${activites.join(', ')})`);
for (const c of contenus) {
  try { await publier(c); } catch (e) { console.error(`${c.id} : ${e.message}`); process.exitCode = 1; }
}
