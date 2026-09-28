import json
d=json.load(open("v2/durs.json")); segs=json.load(open("v2/segs.json"))
T={};c=1.0
for key,_,gap,_ in segs:
    # extra room for scene transitions / on-screen actions
    extra={"intro":0.4,"c5":1.0,"p1b":0.6,"f1":0.8,"f2":0.4}.get(key,0)
    T[key]=round(c,3); c+=d[key]+gap+extra
END=round(c+3.2,2)
json.dump({"T":T,"D":d,"END":END},open("v2/tl.json","w"),indent=1); print(END)
