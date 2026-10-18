#!/bin/sh
# JRE для сборки читалки HWPh (inbox/hwph-xml/jre — для Windows). Temurin 17, Linux x64, в ext/jre17.
set -e
ROOT=/home/diarai/diarai
mkdir -p $ROOT/ext/jre17-dl
cd $ROOT/ext/jre17-dl
curl -sSL -o jre.tar.gz "https://api.adoptium.net/v3/binary/latest/17/ga/linux/x64/jre/hotspot/normal/eclipse"
ls -la jre.tar.gz
mkdir -p $ROOT/ext/jre17
tar -xzf jre.tar.gz -C $ROOT/ext/jre17 --strip-components 1
rm jre.tar.gz
$ROOT/ext/jre17/bin/java -version
du -sh $ROOT/ext/jre17
