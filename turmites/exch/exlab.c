// ./exlab RULE MAXLOG : обменщик с помеченными жетонами.
// Каждая клетка получает номер (дом). Муравей всегда меняет свой жетон на жетон клетки.
// Проверка: цвет клетки == чётность(дом жетона) ^ чётность(клетки) (фон белый).
// На 2^k печатает: t, площадь A, доля сдвинутых жетонов, средний и макс. сдвиг,
// средний радиальный сдвиг (|дом→сейчас| по радиусу от начала), радиус рамки.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#define N 4096
#ifndef ONLYDIFF
#define ONLYDIFF 0
#endif
#ifndef SC
#define SC 4
#endif
static uint8_t g[(long)N*N];
static uint32_t id[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int ac,char**av){int r=atoi(av[1]),M=atoi(av[2]);
 int wc[4],tn[4],ns[4];
 for(int e=0;e<4;e++){int b=(r>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
 for(long i=0;i<(long)N*N;i++)id[i]=i;
 int x=N/2,y=N/2,d=0,s=0,x0=x,x1=x,y0=y,y1=y;
 // жетон в руке: в начале s=0, t=0 → σ=0; дадим ему «дом» вне поля: N*N (чётность 0)
 uint32_t hand=(uint32_t)N*N; long nt=1024;
 for(long t=1;t<=(1L<<M);t++){long p=(long)y*N+x;uint8_t*q=&g[p];
  if(!(*q&2))*q|=2;
  int e=s*2+(*q&1);*q=(*q&2)|wc[e];d=(d+tn[e])&3;s=ns[e];
  {int par(uint32_t h);int ph=(hand==(uint32_t)N*N)?0:((hand%N+hand/N)&1),pc=((id[p]%N+id[p]/N)&1);
  if(!ONLYDIFF||ph!=pc){uint32_t tmp=id[p];id[p]=hand;hand=tmp;}}
  x+=DX[d];y+=DY[d];
  if(x<1||x>=N-1||y<1||y>=N-1){printf("edge %ld\n",t);break;}
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;
  if(t==nt){nt*=2;long A=0,mv=0,bad=0;double sd=0,sr=0,mx=0,s2=0;
   for(int yy=y0;yy<=y1;yy++)for(int xx=x0;xx<=x1;xx++){long pp=(long)yy*N+xx;if(!(g[pp]&2))continue;A++;
    uint32_t h=id[pp];int hx,hy,par;
    if(h==(uint32_t)N*N){hx=N/2;hy=N/2;par=0;} else {hx=h%N;hy=h/N;par=(hx+hy)&1;}
    int c=g[pp]&1; if(c!=(par^((xx+yy)&1)))bad++;
    if(hx!=xx||hy!=yy){mv++;double dx=xx-hx,dy=yy-hy,D=sqrt(dx*dx+dy*dy);sd+=D;s2+=D*D;if(D>mx)mx=D;
     double rx=hx-N/2,ry=hy-N/2,R=sqrt(rx*rx+ry*ry);if(R>0)sr+=(dx*rx+dy*ry)/R;}}
   printf("%ld A=%ld moved=%.3f mean=%.2f max=%.0f radial=%.3f R=%d bad=%ld msd=%.2f tA=%.2f\n",t,A,(double)mv/A,mv?sd/mv:0,mx,mv?sr/mv:0,(x1-x0+y1-y0+2)/4,bad,s2/A,(double)t/A);
   fflush(stdout);}}

 {char fn[64];sprintf(fn,"lab_%d.pgm",r);FILE*f=fopen(fn,"wb");int W=x1-x0+1,H=y1-y0+1;fprintf(f,"P5 %d %d 255\n",W,H);
  for(int yy=y0;yy<=y1;yy++)for(int xx=x0;xx<=x1;xx++){long pp=(long)yy*N+xx;int v=0;
   if(g[pp]&2){uint32_t h=id[pp];int hx,hy;if(h==(uint32_t)N*N){hx=N/2;hy=N/2;}else{hx=h%N;hy=h/N;}
    double D=sqrt((double)(xx-hx)*(xx-hx)+(double)(yy-hy)*(yy-hy));v=40+(int)(D*SC);if(v>255)v=255;}
   fputc(v,f);}fclose(f);}
}
