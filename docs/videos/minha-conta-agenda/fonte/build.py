h=open("v2/video.html").read().replace("__TL__",open("v2/tl.json").read())
open("v2/video_built.html","w").write(h)
