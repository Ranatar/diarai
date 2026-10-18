# Проверка musical-sequence-analysis(1).html: последовательность строится по формуле самой страницы:
# MIDI(n) = 30 + 5n — первая нота n-й группы, группа = [s, s+2, s+4] («Каждая группа: [0, +2, +4]»).
names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def nm(m):
    return "%s%d" % (names[m % 12], m // 12 - 1)

groups = [[30 + 5 * n + d for d in (0, 2, 4)] for n in range(1, 13)]
seq = [m for g in groups for m in g]
print("нот:", len(seq), "групп:", len(groups))
print("диапазон:", nm(seq[0]), "–", nm(seq[-1]), "=", seq[-1] - seq[0], "полутонов =", (seq[-1] - seq[0]) // 12, "окт. +", (seq[-1] - seq[0]) % 12)
steps = [b - a for a, b in zip(seq, seq[1:])]
print("шаги мелодии:", steps[:9], "… тритонов (6) в мелодии:", steps.count(6))

# «уменьшенное трезвучие»: интервалы [0,3,6]
print("интервалы внутри группы:", [g[1] - g[0] for g in groups][:3], [g[2] - g[1] for g in groups][:3], "→ уменьшенных трезвучий:", sum(1 for g in groups if (g[1] - g[0], g[2] - g[1]) == (3, 3)))

# целотоновые ряды
for i, g in enumerate(groups, 1):
    assert len({x % 2 for x in g}) == 1
print("группы в WT0 (чётные классы):", [i for i, g in enumerate(groups, 1) if g[0] % 2 == 0])

# инверсия [0,2,4] -> [0,10,8] = [8,10,0]: есть ли среди групп?
inv = sorted({(-x) % 12 for x in (0, 2, 4)})
pcsets = [sorted({x % 12 for x in g}) for g in groups]
print("инверсия как множество:", inv, "; есть среди групп:", [i for i, p in enumerate(pcsets, 1) if p == inv])

# голоса, если группа — аккорд: нижний, средний, верхний
for k, label in ((0, "нижний"), (1, "средний"), (2, "верхний")):
    v = [g[k] for g in groups]
    print(label, "голос, ходы:", sorted(set(b - a for a, b in zip(v, v[1:]))))
