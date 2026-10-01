python3 -c "
s=open('video.src.html').read().replace('%%STARS%%',open('stars.svg.html').read());open('video.html','w').write(s)"
