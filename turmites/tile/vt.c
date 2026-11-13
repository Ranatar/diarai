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
  if(!strcmp(argv[1],"colors")){ /* ./vt colors CODE E0 N -> строка цветов 0/1 и признак «новая плитка» */
    long long code=atoll(argv[2]); int e=atoi(argv[3]); long long N=atoll(argv[4]); int L=4096;
    decode(code); unsigned char*f=calloc((size_t)L*L*NT,1); int t=0,i=L/2,j=L/2;
    for(long long n=0;n<N;n++){ size_t p=((size_t)j*L+i)*NT+t; int c=f[p]&1; putchar(f[p]&2? '0'+c : 'a'+c); f[p]|=2;
      int ex=(e+OFF[t][c])%SIDES[t]; f[p]^=1; const int*a=ADJ[t][ex]; t=a[0]; i+=a[1]; j+=a[2]; e=a[3];} putchar('\n'); return 0; }
  if(!strcmp(argv[1],"stat")){ /* ./vt stat CODE E0 N -> частоты (тип, ребро входа, цвет) */
    long long code=atoll(argv[2]); int e=atoi(argv[3]); long long N=atoll(argv[4]); int L=4096; static long long h[NT][12][2];
    decode(code); unsigned char*f=calloc((size_t)L*L*NT,1); int t=0,i=L/2,j=L/2;
    for(long long n=0;n<N;n++){ size_t p=((size_t)j*L+i)*NT+t; int c=f[p]&1; h[t][e][c]++;
      int ex=(e+OFF[t][c])%SIDES[t]; f[p]^=1; const int*a=ADJ[t][ex]; t=a[0]; i+=a[1]; j+=a[2]; e=a[3];}
    for(int tt=0;tt<NT;tt++){printf("type %d (%d):",tt,SIDES[tt]); for(int ee=0;ee<SIDES[tt];ee++)printf(" %lld/%lld",h[tt][ee][0],h[tt][ee][1]); printf("\n");} return 0; }
  if(!strcmp(argv[1],"esets")){ /* ./vt esets CODE E0 N -> гистограмма множеств рёбер входа по плиткам (с учётом типа и чётности i,j) */
    long long code=atoll(argv[2]); int e=atoi(argv[3]); long long N=atoll(argv[4]); int L=2048;
    decode(code); unsigned short*m=calloc((size_t)L*L*NT,2); int t=0,i=L/2,j=L/2; unsigned char*f=calloc((size_t)L*L*NT,1);
    for(long long n=0;n<N;n++){ size_t p=((size_t)j*L+i)*NT+t; int c=f[p]&1; m[p]|=1<<e;
      int ex=(e+OFF[t][c])%SIDES[t]; f[p]^=1; const int*a=ADJ[t][ex]; t=a[0]; i+=a[1]; j+=a[2]; e=a[3];}
    static long long H[NT][4][4096]; for(int jj=0;jj<L;jj++)for(int ii=0;ii<L;ii++)for(int tt=0;tt<NT;tt++){unsigned short v=m[((size_t)jj*L+ii)*NT+tt]; if(v) H[tt][(ii&1)+2*(jj&1)][v]++;}
    for(int tt=0;tt<NT;tt++)for(int q=0;q<4;q++)for(int v=0;v<4096;v++)if(H[tt][q][v]){printf("t%d par%d set",tt,q); for(int b=0;b<12;b++)if(v>>b&1)printf(" %d",b); printf(" : %lld\n",H[tt][q][v]);} return 0; }
  if(!strcmp(argv[1],"csig")){ /* ./vt csig N L E0 < codes -> code hash длина (отпечаток строки цветов с отметкой новых плиток) */
    long long N=atoll(argv[2]); int L=atoi(argv[3]),e0=atoi(argv[4]); long long code; unsigned char*f=calloc((size_t)L*L*NT,1);
    size_t*vis=malloc(sizeof(size_t)*(N+1));
    while(scanf("%lld",&code)==1){ decode(code); long long nv=0; int t=0,i=L/2,j=L/2,e=e0; unsigned long long h=1469598103934665603ULL; long long n;
      for(n=0;n<N;n++){ size_t p=((size_t)j*L+i)*NT+t; int c=f[p]&1; h^=(f[p]&2)?c:2+c; h*=1099511628211ULL; if(!(f[p]&2)){f[p]|=2;vis[nv++]=p;}
        int ex=(e+OFF[t][c])%SIDES[t]; f[p]^=1; const int*a=ADJ[t][ex]; t=a[0]; i+=a[1]; j+=a[2]; e=a[3]; if(i<2||j<2||i>=L-2||j>=L-2){n++;break;}}
      for(long long k=0;k<nv;k++)f[vis[k]]=0;
      printf("%lld %016llx %lld %lld\n",code,h,n,nv); }
    return 0; }
  if(!strcmp(argv[1],"csig2")){ /* ./vt csig2 M L E0 < codes -> code hash длина_сжатой шагов плиток
     сжатая строка: пропускаем пассивные плитки (выход не зависит от цвета), подряд идущие посещения одной плитки — одно (цвет первого) */
    long long M=atoll(argv[2]); int L=atoi(argv[3]),e0=atoi(argv[4]); long long code; unsigned char*f=calloc((size_t)L*L*NT,1);
    long long NMAX=5*M; size_t*vis=malloc(sizeof(size_t)*(NMAX+1));
    while(scanf("%lld",&code)==1){ decode(code); long long nv=0,m=0,n; int t=0,i=L/2,j=L/2,e=e0; unsigned long long h=1469598103934665603ULL; size_t last=(size_t)-1;
      for(n=0;n<NMAX&&m<M;n++){ size_t p=((size_t)j*L+i)*NT+t; int c=f[p]&1;
        if(OFF[t][0]!=OFF[t][1] && p!=last){ h^=(f[p]&2)?c:2+c; h*=1099511628211ULL; m++; }
        if(OFF[t][0]!=OFF[t][1]) last=p;
        if(!(f[p]&2)){f[p]|=2;vis[nv++]=p;}
        int ex=(e+OFF[t][c])%SIDES[t]; f[p]^=1; const int*a=ADJ[t][ex]; t=a[0]; i+=a[1]; j+=a[2]; e=a[3]; if(i<2||j<2||i>=L-2||j>=L-2){n++;break;}}
      for(long long k=0;k<nv;k++)f[vis[k]]=0;
      printf("%lld %016llx %lld %lld %lld\n",code,h,m,n,nv); }
    return 0; }
  if(!strcmp(argv[1],"pos")){ /* ./vt pos CODE E0 LOG2N STEP -> t x y (центр плитки муравья) каждые STEP шагов */
    long long code=atoll(argv[2]); int e=atoi(argv[3]); long long N=1LL<<atoi(argv[4]),S=atoll(argv[5]); int L=8192;
    decode(code); unsigned char*f=calloc((size_t)L*L*NT,1); int t=0,i=L/2,j=L/2;
    for(long long n=0;n<N;n++){ size_t p=((size_t)j*L+i)*NT+t; int c=f[p];
      if(n%S==0){ double x=CEN[t][0]+(i-L/2)*A1[0]+(j-L/2)*A2[0], y=CEN[t][1]+(i-L/2)*A1[1]+(j-L/2)*A2[1]; printf("%lld %.2f %.2f\n",n,x,y);}
      int ex=(e+OFF[t][c])%SIDES[t]; f[p]^=1; const int*a=ADJ[t][ex]; t=a[0]; i+=a[1]; j+=a[2]; e=a[3]; if(i<2||j<2||i>=L-2||j>=L-2)break;} return 0; }
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
      for(long long q=1;q<=PMAX&&4*q<E;q++){long long W=4*q<2000?2000:4*q; if(W>E)W=E; int ok=1; for(long long k=E-W;k<E-q;k++) if(s[k]!=s[k+q]){ok=0;break;} if(ok){P=q;break;}}
      long long on=-1; int di=0,dj=0;
      if(P>0){ on=E-P; while(on>0&&s[on-1]==s[on-1+P])on--; for(long long k=on;k<on+P;k++){di+=mv[2*k];dj+=mv[2*k+1];} }
      printf("%lld %lld %lld %lld %d %d %lld %016llx\n",code,E,P,on,di,dj,cells,h); fflush(stdout); }
    return 0; }
  if(!strcmp(argv[1],"bt")){ /* ./vt bt CODE E0 N S -> каждые S шагов: n и число чёрных по (тип, i&1, j&1) */
    long long code=atoll(argv[2]); int e=atoi(argv[3]); long long N=atoll(argv[4]),S=atoll(argv[5]); int L=4096;
    decode(code); unsigned char*f=calloc((size_t)L*L*NT,1); int t=0,i=L/2,j=L/2; long long cnt[NT][4]; memset(cnt,0,sizeof cnt);
    for(long long n=0;n<N;n++){ size_t p=((size_t)j*L+i)*NT+t; int c=f[p]&1;
      if(n%S==0){printf("%lld",n); for(int a=0;a<NT;a++)for(int b=0;b<4;b++)printf(" %lld",cnt[a][b]); printf("\n");}
      cnt[t][(i&1)|(j&1)<<1]+=c?-1:1;
      int ex=(e+OFF[t][c])%SIDES[t]; f[p]^=1; const int*a=ADJ[t][ex]; t=a[0]; i+=a[1]; j+=a[2]; e=a[3]; if(i<2||j<2||i>=L-2||j>=L-2)break;}
    return 0; }
  if(!strcmp(argv[1],"censusl")){ /* ./vt censusl LOG2N L E0 < codes -> как census, коды со входа */
    int lg=atoi(argv[2]),L=atoi(argv[3]),e0=atoi(argv[4]); long long N=1LL<<lg,code; unsigned char*f=malloc((size_t)L*L*NT);
    while(scanf("%lld",&code)==1){ decode(code); memset(f,0,(size_t)L*L*NT);
      int t=0,i=L/2,j=L/2,e=e0; long long n1=0,n2=0,cells=0,black=0,edge=-1;
      for(long long n=1;n<=N;n++){ size_t p=((size_t)j*L+i)*NT+t; int c=f[p]&1; if(!(f[p]&2)){f[p]|=2;cells++;}
        int ex=(e+OFF[t][c])%SIDES[t]; f[p]^=1; black+=c?-1:1;
        const int*a=ADJ[t][ex]; t=a[0]; i+=a[1]; j+=a[2]; e=a[3];
        if(i<2||j<2||i>=L-2||j>=L-2){edge=n;break;}
        if(n==(N>>4))n1=cells; if(n==(N>>2))n2=cells; }
      printf("%lld %lld %lld %lld %lld %lld\n",code,n1,n2,cells,black,edge); fflush(stdout); }
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
