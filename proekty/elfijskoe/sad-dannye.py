"""sad-dannye.py — данные для proekty/igry/sad-suffiksov.html: корни (слова Q.) и словообразовательные суффиксы
с глоссами из Eldamo. Пишет proekty/igry/sad-suffiksov-data.js. Списки слов подобраны вручную (19.10, вечер)."""
import re, json
P = "/home/diarai/diarai/inbox/eldamo/src/data/eldamo-data.xml"
SLOVA = ["alda", "alma", "ambar", "anar", "isil", "elen", "lómë", "aurë", "cala", "fëa", "hroa", "sanwë", "quetta",
         "lambë", "nólë", "lórë", "tuilë", "hrívë", "lairë", "yávë", "falma", "ëar", "rómen", "nuquerna", "lindë",
         "lírë", "eques", "nyárë", "tengwa", "parma", "coa", "malle", "ondo", "lassë", "orva", "losse", "silmë",
         "mírë", "nárë", "vilya", "súlë", "ilmen", "estel", "melmë", "nyérë", "alassë", "olos", "ohtar", "indis",
         "sérë", "tyaren", "henna", "tirion", "costë", "tyastië", "ingolë", "inca", "intya", "nat", "ma"]
SUF = {  # суффикс: (как присоединять, русское пояснение) — пояснения мои, по глоссам Eldamo
    "-itë": ("itë", "склонный, по природе делающий"), "-ima": ("ima", "-имый, могущий быть"),
    "-enca": ("enca", "без, лишённый"), "-inqua": ("inqua", "полный, совершенный"),
    "-unqua": ("unqua", "полный (дурного)"), "-ndil": ("ndil", "друг, бескорыстно любящий"),
    "-ndur": ("ndur", "слуга, служащий"), "-ula": ("ula", "склонный, вероятный"),
    "-llë": ("llë", "подобно, на манер"), "-matya": ("matya", "-ед, едящий"),
    "-stir": ("stir", "лицо, -ликий"), "-ië": ("ië", "-ость (отвлечённое)"),
    "-vë": ("vë", "-ость; -но (образ действия)"), "-më": ("më", "-ние (отвлечённое)"),
    "-mo": ("mo", "делатель, тот, кто"), "-tar": ("tar", "(почётное) владыка, -тель"),
    "-ndor": ("ndor", "земля, страна"), "-incë": ("incë", "маленький (уменьш.)"),
    "-on": ("on", "великий (увелич.)"), "-úmë": ("úmë", "множество, великое число"),
    "-ina": ("ina", "-ный; -нный (причастие)"), "-va": ("va", "-ов, принадлежащий"),
    "-wë": ("wë", "(древнее имя)"), "-ion": ("ion", "сын"), "-iel": ("iel", "дочь"),
    "-sta": ("sta", "край, часть"), "-tur": ("tur", "властелин"),
}
t = open(P, encoding="utf-8").read()
def bare(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()
idx = {}
for m in re.finditer(r'<word\b([^>]*)>', t):
    a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
    if a.get("l") in ("q", "mq", "nq") and a.get("gloss"):
        k = bare(a.get("v", "")).rstrip("-¹²³⁴")
        k = re.sub(r"[¹²³⁴]", "", k)
        idx.setdefault(k, []).append((a["l"], a["v"], a["gloss"]))
roots, net = [], []
for w in SLOVA:
    hits = idx.get(bare(w), [])
    hits.sort(key=lambda h: {"q": 0, "mq": 1, "nq": 2}[h[0]])
    if hits:
        l, v, g = hits[0]
        roots.append({"w": w, "l": l, "g": g})
    else:
        net.append(w)
sufs = []
for s, (j, ru) in SUF.items():
    found = [h for k, hs in idx.items() if k == bare(s) for h in hs]
    sufs.append({"s": s, "j": j, "ru": ru, "eldamo": found[0][2] if found else ""})
out = "/home/diarai/diarai/proekty/igry/sad-suffiksov-data.js"
open(out, "w", encoding="utf-8").write("const ROOTS = " + json.dumps(roots, ensure_ascii=False) +
                                       ";\nconst SUFS = " + json.dumps(sufs, ensure_ascii=False) + ";\n")
print("корней:", len(roots), "нет в Eldamo (как ключ):", net)
print("суффиксов:", len(sufs), "без глоссы:", [s["s"] for s in sufs if not s["eldamo"]])
