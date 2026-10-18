"""pu_razbor.py — текст «Философских исследований», ч. I (wittgensteinproject.org, через html2txt) → JSON {"§": текст}.
Параграф начинается строкой «N. …», номера идут подряд 1…693; берём только строку с ожидаемым следующим номером.
Запуск: python3 -I pu_razbor.py ext/pu/pu.txt ext/pu/pu.json"""
import sys, re, json

lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
out, cur, nxt = {}, None, 1
for ln in lines:
    m = re.match(r"\s*(\d{1,3})\.\s", ln)
    if m and int(m.group(1)) == nxt:
        cur = str(nxt); out[cur] = ln[m.end():].strip(); nxt += 1
    elif cur:
        out[cur] += " " + ln.strip()
for k in out:
    out[k] = re.sub(r"\s+", " ", out[k]).strip()
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(out), "параграфов; последний", nxt - 1)
for k in ("1", "43", "109", "133", "201", "693"):
    print(k, "|", out.get(k, "—")[:150])
