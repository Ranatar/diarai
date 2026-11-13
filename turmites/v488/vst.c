/* ./vst CODE D0 LOG2N out.pgm : в каждый момент прироста правого края — строка: три ряда полоски (y=0 восьм., y=-1 квадр., y=-2 восьм.)
   по x от -W до W, как 3 пикселя по вертикали; чёрный 0, белый посещённый 255, непосещённый 160 */
#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
int main(int argc,char**argv){ int code=atoi(argv[1]),d=atoi(argv[2]),lg=atoi(argv[3]),L=4096,C=L/2,W=320;
  int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)};
  unsigned char*f=calloc((size_t)L*L,1),*img=malloc(4*(2*W+1)*400); int x=C,y=C,Mx=x,rows=0;
  for(long long t=1;t<=(1LL<<lg)&&rows<400;t++){ size_t i=(size_t)y*L+x; int c=f[i]&1; f[i]|=2; d=(d+((x&1)?Ts[c]:To[c]))&7; f[i]^=1; x+=DX[d]; y+=DY[d];
    if(x>Mx){Mx=x; for(int k=0;k<4;k++)for(int xx=-W;xx<=W;xx++){ int yy=C-k; unsigned char v=128;
        if(k<3 && (((C+xx)^yy)&1)==0){ unsigned char q=f[(size_t)yy*L+C+xx]; v=(q&2)?((q&1)?0:255):160; }
        if(k<3 && (((C+xx)^yy)&1)==1 && xx>-W){ unsigned char q=f[(size_t)yy*L+C+xx-1]; v=(q&2)?((q&1)?0:255):160; }
        img[(size_t)(rows*4+k)*(2*W+1)+xx+W]=v; } rows++; } }
  FILE*o=fopen(argv[4],"wb"); fprintf(o,"P5 %d %d 255\n",2*W+1,rows*4); fwrite(img,1,(size_t)rows*4*(2*W+1),o); fclose(o);
}
