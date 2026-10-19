# Эльфийское в архиве

Начато 2026-10-19 по предложению автора («Не хочешь ли найти в архиве ещё что-нибудь на эльфийском?»).

**Как найдено.** `python3 -I proekty/instrumenty/elf_poisk.py --top 45 --min 4` считает в каждом тексте inbox слова, совпадающие с формами Eldamo. Сверху идут курс квенья и его копии (`book/`, `Доклад/ERTP/intro-quenya/`), Atanquesta, схема Eldamo. Не читанным оказалось одно: **`inbox/Доклад/ERTP/elvish-composition-archive/`**, зеркало *Elvish Composition Archive* v0.1.8 (4 марта 2024), сочинения участников Vinyë Lambengolmor (лицензия CC BY-NC-SA 4.0). Ещё раньше разобраны: `Suite_.txt`/`gyjth.txt` (авторский «Трактат» на квенья), «Справочник по эльфийским холмам» (`notes/kvenya-holmy.md`), «Noldolantë» и Маглор (`notes/maglor.md`), KRUMME SIEG (`notes/krumme-sieg.md`).

| Автор | Сочинение | Язык, год | Статус |
|---|---|---|---|
| Chaered | Tengwar ABC | Q, 2023 | не читано |
| Chaered | Gloomy March | Q, 2024 | не читано |
| Chaered | Ninya Masta | Q, 2024 | не читано |
| Delle | Nyare Pá i Corco | Q, 2023 | не читано |
| Ellanto | Ceraib Serthir | S, 2023 | не читано |
| Luinyelle | Vanima ná Valimar | Q, 2022 | прочитано без проверки (дневник 2026-10-19-0607) |
| Luinyelle | A Lirulin | Q, 2022 | не читано |
| Luinyelle | i Korko («Ворон» По) | Q, 2023 | разобран метр — `korko.md` |
| Luinyelle | Feanáron Pataka Vinya | Q, 2023 | не читано |
| В. Степанов | Hymn to Vinyë Lambengolmor | Q, 2022 | не читано |
| В. Степанов | Nalyë Melda | Q, 2023 | не читано |

Текстовые копии лежат в `ext/tmp/eca/` (не в репозитории; пересобрать — `html2txt.py`).
Инструменты: `elf_poisk.py` (поиск), `kv_udar.py` (ударение и метр квенья; `--test` — 19 примеров Толкина и курса).
