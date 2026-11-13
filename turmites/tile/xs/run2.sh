#!/bin/sh
# межпаркетная перепись отпечатков: ./run.sh N L DIR — N шагов, поле L, вывод в xs/DIR
cd "$(dirname "$0")/.."
N=$1; L=$2; D=xs/$3; mkdir -p $D
go(){ python3 -c "print('\n'.join(map(str,range($2))))" | ./vt$1 csig2 $N $L $3 > $D/$1_e$3.txt; }
go 4444 16 0; go 666 36 0; go 333333 9 0; go 3636 324 0; go 488 1024 4; go 488 1024 5; go 31212 1296 6; go 31212 1296 7; go 3464 5184 3
go 4612 82944 6 & go 4612 82944 7 & wait
