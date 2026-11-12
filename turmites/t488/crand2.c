/* Старт на случайном диске: ./crand RULE TAU0 RD OFF LOG2T SEED
   узлы в круге радиуса RD (центр L/2) — случайные 4 бита; муравей стартует в (L/2+OFF, L/2).
   Печатает долю времени (окно 2^(T-2)..2^T) в кругах радиуса RD/4 вокруг: старта, центра диска, точки (-OFF,0), и чем плотность выше средней */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  const char*R=argv[1]; int tau=atoi(argv[2]),RD=atoi(argv[3]),OFF=atoi(argv[4]); long long T=1LL<<atoi(argv[5]); srand(atoi(argv[6]));
  int L=4096,W[2][2],Ex[2][2]; for(int i=0;i<4;i++){W[i>>1][i&1]=R[2*i]-'0';Ex[i>>1][i&1]=R[2*i+1]-'0';}
  unsigned char*f=calloc((size_t)L*L,1); int C=L/2;
  for(int y=C-RD;y<=C+RD;y++)for(int x=C-RD;x<=C+RD;x++) if((x-C)*(x-C)+(y-C)*(y-C)<=RD*RD) f[(size_t)y*L+x]=16|(rand()&15);
  int X=C+OFF,Y=C,k=0,sig=1; double q=RD/4.0; unsigned int*vis=calloc((size_t)L*L,4); double inD=0,inS=0,inC=0,inM=0,tot=0;
  int minx=X,maxx=X,miny=Y,maxy=Y;
  for(long long t=1;t<T;t++){
    unsigned char*p=&f[(size_t)Y*L+X]; int c=(*p>>k)&1,w=W[tau][c],e=Ex[tau][c]; if(w!=c)*p^=1<<k;
    int oct=0; if(tau==0){if(e==0)oct=1;else sig=(e==1)?1:-1;} else {if(e==2)oct=1;else if(e==0)sig=-sig;}
    if(oct){X+=DX[k];Y+=DY[k];k=(k+2)&3;tau=0; if(X<1||Y<1||X>=L-1||Y>=L-1){printf("край\n");return 0;} f[(size_t)Y*L+X]|=16;
      if(X<minx)minx=X;if(X>maxx)maxx=X;if(Y<miny)miny=Y;if(Y>maxy)maxy=Y;}
    else{k=(k+sig)&3;tau=1;}
    if(t>=T/4){ tot++; vis[(size_t)Y*L+X]++; if(hypot(X-C,Y-C)<=RD) inD++; if(hypot(X-C-OFF,Y-C)<q) inS++; if(hypot(X-C,Y-C)<q) inC++; if(hypot(X-C+OFF,Y-C)<q) inM++; }
  }
  if(argc>7){ FILE*o=fopen(argv[7],"wb"); int w=maxx-minx+1,h=maxy-miny+1; double mx=0; for(int y=miny;y<=maxy;y++)for(int x=minx;x<=maxx;x++){double v=vis[(size_t)y*L+x]; if(v>mx)mx=v;}
    fprintf(o,"P5 %d %d 255\n",w,h); for(int y=miny;y<=maxy;y++)for(int x=minx;x<=maxx;x++){ size_t i=(size_t)y*L+x; int v;
      if((x-C-OFF)*(x-C-OFF)+(y-C)*(y-C)<9) v=0; else if(abs((int)hypot(x-C,y-C)-RD)==0) v=128; else if(!(f[i]&16)) v=255; else { double z=sqrt(vis[i]/mx); v=250-(int)(240*z);} fputc(v,o);} fclose(o);}
  { double s1[2]={0},s2[2]={0},nn[2]={0},top[2]={0};
    for(int y=miny;y<=maxy;y++)for(int x=minx;x<=maxx;x++){ size_t i=(size_t)y*L+x; if(!(f[i]&16))continue; int z=hypot(x-C,y-C)<=RD?0:1; double v=vis[i]; s1[z]+=v; s2[z]+=v*v; nn[z]++; }
    for(int z=0;z<2;z++){ double m=s1[z]/nn[z]; printf("%s: посещ. на узел ср %.1f, разброс/ср %.2f\n", z?"нарост":"диск", m, sqrt(s2[z]/nn[z]-m*m)/m); } }
  { int B=8; int nb=L/B; double*g=calloc((size_t)nb*nb,sizeof(double)); for(int y=0;y<L;y++)for(int x=0;x<L;x++) g[(size_t)(y/B)*nb+x/B]+=vis[(size_t)y*L+x];
    double best=0; int bx=0,by=0; for(int y=2;y<nb-2;y++)for(int x=2;x<nb-2;x++){ double s=0; for(int a=-2;a<=2;a++)for(int b=-2;b<=2;b++) s+=g[(size_t)(y+a)*nb+x+b]; if(s>best){best=s;bx=x;by=y;} }
    double px=bx*B+B/2.0-C, py=by*B+B/2.0-C; printf("пик (40x40) в (%+.0f,%+.0f): до старта %.0f, до центра диска %.0f\n",px,py,hypot(px-OFF,py),hypot(px,py)); }
  long long nodes=0; for(size_t i=0;i<(size_t)L*L;i++) if(f[i]&16) nodes++;
  double base=M_PI*q*q/nodes;  /* доля при равномерном */
  long long dn=0; for(int y=C-RD;y<=C+RD;y++)for(int x=C-RD;x<=C+RD;x++) if((x-C)*(x-C)+(y-C)*(y-C)<=RD*RD) dn++;
  printf("время в диске / доля диска в теле: %.3f / %.3f -> %.2f\n",inD/tot,(double)dn/nodes,(inD/tot)/((double)dn/nodes));
  printf("%s RD=%d OFF=%d рамка %dx%d узлов %lld | плотность/равном.: у старта %.2f, в центре диска %.2f, напротив старта %.2f\n",
    R,RD,OFF,maxx-minx,maxy-miny,nodes,inS/tot/base,inC/tot/base,inM/tot/base);
}
