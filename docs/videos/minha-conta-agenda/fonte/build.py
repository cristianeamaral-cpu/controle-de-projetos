h=open("v4/video.html").read().replace("__TL__",open("v4/tl.json").read())
open("v4/video_built.html","w").write(h)
