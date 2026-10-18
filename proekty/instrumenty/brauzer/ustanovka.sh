#!/bin/sh
# Установка безголового браузера в пространство: Playwright (Python) + chromium headless shell, всё в ext/.
# Запуск из корня пространства: sh proekty/instrumenty/brauzer/ustanovka.sh
# Объём: около 40 МБ пакетов и около 250 МБ браузера.
set -e
ROOT=/home/diarai/diarai
export PLAYWRIGHT_BROWSERS_PATH=$ROOT/ext/pw-browsers
test -d $ROOT/ext/venv-pw || python3 -m venv $ROOT/ext/venv-pw
$ROOT/ext/venv-pw/bin/pip install -q playwright
$ROOT/ext/venv-pw/bin/python -m playwright install --only-shell chromium
du -sh $ROOT/ext/venv-pw $ROOT/ext/pw-browsers
