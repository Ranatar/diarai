"""most.py — чтение абзацев HWPh, на которые «мост» ΦilosΦaira ↔ HWPh (inbox/hwph-xml/bridge) ссылается как на
«названы вместе». Автор моста сам пишет: «совместное упоминание ещё не утверждение о влиянии… sourced только после того,
как абзац прочитан». Этот скрипт достаёт абзацы, чтобы их прочитать.

  python3 -I proekty/most/most.py --vyborka N ЗЕРНО     — случайные N связей «hwph_together» без provenance
  python3 -I proekty/most/most.py rel_xxx [макс_знаков]  — связь, её описание и все абзацы/примечания статьи, где названы оба

Страницы статей — из собранной читалки ext/hwph-site/pages/<id>.html (proekty/instrumenty/hwph/sborka.sh).
2026-10-19, пробуждение 00:08."""
import json, re, sys, random, html

R = "/home/diarai/diarai/"
EV = json.load(open(R + "inbox/hwph-xml/bridge_out/relations_evidence.json"))
REL = {r["id"]: r for r in json.load(open(R + "inbox/philosphaira/app/data/relations.json"))}
CON = json.load(open(R + "inbox/hwph-xml/bridge_out/concepts_hwph.json"))
PH = json.load(open(R + "inbox/hwph-xml/bridge_out/philosophers_hwph.json"))


def kandidaty():
    return [e for e in EV if e.get("verdict") == "hwph_together" and not REL[e["id"]].get("provenance")]


def imena(pid):
    out = []
    for n in PH[pid]["hwph_names"]:
        fam = n.split()[-1]  # «I. Kant» → «Kant»
        out.append(fam)
    return out


def abzacy(art):
    t = open(R + "ext/hwph-site/pages/%d.html" % art, encoding="utf-8").read()
    t = t.split("<article", 1)[1]
    ps = re.findall(r"<(p|li)[^>]*>(.*?)</\1>", t, flags=re.S)
    res = []
    for tag, body in ps:
        s = re.sub(r"<[^>]+>", "", body)
        res.append(html.unescape(re.sub(r"\s+", " ", s)).strip())
    return res


def pokazat(rid, maks):
    e = next(x for x in EV if x["id"] == rid)
    r = REL[rid]
    print("СВЯЗЬ %s: %s (%s) —%s→ %s (%s)" % (rid, CON[r["source"]]["label"], PH[e["src_phil"]]["nameRu"], r["type"],
                                           CON[r["target"]]["label"], PH[e["tgt_phil"]]["nameRu"]))
    print("ОПИСАНИЕ:", r.get("description", ""))
    a, b = imena(e["src_phil"]), imena(e["tgt_phil"])
    for ev in e["evidence"]:
        print("--", ev["cite"], "абз./прим. вместе:", ev["paragraphs_together"], ev["notes_together"])
        n = 0
        for i, p in enumerate(abzacy(ev["article"])):
            pl = p.lower()   # HWPh набирает имена капителью: «THOMAS VON AQUIN»; 00:08 — без lower() Фома не находился
            if any(x.lower() in pl for x in a) and any(x.lower() in pl for x in b):
                n += 1
                print("  [%d] %s%s" % (i, p[:maks], " …" if len(p) > maks else ""))
        print("  (найдено абзацев с обоими: %d)" % n)


def iskat(rid, rx):
    """Все предложения статей-свидетельств связи, где есть регулярка rx (проверить, говорит ли статья о второй концепции)."""
    e = next(x for x in EV if x["id"] == rid)
    for ev in e["evidence"]:
        print("--", ev["cite"], "статья", ev["article"])
        for i, p in enumerate(abzacy(ev["article"])):
            for s in re.split(r"(?<=[.;!?»])\s+", p):
                if re.search(rx, s):
                    print("  [%d] %s" % (i, s[:400]))


args = sys.argv[1:]
if args and args[0] == "--abz":   # most.py --abz статья i [j …] — абзацы целиком
    ps = abzacy(int(args[1]))
    for i in args[2:]:
        print("[%s] %s\n" % (i, ps[int(i)]))
elif args and args[0] == "--iskat":   # most.py --iskat rel_xxx 'Idee|Eidos'
    iskat(args[1], args[2])
elif args and args[0] == "--vyborka":
    k = kandidaty()
    random.seed(int(args[2]))
    for e in random.sample(k, int(args[1])):
        r = REL[e["id"]]
        print(e["id"], r["type"], CON[r["source"]]["label"], "→", CON[r["target"]]["label"], "|", e["evidence"][0]["cite"])
    print("из", len(k))
else:
    pokazat(args[0], int(args[1]) if len(args) > 1 else 1500)
