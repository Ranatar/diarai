import sys
lines = [l.rstrip("\n") for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
author = [l.rstrip("\n") for l in open(sys.argv[2], encoding="utf-8") if l.strip()]
out = ["# Aurë rúsëo — Dies irae по-квенийски целиком", "",
       "*Строфы I–XVII — мой черновик (`dies-irae-1.md`, там разбор каждого слова). XVIII–XIX — Lacrimosa и Pie Iesu автора, из `hello_there` (20.10), без изменений. Собрано скриптом.*", ""]
for i in range(0, len(lines), 3):
    out.append("**%s.**  " % ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII","XIV","XV","XVI","XVII"][i // 3])
    out += [l + "  " for l in lines[i:i + 3]]
    out.append("")
out.append("**XVIII–XIX** (автор)  ")
out += [l.strip() + "  " for l in author]
open(sys.argv[3], "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(lines) // 3, "строф моих,", len(author), "строк автора")
