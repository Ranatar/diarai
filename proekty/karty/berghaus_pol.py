import math
D = math.pi / 180


def rotator(dl, dp, dg):  # копия rotator() из globe.html
    dl *= D; dp *= D; dg *= D
    cdp, sdp, cdg, sdg = math.cos(dp), math.sin(dp), math.cos(dg), math.sin(dg)

    def f(lon, lat):
        l = lon * D + dl
        if l > math.pi: l -= 2 * math.pi
        elif l < -math.pi: l += 2 * math.pi
        p = lat * D; cp = math.cos(p)
        x = math.cos(l) * cp; y = math.sin(l) * cp; z = math.sin(p); k = z * cdp + x * sdp
        return (math.atan2(y * cdg - k * sdg, x * cdp - z * sdp) / D,
                math.asin(max(-1, min(1, k * cdg + y * sdg))) / D)
    return f


r = rotator(0, -18, 0)
grid = [(lo, la) for lo in range(-180, 181) for la in range(-90, 91)]
best = max(grid, key=lambda q: r(*q)[1])
worst = min(grid, key=lambda q: r(*q)[1])
print("в центр звезды (phi'=90):", best, [round(v, 2) for v in r(*best)])
print("повёрнутый южный полюс:", worst)
print("точка «центра» (0,18) ->", r(0, 18))
pts = [("Богота", -74, 4.6), ("Каракас", -67, 10.5), ("Ресифи", -35, -8), ("Лима", -77, -12),
       ("Буэнос-Айрес", -58, -34.6), ("Огненная Земля", -68, -54)]
for name, lo, la in pts:
    print(name, [round(v, 1) for v in r(lo, la)])
