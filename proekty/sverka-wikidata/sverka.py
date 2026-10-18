"""Сверка графа ΦilosΦaira (связи проставлены языковыми моделями, автор отбирал)
с Wikidata P737 «находился под влиянием» (проставлено людьми, CC0).

    python3 sverka.py  > otchet.txt

Сравнение на уровне пар философов: связь концепций A и B разных философов
считается связью философов {A, B}. В Wikidata пара есть, если у одного из двух
в P737 стоит другой.
"""
import collections
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
DATA = os.path.join(ROOT, "inbox", "philosphaira", "app", "data")
WD = os.path.join(ROOT, "ext", "wikidata-p737.json")


def load(name):
    return json.load(open(os.path.join(DATA, name), encoding="utf-8"))


phil = {p["id"]: p for p in load("philosophers.json")}
conc = {c["id"]: c for c in load("concepts.json")}
rels = load("relations.json")
rtypes = {t["id"]: t for t in load("relationTypes.json")}
wd = json.load(open(WD, encoding="utf-8"))

# --- проверка сопоставления по году рождения
q2p = {v["qid"]: k for k, v in wd.items()}
bad = []
for k, v in wd.items():
    b = phil[k]["birth"]
    if v["birth"] and min(abs(b - x) for x in v["birth"]) > (15 if b < 1000 else 2):
        bad.append((k, b, v["birth"]))
print("Сопоставление: 100 из 100 найдено в Wikidata; расхождения по году рождения:", bad or "нет")

# --- Wikidata: направленные пары (кто -> на кого повлиял), только внутри сотни
W = set()
for k, v in wd.items():
    for q in v["influenced_by"]:
        if q in q2p and q2p[q] != k:
            W.add((q2p[q], k))
Wu = {frozenset(p) for p in W}
n_infl = sum(1 for v in wd.values() if v["influenced_by"])
print("У скольких из 100 вообще заполнено P737:", n_infl)
print("Пар влияния внутри сотни (направленных):", len(W), " неупорядоченных:", len(Wu))
late = [(a, b) for a, b in W if phil[a]["birth"] > phil[b]["birth"] + 5]
print("Из них «влияние младшего на старшего» (ошибки или ученики-учителя):", late[:10])

# --- граф: пары философов по связям концепций
G = collections.defaultdict(lambda: collections.Counter())
Gw = collections.Counter()
for r in rels:
    a, b = conc.get(r["source"]), conc.get(r["target"])
    if not a or not b or a["philosopher"] == b["philosopher"]:
        continue
    pair = frozenset((a["philosopher"], b["philosopher"]))
    G[pair][r["type"]] += 1
    Gw[pair] += r.get("weight", 1)
G = dict(G)  # заморозить: defaultdict молча добавлял бы пары при чтении
print("\nСвязей всего:", len(rels), " межфилософских пар в графе:", len(G))

pids = sorted(phil)
allpairs = [frozenset((a, b)) for i, a in enumerate(pids) for b in pids[i + 1:]]
base = len(Wu) / len(allpairs)
print("Всего пар философов:", len(allpairs), " доля пар с влиянием по Wikidata: %.3f" % base)

inG = [p for p in allpairs if p in G]
hitG = sum(p in Wu for p in inG)
print("\n1) Пары, связанные в графе: %d; из них есть в Wikidata: %d (%.1f%%), подъём над случаем ×%.1f"
      % (len(inG), hitG, 100 * hitG / len(inG), hitG / len(inG) / base))
print("2) Пары влияния из Wikidata: %d; из них связаны в графе: %d (%.1f%%)"
      % (len(Wu), sum(p in G for p in Wu), 100 * sum(p in G for p in Wu) / len(Wu)))
notG = [p for p in allpairs if p not in G]
print("   для сравнения: среди несвязанных в графе пар влияние по Wikidata у %.1f%%"
      % (100 * sum(p in Wu for p in notG) / len(notG)))


# --- по типам связей
def layer(t):
    return rtypes.get(t, {}).get("layer", "?")


print("\n3) По типам связи (пара засчитывается типу, если у неё есть хоть одна связь этого типа):")
print("   %-24s %-10s %6s %8s %7s" % ("тип", "слой", "пар", "в WD", "подъём"))
rows = []
for t in rtypes:
    ps = [p for p in G if G[p][t]]
    if not ps:
        continue
    h = sum(p in Wu for p in ps)
    rows.append((h / len(ps) / base, t, len(ps), h))
for lift, t, n, h in sorted(rows, reverse=True):
    print("   %-24s %-10s %6d %7.1f%% %6.1f" % (t, layer(t), n, 100 * h / n, lift))


# --- сила связи и AUC
def auc(scores, labels):
    pos = [s for s, l in zip(scores, labels) if l]
    neg = [s for s, l in zip(scores, labels) if not l]
    if not pos or not neg:
        return float("nan")
    random.seed(0)
    k, tot = 0.0, 0
    for _ in range(200000):
        a, b = random.choice(pos), random.choice(neg)
        k += 1 if a > b else 0.5 if a == b else 0
        tot += 1
    return k / tot


lab = [p in Wu for p in allpairs]
print("\n4) AUC (насколько суммарный вес связей пары в графе отличает пары с влиянием по Wikidata):")
print("   по всем парам: %.3f   только среди связанных в графе: %.3f"
      % (auc([Gw[p] for p in allpairs], lab), auc([Gw[p] for p in inG], [p in Wu for p in inG])))
hist = lambda p: sum(c for t, c in G.get(p, {}).items() if layer(t) in ("historical", "both"))
logi = lambda p: sum(c for t, c in G.get(p, {}).items() if layer(t) == "logical")
typo = lambda p: sum(c for t, c in G.get(p, {}).items() if layer(t) == "typological")
for name, f in (("исторический слой", hist), ("логический слой", logi), ("типологический слой", typo)):
    print("   %-20s AUC по всем парам: %.3f" % (name, auc([f(p) for p in allpairs], lab)))


# --- школа: внутри традиции и поперёк
def same(p):
    a, b = tuple(p)
    return bool(set(phil[a]["traditions"]) & set(phil[b]["traditions"]))


print("\n5) Внутри традиции и поперёк:")
for nm, cond in (("общая традиция", same), ("разные традиции", lambda p: not same(p))):
    ap = [p for p in allpairs if cond(p)]
    g = [p for p in ap if p in G]
    w = [p for p in ap if p in Wu]
    print("   %-16s пар %4d | в графе %4d, из них в WD %5.1f%% | в WD %3d, из них в графе %5.1f%%"
          % (nm, len(ap), len(g), 100 * sum(p in Wu for p in g) / max(1, len(g)),
             len(w), 100 * sum(p in G for p in w) / max(1, len(w))))


# --- расхождения
def nm(p):
    return " — ".join(sorted(phil[x]["nameRu"] for x in p))


print("\n6) Влияние по Wikidata, а в графе связи нет:")
for a, b in sorted(W, key=lambda x: (phil[x[0]]["birth"], phil[x[1]]["birth"])):
    if frozenset((a, b)) not in G:
        print("   %s → %s" % (phil[a]["nameRu"], phil[b]["nameRu"]))
print("\n7) Самые сильные пары графа, которых нет в Wikidata (вес; типы):")
for p in [p for p in sorted(G, key=lambda p: -Gw[p]) if p not in Wu][:30]:
    print("   %-40s %3d  %s" % (nm(p), Gw[p], dict(G[p].most_common(3))))

# --- направление: в графе у «прямых» типов источник раньше цели?
print("\n8) Направление связей между философами (источник родился раньше цели):")
for t in rtypes:
    n = k = 0
    for r in rels:
        if r["type"] != t:
            continue
        a, b = conc.get(r["source"]), conc.get(r["target"])
        if not a or not b or a["philosopher"] == b["philosopher"]:
            continue
        n += 1
        k += phil[a["philosopher"]]["birth"] < phil[b["philosopher"]]["birth"]
    if n:
        print("   %-24s %-14s %4d связей, источник старше в %5.1f%%"
              % (t, rtypes[t].get("temporal"), n, 100 * k / n))
