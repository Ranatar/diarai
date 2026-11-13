/* ./vsig D0 STEPS : для каждого из 1024 кодов — хэш пути (последовательность направлений) за STEPS шагов
   и хэш зеркального пути; печатает code min(hash,hash_mirror) — одинаковые подписи = одно поведение */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
int main(int argc,char**argv){
  int d0=atoi(argv[1]); long long S=atoll(argv[2]); int L=4096;
  unsigned char*f=malloc((size_t)L*L);
  for(int code=0;code<1024;code++){
    int To[2]={code&7,(code>>3)&7},Ts[2]={2*((code>>6)&3),2*((code>>8)&3)};
    memset(f,0,(size_t)L*L); int x=L/2,y=L/2,d=d0; unsigned long long h=1469598103934665603ULL,hm=h;
    for(long long t=0;t<S;t++){ size_t i=(size_t)y*L+x; int c=f[i]&1;
      d=(d+((x&1)?Ts[c]:To[c]))&7; f[i]^=1; x+=DX[d]; y+=DY[d];
      h=(h^d)*1099511628211ULL; hm=(hm^((d0*2-d)&7))*1099511628211ULL;
      if(x<2||y<2||x>=L-2||y>=L-2)break; }
    printf("%d %016llx\n",code,h<hm?h:hm);
  }
}
