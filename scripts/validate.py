"""Vérifications sans dépendance : imports, données, chemins statiques."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
for path in ROOT.rglob('*.js'):
    text=path.read_text()
    for dep in re.findall(r"(?:from\s+|import\s*)['\"]([^'\"]+)['\"]",text):
        if dep.startswith('.'):
            assert (path.parent/dep).is_file(),f'Import absent : {path} -> {dep}'
    assert 'localhost' not in text,f'URL de développement dans {path}'
for dep in re.findall(r'(?:src|href)="(\./[^"#]+)"',(ROOT/'index.html').read_text()):
    assert (ROOT/dep).is_file(),f'Asset absent : {dep}'
for path in ROOT.rglob('*.json'):
    data=json.loads(path.read_text())
    if isinstance(data,list) and data and isinstance(data[0],dict) and 'indicatorId' in data[0]:
        for row in data:
            required=['datasetId','indicatorId','indicatorLabel','theme','unit','period','geoCode','geoLabel','geoLevel','source','dataType','methodologyNote','status']
            assert all(k in row for k in required),path
            assert row['value'] is None or isinstance(row['value'],(float,int)),path
            assert row['status']=='available' or row['value'] is None,path
            assert row['source']['retrievedAt'] and row['source']['license'],path
            if not row.get('isDemo'):assert row['source']['url'].startswith('https://'),path
catalog=json.loads((ROOT/'data/catalog.json').read_text())
assert len(catalog['themes'])==14
for ind in catalog['indicators']:
    if ind.get('file'):assert (ROOT/ind['file']).is_file(),ind['file']
print('Validation OK : imports relatifs, assets, JSON, 14 thèmes, métadonnées et statuts.')
