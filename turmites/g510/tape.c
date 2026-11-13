/* ./tape D0 NS P0 K: после того как правый край достиг NS (удв.), печатаем ленту правее P0 (удв. коорд от левого края)
   каждый раз, когда муравей проходит через x=P0 вправо; K строк */
#include <stdio.h>
#include <stdlib.h>
static const int DX[8]={2,1,0,-1,-2,-1,0,1},DY[8]={0,1,2,1,0,-1,-2,-1};
#define L 4096
unsigned char f[3][L];
int main(int argc,char**argv){
  int d0=atoi(argv[1]),ns=atoi(argv[2]),p0=atoi(argv[3]),K=atoi(argv[4]);
  int To[2]={6,7},Ts[2]={6,2}; int x=L/2,y=0,d=d0; int x0=x,x1=x; int on=0;
  for(long long t=0;;t++){
    if(x<x0)x0=x; if(x>x1){x1=x; if(x1-L/2>=ns&&!on)on=1; else if(on==2)return 0;}
    if(on&&x1-x0>2*ns-4&&x0<L/2-ns+4)on=2;
    if(on==2&&x==x0+p0&&(d==0||d==1||d==7)){
      printf("%12lld ",t); for(int r=0;r<3;r++){for(int xx=x0+p0;xx<=x1;xx++){ if(((xx-x0)&1)==(r==1)) putchar(f[r][xx]?'#':'.');} putchar(' ');}
      putchar('\n'); if(--K==0)return 0;}
    unsigned char*c=&f[-y][x]; int cc=*c; d=(d+((x&1)?Ts[cc]:To[cc]))&7; *c^=1; x+=DX[d]; y+=DY[d];
  }
}
