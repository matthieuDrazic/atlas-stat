"""Récupère WDI, valide tous les lots puis remplace l'instantané atomiquement.
Aucun secret nécessaire. Une seule erreur préserve le fichier précédent.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,urllib.request,os,math
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'data/catalog.json').read_text())
territories=json.loads((ROOT/'data/territories.json').read_text())
countries=[t['code'] for t in territories if len(t['code'])==3 and t['level']=='country']
retrieved=datetime.now(timezone.utc).isoformat()
year=datetime.now(timezone.utc).year
out=[]
for ind in catalog['indicators']:
    if ind['mode']!='worldbank':continue
    url='https://api.worldbank.org/v2/country/'+';'.join(countries)+'/indicator/'+ind['apiIndicator']+f'?format=json&date=2000:{year-1}&per_page=1000'
    req=urllib.request.Request(url,headers={'User-Agent':'AtlasDataCenter/1.0 public-statistics'})
    with urllib.request.urlopen(req,timeout=40) as response:payload=json.load(response)
    if not isinstance(payload,list) or len(payload)!=2 or not payload[1]:raise ValueError('Réponse WDI vide ou invalide : '+ind['id'])
    if payload[0].get('pages',1)>1:raise ValueError('Pagination requise : réduire la période.')
    source={'publisher':'Banque mondiale','originalPublisher':ind.get('originalPublisher','Consulter les métadonnées de la série WDI'),'datasetTitle':'World Development Indicators — '+ind['label'],'url':'https://data.worldbank.org/indicator/'+ind['apiIndicator'],'lastUpdate':payload[0].get('lastupdated'),'retrievedAt':retrieved,'license':'CC BY 4.0 (conditions Banque mondiale ; vérifier les exceptions du jeu)'}
    current=[]
    for raw in payload[1]:
        if raw.get('countryiso3code') not in countries:continue
        v=raw.get('value')
        if v is not None and (not isinstance(v,(int,float)) or not math.isfinite(v)):raise ValueError('Valeur WDI non numérique.')
        period=str(raw.get('date',''))
        if len(period)!=4 or not period.isdigit():raise ValueError('Année WDI invalide.')
        current.append({'datasetId':ind['id'],'indicatorId':ind['id'],'indicatorLabel':ind['label'],'theme':ind['theme'],'value':v,'unit':ind['unit'],'period':period,'geoCode':raw['countryiso3code'],'geoLabel':raw['country']['value'],'geoLevel':'country','dimensions':{'nationality':None,'countryOfBirth':None,'age':None,'sex':None,'religion':None},'source':source,'dataType':ind['dataType'],'methodologyNote':ind['methodologyNote'],'confidenceInterval':None,'status':'missing' if v is None else 'available','isDemo':False})
    if not current or not any(r['value'] is not None for r in current):raise ValueError('Aucune valeur exploitable : '+ind['id'])
    out.extend(current)
output=ROOT/'data/production/worldbank.json'
temporary=output.with_suffix('.tmp')
temporary.write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')))
os.replace(temporary,output)
print(f'{len(out)} observations mises à jour ; métadonnées conservées.')
