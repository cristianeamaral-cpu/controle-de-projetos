import json
d=json.load(open("v3/durs.json")); segs=json.load(open("v3/segs.json"))
T={};c=1.0
for key,_,gap,_ in segs:
    # extra room for scene transitions / on-screen actions
    extra={"intro":0.3,"c5":0.9,"p1b":0.6,"f1":0.7,"f2":0.3}.get(key,0)
    T[key]=round(c,3); c+=d[key]+gap+extra
END=round(c+3.0,2)
json.dump({"T":T,"D":d,"END":END},open("v3/tl.json","w"),indent=1); print(END)
