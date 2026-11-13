/* Лэнгтон на кагоме, долгий счёт: кольцевой буфер последних 2^24 шагов. ./kagome2 D0 LOG2N L
   печатает каждые 2^k: t, число посещённых, размах; при выходе к краю — период и начало шоссе (если в буфере) */
#include <stdio.h>
#include <stdlib.h>
static const int DI[6]={1,0,-1,-1,0,1},DJ[6]={0,1,1,0,-1,-1};
#define RB (1<<24)
int main(int argc,char**argv){
  int d=atoi(argv[1]); long long N=1LL<<atoi(argv[2]); int L=atoi(argv[3]);
  unsigned char*f=calloc((size_t)L*L,1),*s=malloc(RB); int i=L/2,j=L/2; long long n,E=-1,cells=0; int i0=i,i1=i,j0=j,j1=j;
  long long next=1024;
  for(n=0;n<N;n++){ size_t p=(size_t)j*L+i; int c=f[p]&1; if(!(f[p]&2)){f[p]|=2;cells++;} f[p]^=1;
    int nd=-1; for(int k=1;k<=2;k++){ int dd=(d+(c?6-k:k))%6; int ni=i+DI[dd],nj=j+DJ[dd]; if(!((ni&1)&&(nj&1))&&dd%3!=d%3){nd=dd;break;} }
    s[n&(RB-1)]=nd|c<<3; d=nd; i+=DI[d]; j+=DJ[d];
    if(i<i0)i0=i; if(i>i1)i1=i; if(j<j0)j0=j; if(j>j1)j1=j;
    if(i<2||j<2||i>L-3||j>L-3){E=n+1;break;}
    if(n+1==next){printf("t=%lld cells=%lld box %d x %d\n",next,cells,i1-i0,j1-j0);fflush(stdout);next*=2;} }
  if(E<0){printf("no edge by %lld, cells %lld\n",N,cells);return 0;}
  long long lo=E>RB?E-RB:0;
  for(long long q=1;q<RB/8;q++){ long long W=4*q<2000?2000:4*q; if(E-W<lo)break; int ok=1;
    for(long long k=E-W;k<E-q;k++) if(s[k&(RB-1)]!=s[(k+q)&(RB-1)]){ok=0;break;}
    if(ok){ long long on=E-q; while(on-1>=lo&&s[(on-1)&(RB-1)]==s[(on-1+q)&(RB-1)])on--; printf("edge %lld period %lld onset %lld%s cells %lld\n",E,q,on,on==lo?" (граница буфера)":"",cells); return 0;} }
  printf("edge %lld no period, cells %lld\n",E,cells);
}
