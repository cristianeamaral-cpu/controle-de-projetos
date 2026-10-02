# Converte o timeline.json do kit (gerado por tts.py, voz pt-BR-AntonioNeural) para o formato do vídeo
# (../timeline.json), mantendo os tempos reais de cada palavra (WordBoundary) para sincronizar as animações.
import json, os
D = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(D, 'timeline.json'), encoding='utf-8'))
sc = [{'id': c['id'], 'start': c['start'], 'dur': c['dur'], 'voStart': c['voStart'], 'voDur': c['audio'],
       'vo': c['vo'], 'words': c.get('words', [])} for c in K]
tl = {'total': round(K[-1]['start'] + K[-1]['dur'], 3), 'scenes': sc, 'voz': 'kit'}
json.dump(tl, open(os.path.join(D, '..', 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
print('timeline.json (kit) total', tl['total'])
