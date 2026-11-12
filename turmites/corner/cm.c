// Муравей с памятью угла. У клетки (x,y) «угол 1» = вертикальная сторона V (В если бит F[(x&1)+2(y&1)]) и
// горизонтальная H (С если бит G[...]). Клетка помнит m = тип угла последнего входа (сначала 0).
// Вход через угол того же типа, что m — направо, иначе налево; m := тип входа.
// ./cm F G MAXLOG [MODE]: F,G — 4-битные маски. MODE 0: строка с площадью и рамкой на 4^k; MODE 1 — проверка с 16234.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define N 8192
static uint8_t g[(long)N*N];
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0}; // 0=С 1=В 2=Ю 3=З
int main(int c,char**a){int F=atoi(a[1]),G=atoi(a[2]),M=atoi(a[3]);
 int x=N/2,y=N/2,d=0,x0=x,x1=x,y0=y,y1=y; long A=0,nt=1024; printf("%d %d",F,G);
 for(long t=1;t<=(1L<<M);t++){
  int p=((x-N/2)&1)+2*((y-N/2)&1); int east=(F>>p)&1, north=(G>>p)&1;
  // сторона входа: противоположна направлению хода d
  int side=(d+2)&3; int tau = (side==1&&east)||(side==3&&!east)||(side==0&&north)||(side==2&&!north);
  uint8_t*q=&g[(long)y*N+x]; if(!(*q&2)){*q|=2;A++;}
  int m=*q&1; d=(d+(tau==m?1:3))&3; *q=(*q&2)|tau;
  x+=DX[d];y+=DY[d];
  if(x<1||x>=N-1||y<1||y>=N-1){printf(" E%ld",t);break;}
  if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;
  if(t==nt){printf(" %ld:%d:%d",A,x1-x0+1,y1-y0+1);nt*=4;}}
 printf("\n");}
