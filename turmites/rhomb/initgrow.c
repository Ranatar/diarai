// Турмит, стартующий внутри чёрной фигуры: ./initgrow RULE STEPS SHAPE R out.pgm  (SHAPE s — квадрат |x|,|y|<=R, d — круг, r — ромб |x|+|y|<=R)
// Печать: на удвоениях t — t, единицы, рамка. Миниатюра 400 (доля чёрного в ячейке).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 8192
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int argc,char**argv){ int rule=atoi(argv[1]); long steps=atol(argv[2]); char S=argv[3][0]; int R=atoi(argv[4]);
  int wc[4],tn[4],ns[4]; for(int e=0;e<4;e++){int b=(rule>>(4*e))&15; wc[e]=b&1; tn[e]=(b>>1)&3; ns[e]=(b>>3)&1;}
  int c=N/2; long ones=0; int minx=c,maxx=c,miny=c,maxy=c;
  for(int y=c-R;y<=c+R;y++)for(int x=c-R;x<=c+R;x++){int dx=x-c,dy=y-c; int in=S=='s'||(S=='d'&&dx*dx+dy*dy<=R*R)||(S=='r'&&abs(dx)+abs(dy)<=R);
    if(in){g[(long)y*N+x]=1;ones++; if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y;}}
  int x=c,y=c,d=0,s=0; long t, nt=1;
  for(t=0;t<steps;t++){ uint8_t*q=&g[(long)y*N+x]; int e=s*2+*q; ones+=wc[e]-*q; *q=wc[e]; d=(d+tn[e])&3; s=ns[e]; x+=DX[d]; y+=DY[d];
    if(x<2||x>=N-2||y<2||y>=N-2) break;
    if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y;
    if(t+1==nt){ printf("t=%ld ones=%ld w=%d h=%d\n",t+1,ones,maxx-minx+1,maxy-miny+1); fflush(stdout); nt*=2; } }
  printf("end t=%ld ones=%ld w=%d h=%d\n",t,ones,maxx-minx+1,maxy-miny+1);
  int Sz=(maxx-minx>maxy-miny?maxx-minx:maxy-miny)+1, P=400; FILE*f=fopen(argv[5],"wb"); fprintf(f,"P5\n%d %d\n255\n",P,P);
  for(int i=0;i<P;i++)for(int j=0;j<P;j++){int cnt=0,tot=0;int x0=minx+(long)j*Sz/P,x1=minx+(long)(j+1)*Sz/P,y0=miny+(long)i*Sz/P,y1=miny+(long)(i+1)*Sz/P;
    if(x1==x0)x1++; if(y1==y0)y1++; for(int yy=y0;yy<y1;yy++)for(int xx=x0;xx<x1;xx++){tot++;cnt+=g[(long)yy*N+xx];} fputc(255-255*cnt/tot,f);}
  fclose(f); return 0; }
