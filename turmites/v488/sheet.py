# лист миниатюр: python sheet.py out.png SIZE COLS a.pgm ...
import sys
from PIL import Image, ImageDraw
out,S,C=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); fs=sys.argv[4:]
R=(len(fs)+C-1)//C; W=Image.new('L',(C*(S+6),R*(S+16)),90); d=ImageDraw.Draw(W)
for k,p in enumerate(fs):
    im=Image.open(p).convert('L'); im.thumbnail((S,S),Image.LANCZOS)
    X=(k%C)*(S+6)+3; Y=(k//C)*(S+16)+14; W.paste(im,(X,Y)); d.text((X,Y-12),p.split('/')[-1].split('.')[0],fill=255)
W.save(out)
