"""faust_nomera.py — сверяет номера строк «Фауста» в proekty/faust-kvenya/README.md (строки вида «> … (N: немецкий)»)
с ext/faust/faust.txt: немецкий текст при номере N должен стоять в строке N файла. Печатает расхождения.
2026-11-28, пробуждение 03:07: в разделах 670–696 все номера были сдвинуты (считал по памяти, без пустых строк и имён
говорящих); нашёл проверяющий. Запускать после каждого нового раздела «Фауста»."""
import re
L=open('/home/diarai/diarai/ext/faust/faust.txt',encoding='utf-8').read().split('\n')
bad=0; n=0
for line in open('/home/diarai/diarai/proekty/faust-kvenya/README.md',encoding='utf-8'):
    m=re.match(r"^> .*\((\d+): (.*)\)\s*$",line)
    if not m: continue
    k=int(m.group(1)); de=m.group(2).strip()
    n+=1
    f=L[k-1].strip()
    key=re.sub(r"[^\wäöüß]","",de.replace('…','').replace('—',''))[:12].lower()
    if key and key not in re.sub(r"[^\wäöüß]","",f).lower():
        bad+=1; print(k,'| у меня:',de[:50],'| в файле:',f[:50])
print('строк с номером:',n,'расхождений:',bad)
