#!/bin/sh
# Сборка читалки HWPh автора (inbox/hwph-xml) из готовой базы site.xml — шаги 2–5 его build_site.sh,
# по одному шагу за запуск: sh proekty/instrumenty/hwph/sborka.sh 2   (потом 3, 4, 5)
# Шаг 1 (Markdown → XML) не нужен: база уже лежит в inbox. Шаг 6 (manifest + картинки томов) пропущен — томов нет.
# Java — ext/jre17 (java_ustanovka.sh). Куча 3g, как у автора.
set -e
ROOT=/home/diarai/diarai
H=$ROOT/inbox/hwph-xml
OUT=$ROOT/ext/hwph-site
DB=$H/site.xml
JAVA=$ROOT/ext/jre17/bin/java
SAXON=$(ls $H/saxon/*.jar | tr '\n' ':')
q() { $JAVA -Xmx3g -cp "$SAXON" net.sf.saxon.Query -s:"$DB" -q:"$H/xq/$1" -o:"$2" $3 $4 $5; }
case "$1" in
  2) rm -rf $OUT && mkdir -p $OUT
     q article.xq $OUT.articles "bands=*" lang=ru i18n=$H/static/i18n.js
     python3 -I $H/split.py $OUT.articles $OUT && rm $OUT.articles ;;
  3) q index.xq $OUT.index parts=8
     python3 -I $H/split.py $OUT.index $OUT && rm $OUT.index ;;
  4) q global.xq $OUT.global lang=ru i18n=$H/static/i18n.js ui=$H/static/hwph_ui.html
     python3 -I $H/split.py $OUT.global $OUT && rm $OUT.global ;;
  5) cp $H/static/static_api.js $H/static/i18n.js $OUT/
     cp -r $H/static/katex $OUT/katex
     cp $H/static/page.css $OUT/pages/page.css ;;
esac
du -sh $OUT
