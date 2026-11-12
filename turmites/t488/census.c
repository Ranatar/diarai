/* Перепись муравьёв на развязках: все 6^4 правил, старты τ0=0 и τ0=1 (σ=+1).
   ./census LOG2N L > census.txt : rule tau0 узлы(2^(n-4)) узлы(2^(n-2)) узлы(2^n) чёрные(2^n) край_t период? */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  int lg=atoi(argv[1]), L=atoi(argv[2]);
  unsigned char*f=malloc((size_t)L*L);
  for(int code=0;code<1296;code++){
    int W[2][2],Ex[2][2],cc=code; char R[9];
    for(int i=0;i<4;i++){int v=cc%6;cc/=6;W[i>>1][i&1]=v/3;Ex[i>>1][i&1]=v%3;R[2*i]='0'+v/3;R[2*i+1]='0'+v%3;}
    R[8]=0;
    for(int t0=0;t0<2;t0++){
      memset(f,0,(size_t)L*L);
      int X=L/2,Y=L/2,k=0,tau=t0,sig=1; long long black=0,nodes=1,edge=-1; f[(size_t)Y*L+X]|=16;
      long long N=1LL<<lg, n1=-1,n2=-1;
      long long t;
      for(t=1;t<=N;t++){
        unsigned char*p=&f[(size_t)Y*L+X];
        int c=(*p>>k)&1, w=W[tau][c], e=Ex[tau][c];
        if(w!=c){ *p^=1<<k; black+= w?1:-1; }
        int oct=0;
        if(tau==0){ if(e==0) oct=1; else sig=(e==1)?1:-1; }
        else { if(e==2) oct=1; else if(e==0) sig=-sig; }
        if(oct){ X+=DX[k]; Y+=DY[k]; k=(k+2)&3; tau=0;
          if(X<1||Y<1||X>=L-1||Y>=L-1){edge=t;break;}
          unsigned char*q=&f[(size_t)Y*L+X]; if(!(*q&16)){*q|=16;nodes++;} }
        else { k=(k+sig)&3; tau=1; }
        if(t==(N>>4)) n1=nodes; if(t==(N>>2)) n2=nodes;
      }
      printf("%s %d %lld %lld %lld %lld %lld\n",R,t0,n1,n2,nodes,black,edge);
    }
    fflush(stdout);
  }
}
