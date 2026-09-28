h=open("v3/video.html").read().replace("__TL__",open("v3/tl.json").read())
open("v3/video_built.html","w").write(h)
