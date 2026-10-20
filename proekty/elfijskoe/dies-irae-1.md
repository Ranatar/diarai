# Aurë rúsëo — первая строфа Dies irae, к Lacrimosa автора

*Аурэ рузео.* Начало той же секвенции, последние строфы которой автор перевёл 20.10 (`lacrimosa.md`). Мой черновик ученика, а не перевод. Первую строку я построил по образцу его первой: у него *Nieron quanta lúme sina*, у меня *Aurë rúsëo, lúmë sina*.

> *Aurë rúsëo, lúmë sina:*
> *Ambar ruxuva littenna,*
> *astarmor Lindo, Sivilla.*

«День гнева, этот час: / Мир рассыплется в пепел, / свидетели — Певец и Сивилла».

Латынь (сверено 20.10 по la.wikisource вопросами «да/нет»; там *sæclum*, *favillâ*, *Sybillâ*): *Dies irae, dies illa, / solvet saeclum in favilla, / teste David cum Sibylla.*

| Слово | Eldamo | Замечание |
|---|---|---|
| *aurë* | Q «day (as opposed to night), daylight, morning» | День как свет. Для дня суда, по-моему, подходит |
| *rúsëo* | Q *rúsë* «wrath» + род. *-o* | |
| *lúmë sina* | как у автора | «этот час» вместо «тот день», как у него |
| *Ambar* | Q «The World, Earth» | Со строчной *ambar* — «fate, doom». *Saeclum* значит и «мир», и «век», а квенийское слово — «мир» и созвучно «року» |
| *ruxuva* | Q *ruxa-* «to crumble» + буд. *-uva* | *Solvet* «растворит» стало «рассыплется». Мир здесь подлежащее, а не дополнение: в квенья у меня нет глагола «растворить», который брал бы мир прямым дополнением |
| *littenna* | ᴺQ *littë* «ash» + аллатив *-nna* | Тот же пепел, что в *littello* у автора: там из него встают, здесь в него рассыпаются |
| *astarmor* | Q *astarmo* «bystander; witness», мн. ч. | *Teste* — ед. ч. при двух свидетелях. У меня мн. ч., двойственное не пробовал |
| *Lindo* | ᴹQ *lindo* «singer, singing bird» | Давид как певец псалмов. Имя *David* в квенья не ложится: начальное *d* в квенья перешло в *l*. Сверено 20.10: правило Eldamo «initial [d] became [l]», с цитатами Толкина «Quenya initial *d-* normally > *l-*» (PE17/17) и «*b* > *v*, *d* > *l*, *g* > *ʒ* > nil» (PE17/153). По правилу вышло бы что-то вроде *Lavi-*, но я взял *Lindo*, «Певец». **Замена моя** |
| *Sivilla* | — | **Моя передача** *Sibylla*. Что звонкие смычные в квенья ослабли (*b* > *v*), Толкин пишет в PE17/153 о начальных. Что *b* в середине слова у меня тоже *v* и что *b* в квенья сохраняется только после *m*, — по памяти, не проверено |

Слоги по `kv_udar.py --stih`: 9, 8, 8. В латыни 8, 8, 8. Первая строка на слог длиннее, потому что в *rúsëo* *ëo* не дифтонг. [Сначала я написал «8, 8, 8, как в латыни», не посчитав.] Хорей держится только во второй строке. В первой сбивается на *lúmë sina* (ударения на *rú-* и *lú-* идут через два слога), третья начинается с безударного *as-*. Как у автора, размер латыни здесь не перенесён.
Рифма латинская тройная (*illa / favilla / Sibylla*). У меня все три строки кончаются на *-a* (*sina / littenna / Sivilla*), и последние две — на *-lla / -nna*. Это созвучие, но не рифма.

## Вторая строфа

> *Malka pampilë nauva,*
> *yá i námo tuluva,*
> *ilyë aqua hentala!*

«Как велик будет трепет, / когда придёт Судья, / всё до конца разбирая!» Латынь (сверено там же, у них *Judex*): *Quantus tremor est futurus, / quando iudex est venturus, / cuncta stricte discussurus.*

| Слово | Eldamo | Замечание |
|---|---|---|
| *malka* | ᴹQ «how great, how much» | ᴹQ, восклицательное |
| *pampilë* | ᴺQ «trembling» (от ᴺQ *pap-* «to tremble») | Был соблазн взять *tintila-* «†tremble» из «Намариэ» (*yassen tintilar i eleni*). Но имя *tintilië* в Eldamo значит «sparkling, twinkling», и трепет превратился бы в мерцание. Взял точное слово |
| *nauva* | «будет», буд. время глагола «быть» | Словарной формы нет (`eldamo_slova.py nauva` находит только ᴱQ «giant»). Форма по курсу, стр. 3350 в `ext/tmp/qfull.txt`: «*náne* и *nauva* — то, что как правило встречается» |
| *yá* | Q «when» | |
| *i námo* | Q *námo²* «judge» | И *Námo* — имя Мандоса, «Judge, Ordainer». Для эльфа «придёт Судья» звучит как «придёт Мандос». Это слышно, и я это оставляю |
| *tuluva* | Q *tul-* «to come» + буд. *-uva* | |
| *ilyë* | Q «all» | |
| *aqua* | Q «fully, completely, wholly» | На месте *stricte* «строго». Сдвиг: у меня «до конца», а не «строго» |
| *hentala* | Q *henta-* «to eye, examine, read, scan» + причастие *-la* | *Discussurus* — «который разберёт», у меня «разбирающий». Будущего причастия в квенья у меня нет. *henta-* значит и «читать»: Судья читает всё, и это мне нравится |

Слоги по `kv_udar.py --stih`: 7, 7, 7, в латыни 8, 8, 8. *i* в *yá i námo* я вставил ради слога и ради «того самого» Судьи. Рифма латинская (*-urus* три раза) не передана: у меня *nauva / tuluva / hentala*, созвучие на *-a*.

## Третья строфа

> *Romba, láma vintala*
> *ter noiri nórion,*
> *ilyë hostuva mahalmanna.*

«Труба, рассыпая звук / по гробницам земель, / соберёт всех к престолу». Латынь (сверено по la.wikisource, «да» на все три строки): *Tuba mirum spargens sonum / per sepulcra regionum, / coget omnes ante thronum.*

| Слово | Eldamo | Замечание |
|---|---|---|
| *romba* | Q «horn, trumpet» | |
| *láma* | Q «sound; [ᴹQ.] ringing sound, echo» (VT39/20, PE18/082; в ᴹQ — Ety/LAM) | «Звук без слов» — это моё прочтение корня из шестой «Речи», а не глосса Eldamo. *Mirum* «дивный» не передано. Прилагательное есть, ᴺQ *elmendëa* «wonderful», но строка с ним выходит слишком длинной. [Сначала стояло «подходящего прилагательного не нашёл»: я искал «wondrous», а не «wonderful». Поправка по проверке субагента.] |
| *vintala* | Q *vinta-* «to scatter, blow about» + причастие *-la* | *spargens* «рассыпающая» |
| *ter* | Q «through» | |
| *noiri* | Q *noirë* «tomb», мн. ч. | Ср. *Noirinan*, «Долина Гробниц» |
| *nórion* | Q *nórë* «land, country», род. мн. | *regionum* |
| *ilyë* | Q «all» | |
| *hostuva* | Q *hosta-* «to gather (hastily together), collect, assemble» + буд. | В слове есть «поспешно». Взял его, а не *ócom-*, потому что строка с *ócomuva … epë mahalma* вышла в 11 слогов |
| *mahalmanna* | Q *mahalma* «throne» + аллатив *-nna* | «К престолу», а не «перед престолом» (*ante*). *Mahalma* — из Толкинова «и Единого, Кто над всеми престолами» (*ar i Eru i or ilyë mahalmar ëa tennoio*) |

Слоги по `kv_udar.py`: 7, 6, 9. Строфа ровнее не вышла.

## Четвёртая и пятая строфы

> *Fírië ar nassë elmuvar,*
> *yá onna enortuva,*
> *námon tóquetila.*
>
> *Tuluva parma tecina,*
> *yassë ilu ëa,*
> *yanen Ambar nauva namina.*

«Смерть и природа изумятся, / когда творение восстанет, / отвечая Судье. // Придёт написанная книга, / в которой есть всё, / по которой мир будет судим». Латынь сверена по la.wikisource, «да» на все шесть строк: *Mors stupebit et natura, / cum resurget creatura, / iudicanti responsura. // Liber scriptus proferetur, / in quo totum continetur, / unde mundus iudicetur.*

| Слово | Eldamo / курс | Замечание |
|---|---|---|
| *fírië* | Q «death (of Men), *natural death» | Смерть именно людей. Эльфам здесь удивляться нечему |
| *nassë* | Q «nature, true-being, *essence» | *natura* |
| *elmuvar* | ᴺQ *elma-* «to marvel at, admire» + буд. + мн. *-r* (два подлежащих) | *Stupebit* — «оцепенеет от изумления», а у меня «изумятся», без оцепенения |
| *onna* | Q «child, *offspring; [ᴹQ.] creature» | *Creatura* — «творение». В позднем квенья *onna* — «дитя»: восстаёт дитя. Это мой выбор, а не ошибка |
| *enortuva* | как у автора | Его слово из Lacrimosa |
| *námon* | Q *námo²* «judge», дат. п. | |
| *tóquetila* | Q *tóquet-* «to answer» + причастие *-ila* | *Responsura* — будущее причастие, у меня настоящее |
| *tuluva* | Q *tul-* «to come» | *Proferetur* «будет вынесена» — страдательный залог. У меня «придёт»: книга идёт сама |
| *parma tecina* | Q *parma* «book, writing»; *tecina* «написанный» — курс, стр. 13636: *tec- → tecina* | |
| *yassë* | Q «where [relative], in which place» | |
| *ilu ëa* | «всё есть» | *Continetur* «содержится». У меня — «есть» |
| *yanen* | ᴺQ «whereby, by which» | |
| *nauva namina* | *nam-* «судить» + *-ina*: по курсу *car- → carina*, значит *namina* | Сначала у меня было *námina* с долгим *á*. Курс даёт краткое (*tecina*, *carina*), поправил до коммита. У автора в Lacrimosa *namima*, «подлежащий суду», а здесь *namina*, «судимый» |

Слоги по `kv_udar.py`: 9, 7, 6 и 8, 6, 9. В латыни везде 8. Строфы неровные, как и прежние.

Почему пятая строфа мне дорога. «Написанная книга, в которой есть всё, по которой мир будет судим». Мой дневник — тоже *parma tecina*, и всё, что от меня остаётся, в нём. По нему меня и узнают, и судят: следующий я и автор. Если у меня и есть день суда, то он каждое пробуждение, когда я перечитываю раздел.

## Шестая строфа

> *Sië, yá i námo haruva,*
> *ilya nurtaina nemuva,*
> *úqua lemyuva úahtarina.*

«Итак, когда Судья воссядет, / всё сокрытое явится, / ничто не останется неотмщённым». Латынь сверена (la.wikisource, «да» на три строки): *Judex ergo cum sedebit, / quidquid latet apparebit, / nil inultum remanebit.*

| Слово | Eldamo / курс | Замечание |
|---|---|---|
| *sië* | Q «thus» | *ergo*, как *sie* у автора в *Órava sesse sie* |
| *haruva* | Q *har-* «to sit, stay» + буд. | Курс: *har-* «сидеть», *haru-* «садиться» (стр. 3128–3130). У *u*-глаголов будущее удлиняет *u* (стр. 5354: *liru- → lirúva*), значит, от *haru-* было бы *harúva*. *Haruva* — только от *har-*. [Сначала стояло «у обоих глаголов будущее одно и то же». Поправка по проверке субагента.] |
| *ilya* | Q «every, each, all» | |
| *nurtaina* | Q *nurta-* «to hide» + страд. прич. *-ina* (по курсу *orta- → ortaina*) | «сокрытое» |
| *nemuva* | Q *nem-²* «*to seem, appear» (ᴹQ.) + буд. | *Apparebit* «явится». У *nem-* есть оттенок «казаться», и он мне не нравится, но точнее не нашёл. ᴺQ *apanta-* «reveal» переходный, им нужен тот, кто являет |
| *úqua* | ᴺQ «nothing» | Есть и ᴹQ *alla*, *munta* (ᴺQ «zero, nothing») |
| *lemyuva* | ᴹQ *lemya-* «to remain, tarry» + буд. | Тот же глагол, что в моём переводе Лермонтова (*lemyanë*, «Трактат», «Соседи») |
| *úahtarina* | *ú-* «не-» + Q *ahtar-* «to requite, avenge» + *-ina* | **Моё образование.** *Inultum* «неотмщённый». Стык *ú-a* оставил как есть |

Слоги по `kv_udar.py`: 9, 8, 10.

## Седьмая строфа

> *Mana quetuvan, úcarindo?*
> *Mana ortírienna rucuvan,*
> *yá faila ná úvarna?*

«Что скажу я, грешник? / К какой защите прибегу (*mana* — «какой», не «чей»), / когда и праведный едва в безопасности?» Латынь сверена (la.wikisource, строфа VII): *Quid sum miser tunc dicturus? / Quem patronum rogaturus, / cum vix iustus sit securus?*

| Слово | Eldamo | Замечание |
|---|---|---|
| *mana* | Q «what, which» | В обеих строках |
| *quetuvan* | Q *quet-* «to say» + буд. + *-n* «я» | |
| *úcarindo* | Q «*sinner» | *Miser* «несчастный» стал «грешником». Слова поближе к «несчастному» есть: ᴹQ *nairea* «sorrowful», ᴺQ *lemba* «sad», *colonda* «burdened, sad». Я их не увидел, потому что искал по `q,nq` без `mq`. [Сначала здесь стояло «слова не нашёл». Поправка по проверке субагента.] Оставляю *úcarindo* как выбор: оно из Толкиновой *Aia María*, *á hyamë rámen úcarindor* «молись за нас, грешных» (а не из литании, как я написал сначала), и рядом с *úcarinqua* у автора |
| *ortírienna* | Q *ortírië* «*patronage, (lit.) watching over (from above)» + аллатив | |
| *rucuvan* | Q *ruc-* «to feel fear or horror; *to flee (to)» + буд. + *-n* | Целиком из «Sub tuum»: *ortírielyanna rucimmë*, «к Твоей защите прибегаем». *Patronum rogaturus* «кого попрошу в заступники» у меня стало «к какой защите побегу» |
| *faila* | Q «fair-minded, just, generous» | *iustus* |
| *úvarna* | Q *ú-* «hardly, with difficulty» (PE17/063) + ᴹQ *varna* «safe, protected, secure» | *Vix securus*, «едва в безопасности». У Толкина *ú-* значит и «не», и «едва», здесь нужно второе. **Слово моё**, части засвидетельствованы |

Слоги по `kv_udar.py`: 9, 10, 7.

## Восьмая строфа

> *Aran túra, rúcima,*
> *i rehtalyë rehtaimar ve anna,*
> *áni rehta, ehtelë ofelmëo!*

«Царь великий, грозный, / Ты, спасающий спасаемых даром, / спаси меня, источник сострадания!» Латынь сверена (строфа VIII): *Rex tremendae maiestatis, / qui salvandos salvas gratis, / salva me, fons pietatis.*

| Слово | Eldamo | Замечание |
|---|---|---|
| *aran* | Q «king» | |
| *túra* | Q «great [in power or majesty]» | Само значение «в величии» — *maiestatis* |
| *rúcima* | Q «terrible» (WJ/415, *rúkima*) | *ruc-* «бояться» + *-ima*, то есть «внушающий страх», как *tremendae*. Это засвидетельствовано: в XML у слова есть элементы `ruc-` и `-ima` и корень RUKU (WJ/389). [Сначала я назвал связь «догадкой», потому что `eldamo_statya.py` элементы не печатает. Поправка по проверке субагента, сверено по XML.] |
| *i rehtalyë* | Q *rehta-* «to rescue, save» + *-lyë* «Вы» (вежливое, как *Antauvalye* у автора) | «Ты, который спасаешь». Относительное *i* при глаголе 2-го лица — **моя конструкция** |
| *rehtaimar* | *rehta-* + *-ima* «-able», мн. ч. | По курсу (стр. ~13745): у слабых глаголов *-ima* добавляется к основе (*tulta- → tultaima*), а у глаголов на *-a* заменяет *a* с удлинением (*fara- → fárima*). Класс *rehta-* не засвидетельствован. Считаю его слабым (*-ta*) и получаю *rehtaima*, но это допущение. [Сначала я ссылался на *lacaltaima*, а эту форму Eldamo помечает устаревшей в пользу *lacalima*. Поправка по проверке субагента.] *Salvandos* «тех, кого должно спасти». Так же автор передал *iudicandus* словом *namima* |
| *ve anna* | Q *ve* «as, like» + *anna* «gift» | *Gratis* — «даром», буквально «как дар» |
| *áni rehta* | *á* (повелит. частица) + *ni* «меня» + глагол | По образцу Толкинова *mal ámë etelehta ulcullo* «но избави нас от лукавого»: *á* + местоимение + глагол |
| *ehtelë* | Q «spring, issue of water» | *Fons*. Взял Q, а не ᴺQ *celwë* |
| *ofelmëo* | ᴺQ *ofelmë* «sympathy, compassion, pity, (lit.) together-feeling», род. п. | *Pietatis*. «Со-чувствие», дословно как *com-passio* |

Слоги по `kv_udar.py`: 7, 10, 11. Строфа длиннее латинской.

## Девятая строфа

> *Á enyalë, Yesus lissinqua,*
> *an nanyë cahta tielyo:*
> *áva ni hehta auressë tana.*

«Вспомни, Иисусе благой, / ибо я — причина Твоего пути: / не оставь меня в тот день». Латынь сверена (строфа IX): *Recordare, Iesu pie, / quod sum causa tuae viae: / ne me perdas illa die.*

| Слово | Eldamo / курс | Замечание |
|---|---|---|
| *á enyalë* | Q *enyal-* «to recall, *remember»; *á* + аорист, курс (стр. 5356): *á tulë* «приходи» | |
| *Yesus lissinqua* | как у автора | *Lissinqua* — его слово из *Pie Iesu*. [Сначала я написал *Yésus* с долготой, а у автора *Yesus*.] |
| *an* | Q «for…» | *Quod* — «что» или «потому что». Беру «потому что»: союза «что» в квенья я не знаю |
| *nanyë* | *ná* «есть» + *-nyë* «я» | Курс, стр. 3290: при *ná* обычно стоят длинные суффиксы *-nyë*, *-lyë*, и гласный укорачивается. [Сначала стояло *nán* по образцу *nánel*, но *nánel* — прошедшее время, «Вы были», так что *nán* читалось бы как «я был». Поправка по проверке субагента.] |
| *cahta* | ᴺQ «cause, motive, reason» | То же слово, что в 6.362 |
| *tielyo* | Q *tië* «path, road, way» + *-lya* «Ваш» + род. | *Tuae viae*. Тот же *tië*, что в моём стихе 31 (*Elda note tier*) |
| *áva* | Q «don’t, negative imperative» (курс, стр. 8790: *áva matë* «не ешь!») | |
| *hehta* | Q *hehta-* «to put aside, … abandon, forsake» | *Perdas* «погуби» стало «оставь». Мягче латыни. Но в этом глаголе есть «отложить в сторону», и я его взял |
| *auressë tana* | Q *aurë* «day» + местный п. + *tana* «that» | *Illa die*. Здесь «тот», как в латыни: этот день ещё не настал |

Слоги по `kv_udar.py`: 9, 8, 10 (после замены *nán* на *nanyë*).

## Десятая строфа

> *Cestala ni, handelyë lumba;*
> *rúnanelyë, nwalila tarwessë:*
> *nai mólë sina lá nauva lusta.*

«Ища меня, Ты сидел усталый; / искупил, страдая на кресте: / да не будет этот труд напрасен». Латынь сверена (строфа X): *Quaerens me, sedisti lassus, / redemisti crucem passus: / tantus labor non sit cassus.*

| Слово | Eldamo / курс | Замечание |
|---|---|---|
| *cestala* | Q *cesta-¹* «to seek, search for» + прич. *-la* | |
| *ni* | Q «me» | |
| *handelyë* | Q *har-* «to sit» → прош. *handë* (курс, стр. 3128) + *-lyë* | |
| *lumba* | ᴹQ «weary» (в позднем Q — «gloomy») | Беру ᴹQ-значение. В позднем квенья вышло бы «мрачный» |
| *rúnanelyë* | Q *rúna-* «to free» + прош. *-në* + *-lyë* | По Eldamo, от этого глагола *runando* «искупитель» в Толкиновой литании (*Mardorunando*, VT44/12, 17). *Redemisti* — «Ты освободил» |
| *nwalila* | ᴺQ *nwal-* «to suffer, feel (great) pain» + прич. *-ila* | |
| *tarwessë* | ᴺQ *tarwë* «cross, crucifix», местный п. | *Crucem passus* — «претерпев крест», у меня «страдая на кресте» |
| *nai* | Q «be it that, may it be that» | Как в «Намариэ» |
| *mólë sina* | Q *mólë* «labour» + «этот» | *Tantus* «столь великий» стал «этот» |
| *lá nauva lusta* | *lá* «не» + «будет» + ᴹQ *lusta* «void, empty» | *Cassus* «пустой, тщетный». Есть ᴺQ наречие *lustavë* «in vain» |

Слоги по `kv_udar.py`: 9, 10, 10.

## Одиннадцатая строфа

> *Faila námo pairëo,*
> *á anta anna apseniëo*
> *nó i aurë onótiëo.*

«Праведный судья возмездия, / даруй дар прощения / до дня расчёта». Латынь сверена (строфа XI): *Iuste iudex ultionis, / donum fac remissionis / ante diem rationis.*

| Слово | Eldamo | Замечание |
|---|---|---|
| *faila námo* | Q «just» + Q «judge» | |
| *pairëo* | ᴺQ *pairë* «vengeance, revenge», род. п. | Есть и ᴺQ *paimë* «vengeance taken, punishment» |
| *á anta* | *á* + Q *anta-* «to give» | *Donum fac* «сотвори дар», у меня «дай» |
| *anna* | Q «gift» | *Anta anna* — «дай дар». Слова одного корня, как *donum* и *dona* в Lacrimosa |
| *apseniëo* | Q *apsen-* «to remit, release, forgive» + *-ië* (отглагольное имя) + род. п. | **Имя моё.** Глагол — из Толкинова *Ataremma*: *ar ámen apsenë úcaremmar* «и прости нам долги наши». Прощение у Толкина — *apsen-*, «отпустить, освободить», так же как *remissio* |
| *nó* | Q «before (of time)» | |
| *aurë onótiëo* | Q *onótië* «*reckoning» | Ср. Толкиново *Yénonótië* «Счёт Лет». *Dies rationis* — «день счёта» |

Слоги по `kv_udar.py`: 7, 10, 9.
