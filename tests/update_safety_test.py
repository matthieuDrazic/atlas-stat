"""Teste acquisition et conservation du dernier instantané sans réseau."""
from pathlib import Path
import tempfile,shutil,json,runpy,urllib.request
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
class Response:
    def __init__(self,payload):self.data=json.dumps(payload).encode();self.pos=0
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def read(self,*args):return self.data
with tempfile.TemporaryDirectory() as temp:
    root=Path(temp);(root/'scripts').mkdir();(root/'data/production').mkdir(parents=True)
    shutil.copy(ROOT/'scripts/update_data.py',root/'scripts/update_data.py')
    shutil.copy(ROOT/'data/catalog.json',root/'data/catalog.json')
    shutil.copy(ROOT/'data/territories.json',root/'data/territories.json')
    target=root/'data/production/worldbank.json';target.write_text('[{"lastValid":true}]')
    original=target.read_bytes()
    with patch.object(urllib.request,'urlopen',side_effect=OSError('Source temporairement indisponible')):
        try:runpy.run_path(str(root/'scripts/update_data.py'))
        except OSError:pass
        else:raise AssertionError('Erreur de source non propagée')
    assert target.read_bytes()==original,'Dernier fichier valide écrasé'
    payload=[{'pages':1,'lastupdated':'2026-01-01'},[{'countryiso3code':'FRA','country':{'value':'France'},'date':'2024','value':42}]]
    with patch.object(urllib.request,'urlopen',side_effect=lambda *args,**kwargs:Response(payload)):
        runpy.run_path(str(root/'scripts/update_data.py'))
    rows=json.loads(target.read_text());assert len(rows)==5
    assert all(r['source']['retrievedAt'] and r['status']=='available' and not r['isDemo'] for r in rows)
    successful=target.read_bytes()
    malformed=[{'pages':1},[{'countryiso3code':'FRA','country':{'value':'France'},'date':'2024','value':'invalide'}]]
    with patch.object(urllib.request,'urlopen',side_effect=lambda *args,**kwargs:Response(malformed)):
        try:runpy.run_path(str(root/'scripts/update_data.py'))
        except ValueError:pass
        else:raise AssertionError('Format malformé accepté')
    assert target.read_bytes()==successful
print('PASS : acquisition valide, métadonnées, échec réseau et format invalide préservent le dernier instantané.')
