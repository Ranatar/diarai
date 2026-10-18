"""Коллация редакций «Relatio fratris Aidani» с таблицей поправок автора.

python3 kollaciya.py [корень inbox] > otchet.txt

Редакции (все из inbox автора):
  H0  html-generated/relatio_aidani.html
  DEC html-generated/relatio_aidani_decorative.html
  MD  Synthesises-of-concepts/various/relatio_aidani.md
  LA  html-generated/relatio_aidani_la.html
  COD html-generated/relatio_aidani_codex.html
  SYN html-generated/relatio_aidani_synthetica.html
Для каждой поправки № 1–41 (разделы II–V; VI — особенности, а не ошибки) печатается,
в каких редакциях стоит «лекция рукописи» и в каких — предложенное исправление.
"""
import html, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "inbox"
V = {
    "H0": "html-generated/relatio_aidani.html",
    "DEC": "html-generated/relatio_aidani_decorative.html",
    "MD": "Synthesises-of-concepts/various/relatio_aidani.md",
    "LA": "html-generated/relatio_aidani_la.html",
    "COD": "html-generated/relatio_aidani_codex.html",
    "SYN": "html-generated/relatio_aidani_synthetica.html",
}


def load(p):
    t = open(os.path.join(ROOT, p), encoding="utf-8").read()
    if p.endswith(".html"):
        t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return norm(t)


def norm(s):
    s = s.replace("*", "").replace("`", "").lower()
    s = s.replace("v", "u").replace("j", "i")
    s = re.sub(r"[^a-zà-ÿì ]+", " ", s)
    return " " + re.sub(r"\s+", " ", s).strip() + " "


T = {k: load(p) for k, p in V.items()}
corr = open(os.path.join(ROOT, "Synthesises-of-concepts/various/correctiones_relatio_aidani.md"), encoding="utf-8").read()


def pieces(cell):
    """Куски ячейки, которые можно искать дословно: между многоточиями, «или», «/», скобками."""
    cell = re.sub(r"\(.*?\)", " ", cell)
    out = []
    for p in re.split(r"…|\.\.\.|/|\bили\b|;", cell):
        p = norm(p).strip()
        if len(p) >= 4 and re.search(r"[a-z]", p):
            out.append(" " + p + " ")
    return out


print("№   " + " ".join(f"{k:>4}" for k in V) + "   (L = ошибочная лекция есть, f = исправление есть, . = ни того ни другого)")
for line in corr.splitlines():
    m = re.match(r"\|\s*(\d+)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|", line)
    if not m or int(m.group(1)) > 41:
        continue
    num, lec, fix = int(m.group(1)), m.group(3), m.group(4)
    L, F = pieces(lec), pieces(fix) if num <= 32 else []
    row = []
    for k in V:
        has_l = any(p in T[k] for p in L)
        has_f = any(p in T[k] for p in F)
        row.append(("L" if has_l else "") + ("f" if has_f else "") or ".")
    print(f"{num:<3} " + " ".join(f"{c:>4}" for c in row) + "   " + re.sub(r"[*`]", "", lec).strip()[:60])
