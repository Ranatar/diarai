/* Вант на периодическом паркете (таблица из gen.py, -DTILING="t31212.h").
   Состояние: плитка (тип t, ячейка i,j), ребро входа e. На цвете c выход через ребро (e + OFF[t][c]) mod SIDES[t],
   цвет меняется. Правило: код в смешанной системе по классам многоугольников (по числу сторон, в порядке типов):
   для каждого класса k: off(k,0) + n_k * off(k,1), классы перемножаются.
   ./vt seq CODE E0 N           -> число чёрных после каждого хода (для сверки с OEIS)
   ./vt census LOG2N L E0 [from to] -> code n(N/16) n(N/4) n(N) black edge */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include TILING
static int OFF[NT][2], NCL, CLS[NT], CLN[NT];
static long long NRULES=1;
static void setup(void){ NCL=0; for(int t=0;t<NT;t++){ int k=-1; for(int u=0;u<t;u++) if(SIDES[u]==SIDES[t]){k=CLS[u];break;}
  if(k<0){k=NCL++; CLN[k]=SIDES[t]; NRULES*=SIDES[t]*SIDES[t];} CLS[t]=k; } }
static void decode(long long code){ int o[8][2]; for(int k=0;k<NCL;k++){o[k][0]=code%CLN[k]; code/=CLN[k]; o[k][1]=code%CLN[k]; code/=CLN[k];}
  for(int t=0;t<NT;t++){OFF[t][0]=o[CLS[t]][0]; OFF[t][1]=o[CLS[t]][1];} }
int main(int argc,char**argv){
  setup();
  if(!strcmp(argv[1],"seq")){ long long code=atoll(argv[2]); int e=atoi(argv[3]); long long N=atoll(argv[4]); int L=8192;
    decode(code); unsigned char*f=calloc((size_t)L*L*NT,1); int t=0,i=L/2,j=L/2; long long black=0; printf("0\n");
    for(long long n=1;n<=N;n++){ size_t p=((size_t)j*L+i)*NT+t; int c=f[p]; int ex=(e+OFF[t][c])%SIDES[t]; f[p]^=1; black+=c?-1:1;
      const int*a=ADJ[t][ex]; t=a[0]; i+=a[1]; j+=a[2]; e=a[3]; printf("%lld\n",black);} return 0; }
  if(!strcmp(argv[1],"dump")){ /* ./vt dump CODE E0 N -> t i j color по посещённым; последняя строка — муравей */
    long long code=atoll(argv[2]); int e=atoi(argv[3]); long long N=atoll(argv[4]); int L=4096;
    decode(code); unsigned char*f=calloc((size_t)L*L*NT,1); int t=0,i=L/2,j=L/2;
    for(long long n=0;n<N;n++){ size_t p=((size_t)j*L+i)*NT+t; int c=f[p]&1; f[p]|=2;
      int ex=(e+OFF[t][c])%SIDES[t]; f[p]^=1; const int*a=ADJ[t][ex]; t=a[0]; i+=a[1]; j+=a[2]; e=a[3]; if(i<2||j<2||i>=L-2||j>=L-2)break;}
    for(int jj=0;jj<L;jj++)for(int ii=0;ii<L;ii++)for(int tt=0;tt<NT;tt++){unsigned char v=f[((size_t)jj*L+ii)*NT+tt]; if(v&2)printf("%d %d %d %d\n",tt,ii-L/2,jj-L/2,v&1);}
    printf("A %d %d %d\n",t,i-L/2,j-L/2); return 0; }
  if(!strcmp(argv[1],"new")){ /* ./vt new CODE E0 LOG2N -> моменты появления новых плиток: n t i j */
    long long code=atoll(argv[2]); int e=atoi(argv[3]); long long N=1LL<<atoi(argv[4]); int L=4096;
    decode(code); unsigned char*f=calloc((size_t)L*L*NT,1); int t=0,i=L/2,j=L/2; long long cells=0;
    for(long long n=0;n<N;n++){ size_t p=((size_t)j*L+i)*NT+t; int c=f[p]&1; if(!(f[p]&2)){f[p]|=2;cells++; printf("%lld %lld %d %d %d\n",cells,n,t,i-L/2,j-L/2);}
      int ex=(e+OFF[t][c])%SIDES[t]; f[p]^=1; const int*a=ADJ[t][ex]; t=a[0]; i+=a[1]; j+=a[2]; e=a[3]; if(i<2||j<2||i>=L-2||j>=L-2)break;} return 0; }
  if(!strcmp(argv[1],"onset")){ /* ./vt onset LOG2N L E0 < codes -> code edge period onset di dj cells sig */
    int lg=atoi(argv[2]),L=atoi(argv[3]),e0=atoi(argv[4]); long long N=1LL<<lg,code; const long long PMAX=200000;
    unsigned char*f=malloc((size_t)L*L*NT); unsigned short*s=malloc((N+1)*2); signed char*mv=malloc((N+1)*2);
    while(scanf("%lld",&code)==1){ decode(code); memset(f,0,(size_t)L*L*NT);
      int t=0,i=L/2,j=L/2,e=e0; long long n,cells=0,edge=-1; unsigned long long h=1469598103934665603ULL;
      for(n=0;n<N;n++){ size_t p=((size_t)j*L+i)*NT+t; int c=f[p]&1; if(!(f[p]&2)){f[p]|=2;cells++;}
        int ex=(e+OFF[t][c])%SIDES[t]; f[p]^=1; s[n]=t|ex<<4|c<<8;
        if(n<100000){h^=s[n];h*=1099511628211ULL;}
        const int*a=ADJ[t][ex]; t=a[0]; i+=a[1]; j+=a[2]; e=a[3]; mv[2*n]=a[1]; mv[2*n+1]=a[2];
        if(i<2||j<2||i>=L-2||j>=L-2){edge=n+1;break;} }
      if(edge<0){printf("%lld -1 -1 -1 0 0 %lld %016llx\n",code,cells,h);fflush(stdout);continue;}
      long long E=edge,P=-1;
      for(long long q=1;q<=PMAX&&4*q<E;q++){int ok=1; for(long long k=E-4*q;k<E-q;k++) if(s[k]!=s[k+q]){ok=0;break;} if(ok){P=q;break;}}
      long long on=-1; int di=0,dj=0;
      if(P>0){ on=E-P; while(on>0&&s[on-1]==s[on-1+P])on--; for(long long k=on;k<on+P;k++){di+=mv[2*k];dj+=mv[2*k+1];} }
      printf("%lld %lld %lld %lld %d %d %lld %016llx\n",code,E,P,on,di,dj,cells,h); fflush(stdout); }
    return 0; }
  int lg=atoi(argv[2]),L=atoi(argv[3]),e0=atoi(argv[4]); long long from=argc>5?atoll(argv[5]):0,to=argc>6?atoll(argv[6]):NRULES;
  unsigned char*f=malloc((size_t)L*L*NT); long long N=1LL<<lg;
  for(long long code=from;code<to;code++){ decode(code); memset(f,0,(size_t)L*L*NT);
    int t=0,i=L/2,j=L/2,e=e0; long long n1=0,n2=0,cells=0,black=0,edge=-1;
    for(long long n=1;n<=N;n++){ size_t p=((size_t)j*L+i)*NT+t; int c=f[p]&1; if(!(f[p]&2)){f[p]|=2;cells++;}
      int ex=(e+OFF[t][c])%SIDES[t]; f[p]^=1; black+=c?-1:1;
      const int*a=ADJ[t][ex]; t=a[0]; i+=a[1]; j+=a[2]; e=a[3];
      if(i<2||j<2||i>=L-2||j>=L-2){edge=n;break;}
      if(n==(N>>4))n1=cells; if(n==(N>>2))n2=cells; }
    printf("%lld %lld %lld %lld %lld %lld\n",code,n1,n2,cells,black,edge); fflush(stdout); }
}
