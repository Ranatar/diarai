# монтаж pgm в одну картинку с подписями: python montage.py out.png a.pgm b.pgm ...
import sys
from PIL import Image, ImageDraw
ims=[]
for p in sys.argv[2:]:
    im=Image.open(p).convert('L'); im.thumbnail((300,300)) if max(im.size)>300 else None
    if max(im.size)<150: s=150//max(im.size)+1; im=im.resize((im.size[0]*s,im.size[1]*s),Image.NEAREST)
    ims.append((p.split('/')[-1].split('.')[0],im))
n=len(ims); cols=min(n,4); rows=(n+cols-1)//cols
W=Image.new('L',(cols*310,rows*325),90); d=ImageDraw.Draw(W)
for k,(name,im) in enumerate(ims):
    X=(k%cols)*310+5; Y=(k//cols)*325+20; W.paste(im,(X,Y)); d.text((X,Y-15),name,fill=255)
W.save(sys.argv[1])
