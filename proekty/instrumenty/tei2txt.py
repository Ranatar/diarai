"""TEI XML (EEBO-TCP) -> plain text. Usage: python3 -I tei2txt.py in.xml out.txt
Notes (<note>) are dropped; page breaks become spaces; </p> -> blank line."""
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
b = t[t.find("<text"):]
b = re.sub(r"<note[^>]*>.*?</note>", "", b, flags=re.S)
b = re.sub(r"<pb[^>]*/>", " ", b)
b = re.sub(r"</p>", "\n\n", b)
b = re.sub(r"<[^>]+>", "", b)
b = b.replace("&amp;", "&")
b = re.sub(r"[ \t]+", " ", b)
b = re.sub(r"\n\s*\n+", "\n\n", b)
open(sys.argv[2], "w", encoding="utf-8").write(b)
print(len(b.split()), "words")
