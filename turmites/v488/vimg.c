/* ./vimg CODE D0 LOG2N L out.pgm : поле после 2^N шагов, обрезка по посещённым; пиксель на клетку удвоенной решётки:
   восьмиугольник/квадрат: белый 255, чёрный 0, непосещённый 200; прочие узлы удвоенной решётки — 128 (фон «щелей») */
#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
int main(int argc,char**argv){
  int code=atoi(argv[1]),d=atoi(argv[2]),lg=atoi(argv[3]),L=atoi(argv[4]);
  int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)};
  unsigned char*f=calloc((size_t)L*L,1); int x=L/2&~1,y=L/2&~1,mx=x,Mx=x,my=y,My=y; long long t,N=1LL<<lg;
  for(t=1;t<=N;t++){ size_t i=(size_t)y*L+x; int c=f[i]&1; f[i]|=2; d=(d+((x&1)?Ts[c]:To[c]))&7; f[i]^=1;
    x+=DX[d]; y+=DY[d]; if(x<2||y<2||x>=L-2||y>=L-2)break;
    if(x<mx)mx=x;if(x>Mx)Mx=x;if(y<my)my=y;if(y>My)My=y; }
  FILE*o=fopen(argv[5],"wb"); int W=Mx-mx+3,H=My-my+3; fprintf(o,"P5 %d %d 255\n",W,H);
  for(int yy=My+1;yy>=my-1;yy--)for(int xx=mx-1;xx<=Mx+1;xx++){ unsigned char v=128;
    if(((xx^yy)&1)==0){ unsigned char q=f[(size_t)yy*L+xx]; v=(q&2)?((q&1)?0:255):200; } fputc(v,o);}
  fclose(o); fprintf(stderr,"%d t=%lld bbox %dx%d\n",code,t-1,W,H);
}
