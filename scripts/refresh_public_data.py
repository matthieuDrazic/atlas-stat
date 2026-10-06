"""Petites extractions publiques : un fichier validé par base, écriture atomique.
Chaque base échoue indépendamment ; son dernier instantané est préservé.
"""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import urllib.request,urllib.parse,json,math,os,sys
ROOT=Path(__file__).resolve().parents[1]
CAT=json.loads((ROOT/'data/catalog.json').read_text())['indicators']
TERR=json.loads((ROOT/'data/territories.json').read_text())
NOW=datetime.now(timezone.utc).isoformat()
YEAR=datetime.now(timezone.utc).year

def get(url):
    request=urllib.request.Request(url,headers={'User-Agent':'AtlasDataCenter/2.0 public statistics','Accept':'application/json'})
    with urllib.request.urlopen(request,timeout=25) as response:return json.load(response)

def record(ind,t,period,value,source,dimensions=None,note=None,status=None):
    if value is not None and (not isinstance(value,(int,float)) or isinstance(value,bool) or not math.isfinite(value)):raise ValueError('Valeur numérique invalide')
    period=str(period)
    if len(period)!=4 or not period.isdigit():raise ValueError('Année invalide')
    if status=='suppressed':value=None
    return {'datasetId':ind.get('datasetId',ind['id']),'indicatorId':ind['id'],'indicatorLabel':ind['label'],'theme':ind['theme'],'value':value,'unit':ind['unit'],'period':period,'geoCode':t['code'],'geoLabel':t['label'],'geoLevel':t['level'],'dimensions':{'nationality':None,'countryOfBirth':None,'age':None,'sex':None,'religion':None,**(dimensions or {})},'source':source,'dataType':ind['dataType'],'methodologyNote':note or ind['methodologyNote'],'confidenceInterval':None,'status':status or ('missing' if value is None else 'available'),'isDemo':False}

def insee():
    ind=next(i for i in CAT if i['id']=='population-insee');base='https://api.insee.fr/melodi/'
    metadata=get(base+'catalog/'+ind['datasetId'])
    source={'publisher':'INSEE','originalPublisher':'Institut national de la statistique et des études économiques','datasetTitle':'Populations de référence','url':'https://catalogue-donnees.insee.fr/fr/catalogue/recherche/'+ind['datasetId'],'lastUpdate':metadata.get('modified'),'publishedAt':metadata.get('issued'),'retrievedAt':NOW,'license':'Licence Ouverte / Open Licence 2.0'}
    def one(t):
        params=urllib.parse.urlencode({'GEO':t['inseeGeo'],'POPREF_MEASURE':'PMUN','maxResult':50})
        payload=get(base+'data/'+ind['datasetId']+'?'+params)
        if payload.get('identifier')!=ind['datasetId'] or payload.get('paging',{}).get('next'):raise ValueError('Jeu INSEE inattendu ou paginé')
        rows=[]
        for o in payload['observations']:
            d=o['dimensions'];m=o['measures'].get('OBS_VALUE_NIVEAU',{})
            if d['POPREF_MEASURE']!='PMUN':continue
            if not (d['GEO']==t['inseeGeo'] or d['GEO'].endswith('-'+t['inseeGeo'])):raise ValueError('Territoire INSEE inattendu')
            if 'value' not in m:raise ValueError('Valeur INSEE absente')
            flag=m.get('status') or d.get('OBS_STATUS')
            rows.append(record(ind,t,d['TIME_PERIOD'],m['value'],source,{'geographyReference':d['GEO'].split('-')[0],'populationMeasure':'PMUN','sourceFlag':flag},ind['methodologyNote']+' Géographie publiée : '+d['GEO']+'.','suppressed' if flag in ['C','S'] else None))
        if not rows:raise ValueError('Population municipale absente pour '+t['label'])
        return rows
    with ThreadPoolExecutor(max_workers=4) as pool:return [r for batch in pool.map(one,[t for t in TERR if t.get('inseeGeo')]) for r in batch]

def eurostat():
    ind=next(i for i in CAT if i['id']=='chomage-eurostat');params=[('format','JSON'),('lang','FR'),*ind['apiFilters'].items(),('sinceTimePeriod','2000'),('untilTimePeriod',str(YEAR-1))]
    params.extend(('geo',v) for v in ind['eurostatGeo'].values())
    payload=get('https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/'+ind['datasetId']+'?'+urllib.parse.urlencode(params))
    if payload.get('error') or payload.get('warning') or 'id' not in payload:raise ValueError('Réponse Eurostat invalide')
    source={'publisher':'Eurostat','originalPublisher':'Instituts statistiques nationaux — enquêtes EU-LFS, harmonisation Eurostat','datasetTitle':payload['label'],'url':'https://ec.europa.eu/eurostat/databrowser/view/'+ind['datasetId']+'/default/table?lang=fr','lastUpdate':payload.get('updated'),'retrievedAt':NOW,'license':'Réutilisation des données Eurostat avec attribution — politique de la Commission européenne'}
    indices=[]
    for name in payload['id']:
        index=payload['dimension'][name]['category']['index'];indices.append(index if isinstance(index,list) else sorted(index,key=index.get))
    count=math.prod(payload['size']);reverse={v:k for k,v in ind['eurostatGeo'].items()};rows=[]
    for flat in range(count):
        offset=flat;c={}
        for d in range(len(payload['id'])-1,-1,-1):c[payload['id'][d]]=indices[d][offset%payload['size'][d]];offset//=payload['size'][d]
        if any(c[k]!=v for k,v in ind['apiFilters'].items()):raise ValueError('Filtre Eurostat inattendu')
        t=next(t for t in TERR if t['code']==reverse[c['geo']]);value=payload.get('value',{}).get(str(flat));flag=payload.get('status',{}).get(str(flat))
        note=ind['methodologyNote']+((' Code de qualité Eurostat : '+flag+'.') if flag else '')
        rows.append(record(ind,t,c['time'],value,source,{'age':'15–74 ans','sex':'Tous','population':'Population active','sourceFlag':flag},note,'suppressed' if flag=='c' else None))
    return rows

def worldbank():
    countries=[t for t in TERR if t['level']=='country' and len(t['code'])==3]
    def one(ind):
        url='https://api.worldbank.org/v2/country/'+';'.join(t['code'] for t in countries)+'/indicator/'+ind['apiIndicator']+f'?format=json&date=2000:{YEAR-1}&per_page=1000'
        p=get(url)
        if not isinstance(p,list) or len(p)!=2 or not p[1] or p[0].get('pages',1)>1:raise ValueError('Réponse WDI invalide : '+ind['id'])
        source={'publisher':'Banque mondiale','originalPublisher':ind.get('originalPublisher','Consulter les métadonnées de la série WDI'),'datasetTitle':'World Development Indicators — '+ind['label'],'url':'https://data.worldbank.org/indicator/'+ind['apiIndicator'],'lastUpdate':p[0].get('lastupdated'),'retrievedAt':NOW,'license':'CC BY 4.0 ; vérifier les conditions du jeu et de ses producteurs initiaux'}
        rows=[]
        for raw in p[1]:
            t=next((t for t in countries if t['code']==raw.get('countryiso3code')),None)
            if t:rows.append(record(ind,t,raw['date'],raw['value'],source))
        if not any(r['value'] is not None for r in rows):raise ValueError('WDI sans valeur : '+ind['id'])
        return rows
    with ThreadPoolExecutor(max_workers=3) as pool:return [r for batch in pool.map(one,[i for i in CAT if i['mode']=='worldbank']) for r in batch]

def atomic(path,value):
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(value,ensure_ascii=False,separators=(',',':'))+'\n');os.replace(temp,path)

def main():
    status_path=ROOT/'data/source-status.json'
    status=json.loads(status_path.read_text()) if status_path.exists() else {}
    failed=[]
    for provider,collect in [('insee',insee),('eurostat',eurostat),('worldbank',worldbank)]:
        try:
            rows=collect()
            if not rows or not any(r['value'] is not None for r in rows):raise ValueError('Aucune observation exploitable')
            if len(rows)>5000:raise ValueError('Extraction trop volumineuse')
            keys=[json.dumps([r['indicatorId'],r['geoCode'],r['period'],r['dimensions']],sort_keys=True) for r in rows]
            if len(keys)!=len(set(keys)):raise ValueError('Doublons d’observations')
            atomic(ROOT/f'data/production/{provider}.json',rows)
            status[provider]={'count':len(rows),'retrievedAt':NOW,'lastUpdate':max(str(r['source'].get('lastUpdate') or '') for r in rows),'periods':sorted(set(r['period'] for r in rows)),'lastAttempt':NOW,'lastAttemptStatus':'success'}
            print(provider+': '+str(len(rows))+' observations réelles validées')
        except Exception as error:
            failed.append(provider);status.setdefault(provider,{}).update({'lastAttempt':NOW,'lastAttemptStatus':'error','error':str(error)})
            print(provider+': dernière copie conservée ; '+str(error),file=sys.stderr)
    atomic(status_path,status)
    # Les autres bases valides restent utilisables ; le statut signale l’échec partiel.
    if len(failed)==3:raise SystemExit(1)
if __name__=='__main__':main()
