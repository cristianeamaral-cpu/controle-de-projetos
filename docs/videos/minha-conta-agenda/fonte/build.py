import json
h=open("video.html").read().replace("__TL__",open("tl.json").read())
open("video_built.html","w").write(h)
