export const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const norm=v=>String(v??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
export const fmt=(v,unit='')=>v==null?'Non disponible':new Intl.NumberFormat('fr-FR',{maximumFractionDigits:unit==='personnes'?0:2}).format(v)+(unit==='%'?' %':unit==='EUR'?' €':'');
export const safeURL=v=>{try{const u=new URL(v);return ['https:','http:'].includes(u.protocol)?u.href:''}catch{return ''}};
export function toast(message){const e=document.querySelector('#toast');e.textContent=message;e.style.display='block';clearTimeout(toast.timer);toast.timer=setTimeout(()=>e.style.display='none',4500)}
export async function getJSON(path){const r=await fetch(path,{signal:AbortSignal.timeout(15000)});if(!r.ok)throw new Error(`Fichier indisponible (${r.status}) : ${path}`);return r.json()}
export function saveLocal(key,value){try{localStorage.setItem(key,JSON.stringify(value));return true}catch{return false}}
export function loadLocal(key,fallback){try{return JSON.parse(localStorage.getItem(key))??fallback}catch{return fallback}}
export const colors=['#007f86','#cb7900','#725ac1','#cf5472','#46813e'];
