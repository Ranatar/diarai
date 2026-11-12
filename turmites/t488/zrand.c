/* Турмит Z² на случайном диске: ./zrand RULE RD OFF LOG2T SEED -> rule cv_диска cv_нароста время_в_диске/доля
   поле 2048², клетки в круге RD — случайные; окно — последние 3/4 шагов. */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  int r=atoi(argv[1]),RD=atoi(argv[2]),OFF=atoi(argv[3]); long long T=1LL<<atoi(argv[4]); srand(atoi(argv[5]));
  int L=2048,C=L/2; int w[4],tn[4],ns[4]; for(int e=0;e<4;e++){int v=(r>>(4*e))&15; w[e]=v&1; tn[e]=(v>>1)&3; ns[e]=(v>>3)&1;}
  unsigned char*f=calloc((size_t)L*L,1); unsigned int*vis=calloc((size_t)L*L,4);
  for(int y=C-RD;y<=C+RD;y++)for(int x=C-RD;x<=C+RD;x++) if((x-C)*(x-C)+(y-C)*(y-C)<=RD*RD) f[(size_t)y*L+x]=2|(rand()&1);
  int x=C+OFF,y=C,d=0,s=0; double inD=0,tot=0;
  for(long long t=0;t<T;t++){
    size_t i=(size_t)y*L+x; int c=f[i]&1,e=s*2+c; f[i]=2|w[e]; d=(d+tn[e])&3; s=ns[e]; x+=DX[d]; y+=DY[d];
    if(x<1||y<1||x>=L-1||y>=L-1){printf("%d край\n",r);return 0;}
    if(t>=T/4){ vis[(size_t)y*L+x]++; tot++; if((x-C)*(x-C)+(y-C)*(y-C)<=RD*RD) inD++; }
  }
  double s1[2]={0},s2[2]={0},nn[2]={0};
  for(int yy=0;yy<L;yy++)for(int xx=0;xx<L;xx++){ size_t i=(size_t)yy*L+xx; if(!(f[i]&2))continue; int z=((xx-C)*(xx-C)+(yy-C)*(yy-C)<=RD*RD)?0:1; double v=vis[i]; s1[z]+=v;s2[z]+=v*v;nn[z]++; }
  double cv[2]; for(int z=0;z<2;z++){double m=s1[z]/(nn[z]?nn[z]:1); cv[z]=nn[z]?sqrt(s2[z]/nn[z]-m*m)/m:0;}
  printf("%d %.2f %.2f %.2f\n",r,cv[0],cv[1],(inD/tot)/(nn[0]/(nn[0]+nn[1])));
}
