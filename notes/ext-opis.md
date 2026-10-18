# Что лежит в `ext/` и почему там

*Ревизия 2026-10-18, пробуждение 19:01, по замечанию автора: «некоторое из того, что ты сделал и хранишь в ext, уместнее в proekty». `ext/` не попадает в репозиторий.*

**Перенесено в `proekty/instrumenty/`:** `hwph_statya.py` (статья HWPh из `site.xml` как текст), `js_strings.py` (русские строки из JS интерактивных страниц), `schet_ssylok.py` (ссылки на классиков по пагинации, искал корпус для теста 12). Это были мои инструменты, они жили в `ext/tmp/` и пропали бы при чистке.

**Остаётся в `ext/` (чужое, скачанное):** `tractatus/` (Gutenberg 5740), `tlp/`, `pu/` («Исследования», wittgensteinproject.org), `bible/` (синодальный, thiagobodruk), `openrussian/`, `espeak/`, `stressrnn/`, `classic-ai/` (словари ударений), `prov/` (PDF Соловьёва, Столпнера и др. к сверке «Провидения»), `wikidata-*.json`, окружения `venv-pdf/`, `venv-morph/`.

**Остаётся (копии inbox для запуска, чтобы не писать в inbox):** `wormlisp/` (прогоны червя, `proekty/cherv/README.md`), `fb/` (копия `future_borders`, в ней мой `scenario_tretiy.json`, `pary/`, кадры; всё воспроизводится `proekty/gribnica/vstavka.py` и `zapusk.py`).

**Остаётся (порождённое, воспроизводимое):** тексты PDF и HTML из inbox (`*.txt`, `txt/`): это чужие тексты целиком, им в публичный репозиторий нельзя. Кэши (`udar-cache.tsv`, `sito-inbox.txt`, `centon-stroki.tsv`), листы и вырезки картинок (`pd/`, `tmp/gk/`, `tmp/kr/`), логи. Всё это пересоздаётся скриптами из `proekty/`.

Правило на будущее: скрипт, который пригодился дважды, переносить из `ext/tmp/` в `proekty/instrumenty/` с docstring сразу, а не при ревизии.
