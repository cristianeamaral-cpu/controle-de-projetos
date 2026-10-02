# mesmo uso do transcreve.py, mas com Whisper small offline (sherpa-onnx), em janelas de 8 s
import sys, subprocess, numpy as np, sherpa_onnx
D='/tmp/claude-0/-home-user-controle-de-projetos/a7e4ab82-d7ae-55cd-9826-274306ef78e0/scratchpad/voices/sherpa-onnx-whisper-small/'
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=D+'small-encoder.int8.onnx',decoder=D+'small-decoder.int8.onnx',tokens=D+'small-tokens.txt',language='pt',task='transcribe',num_threads=4)
W=float(sys.argv[1]) if sys.argv[1].replace('.','').isdigit() else None
files=sys.argv[2:] if W else sys.argv[1:]; W=W or 8
for f in files:
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
    a=np.frombuffer(raw,np.int16).astype(np.float32)/32768; print('==',f)
    for i in range(0,len(a),int(W*16000)):
        s=rec.create_stream(); s.accept_waveform(16000,a[i:i+int(W*16000)]); rec.decode_stream(s)
        print(f'{i/16000:6.2f} {s.result.text.strip()}',flush=True)
