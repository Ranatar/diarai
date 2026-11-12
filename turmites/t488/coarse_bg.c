/* Муравей на круговых развязках (4.8.8 = квадратная решётка узлов, в узле кольцо из 4 вершин, 4 бита).
   ./coarse RULE TAU0 SIG0 LOG2N [L]
   RULE — 8 цифр 'we' для (τ,c)=00,01,10,11 (см. intrinsic.py). Вершина k узла смотрит ребром наружу в сторону k (0N 1E 2S 3W),
   по часовой: k -> k+1. Печатает на 2^j: число чёрных вершин, число посещённых узлов. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,char**argv){
  const char*R=argv[1]; int tau=atoi(argv[2]), sig=atoi(argv[3]); int lg=atoi(argv[4]);
  int L=argc>5?atoi(argv[5]):4096;
  int W[2][2],Ex[2][2];
  for(int i=0;i<4;i++){W[i>>1][i&1]=R[2*i]-'0';Ex[i>>1][i&1]=R[2*i+1]-'0';}
  unsigned char*f=calloc((size_t)L*L,1); if(getenv("BG")) for(size_t i=0;i<(size_t)L*L;i++) f[i]=15; long long bgb=getenv("BG")?1:0;
  int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
  int X=L/2,Y=L/2,k=0; long long black=0,nodes=1; f[(size_t)Y*L+X]|=16;
  if(sig==0) sig=1;
  long long N=1LL<<lg; int nextp=1;
  for(long long t=1;t<=N;t++){
    unsigned char*p=&f[(size_t)Y*L+X];
    int c=(*p>>k)&1, w=W[tau][c], e=Ex[tau][c];
    if(w!=c){ *p^=1<<k; black+= w?1:-1; }
    int oct=0;
    if(tau==0){ if(e==0) oct=1; else { sig=(e==1)?1:-1; } }
    else { if(e==2) oct=1; else if(e==0) sig=-sig; }
    if(oct){ X+=DX[k]; Y+=DY[k]; k=(k+2)&3; tau=0;
      if(X<1||Y<1||X>=L-1||Y>=L-1){printf("край на t=%lld\n",t);break;}
      unsigned char*q=&f[(size_t)Y*L+X]; if(!(*q&16)){*q|=16;nodes++;} }
    else { k=(k+sig)&3; tau=1; }
    if(t==((long long)1<<nextp)){ printf("%d %lld %lld\n",nextp,black,nodes); nextp++; }
  }
  return 0;
}
