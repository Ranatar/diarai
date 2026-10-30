// Игрушка: тело растёт хордами. Точка p внутри; ориентация чередуется, знак случайный; от p до первой белой e,
// e красим. Новая p = e - dir*k, k равномерно в [1, max(1, ALPHA*n)] (n — длина хорды). ALPHA=1 — точка где угодно на хорде,
// малое ALPHA — поворот у самого края. ./toy ALPHA AREA SEED out.pgm
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 8192
static uint8_t g[N*N]; static long hc[N];
static uint64_t rs=88172645463325252ULL; static inline uint64_t rng(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
int main(int argc,char**argv){ double al=atof(argv[1]); long AR=atol(argv[2]); rs+=atol(argv[3])*2654435761ULL;
  int c=N/2; for(int y=c-2;y<=c+2;y++)for(int x=c-2;x<=c+2;x++) g[(long)y*N+x]=1;
  long A0=25; int S0=getenv("INIT")?atoi(getenv("INIT")+1):0; char IT=getenv("INIT")?getenv("INIT")[0]:0; // INIT=sR квадрат |x|,|y|<=R; dR круг; rR ромб |x|+|y|<=R
  if(IT){ A0=0; for(int y=c-S0;y<=c+S0;y++)for(int x=c-S0;x<=c+S0;x++){ int dx=x-c,dy=y-c; int in= IT=='s' || (IT=='d'&&dx*dx+dy*dy<=S0*S0) || (IT=='r'&&abs(dx)+abs(dy)<=S0); if(in){g[(long)y*N+x]=1;A0++;} } }
  long H0=getenv("H0")?atol(getenv("H0")):0, FR=getenv("FR")?atol(getenv("FR")):0, nh=0; double Q=getenv("Q")?atof(getenv("Q")):0; long A=A0; int x=c,y=c,o=0,minx=c-(IT?S0:2),maxx=c+(IT?S0:2),miny=c-(IT?S0:2),maxy=c+(IT?S0:2);
  int PAR=getenv("PAR")?atoi(getenv("PAR")):0, pdx=1,pdy=0; long lastn=0;
  while(A<AR){ int sg=(rng()>>20)&1?1:-1; int dx=o?0:sg, dy=o?sg:0; o^=1;
    if(PAR){ int r=(lastn&1)^(PAR==2); if(r){dx=-pdy;dy=pdx;}else{dx=pdy;dy=-pdx;} pdx=dx;pdy=dy; }
    int ex=x,ey=y,n=0; while(g[(long)ey*N+ex]){ex+=dx;ey+=dy;n++;}
    if(H0>0 && A>=H0){ if(!dy) hc[ey]++; nh++; if(FR){ if(nh>=FR) break; goto skip; } }
    g[(long)ey*N+ex]=1; A++; lastn=n;
    skip:;
    if(ex<minx)minx=ex;if(ex>maxx)maxx=ex;if(ey<miny)miny=ey;if(ey>maxy)maxy=ey;
    if(minx<10||miny<10||maxx>N-10||maxy>N-10) break;
    if(Q>0 && ((rng()>>11)%1000000)/1e6<Q){ do{ x=minx+(int)((rng()>>11)%(maxx-minx+1)); y=miny+(int)((rng()>>11)%(maxy-miny+1)); }while(!g[(long)y*N+x]); continue; }
    if(getenv("BETA")){ double b=atof(getenv("BETA")), J=getenv("J")?atof(getenv("J")):0; double u=((rng()>>11)%1000001)/1e6*2-1;
      long k=(long)((b+J*u)*n+0.5); if(getenv("FLOOR")) k=(long)(b*n); if(getenv("CEIL")) k=n-(long)(b*n); if(getenv("RR")) k=(long)((b+J*u)*n+((rng()>>11)%1000000)/1e6); if(k<1)k=1; if(k>n)k=n; x=ex-dx*k; y=ey-dy*k; continue; }
    if(al<0){ long k=n/2; if(k<1)k=1; x=ex-dx*k; y=ey-dy*k; continue; }
    long km=(long)(al*n); if(km<1)km=1; long k=1+(long)((rng()>>11)%km); if(k>n)k=n;
    x=ex-dx*k; y=ey-dy*k; }
  if(getenv("HOUT")){ FILE*h=fopen(getenv("HOUT"),"w"); for(int yy=miny;yy<=maxy;yy++){ long w=0; for(int xx=minx;xx<=maxx;xx++) w+=g[(long)yy*N+xx]; fprintf(h,"%d %ld %ld\n",yy,hc[yy],w);} fclose(h); }
  FILE*f=fopen(argv[4],"wb"); int S=(maxx-minx>maxy-miny?maxx-minx:maxy-miny)+1, P=400;
  fprintf(f,"P5\n%d %d\n255\n",P,P);
  for(int i=0;i<P;i++)for(int j=0;j<P;j++){int cnt=0,tot=0;int x0=minx+(long)j*S/P,x1=minx+(long)(j+1)*S/P,y0=miny+(long)i*S/P,y1=miny+(long)(i+1)*S/P;
    if(x1==x0)x1++; if(y1==y0)y1++; for(int yy=y0;yy<y1;yy++)for(int xx=x0;xx<x1;xx++){tot++;cnt+=g[(long)yy*N+xx];} fputc(255-255*cnt/tot,f);}
  fclose(f); printf("alpha=%g A=%ld w=%d h=%d\n",al,A,maxx-minx+1,maxy-miny+1); return 0; }
