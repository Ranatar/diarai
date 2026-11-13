/* Муравей Лэнгтона на вершинах кагоме: вершины треугольной решётки (i,j) без (нечёт, нечёт).
   В вершине пересекаются две прямые; муравей, придя по одной, уходит по другой: на белом — налево, на чёрном — направо.
   ./kagome D0 N -> печатает начало и период шоссе (по записи (d,c)), или строку цветов при N<0 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int DI[6]={1,0,-1,-1,0,1},DJ[6]={0,1,1,0,-1,-1};
#define L 8192
int main(int argc,char**argv){
  int d=atoi(argv[1]); long long N=atoll(argv[2]); int pr=N<0; if(pr)N=-N;
  unsigned char*f=calloc((size_t)L*L,1); unsigned char*s=malloc(N); int i=L/2,j=L/2; long long n,E=-1;
  for(n=0;n<N;n++){ size_t p=(size_t)j*L+i; int c=f[p]&1; if(pr)putchar(f[p]&2?'0'+c:'a'+c); f[p]|=2; f[p]^=1;
    int nd=-1;
    for(int k=1;k<=2;k++){ int dd=(d+(c?6-k:k))%6; int ni=i+DI[dd],nj=j+DJ[dd]; if(!((ni&1)&&(nj&1))&&dd%3!=d%3){nd=dd;break;} }
    if(nd<0){printf("stuck\n");return 1;}
    s[n]=nd|c<<3; d=nd; i+=DI[d]; j+=DJ[d]; if(i<2||j<2||i>L-3||j>L-3){E=n+1;break;} }
  if(pr){putchar('\n');return 0;}
  if(E<0){printf("no edge, n=%lld\n",n);return 0;}
  for(long long q=1;q<200000&&4*q<E;q++){ long long W=4*q<50000?50000:4*q; if(W>E)W=E; int ok=1; for(long long k=E-W;k<E-q;k++) if(s[k]!=s[k+q]){ok=0;break;}
    if(ok){ long long on=E-q; while(on>0&&s[on-1]==s[on-1+q])on--; printf("edge %lld period %lld onset %lld\n",E,q,on); return 0;} }
  printf("edge %lld no period\n",E);
}
