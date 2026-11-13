/* Догонка: ./vdeep LOG2N L D0 < codes -> code edge period onset dx dy cells
   как vonset, но шаги в кольцевом буфере 2^RB; если начало шоссе дальше буфера — onset печатается со знаком '<' не нужен:
   печатается -2 (начало раньше, чем помнит буфер). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define RB 24
#define M ((1LL<<RB)-1)
#define PMAX 200000
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
int main(int argc,char**argv){
  int lg=atoi(argv[1]),L=atoi(argv[2]),d0=atoi(argv[3]); long long N=1LL<<lg;
  unsigned char*f=malloc((size_t)L*L),*s=malloc(M+1); int code;
  while(scanf("%d",&code)==1){
    int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)};
    memset(f,0,(size_t)L*L); int x=L/2&~1,y=L/2&~1,d=d0; long long t,cells=0,edge=-1;
    for(t=0;t<N;t++){ size_t i=(size_t)y*L+x; int c=f[i]&1; if(!(f[i]&2)){f[i]|=2;cells++;}
      d=(d+((x&1)?Ts[c]:To[c]))&7; f[i]^=1; s[t&M]=d|(c<<3)|((x&1)<<4);
      x+=DX[d]; y+=DY[d]; if(x<2||y<2||x>=L-2||y>=L-2){edge=t+1;break;} }
    if(edge<0){printf("%d -1 -1 -1 0 0 %lld\n",code,cells);fflush(stdout);continue;}
    long long E=edge,P=-1,lo=E>M?E-M:0;
    for(long long p=1;p<=PMAX&&E-4*p>=lo;p++){ int ok=1; for(long long k=E-4*p;k<E-p;k++) if(s[k&M]!=s[(k+p)&M]){ok=0;break;} if(ok){P=p;break;} }
    long long on=-1; int ddx=0,ddy=0;
    if(P>0){ on=E-P; while(on>lo&&s[(on-1)&M]==s[(on-1+P)&M])on--; if(on==lo&&lo>0)on=-2;
      else for(long long k=on;k<on+P;k++){ddx+=DX[s[k&M]&7];ddy+=DY[s[k&M]&7];} }
    printf("%d %lld %lld %lld %d %d %lld\n",code,E,P,on,ddx,ddy,cells); fflush(stdout);
  }
}
