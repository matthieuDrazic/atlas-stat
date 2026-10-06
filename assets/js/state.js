import {loadLocal,saveLocal} from './utils.js';
export const state={catalog:[],themes:[],territories:[],synonyms:{},records:[],favorites:loadLocal('atlas-favorites',[]),recent:loadLocal('atlas-recent',[]),filters:{theme:'all',indicator:'population-demo',geo:'FR',from:'2020',to:'2024',source:'all',unit:'all',category:'all',population:'all'},chart:'auto',compare:['FR-53','FR-28'],page:0,route:'home',request:0};
export function remember(){const entry={...state.filters};state.recent=[entry,...state.recent.filter(x=>JSON.stringify(x)!==JSON.stringify(entry))].slice(0,6);saveLocal('atlas-recent',state.recent)}
export function addFavorite(){const f={...state.filters};if(!state.favorites.some(x=>JSON.stringify(x)===JSON.stringify(f)))state.favorites.push(f);return saveLocal('atlas-favorites',state.favorites)}
export function removeFavorite(index){state.favorites.splice(index,1);saveLocal('atlas-favorites',state.favorites)}
