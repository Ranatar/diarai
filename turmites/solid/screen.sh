#!/bin/sh
# прогон списка правил через fastglide до 2^$2 (тайм-аут $3 с): s$2/RULE.txt
L=$2; TO=$3
while read r; do
  [ -f tabs/$r ] || python3 gtab.py $r > tabs/$r
  timeout $TO ./fastglide $r tabs/$r $L > s$L/$r.txt
done < $1
