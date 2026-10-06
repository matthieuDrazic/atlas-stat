import {normalizeRecord} from './csv-adapter.js';
// Chaque cube INSEE possède ses dimensions. Le mapping est obligatoire, sans deviner les codes.
export function inseeAdapter(rows,indicator,{source,mapRow}){if(!Array.isArray(rows)||typeof mapRow!=='function')throw new Error('INSEE : tableau et correspondance explicite des dimensions requis.');if(source.publisher!=='INSEE')throw new Error('Le producteur doit être INSEE pour cet adaptateur.');return rows.map(row=>normalizeRecord(mapRow(row),indicator,source))}
