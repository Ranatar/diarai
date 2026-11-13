/* Начало шоссе у вантов 4.8.8: ./vonset LOG2N L D0 < codes  -> code edge_t period onset dx dy cells
   Записывает (d,c) на каждом шаге; у края ищет наименьший период P≤PMAX, при котором последние 4P шагов периодичны,
   и идёт назад, пока s[t]==s[t+P]: onset — первый шаг периодического движения (точно до шага).
   Если края нет: edge=-1, period=-1. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define PMAX 100000
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
int main(int argc,char**argv){
  int lg=atoi(argv[1]),L=atoi(argv[2]),d0=atoi(argv[3]); long long N=1LL<<lg;
  unsigned char*f=malloc((size_t)L*L),*s=malloc(N+1); int code;
  while(scanf("%d",&code)==1){
    int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)};
    memset(f,0,(size_t)L*L); int x=L/2&~1,y=L/2&~1,d=d0; long long t,cells=0,edge=-1;
    for(t=0;t<N;t++){ size_t i=(size_t)y*L+x; int c=f[i]&1; if(!(f[i]&2)){f[i]|=2;cells++;}
      d=(d+((x&1)?Ts[c]:To[c]))&7; f[i]^=1; s[t]=d|(c<<3)|((x&1)<<4);
      x+=DX[d]; y+=DY[d]; if(x<2||y<2||x>=L-2||y>=L-2){edge=t+1;break;} }
    if(edge<0){printf("%d -1 -1 -1 0 0 %lld\n",code,cells);fflush(stdout);continue;}
    long long E=edge,P=-1;
    for(long long p=1;p<=PMAX&&4*p<E;p++){ int ok=1; for(long long k=E-4*p;k<E-p;k++) if(s[k]!=s[k+p]){ok=0;break;} if(ok){P=p;break;} }
    long long on=-1; int ddx=0,ddy=0;
    if(P>0){ on=E-P; while(on>0&&s[on-1]==s[on-1+P])on--;
      for(long long k=on;k<on+P;k++){ddx+=DX[s[k]&7];ddy+=DY[s[k]&7];} }
    printf("%d %lld %lld %lld %d %d %lld\n",code,E,P,on,ddx,ddy,cells); fflush(stdout);
  }
}
