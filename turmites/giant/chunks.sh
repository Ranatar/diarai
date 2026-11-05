#!/bin/sh
# ./chunks.sh RULE NAME : гонит big кусками по 600 с, продолжая с ck/NAME; лог giant/log_NAME.txt
cd "$(dirname "$0")"
while true; do
  ./big $1 ck/$2 100000000000000 600 >> log_$2.txt 2>&1
  tail -n 1 log_$2.txt | grep -q "stop time" || break
done
