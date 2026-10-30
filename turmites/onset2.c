// Начало двойного шоссе/челнока по оси: ./onset2 RULE STEPS M
// Проход 1: STEPS шагов (или до края поля), конец — рамка; ось роста — длинная сторона рамки, полоса — поперечная координата муравья в конце.
// Проход 2: последний момент, когда поперечная координата отходила от полосы больше чем на M. Печать: rule onset ось полоса.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define N 16384
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int wc[4],tn[4],ns[4];
long run(long steps,int pass,int axis,int band,int M,int*fx,int*fy,int*bw,int*bh){
  memset(g,0,sizeof g); int x=N/2,y=N/2,d=0,s=0,minx=x,maxx=x,miny=y,maxy=y; long t,last=-1;
  for(t=0;t<steps;t++){ uint8_t*c=&g[(long)y*N+x]; int e=s*2+*c; *c=wc[e]; d=(d+tn[e])&3; s=ns[e]; x+=DX[d]; y+=DY[d];
    if(x<1||x>=N-1||y<1||y>=N-1) break;
    if(pass==1){ if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y; }
    else { int q=axis==0?y:axis==1?x:axis==2?x-y:x+y; if(abs(q-band)>M) last=t+1; } }
  if(pass==1){*fx=x;*fy=y;*bw=maxx-minx+1;*bh=maxy-miny+1; return t;}
  return last; }
int main(int argc,char**argv){ int rule=atoi(argv[1]); long steps=atol(argv[2]); int M=atoi(argv[3]);
  for(int e=0;e<4;e++){int b=(rule>>(4*e))&15;wc[e]=b&1;tn[e]=(b>>1)&3;ns[e]=(b>>3)&1;}
  int fx,fy,bw,bh; long T=run(steps,1,0,0,0,&fx,&fy,&bw,&bh);
  int axis= bw>bh ? 0 : 1; if(getenv("AX")) axis=atoi(getenv("AX")); // 0: горизонт (полоса по y), 1: вертик., 2: диагональ x-y=const, 3: x+y=const
  int band= axis==0? fy : axis==1? fx : axis==2? fx-fy : fx+fy;
  for(int i=3;i<argc+0 && i<argc;i++){ M=atoi(argv[i]); long on=run(T,2,axis,band,M,0,0,0,0);
    printf("%d onset=%ld M=%d axis=%s band=%d steps=%ld box=%dx%d\n",rule,on,M,axis==0?"horiz":axis==1?"vert":axis==2?"diag-":"diag+",band-(axis==2?0:N/2*(axis==3?2:1)),T,bw,bh); fflush(stdout);} return 0; }
