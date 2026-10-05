# Trilha original PSA (sintetizada, sem direitos de terceiros). 120 BPM, Lá menor.
# Estrutura casada com timeline.json (tempos em segundos): intro tensa → riser → DROP no reveal → groove → final.
import numpy as np, json, wave

SR = 48000
TL = json.load(open('timeline_cortes.json', encoding='utf-8'))
STARTS = {c['id']: c['start'] for c in TL}
TOTAL = json.load(open('cortes.json'))['total']
DROP = next((c['start'] for c in TL if c.get('drop')), TL[min(3, len(TL) - 1)]['start'])   # cena com "drop": true
CUTS = [c['start'] for c in TL[1:]]
FIM_GROOVE = TL[-1]['start'] + 4.15         # groove até ~4 s da última cena, depois acorde final
BEAT = 0.5
N = int(TOTAL * SR) + SR * 3
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)

def put(sig, t, gl=1.0, gr=None):
    gr = gl if gr is None else gr
    i = int(t * SR)
    if i >= N: return
    s = sig[: N - i]
    L[i:i + len(s)] += s * gl; R[i:i + len(s)] += s * gr

def tt(d): return np.arange(int(d * SR)) / SR

def fftfilt(x, lo=0, hi=SR / 2):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))

def saw(freq, t, nh=8, bright=None):
    out = np.zeros_like(t)
    for n in range(1, nh + 1):
        if freq * n > 16000: break
        a = 1 / n if bright is None else (1 / n) * np.clip(bright * 8 - n + 1, 0, 1)
        out += a * np.sin(2 * np.pi * freq * n * t)
    return out

# ── instrumentos
def kick():
    t = tt(0.45); f = 45 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.16) + 0.25 * rng.standard_normal(len(t)) * np.exp(-t / 0.004)

def clap():
    t = tt(0.3); n = fftfilt(rng.standard_normal(len(t)), 900, 5000)
    env = np.exp(-t / 0.09)
    for d in (0.0, 0.011, 0.022): env += 0.6 * np.exp(-np.clip(t - d, 0, None) / 0.006) * (t >= d)
    return n * env / 4

HATN = fftfilt(rng.standard_normal(int(0.3 * SR)), 7000)
def hat(d=0.035): t = tt(0.3); return HATN * np.exp(-t / d)

def pluck(m, d=0.22):
    t = tt(0.6); f = mtof(m)
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * saw(f, t, 6)) * np.exp(-t / d)

def bassnote(m, d=0.22):
    t = tt(d); env = np.minimum(1, t / 0.005) * np.exp(-t / 0.18)
    return (saw(mtof(m), t, 10) * 0.55 + np.sin(2 * np.pi * mtof(m) * t)) * env

def pad(ms, d, bright=0.6):
    t = tt(d); out = np.zeros_like(t)
    for m in ms:
        for det in (-0.12, 0.12):
            out += saw(mtof(m + det), t, 7, bright)
    env = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.4)
    return out * env / len(ms)

def impact():
    t = tt(2.5); f = 30 + 40 * np.exp(-t / 0.2)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.8)
    noise = fftfilt(rng.standard_normal(len(t)), 80, 9000) * np.exp(-t / 0.25) * 0.5
    return boom + noise

def whoosh(d=0.5):
    t = tt(d); x = t / d
    return fftfilt(rng.standard_normal(len(t)), 1500, 12000) * (np.sin(np.pi * x) ** 3) * 0.5

def riser(d):
    t = tt(d); x = t / d
    sweep = np.sin(2 * np.pi * np.cumsum(180 + 1400 * x ** 2) / SR) * 0.25
    return (fftfilt(rng.standard_normal(len(t)), 2500) * 0.6 + sweep) * x ** 2.2

# ── harmonia: Am F C G (1 acorde por compasso de 2s)
CH = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
ROOT = [45, 41, 48, 43]

# INTRO (0 → DROP): pad escuro abrindo, tique-taque (pressa), batida de coração, riser
put(pad([45, 52, 57, 60], DROP + 0.2, 0.25), 0, 0.28)
t = 0.0
while t < DROP - 0.3:
    put(hat(0.012) * 0.3, t, 0.7, 0.4)                    # tique
    if (t / BEAT) % 2 == 0: put(kick() * 0.3, t)        # coração
    t += BEAT
put(riser(3.0), DROP - 3.0, 0.9)
put(whoosh(1.2)[::-1] * 0.8, DROP - 1.2)                  # sucção reversa antes do drop

# DROP
put(impact() * 1.1, DROP)
put(pad(CH[0] + [69], 3.0, 1.0) * 0.6, DROP)

# GROOVE
bar = 0; t = DROP
while t < FIM_GROOVE - 1e-6:
    c = bar % 4
    for b in range(4):
        tb = t + b * BEAT
        put(kick() * 0.9, tb)
        if b in (1, 3): put(clap() * 1.7, tb, 0.9, 1.0)
        for s in range(4):                                # hats em 16 avos
            v = [0.5, 0.25, 0.7, 0.3][s]
            put(hat(0.03 if s != 2 else 0.12) * v * 0.75, tb + s * BEAT / 4, 0.6, 0.9)
        put(bassnote(ROOT[c] + 12 * (b % 2 == 1)) * 0.5, tb + BEAT / 2)   # baixo no contratempo
    if bar >= 1:                                          # arpejo entra 1 compasso depois do drop
        notas = [m + 12 for m in CH[c]] + [CH[c][0] + 24]
        for s in range(16):
            m = notas[[0, 1, 2, 3, 2, 1, 0, 2][s % 8]]
            ts = t + s * BEAT / 4
            p = pluck(m) * 0.24
            put(p, ts, 0.8, 0.5)
            put(p * 0.35, ts + 0.375, 0.3, 0.8)          # eco pingue-pongue
    put(pad(CH[c], 2.0, 0.55) * 0.35, t)
    bar += 1; t += 2 * BEAT * 2

# whooshes nos cortes (menos no drop, que já tem impacto)
for c in CUTS:
    if abs(c - DROP) > 0.1: put(whoosh(0.45) * 0.55, c - 0.3)

# FINAL: acorde grande + impacto
put(impact() * 0.8, FIM_GROOVE)
put(pad([45, 57, 60, 64, 69, 72], TOTAL - FIM_GROOVE + 1.5, 0.9) * 0.9, FIM_GROOVE)
put(pluck(81, 0.8) * 0.3, FIM_GROOVE); put(pluck(76, 0.8) * 0.25, FIM_GROOVE + 0.25)

# reverb (IR sintética) + master
def reverb(x, d=1.8, mix=0.18):
    ir = rng.standard_normal(int(d * SR)) * np.exp(-np.arange(int(d * SR)) / SR / 0.45)
    n = len(x) + len(ir); nf = 1 << (n - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, nf) * np.fft.rfft(ir, nf), nf)[: len(x)]
    return x + mix * y / np.max(np.abs(y)) * np.max(np.abs(x))
L = reverb(L); R = reverb(R)
st = np.stack([L, R], 1)[: int(TOTAL * SR)]
fade = int(1.5 * SR); st[-fade:] *= np.linspace(1, 0, fade)[:, None]
st = np.tanh(st / np.max(np.abs(st)) * 1.4) / np.tanh(1.4) * 0.89   # saturação leve
with wave.open('trilha.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('trilha.wav', round(TOTAL, 2), 's · drop em', DROP)
