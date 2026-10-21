"""yavnaya.py — явная формула Римана (1859) для f(x) = Σ F(x^(1/n))/n, по K нулям.

  ext/venv-pdf/bin/python -I proekty/riemann/yavnaya.py tochki K [K2 …]   — таблица в нескольких точках
  ext/venv-pdf/bin/python -I proekty/riemann/yavnaya.py risunok out.png   — лестница и приближения (PIL)

Нули кэшируются в ext/riemann/nuli.json. Li(x^ρ) считается как Ei(ρ·log x) («верно»)
и, для сравнения, как li от главного значения x^ρ («наивно»). 21.10, пробуждение 06:08."""
import sys, json, os
import mpmath as mp
mp.mp.dps = 20
KESH = "/home/diarai/diarai/ext/riemann/nuli.json"

def nuli(K):
    t = json.load(open(KESH)) if os.path.exists(KESH) else []
    while len(t) < K:
        t.append(float(mp.zetazero(len(t) + 1).imag))
    json.dump(t, open(KESH, "w"))
    return t[:K]

def prostye(n):
    s = [True] * (n + 1); s[0] = s[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            for j in range(i * i, n + 1, i): s[j] = False
    return [i for i in range(n + 1) if s[i]]

P = prostye(10000)
def F(x):  # число простых ≤ x, на скачке — полусумма (Риман, стр. 200–204)
    c = sum(1 for p in P if p < x); return c + (0.5 if any(abs(p - x) < 1e-12 for p in P) else 0)
def f_tochno(x):
    s, n = 0.0, 1
    while x ** (1.0 / n) >= 2:
        s += F(x ** (1.0 / n)) / n; n += 1
    return s

def hvost(x):  # ∫_x^∞ dt / ((t²−1) t log t)
    return mp.quad(lambda t: 1 / ((t * t - 1) * t * mp.log(t)), [x, mp.inf])

def f_K(x, t, C, naivno=False):
    L = mp.log(x); s = mp.li(x) + hvost(x) + C
    for tk in t:
        rho = mp.mpc(0.5, tk)
        if naivno:
            term = mp.ei(mp.log(mp.power(x, rho)))   # главная ветвь log(x^ρ)
        else:
            term = mp.ei(rho * L)
        s -= 2 * mp.re(term)
    return float(s)

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "tochki":
        Ks = [int(k) for k in a[1:]]
        t = nuli(max(Ks))
        C1, C2 = -mp.log(2), mp.log(mp.gamma(1.25) * (-0.5) * mp.pi ** (-0.25) * mp.zeta(0.5))
        print("x     f точно | K  Ei(-log2)  Ei(log ξ(t=0))  наивно(-log2)")
        for x in (10.5, 20.5, 30.5, 50.5, 97.5):
            for K in Ks:
                print(f"{x:5} {f_tochno(x):8.4f} | {K:3} {f_K(x, t[:K], C1):9.4f} {f_K(x, t[:K], C2):9.4f} {f_K(x, t[:K], C1, True):9.4f}")

    if a[0] == "risunok":
        from PIL import Image, ImageDraw, ImageFont
        out = a[1]; t = nuli(50); C = -mp.log(2)
        xs = [2 + 0.1 * i for i in range(581)]
        ser = {"K = 0": [f_K(x, [], C) for x in xs],
               "K = 10": [f_K(x, t[:10], C) for x in xs],
               "K = 50": [f_K(x, t[:50], C) for x in xs]}
        ex = [f_tochno(x) for x in xs]
        W, H, L, R, T, B = 1200, 700, 80, 30, 60, 70
        im = Image.new("RGB", (W, H), "#fcfcfb"); d = ImageDraw.Draw(im)
        try: fnt = ImageFont.truetype("DejaVuSans.ttf", 18); fs = ImageFont.truetype("DejaVuSans.ttf", 15)
        except Exception: fnt = fs = ImageFont.load_default()
        ymin, ymax = 0, 22
        X = lambda x: L + (x - 2) / 58 * (W - L - R)
        Yp = lambda y: H - B - (y - ymin) / (ymax - ymin) * (H - T - B)
        for y in range(0, 23, 5):
            d.line([(L, Yp(y)), (W - R, Yp(y))], fill="#e8e7e3", width=1); d.text((L - 35, Yp(y) - 9), str(y), fill="#52514e", font=fs)
        for x in range(10, 61, 10):
            d.text((X(x) - 8, H - B + 8), str(x), fill="#52514e", font=fs)
        d.line([(L, H - B), (W - R, H - B)], fill="#52514e", width=1)
        cols = {"K = 0": "#1baf7a", "K = 10": "#2a78d6", "K = 50": "#eb6834"}
        for k, ys in ser.items():
            d.line([(X(x), Yp(y)) for x, y in zip(xs, ys)], fill=cols[k], width=2)
        d.line([(X(x), Yp(y)) for x, y in zip(xs, ex)], fill="#0b0b0b", width=2)
        d.text((L, 15), "Явная формула Римана (1859): f(x) = F(x) + F(x^1/2)/2 + … и её приближения по K нулям ζ", fill="#0b0b0b", font=fnt)
        lx = L + 20; ly = T + 10
        for name, c in [("f(x) точно (лестница)", "#0b0b0b"), ("K = 0: Li(x) − log 2 + хвост", "#1baf7a"), ("K = 10 нулей", "#2a78d6"), ("K = 50 нулей", "#eb6834")]:
            d.line([(lx, ly + 9), (lx + 30, ly + 9)], fill=c, width=3); d.text((lx + 40, ly), name, fill="#0b0b0b", font=fs); ly += 24
        d.text((W // 2 - 20, H - 35), "x", fill="#52514e", font=fs)
        im.save(out); print("сохранено", out)
