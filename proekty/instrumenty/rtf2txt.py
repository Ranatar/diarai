"""rtf2txt.py вход.rtf выход.txt — RTF в простой текст (без форматирования).
Разбор по известной схеме «striprtf»: группы {}, управляющие слова, \\'hh (cp1252), \\uN с пропуском \\ucN символов замены,
пропуск служебных групп (fonttbl, colortbl, stylesheet, info, pict, \\* …). 2026-10-21 (курс Фаускангера, pandoc нет)."""
import re, sys

SKIP = {"fonttbl", "colortbl", "stylesheet", "info", "pict", "header", "footer", "headerl", "headerr",
        "footerl", "footerr", "object", "datastore", "themedata", "latentstyles", "listtable",
        "listoverridetable", "rsidtbl", "generator", "xmlnstbl", "mmathPr", "filetbl", "revtbl"}
BREAK = {"par": "\n", "line": "\n", "sect": "\n\n", "page": "\n\n", "tab": "\t", "cell": " | ", "row": "\n",
         "emdash": "\u2014", "endash": "\u2013", "lquote": "\u2018", "rquote": "\u2019",
         "ldblquote": "\u201c", "rdblquote": "\u201d", "bullet": "\u2022", "emspace": " ", "enspace": " "}
TOK = re.compile(r"\\([a-z]{1,32})(-?\d{1,10})?[ ]?|\\'([0-9a-fA-F]{2})|\\([^a-z])|([{}])|[\r\n]+|(.)", re.S | re.I)

def convert(text):
    stack, ignorable, ucskip, curskip, out = [], False, 1, 0, []
    for m in TOK.finditer(text):
        word, arg, hexc, char, brace, tchar = m.groups()
        if brace:
            curskip = 0
            if brace == "{":
                stack.append((ucskip, ignorable))
            elif stack:
                ucskip, ignorable = stack.pop()
        elif char:
            curskip = 0
            if char == "~":
                if not ignorable: out.append("\xa0")
            elif char in "{}\\":
                if not ignorable: out.append(char)
            elif char == "*":
                ignorable = True
        elif word:
            curskip = 0
            w = word.lower()
            if w in SKIP:
                ignorable = True
            elif ignorable:
                pass
            elif w in BREAK:
                out.append(BREAK[w])
            elif w == "uc":
                ucskip = int(arg)
            elif w == "u":
                c = int(arg)
                if c < 0: c += 0x10000
                out.append(chr(c))
                curskip = ucskip
        elif hexc:
            if curskip > 0:
                curskip -= 1
            elif not ignorable:
                out.append(bytes([int(hexc, 16)]).decode("cp1252", errors="replace"))
        elif tchar:
            if curskip > 0:
                curskip -= 1
            elif not ignorable:
                out.append(tchar)
    return "".join(out)

if __name__ == "__main__":
    src = open(sys.argv[1], encoding="latin-1").read()
    txt = convert(src)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    open(sys.argv[2], "w", encoding="utf-8").write(txt)
    print(len(txt.split()), "слов")
