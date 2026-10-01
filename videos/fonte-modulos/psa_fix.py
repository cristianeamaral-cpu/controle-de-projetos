# Pronúncia brasileira para "PSA" e "Ecossistema" (ajuste fonético antes da síntese Kokoro).
import re
RULES=[
 (r"p[ˈˌ]?e [ˈˌ]?ɛsj [ˈˌ]?a", "pˌe ˌɛsi ˈa"),          # "pê ésse á"  (antes: "pê éssy á")
 (r"[ˈˌ]?ekosist[ˈˌ]?emæ",   "ˌekosistˈẽmɐ"),          # "ecossistêma" (ê nasal, como no Brasil)
 (r"s[ˈˌ]?e [ˈˌ]?ɛxi [ˈˌ]?ɛmy", "sˌe ˌɛxi ˈẽmi"),      # "cê érre ême" (CRM)
]
def fix(ph):
    for a,b in RULES: ph=re.sub(a,b,ph)
    return ph
def create(k,text,**kw):
    ph=fix(k.tokenizer.phonemize(text,'pt-br'))
    return k.create(ph,is_phonemes=True,**kw)
