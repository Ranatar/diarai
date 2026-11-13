/* машина 26427 с достройкой таблицы на лету: переход клетки считается муравьём внутри столбца.
   ./tmsim2 N [EVERY] : печатает ленту (id содержимых) при каждой новой клетке справа; ids2.txt — id -> содержимое */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../tile/t4612.h"
static int OFF[NT][2], NCL, CLS[NT], CLN[NT];
static void setup(void){ NCL=0; for(int t=0;t<NT;t++){ int k=-1; for(int u=0;u<t;u++) if(SIDES[u]==SIDES[t]){k=CLS[u];break;}
  if(k<0){k=NCL++; CLN[k]=SIDES[t];} CLS[t]=k; } }
static void decode(long long code){ int o[8][2]; for(int k=0;k<NCL;k++){o[k][0]=code%CLN[k]; code/=CLN[k]; o[k][1]=code%CLN[k]; code/=CLN[k];}
  for(int t=0;t<NT;t++){OFF[t][0]=o[CLS[t]][0]; OFF[t][1]=o[CLS[t]][1];} }
#define MLO (-2)
#define R 4
#define MC 50000
long long cv[MC]; int ncv=0;
#define HS (1<<20)
long long hkey[HS]; int hval[HS];
int cid(long long c){ unsigned h=(unsigned)((unsigned long long)(c+1)*11400714819323198485ull>>44)%HS;
  while(hkey[h]){ if(hkey[h]==c+1) return hval[h]; h=(h+1)%HS; } if(ncv>=MC){fprintf(stderr,"MC\n");exit(1);} hkey[h]=c+1; hval[h]=ncv; cv[ncv]=c; return ncv++; }
int *TS,*TN,*TC; int NS=R*NT*12; long long computed=0;
/* оракул: состояние s=(r*NT+t)*12+e, содержимое c -> сторона, новое s, новое c */
void oracle(int s,int b){ long long c=cv[b]; int r=s/(NT*12), t=(s/12)%NT, e=s%12; int i=0, m=MLO+r;
  for(long long it=0;;it++){ if(it>100000000){fprintf(stderr,"зацикл\n");exit(1);}
    int rr=m-MLO; if(rr<0||rr>=R){fprintf(stderr,"вылет из полосы s=%d c=%lld\n",s,c);exit(1);}
    int bit=rr*NT+t; int col=(c>>bit)&1; int ex=(e+OFF[t][col])%SIDES[t]; c^=1LL<<bit;
    const int*a=ADJ[t][ex]; t=a[0]; e=a[3]; int di=a[1], dj=a[2]; m+=di+dj; i+=di;
    if(i!=0){ int r2=m-MLO; if(r2<0||r2>=R){fprintf(stderr,"вылет при выходе\n");exit(1);}
      int idx=s*MC+b; TS[idx]=i>0; TN[idx]=(r2*NT+t)*12+e; TC[idx]=cid(c); computed++; return; } } }
int main(int argc,char**argv){ long long N=atoll(argv[1]); setup(); decode(26427); cid(0);
  TS=malloc(sizeof(int)*(size_t)NS*MC); TN=malloc(sizeof(int)*(size_t)NS*MC); TC=malloc(sizeof(int)*(size_t)NS*MC);
  memset(TS,0xff,sizeof(int)*(size_t)NS*MC);
  /* сверка с извлечённой таблицей */
  FILE*f=fopen("../tile/cnt/tm26427.txt","r"); long long s,c,side,ns,ncc,cnt; int bad=0,tot=0;
  while(fscanf(f,"%lld %lld %lld %lld %lld %lld",&s,&c,&side,&ns,&ncc,&cnt)==6){ int b=cid(c); oracle(s,b); int idx=s*MC+b; tot++;
    if(TS[idx]!=side||TN[idx]!=ns||cv[TC[idx]]!=ncc) bad++; }
  fprintf(stderr,"сверка с таблицей: %d из %d расходятся\n",bad,tot); if(bad) return 1;
  #define NX 20
  #define CAP 4000000
  static int sq[NX][CAP]; static long long nsq[NX]; static long long vis[NX], visr[NX];
  int L=1<<16,O=8; int*tp=calloc(L,sizeof(int)); int k=O,q=150;
  for(long long n=0;n<N;n++){ int b=tp[k]; int idx=q*MC+b; if(TS[idx]<0) oracle(q,b);
    int sd=TS[idx]; int nb=TC[idx]; int x=k-O+1;
    if(n>N/2 && x>=0 && x<NX){ vis[x]++; if(sd) visr[x]++; if(nb!=b && nsq[x]<CAP) sq[x][nsq[x]++]=nb; }
    tp[k]=nb; q=TN[idx]; k+=sd?1:-1; }
  for(int x=0;x<NX;x++){ long long m=nsq[x]; long long p; int found=0;
    for(p=1;p<=m/3;p++){ long long i; for(i=0;i+p<m;i++) if(sq[x][i]!=sq[x][i+p]) break; if(i+p>=m){found=1;break;} }
    printf("клетка %d (x-1=%d): смен %lld, вправо %lld, период смен %lld\n",x,x-1,m,visr[x],found?p:-1); }
  FILE*g=fopen("ids2.txt","w"); for(int i=0;i<ncv;i++)fprintf(g,"%d %lld\n",i,cv[i]); fclose(g);
  fprintf(stderr,"достроено %lld, содержимых %d\n",computed,ncv); return 0; }
