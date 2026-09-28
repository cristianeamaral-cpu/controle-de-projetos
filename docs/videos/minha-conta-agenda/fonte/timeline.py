import json
d=json.load(open("durs.json"))
order=["intro","conta1","conta2","conta3","conta4","sync1","sync2","p1","p2","p3","d1","d2","d3","fim"]
gap={"intro":1.1,"conta1":0.3,"conta2":0.25,"conta3":0.3,"conta4":2.2,"sync1":0.5,"sync2":0.5,"p1":0.8,"p2":0.8,"p3":1.0,"d1":0.3,"d2":0.35,"d3":0.9,"fim":1.0}
T={};c=0.9
for k in order: T[k]=round(c,3); c+=d[k]+gap[k]
END=round(c+4.2,2)
json.dump({"T":T,"D":d,"END":END},open("tl.json","w"),indent=1); print(T,END)
