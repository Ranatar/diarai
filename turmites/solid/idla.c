// Игрушка IDLA с полётами: из клетки, где прибавили, муравей летит по осям (направление случайно),
// длина полёта — геометрическая со средним L0 (обрыв на «поре»), пока не выйдет на белую клетку; её — в тело.
// Шаги = сумма длин полётов. ./idla L0 AREA SEED -> печать A t на удвоениях A; out.pgm
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define N 4096
static uint8_t g[N*N];
static uint64_t rs=88172645463325252ULL; static inline uint64_t rng(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
int main(int argc,char**argv){ double L0=atof(argv[1]); long AR=atol(argv[2]); rs+=atol(argv[3])*2654435761ULL;
  int c=N/2; g[(long)c*N+c]=1; long A=1, t=0, nextA=1024; int x=c,y=c; double p=1.0/L0;
  int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
  int MODE=getenv("MODE")?atoi(getenv("MODE")):0, d=0, added=0; // 0: случайное направление, остаёмся у края; 1: из центра (настоящая IDLA); 2: после прибавки разворот, дальше всегда направо; 3: всегда направо, без разворота
  while(A<AR){ if(MODE==0||MODE==1) d=(rng()>>30)&3; else if(MODE==2&&added) d=(d+2)&3; else d=(d+1)&3;
    if(MODE==1&&added){x=c;y=c;} added=0; double u=((rng()>>11)+1.0)/9007199254740993.0; if(getenv("LREL")) p=1.0/(atof(getenv("LREL"))*sqrt((double)A)+1); long len=1+(long)(log(u)/log(1-p));
    for(long i=0;i<len;i++){ x+=DX[d]; y+=DY[d]; t++; if(!g[(long)y*N+x]){ g[(long)y*N+x]=1; A++; added=1; break; } }
    if(x<5||y<5||x>N-5||y>N-5) break;
    if(A>=nextA){ printf("%ld %ld\n",A,t); nextA*=2; } }
  if(argc>4){ int minx=N,maxx=0,miny=N,maxy=0; for(int yy=0;yy<N;yy++)for(int xx=0;xx<N;xx++) if(g[(long)yy*N+xx]){if(xx<minx)minx=xx;if(xx>maxx)maxx=xx;if(yy<miny)miny=yy;if(yy>maxy)maxy=yy;}
    int S=(maxx-minx>maxy-miny?maxx-minx:maxy-miny)+1, P=400; FILE*f=fopen(argv[4],"wb"); fprintf(f,"P5\n%d %d\n255\n",P,P);
    for(int i=0;i<P;i++)for(int j=0;j<P;j++){int cnt=0,tot=0;int x0=minx+(long)j*S/P,x1=minx+(long)(j+1)*S/P,y0=miny+(long)i*S/P,y1=miny+(long)(i+1)*S/P;
      if(x1==x0)x1++; if(y1==y0)y1++; for(int yy=y0;yy<y1;yy++)for(int xx=x0;xx<x1;xx++){tot++;cnt+=g[(long)yy*N+xx];} fputc(255-255*cnt/tot,f);}
    fclose(f); fprintf(stderr,"w=%d h=%d\n",maxx-minx+1,maxy-miny+1); }
  return 0; }
