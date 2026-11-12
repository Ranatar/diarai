/* Перепись муравьёв на манхэттенской разметке: тип ребра: линия x=k+1/2 — тип k&1; линия y=m+1/2 — тип (m+1)&1.
   Правило: для (τ,c) — запись w и поворот t (0N 1R 2U 3L); 4096 правил, код = Σ (w*4+t)<<(3*(2τ+c)).
   Старт: τ=0 (как будто пришли по ребру типа 0, смотрим на север), всё белое.
   ./mcensus LOG2N L [from to] -> code n(N/16) n(N/4) n(N) black edge entropy(2x2) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  int lg=atoi(argv[1]),L=atoi(argv[2]); int from=argc>3?atoi(argv[3]):0,to=argc>4?atoi(argv[4]):4096;
  unsigned char*f=malloc((size_t)L*L);
  for(int code=from;code<to;code++){
    int W[4],T[4]; for(int e=0;e<4;e++){int v=(code>>(3*e))&7; W[e]=v>>2; T[e]=v&3;}
    memset(f,0,(size_t)L*L);
    int x=L/2,y=L/2,d=0,tau=0; long long N=1LL<<lg,n1=0,n2=0,cells=0,black=0,edge=-1,t;
    for(t=1;t<=N;t++){
      size_t i=(size_t)y*L+x; int c=f[i]&1; if(!(f[i]&2)){f[i]|=2;cells++;}
      int e=2*tau+c; if(W[e]!=c){f[i]^=1; black+=W[e]?1:-1;}
      d=(d+T[e])&3; int nx=x+DX[d],ny=y+DY[d];
      if(d&1) tau=(nx<x?nx:x)&1; else tau=((ny<y?ny:y)+1)&1;
      x=nx;y=ny; if(x<1||y<1||x>=L-1||y>=L-1){edge=t;break;}
      if(t==(N>>4))n1=cells; if(t==(N>>2))n2=cells;
    }
    printf("%d %lld %lld %lld %lld %lld\n",code,n1,n2,cells,black,edge); fflush(stdout);
  }
}
