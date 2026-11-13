// быстрая симуляция машины 26427: ./tmsim N > out ; печатает ленту (id содержимых) при каждой новой клетке справа
#include <stdio.h>
#include <stdlib.h>
#define MC 1024
long long cv[MC]; int nc_=0; int st[7]={27,60,99,132,147,150,219};
int cid(long long c){for(int i=0;i<nc_;i++)if(cv[i]==c)return i; cv[nc_]=c; return nc_++;}
int sid(int s){for(int i=0;i<7;i++)if(st[i]==s)return i; return -1;}
int TS[7][MC],TN[7][MC],TC[7][MC];
int main(int argc,char**argv){ long long N=atoll(argv[1]); cid(0);
  for(int a=0;a<7;a++)for(int b=0;b<MC;b++)TS[a][b]=-1;
  FILE*f=fopen("../tile/cnt/tm26427.txt","r"); long long s,c,side,ns,ncc,cnt;
  while(fscanf(f,"%lld %lld %lld %lld %lld %lld",&s,&c,&side,&ns,&ncc,&cnt)==6){int a=sid(s),b=cid(c); TS[a][b]=side; TN[a][b]=sid(ns); TC[a][b]=cid(ncc);}
  FILE*g=fopen("ids.txt","w"); for(int i=0;i<nc_;i++)fprintf(g,"%d %lld\n",i,cv[i]); fclose(g);
  int L=4096,O=8; int*tp=calloc(L,sizeof(int)); int k=O,q=sid(150),hi=O;
  for(long long n=0;n<N;n++){ int b=tp[k]; if(TS[q][b]<0){printf("нет пары %lld\n",n);return 1;}
    int sd=TS[q][b]; tp[k]=TC[q][b]; q=TN[q][b]; k+=sd?1:-1;
    if(k>hi){hi=k; printf("%lld",n); for(int x=O-1;x<=hi;x++)printf(" %d",tp[x]); printf("\n"); fflush(stdout);} }
  return 0; }
