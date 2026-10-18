"""list_hrono.py папка out_prefix [столбцов] [размер] [на лист]
Листы картинок ChatGPT из корня папки (без подпапок) в хронологическом порядке по имени
«ChatGPT Image 17 мая 2026 г., 13_43_31 (1).png». На каждой плитке номер; рядом пишется
out_prefix-spisok.txt: номер, дата-время, имя файла. Нераспознанные имена идут в конец."""
import os, re, sys
from PIL import Image, ImageDraw

MES = {"янв": 1, "февр": 2, "мар": 3, "апр": 4, "мая": 5, "июн": 6, "июл": 7, "авг": 8,
       "сент": 9, "окт": 10, "нояб": 11, "дек": 12}
RX = re.compile(r"(\d{1,2})[ _]([а-я]+)\.?[ _](\d{4})[ _]г?\.?,?[ _]*(\d\d)_(\d\d)_(\d\d)(?: \((\d)\))?")

def key(f):
    m = RX.search(f)
    if not m or m.group(2) not in MES:
        return (9999, 0, 0, 0, 0, 0, 0, f)
    d, mo, y, H, M, S, k = m.groups()
    return (int(y), MES[mo], int(d), int(H), int(M), int(S), int(k or 0), f)

src, pref = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 8
S = int(sys.argv[4]) if len(sys.argv) > 4 else 160
per = int(sys.argv[5]) if len(sys.argv) > 5 else 48
files = sorted((f for f in os.listdir(src) if f.lower().endswith((".png", ".jpg", ".jpeg"))
                and os.path.isfile(os.path.join(src, f))), key=key)
with open(pref + "-spisok.txt", "w", encoding="utf-8") as out:
    for i, f in enumerate(files):
        k = key(f)
        when = "%04d-%02d-%02d %02d:%02d" % k[:5] if k[0] != 9999 else "????"
        out.write("%03d\t%s\t%s\n" % (i, when, f))
for s in range(0, len(files), per):
    chunk = files[s:s + per]
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * S, rows * S), (20, 20, 20))
    dr = ImageDraw.Draw(sheet)
    for n, f in enumerate(chunk):
        x, y = (n % cols) * S, (n // cols) * S
        try:
            im = Image.open(os.path.join(src, f)).convert("RGB")
            im.thumbnail((S - 4, S - 4))
            sheet.paste(im, (x + (S - im.width) // 2, y + (S - im.height) // 2))
        except Exception:
            pass
        dr.rectangle([x, y, x + 30, y + 13], fill=(0, 0, 0))
        dr.text((x + 2, y + 1), "%03d" % (s + n), fill=(255, 255, 0))
    sheet.save("%s-%02d.png" % (pref, s // per))
print(len(files), "картинок,", (len(files) + per - 1) // per, "листов")
