import {loadLocal,saveLocal} from './utils.js';
const PREFIX='atlas-cache:';const MAX=12;export function readCache(key){return loadLocal(PREFIX+key,null)}
export function writeCache(key,records){const keys=Object.keys(localStorage).filter(k=>k.startsWith(PREFIX));if(keys.length>=MAX&&!keys.includes(PREFIX+key)){keys.sort((a,b)=>(loadLocal(a,{}).cachedAt??'').localeCompare(loadLocal(b,{}).cachedAt??''));localStorage.removeItem(keys[0])}return saveLocal(PREFIX+key,{cachedAt:new Date().toISOString(),records})}
export function clearCache(){for(const key of Object.keys(localStorage))if(key.startsWith(PREFIX))localStorage.removeItem(key)}
