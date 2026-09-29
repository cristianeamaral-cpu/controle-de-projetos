#!/bin/sh
# Mixa a narração gravada (Roteiro.ogg, 1 min 44 s) com a trilha de fundo.
# Uso: sh mixar-gravacao.sh Roteiro.ogg music_loop.wav frames/ saida.mp4
REC=$1; MUSIC=$2; FRAMES=$3; OUT=$4; END=110.92
ffmpeg -y -i "$REC" -ac 1 -af "afftdn=nf=-45,highpass=f=80,lowpass=f=14000,equalizer=f=200:t=q:w=1:g=-1.5,equalizer=f=3500:t=q:w=1.2:g=1.5,deesser=i=0.3,acompressor=threshold=-22dB:ratio=2.5:attack=10:release=150,loudnorm=I=-17:TP=-2:LRA=8,adelay=480,apad=whole_dur=$END,aresample=48000,aformat=channel_layouts=stereo" voice.wav
ffmpeg -y -i voice.wav -i "$MUSIC" -filter_complex "[1:a]aresample=48000,atrim=0:$END,afade=t=in:d=0.5,afade=t=out:st=108.72:d=2.2,volume=1.25[mu];[0:a]asplit[v][sc];[mu][sc]sidechaincompress=threshold=0.03:ratio=3:attack=80:release=600[md];[v][md]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[out]" -map "[out]" mix.wav
ffmpeg -y -framerate 30 -i "$FRAMES/f%05d.jpg" -i mix.wav -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
