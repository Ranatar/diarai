# Orbis pictus на квенья: пословная сверка с Eldamo (субагент, 19.10)

Предмет: `inbox/gyjth.txt` (перевод глав Invitatio, Deus, Mundus, Coelum, Metalla, Homo, Anima hominis, Eclipses, Prudentia из «Orbis sensualium pictus» Коменского). Латынь сверялась по `ext/orbis/pg28299.txt` (Gutenberg #28299).

## Метод

- Каждое знаменательное слово искалось в `inbox/eldamo/src/data/eldamo-data.xml` через `proekty/instrumenty/eldamo_slovo.py` (поиск по началу формы, диакритика не учитывается). Сначала искалась форма целиком, потом основа без падежных и глагольных окончаний (-nen, -sse, -llo, -nna, -o, -va, -r, -i; -s, -lye, -mme, -n, -ie, -ne, -iéva).
- **Ловушка с написанием.** Eldamo даёт ᴹQ/ᴱQ в старой орфографии: *qu* пишется как **q** (ilqa, qanta, qilta), *c* как **k** (kelure, tulko, kalya-), *x* как **ks** (maksa). Поэтому «не найдено» по одному ключу ничего не значит: `maxa` по префиксу находит только нq. *maxa-* «варить», а мQ. *maksa* «мягкий» всплыло лишь в обратном поиске по глоссе. Такие слова я переискивал во втором написании.
- Для слов, которых не нашлось, делался обратный поиск по латинскому смыслу через `eldamo_gloss.py`: soft, steel, quicksilver, coin, support/prop, cauldron, element, creature/animal, inhabit, ever, vocal/sounding, eclipse, darken/obscure, illuminate, moon, take away/deprive, back/crown of head, escape/fleeting, seize/catch, careful/cautious/heed, many, rib/Eve/threefold/trinity.
- Грамматические вопросы сверялись с курсом `ext/tmp/qfull.txt`: будущее совершенное -iéva (стр. 16072 и далее), причастия -ienwa и -iéla (13706–13720), прошедшее совершенное -iénë (16052).
- Слои: q — поздний квенья Толкина; mq — средний (1930–50-е); eq — ранний квенья (1910–20-е); nq — неоквенья (фанатское словотворчество, в Eldamo это помечено); «нет» — словарной статьи нет, слово, видимо, сложено переводчиком.
- В колонке «глосса» стоят английские глоссы Eldamo дословно (иногда с сокращениями). Курсив и вопросы со звёздочкой — тоже из Eldamo.
- Оценки: **ок** — подходит; **сдвиг** — значение уходит от латыни; **морф.** — сомнительная морфология; **нет** — не найдено; **?** — не уверен.

## Таблица

### Заглавие

| квенья | лемма | слой | глосса Eldamo | латынь | замечание |
|---|---|---|---|---|---|
| Ea | Eä | q | Creation, the (Material) Universe, Cosmos, World | Orbis | ок |
| appalie | appalë | nq | sense of touch, sensation, feeling [physical] | sensualium | ок, но это «осязание, физическое ощущение», а не «чувственное» вообще; написание -ie вместо -ë |
| emmainen | emma | q | *picture | pictus | ок; творительный мн. ч. «картинками» |

### Invitatio (Istyar ar yonyo)

| квенья | лемма | слой | глосса Eldamo | латынь | замечание |
|---|---|---|---|---|---|
| Istyar | istyar | mq | scholar, learned man, lore-master, wizard | Magister | ок |
| yonyo | yonyo | q | (big) boy, son | Puer | ок |
| Analelya | analelya- | nq | to approach | Veni | ок; голая основа как повелительное, без á |
| pare | par- | q | to learn (форма *pare* засвидетельствована, PE22/154) | disce | ок |
| na | ná/na | q | быть | (sapere) | «pare na nolmo» = «учись быть мудрецом» |
| nolmo | nolmo | q | wise person | sapere | **сдвиг**: глагол «быть мудрым» передан существительным «мудрец»; ср. «Mana na nolmo?» = «Что такое мудрец?» вместо «Что значит быть мудрым?». У eq. *nolmo* есть омоним «яма» (pit) |
| Mana | mana | q | what | Quid | ок |
| Ilqua | ilqa | mq | all the, the whole; everything, all | omnia | ок (в Eldamo ᴹQ *ilqa*) |
| valda | valda | nq/eq | worth; worthy, dear (нq. *valda-* «иметь значение») | necessaria | **сдвиг**: «ценное, значимое», а не «необходимое»; у q. *valda* есть омоним «возбуждённый, дикий» |
| térava | téra | mq | straight, right | recte | **морф.**: наречие обычно образуют на -vë; -va — это притяжательный падеж («прямого») |
| hanya | hanya- | mq | to understand, know about | intelligere | ок |
| care | car- | q | to do, make | agere | ок |
| nyare | nyar- | q | to relate, recite | eloqui | ок |
| Man | man | q | who | Quis | ок |
| onóltiéva | nolta- | nq | to teach, educate (lit. make knowledgable) | docebit | будущее совершенное (перфект o-nóltie + -va; по курсу это *(a)mátiéva*, из QVS 1948) = «научит (к тому времени)». **Сдвиг времени**: латынь — простое будущее |
| nye | nye | q | me | me | ок |
| si | si¹ / sí | q | this, here / now | hoc | ок (если si¹ «это») |
| Inye | inyë | q | I (emphatic) | Ego | ок |
| ó | ó | q | with | cum | ок |
| Eruo | Eru | q | God (род. п.) | DEO | ок |
| sámë | sámë | nq | salvation, saving, help | (нет) | **добавлено**: «с помощью Божьей» вместо «с Богом». Ср. q. *sáma* «ум» |
| Manen | manen | q | how | Quomodo | ок |
| Utúliévan | tul- | q | to come | Ducam | **сдвиг**: «приду / буду пришедшим» (будущее совершенное от «приходить»), а не «поведу». «Вести» — это *tulya-*, и переводчик сам ставит *tulyavalye* через две строки |
| lye | lye | q | you | te | ок |
| ter | ter | q/mq | through | per | ок |
| Atániévan | tana- | q | to show, indicate | Ostendam | ок по смыслу; время — будущее совершенное |
| éstiévan | esta-¹ | mq | to name | Nominabo | ок по смыслу; время — будущее совершенное. Строчная é в начале предложения — опечатка |
| Cene | cen- | q | to see, behold, look | En | ок («смотри») |
| sís | sís | q | here | adsum | ок |
| ean | ëa- | q | to be, exist | adsum | ок, но *ëa-* значит «существовать», а не «присутствовать» (ср. *ná*) |
| tulyavalye | tulya- | q | *to lead; to fetch | duc | **морф.**: после á стоит будущее время *tulya-va* + -lye (форма QVS без u); повелительное с будущим смешано |
| Eruva | Eru | q | — (притяж. п.) | DEI | ок |
| essenen | essë | q | name | in nomine | ок (творительный) |
| Nó | nó¹ | q | before (of time); at back (of place) | Ante | ок |
| ilu | ilu | q/mq | everything, all, the whole / universe, world | omnia | ок |
| mauralye | maura- | nq | to need, require | debes | ок |
| asamahti | asamahte | nq | simple, (lit.) easily handled | simplices | ок (мн. ч.) |
| lámar | láma | q | sound | Sonos | ок |
| yanen | yanen | nq | whereby, by which | ex quibus | ок (ед. ч. при мн. антецеденте) |
| pahta | pahta² | q | speech | Sermo | ок; есть омоним *pahta¹* «закрытый, частный» |
| Quendeva | Quendë | q | Elf | humanus | **сдвиг**: «эльфийская речь» вместо «человеческой» (подстановка мира) |
| partaima | parta- | nq | to arrange, compose, order | constat | **сдвиг**: -ima значит «составимая», а не «состоит» |
| celvar | celva | q | animal, living thing that moves | Animalia | ок |
| istar | ista- | q | to know | sciunt | ок |
| canta | canta- | q | ? (без глоссы, PE17/113); ср. canta² «shape» | formare | ? — глагол засвидетельствован, но без значения; вывод из *canta²* «форма» правдоподобен. Есть омоним *canta¹* «четыре» |
| lambalya | lamba | q | (physical) tongue | tua Lingua | ок |
| ista | ista- | q | to know | scit | ок |
| oveanta | ovëanta- | nq | to imitate, make like | imitari | ок |
| málya | má | q | hand | tua Manus | ок |
| emmata | emmata- | nq | to draw/create (a picture) | pingere | ок; латинское «potest» передано через *ista* «умеет» |
| Kato | kato | mq | afterwards | Postea | ок (написание с k, как в Eldamo) |
| minelélievamme | mina + lelya-¹ | q | into + to go, proceed | ibimus | будущее совершенное 1 мн. искл. (*elélie* + -va + -mme) с приставкой mina-/min- «в». **Морф.**: приставка дублирует аллатив *Eanna*; время — будущее совершенное |
| Eanna | Eä | q | World (аллатив) | Mundum | ок |
| ecénievamme | cen- | q | to see, behold | spectabimus | ок по смыслу; будущее совершенное |
| samelye | sam- | q | иметь | habes | ок (в курсе *sam-* «иметь»; отдельно не искал) |
| coiva | coiva | nq | lively, living; awake | vivum | ок |
| lámea | (láma + -ëa) | нет | — | (vocale) | **нет**: статьи нет; прозрачное «звучащий» от *láma*. Обратный поиск vocal/sounding дал только óma, ómanda, salamba |
| tengwasse | tengwassë | q | alphabet | (alphabetum) | ок: это само толкиновское слово «алфавит» (PE22/149), а не местный падеж от *tengwa*. В роли дополнения к *samelye* форма правильная |

### Deus (Eru)

| квенья | лемма | слой | глосса Eldamo | латынь | замечание |
|---|---|---|---|---|---|
| Eru | Eru | q | God | Deus | ок |
| ea | ëa- | q | to be, exist | est | ок |
| insello | insë | q | himself, herself (+ -llo) | ex seipso | ок, «из себя» |
| oirello / oirenna | oire | mq | everlasting (?age) | ab aeterno in aeternum | ок |
| Anilvanya | ilvan(y)a | q | perfect | Perfectissimum | ок (an- + превосходная степень) |
| anainima | aina + -ima | q (основа) | holy, revered | beatissimum | **морф.**: формы нет, -ima («способный быть») при *aina* неясно; смысл «святейший» близок к «блаженнейшему» |
| náve | návë | q | being | Ens | ок (есть омоним eq. *náve* «проницательность») |
| Ealaryo | ëala | q | spirit (not incarnate), being | Essentiâ | ок («его бытия») |
| súlea | súlë + -ëa | q (основа) | breath; (movement of) spirit | Spiritualis | производное «духовный» не засвидетельствовано, но прозрачно |
| er | er | q | one | unus | ок (отдельно не искал, общеизвестно) |
| Námieryo | námië | q | single judgment or desire | Hypostasi | **сдвиг**: *námië* — «отдельное суждение или желание», а не «ипостась» |
| nelinqua | (nel- + -inqua) | нет | — (нq. *nelqua* «угловатый», eq. *nelqa*) | Trinus | **нет**: «троичный» не найден; у Толкина есть *Neldië* «*Троица» (VT44). Искал nelinq, nelq, nelde, threefold/triple/trinity |
| Níraryo | níra | q | will (as a potential or faculty) | Voluntate | ок |
| aina | aina | q | holy | Sanctus | ок |
| faila | faila | q | fair-minded, just, generous | Justus | ок |
| óravinqua | órava- + -inqua | q (основа) | *to have mercy | Clemens | производное «милосердный» не засвидетельствовано, но правдоподобно |
| naite | naitë | q | true | Verax | ок |
| Turmeryo | turmë | nq | governing power, strength | Potentiâ | ок; *turmen* — «королевство» |
| antúra | túra | q | big, great | maximus | ок (an- + превосходная степень) |
| Máraleryo | máralë | q | goodness | Bonitate | ок |
| anmána | mána | q/mq | blessing, good thing (q) / blessed (mq) | Optimus | **сдвиг**: «преблагословенный»; «наилучший» было бы *anmára* |
| Nolweryo | nolwe | mq | wisdom, (secret) lore | Sapientiâ | ок |
| úlestaima | lesta- | nq | to measure | immensus | ок («неизмеримый»; ú- + -ima) |
| Cala | cala | q | light | Lux | ок |
| alacestaima | alacestima | nq | unsearchable | inaccessa | **сдвиг**: «неисследимый», а не «неприступный». Форма с -aima против нq. *alacestima* |
| hinna | hinna | mq | still; *hither (to us) | tamen | **сдвиг/?**: у Толкина это временное «всё ещё» (*i·aldar hinna ólar* «дерево всё ещё растёт», PE22/116), а не уступительное «однако». Переводчик последовательно ставит его на место *tamen* |
| ilu ilusse | ilu | q | everything, all | omnia in omnibus | ок |
| Ilinomesse | ilinomë | nq | everywhere | Ubique | **морф.**: местный падеж от наречия «везде» избыточен |
| alanomesse | ala- + nómë | нет | not + place | nullibi | **нет** как слово; прозрачно «в нигде» |
| Anhéra | héra | mq | chief, principal | Summum | ок |
| alme | almë | q | good (or blessed) thing, blessing | Bonum | ок |
| erya | erya | mq | single, sole | solus | ок |
| alaloitala | alaloitala | nq | unfailing | inexhaustus | ок (на основе q. *loita-* «упустить, не дотянуть») |
| celure | kelure | mq | fountain | Fons | ок (в Eldamo пишется с k, PE22/110) |
| ilya | ilya | q | all | omnium | ок |
| alimo | alima | q | fair, good | Bonorum | ок по смыслу; морф.: род. ед. при «всех благ» |
| Sívë … tambe | sívë¹, tambë | q | *as; *as, so | Ut … ita | ок (так в VT43) |
| Ontar | ontar | nq | parent (gender neutral) | Creator | **сдвиг**: «родитель», а не «творец»; ср. *Eruontarië* «Богородица» |
| Cáno | cáno | q | commander, chief(tain), ruler, governor | Gubernator | ок |
| Varno | varno | nq | protector, guard | Conservator | ок |
| nation | nat | q | thing | rerum | ок (род. мн.) |
| estalme | esta-¹ | mq | to name | vocamus | ок (1 мн. **искл.**; в главе Eclipses — *estalve*, 1 мн. **вкл.**: непоследовательно) |

### Mundus (Ea)

| квенья | лемма | слой | глосса Eldamo | латынь | замечание |
|---|---|---|---|---|---|
| Menel | menel | q | the heavens, firmament, sky | Coelum | ок |
| harya | harya- | q | to have | habet | ок |
| nár | nár | q | fire (as an element) | Ignem | ок |
| eleni | elen | q | star | Stellas | ок |
| Fanyar | fanya | q | (white) cloud | Nubes | ок |
| lingar | linga- | q | *to hang, dangle | pendent | ок |
| vilyasse | vilya | q | air, sky | in Aere | ок |
| Aiwi | aiwë | q | (small) bird | Aves | ок |
| wiler | wil- | mq | to fly | volant | ок |
| nu | nu | q | under | sub | ок |
| Lingwi | lingwë | q | fish | Pisces | ок |
| luter | lut- | q | to float | natant | ок |
| nénesse | nén | q | water | in Aqua | ок (долгота в падежной форме — вопрос) |
| Cemen | cemen | q | the earth | Terra | ок |
| ambor | ambo | q | hill, rising ground, mount | Montes | ок; **омоним**: мQ. *ambor* «грудь» |
| tauri | taurë | q | forest | Sylvas | ок |
| restar | resta | q | sown field, tilled ground | Campos | ок |
| nastor | nasto | mq | animal, beast | Animalia | ок: мн. ч. от мQ. *nasto* (найден обратным поиском; по префиксу *nastor* — 0) |
| Queni | quén | q | person, individual | Homines | ок |
| San | san | q | *then, so, thus | Ita | ок |
| analte | alta | mq | large, great in size | maxima | ок (an- + мн. ч.) |
| hroar | hröa | q | body, bodily form | Corpora | ок |
| Eava | Eä | q | — (притяж. п.) | Mundi | ок |
| ermastar | erma + ? | нет | erma: (physical) matter | Elementa | **нет**: *erma* «материя» + -sta(r)?; в нq «элемент» — это *sundë*. Искал erma, ermast, element |
| canta | canta¹ | q | four | quatuor | ок |
| nar | ná- | q | are | sunt | ок |
| quantaine | quanta | q | full, filled | plena | ок (мн. ч.) |
| vére | véra | q | personal, private, own | suis | ок (мн. ч.) |
| laulemontaron | laulemo | nq/eq | inhabitant | Habitatoribus | **морф./?**: правдоподобный разбор — *laulemo* + -nta «их» → *laulemonta*, род. мн. *-ron*: «их собственных обитателей». Слово взято из Qenya Lexicon 1910-х (eq), нq его повторяет |

### Coelum (Menel)

| квенья | лемма | слой | глосса Eldamo | латынь | замечание |
|---|---|---|---|---|---|
| pele | pel- | q | to go round, encircle | rotatur | ок |
| quilta | quilta- | nq | to gird, encircle | ambit | ок |
| ya | ya | q | which | (stantem) | ок |
| hara | har- | q | to sit, stay | stantem | ок, лёгкий сдвиг («сидит/пребывает» вместо «стоит») |
| humpe | humpe | mq | in the middle | in medio | ок |
| Anar | Anar | q | Sun | Sol | ок |
| nai | nai | q | maybe; be it that | (est) | ? — «пусть будет где угодно» передаёт «ubi ubi est» уступительно; натяжка, но допустимо |
| ainome | ainomë | nq | any place, anywhere | ubi ubi | ок |
| cale | cal- | q | to shine | fulget | ок |
| oio | oi(o) | q | ever, everlastingly | perpetuo | ок; у мQ. *oio* есть омоним «птица» |
| lan | lan | q | *while | ut ut (хотя) | **сдвиг**: «пока», а не «хотя» |
| fantaima | fanta- | q | to veil, cloak, mantle | eripiant | **сдвиг**: «скрываемый» (-ima) вместо «пусть отнимают» |
| mello | me + -llo | q | от нас (искл.) | a nobis | ок (в Eclipses — *vello*, вкл.) |
| lumboinen | lumbo | q | cloud; gloom, dark | densa Nubila | ок |
| tyare | tyar- | q | to cause | facit | ок |
| armaryainen | arma | q | ray of sunlight | Radiis suis | ок |
| áre | árë | q | sunlight | Lucem | ок |
| aure | aurë | q | day (as opposed to night), daylight | Diem | ок; «Lux Diem» опущено как отдельная мысль |
| Anqua | anqua | nq | opposite, against | Ex opposito | ок |
| so | so | q | его (род. отн.) | illius | ? (местоимение; отдельно не искал, по префиксу шум) |
| huine | huinë | q | gloom, darkness, deep shadow | Tenebrae | ок |
| epetai | epetai | q | consequently | inde | ок |
| lóme | lómë | q | night | Nox | ок |
| Lómesse | lómë | q | — (местн. п.) | Nocte | ок |
| cale | cal- | q | to shine | splendet | ок |
| Isil | Isil | q | Moon | Luna | ок |
| alcar | alca- | q | to glitter | micant | ок (мн. ч.); **омоним**: сущ. *alcar* «слава, сияние» |
| tintilar | tintila- | q | to twinkle, sparkle | scintillant | ок (так у Толкина в «Намариэ») |
| Sinyesse | sinye | mq | evening | Vesperi | ок |
| lúta | lúta- | nq/eq | to have time pass | est | **сдвиг**: «проходят сумерки» вместо «бывают» |
| undóme | undómë | q | twilight | Crepusculum | ок |
| Arinesse | arin | mq | morning | Manè | ок |
| lútar | lúta- | nq/eq | to have time pass | (est) | то же |
| amaurea | amaurëa | q | dawn, early day | Aurora | ок |
| ambaróne | ambarónë | q | dawn | Diluculum | ок |

### Metalla (Tincor)

| квенья | лемма | слой | глосса Eldamo | латынь | замечание |
|---|---|---|---|---|---|
| Tincor | tinco | q | metal | Metalla | ок |
| Canu | canu | nq | lead [metal] | Plumbum | ок (из eq. *Kanu*) |
| maxa | maksa | mq | soft, pliant | molle | ок. **Ловушка поиска**: по префиксу *maxa* есть только нq. *maxa-* «варить» |
| lunga | lunga | mq | heavy | grave | ок |
| Anga | anga | q | iron | Ferrum | ок |
| torna | torna | q | hard | durum | ок |
| anastorna | ana- + torna | q (основа) | hard | durior | сравнительная степень с ana- — неоконвенция; в статье *torna* стоит толкиновское *aristorna* (PE17/056) |
| tornanga | tornanga | q | hard-iron, iron hard (нq: *steel) | Calybs | **ок, и это находка**: слово Толкина, PE17/056; обычное нq. «сталь» — *axë* |
| Latúcenénen | latúcen | nq | tin [metal] | e Stanno | ок; творительный «из олова» |
| care | car- | q | to do, make | Faciunt | ок |
| yulmar | yulma | q | cup, drinking vessel | Cantharos | ок |
| úreyulmar | úrë + yulma | нет | úrë: heat | Ahena | **нет**: «чаши для жара» вместо «котлов»; в нq есть *tambin* «котёл» |
| urusenen | urus | q | copper (основа *urust-*, VT41/10) | e Cupro | **морф.**: творительный от основы *urust-* — *urustenen* |
| lícutulcor | lícuma + tulko | q + mq | taper, candle + support, prop | Candelabra | **нет** как слово; составное «опоры свечей», правдоподобно (*tulko* в Eldamo с k) |
| calasenen | calas | nq | brass (основа *kalass-*) | ex Orichalco | ок по смыслу; **морф.**: ожидалось *calassenen* |
| telpilini | telpilin | nq/eq | silver piece, *silver coin | Thaleros | **ок, точно**: монета из Qenya Lexicon |
| telpenen | telpë | q | silver | ex Argento | ок |
| maltastar | malta + ? | нет | malta: gold | Scutatos et Coronatos | **нет**: суффикс -star неясен; в eq «золотая монета» — *kulusta* |
| maltanen | malta | q | gold (metal) | ex Auro | ок |
| Coina | coina | nq | alive, living | Vivum | ок |
| telpe | telpë | q | silver | Argentum | ок (калька «живое серебро») |
| voro | voro | mq | ever, continually | semper | ок |
| sirea | sirea | mq | flowing, liquid | liquet | ок |
| nware | nwar- | q | to fret, wear away | corrodit | ок |

### Homo (Quen)

| квенья | лемма | слой | глосса Eldamo | латынь | замечание |
|---|---|---|---|---|---|
| Atan | Atan | q | Man, (lit.) the Second (People) | Adamus | **сдвиг/игра**: Адам назван «Человеком». Это калька еврейского *adam*, удачная |
| nér | nér | q | man, male person | Homo | ок |
| minya | minya | q | first | primus | ок |
| cántienwa | canta- | q | ? | formatus | **морф.**: страдательное причастие перфекта (*cárienwa* по PE17/68) с долгой á; глагол без глоссы |
| Erunen | Eru | q | — (творит. п.) | a Deo | ок |
| epe | epë | q | after (of time); before (in all relations but time) | ad | **сдвиг**: «перед своим образом», а не «по образу» |
| véra | véra | q | own | suam | ок |
| emmarya | emma | q | *picture | Imaginem | ок |
| ré | ré | q | day (sunset to sunset) | die | ок |
| enqueasse | enquëa | q | sixth | sextâ | ок |
| umbollo | umbo(n) | q | hill, lump, clump, mass | e Gleba | ок, хорошо |
| cemenva | cemen | q | earth | Terrae | ок |
| Enwe | ? | нет | — | Eva | **нет**: имени нет ни в одном слое (только Sindarin/Gnomish *enwe-* вне темы) |
| nís | nís | q | woman | mulier | ок |
| ambaxollo | ambo(s)? + axo¹ | нет | axo¹: bone; нq *ambos* «грудь», *amboraxosta* «грудная клетка» | e costâ | **нет** как слово; «грудная кость» — правдоподобная неоформа для «ребра» |
| nérva | nér | q | — (притяж. п.) | viri | ок |
| Esto | esto | q | they (emphatic dual) | Hi | **ок, тонко**: двойственное число для Адама и Евы |
| cúptienwe | cupta- | nq | to deceive, lie | seducti | ок (страд. прич. перфекта, мн.) |
| Melkornen | Melkor | q | — | à Diabolo | замена мира (Дьявол → Мелькор) |
| fanaryasse | fana | q | raiment, veil; (bright) shape or figure | sub specie | ок, точно |
| lóceva | lócë² | q | snake, serpent | Serpentis | ок |
| íre | íre² | mq | when | cum | ок |
| mátielanette | mat- | q | to eat | comederent | **морф.**: похоже на причастие перфекта *mátiéla* + прошедшее -ne + двойств. -tte; в курсе прошедшее совершенное — *(a)mátiénë* |
| nótime | nótima | q | countable, limited in number | de (fructu) | **сдвиг/?**: «немногие из плодов» — так передан партитив *de* |
| yávélion | yávë | q | fruit | fructu | ок: партитивное мн. *-li* + род. п.; долгая é лишняя |
| aldava | alda | q | tree | arboris | ок |
| avanwa | avanwa | q | refused, forbidden, banned | vetitae | ок |
| umbartienwe | umbarta- | q | to define, decree, destine | damnati | ок («обречённые») |
| unqualenna | unqualë | q | death agony | ad miseriam | **сдвиг**: «к предсмертной муке», а не «к бедствию» |
| fírienna | fírië | q | death (of Men) | mortem | ок |
| ilye | ilya | q | all | omni | ок |
| hilmittar | hilmë¹ + ? | нет | offspring, *descendant (нq) | posteritate | **нет**: суффикс -itta неясен |
| héctienwe | hehta- | q | to put aside, exclude, abandon, forsake | ejecti | ок по смыслу; **написание**: -ct- вместо -ht- |
| Amanello | Aman | q | Blessed Realm | e Paradiso | замена мира (рай → Аман) |

### Anima hominis (Quenva fea)

| квенья | лемма | слой | глосса Eldamo | латынь | замечание |
|---|---|---|---|---|---|
| Quenva | quén | q | person | hominis | ок |
| fea | fëa | q | (indwelling) spirit, soul | Anima | ок |
| coivie | coivië | q | life | vita | ок |
| hrondova | hrondo | q | (physical) body | corporis | ок |
| ilúveryasse | ilúvë | q | the whole, the all, allness | in toto | ок |
| erya | erya | mq | single, sole | una | ок |
| Rie | rië² | q | only | Tantùm | ок |
| ceula | ceula | q | ?alive (of vegetable) | Vegetativa | **ок, находка**: точное толкиновское слово |
| olvassen | olva | q | plant | in Plantis | ок |
| cityalea | cityalëa | nq | ticklish, susceptible, sensitive | Sensitiva | ок, но буквально «щекотливая» (из eq. *kitya-* «щекотать») |
| celvassen | celva | q | animal | in Animalibus | ок |
| an | an | q | for; and | Etiam | ок/? |
| handa | handa¹ | mq | understanding, intelligent | Rationalis | ок |
| quenessen | quén? | нет | — | in Homine | **морф./?**: местный мн. от *quén* ожидался бы как *quenissen*; существительного *quenessë* нет |
| telda | telda | q | last, final | (consistet) | **? / сдвиг**: «последний» сюда не подходит; фраза «Si telda neme nelnen» не разбирается |
| neme | nem-² | q/mq | *to seem, appear (ещё *nem-¹* «судить») | consistet | **?**: «кажется», а не «состоит» |
| nelnen | nel- (nelde) | q | three | in tribus | **морф.**: творительный от основы *nel-*, а не от *neldë* (ожидалось *neldenen*) |
| Handelenen | handele | mq | intellect | In Mente (Intellectu) | ок |
| names | nam- | q | to judge | cognoscit | ок, лёгкий сдвиг |
| hanyas | hanya- | mq | to understand | intelligit | ок |
| mane | manë | nq | good (moral) | bonum | ок; у мQ. *mane* есть омоним «кто» |
| ulca | ulca | q | evil | malum | ок |
| nanwa | nanwa¹ | q | existing, actual (true) | verum | ок |
| hya | hya¹ | q | or | vel | ок |
| vea | vëa¹ | q | seeming, apparent | apparens | **ок, точно** (PE17/189) |
| Níranen | níra | q | will | In Voluntate | ок |
| ciles | cil- | nq | to choose, select | eligit | ок |
| yestas | yesta- | mq | to desire | concupiscit | ок; у нq. *yesta-* значение «начинать» |
| auquers | auquer- | nq | to reject, (lit.) turn away | rejicit | ок по смыслу; **морф.**: аорист *auquere-s* усечён до *auquers* |
| munes | mun- | mq | to dislike, to not like | aversatur | ок |
| haninar | ? (hanya-?) | нет | — | cognitum | **нет**: форма не разбирается (причастие от *hanya-* было бы *hanyaina*) |
| Súlenen | súlë | q | breath; spirit | In Animo | ок |
| roitas | roita- | mq | to pursue | prosequitur | ок |
| cilina | cil- + -ina | nq | chosen | electum | ок |
| mána | mána | q | blessing, good thing | Bonum | ок |
| avaneves | avanev- | nq | to avoid, (lit.) refuse to face | fugit | ок |
| auquerina | auquer- | nq | rejected | rejectum | ок |
| ulco | ulco | q | evil | Malum | ок |
| Silo | silo | q | hence | Hinc | ок |
| estel | estel | q | hope, trust | Spes | ок |
| sosse | sossë | nq | fear | Timor | ок |
| íresse | írë | q | desire | in cupidine | ок |
| uhtiesse | uhta- | q | to dislike, feel disgust with, avoid | aversatione | ок (отглагольное на -ie) |
| emel | emel | q | love [abstract] | Amor | ок |
| alasse | alassë | q | happiness | Gaudium | ок |
| tyaliesse | tyalië | q/mq | mirth / play, game | in fruitione | **сдвиг**: «в веселье/игре», а не «в обладании» |
| nan | nan | mq | but, on the contrary | Sed | ок |
| rúse | rúsë | q | wrath | Ira | ок |
| nyére | nyérë | nq | grief | Dolor | ок |
| nwaliesse | nwal- | nq | to suffer, feel (great) pain | in passione | ок, хорошо |
| naite | naitë | q | true | Vera | ок |
| hanie | hanya- | mq | understand (отглаг. сущ.) | cognitio | ок; как сущ. не засвидетельствовано |
| engwion | engwë | q | thing [that exists] | rei | ок (род. мн. при лат. ед.) |
| nolme | nolmë | q | knowledge, philosophy (including science) | Scientia | **ок, точно** (PM/344) |
| laite | laitë | nq | false | falsa | ок; у мQ. *laite* есть омоним «цвет» |
| loima | loima | q | mistake | Error | ок |
| intya | intya | mq | guess, supposition, idea, notion | Opinio | ок |
| quistie | quista- | q | to suppose | Suspicio | ок по смыслу (отглаг. сущ.); нq. *quista* «предположение» |

### Eclipses (Halatier)

| квенья | лемма | слой | глосса Eldamo | латынь | замечание |
|---|---|---|---|---|---|
| Halatier / halatie | (hala + ?) | нет | hala: cast shadow | Eclipses / Eclipsin | **нет**: «затенение»; в нq «затмение» — *ulva*. Искал halat, eclipse, darken |
| celure | kelure | mq | fountain | fons | ок |
| ário | árë | q | sunlight | Lucis | ок |
| calyala | kalya- | mq | to illuminate | illuminans | ок (k/c) |
| ilquanna | ilqa | mq | everything | omnia | ок |
| Mal | mal | q | but | sed | ок |
| armaryar | arma | q | ray of sunlight | ejus radiis | ок |
| lá | lá¹ | q | no, not | non | ок |
| terer | ter- | nq/eq | to pierce | penetrantur | ок (страд. оборот передан действительным) |
| Imbar | Imbar | q | Habitation (= Земля) | Terra | ок |
| Itil | ? | нет | — (есть только q. *itila* «мерцающий») | Luna | **нет**: в квенья Луна — *Isil*; «Itil» похоже на синдаринское *Ithil* без th. Тот же текст выше пишет *Isil* — непоследовательно |
| nulle | nulla | mq | dark, dusky, obscure | opaca | ок (мн. ч.) |
| hrondor | hrondo | q | body | Corpora | ок |
| pan | pan | q | *since | nam | ок |
| halatter | (hala + -ta-?) | нет | hala: cast shadow | jaciunt umbram | **нет**: глагол «отбрасывать тень» в Eldamo не найден |
| anqua | anqua | nq | opposite | oppositum | ок |
| nómenna | nómë | q | place | in locum | ок |
| Etta | etta | q | *therefore | Ideo | ок |
| yá | yá | q | when | cum | ок |
| nalanta | nalanta- | nq | to attack, (lit.) fall upon | incidit | **сдвиг**: в нq это «нападает», буквально «падает на»; латынь — «попадает в» |
| Imbarva | Imbar | q | — | Terrae | ок |
| halanna | hala | q | cast shadow, *shade | in umbram | ок |
| nunurras | ? | нет | — | obscuratur | **нет**: искал nunur, nur-, darken/obscure/dim. Есть мQ. *nulla* «тёмный» |
| estalve | esta- | mq | to name | vocamus | ок (1 мн. вкл.) |
| Isilo | Isil | q | Moon | Lunae | ок |
| An | an | q | for | vero | ок |
| mene | men- | q | to go, proceed | currit | ок |
| imbe | imbë¹ | q | between, among | inter | ок |
| teteltas | telta- | mq | to canopy, overshadow, screen | obtegit | ок по смыслу; удвоение *te-* (перфект без -ie?) — **морф.?** |
| halaryanen | hala | q | cast shadow | umbrâ suâ | ок |
| si | si¹ | q | this | hoc | ок |
| Anaro | Anar | q | — | Solis | ок |
| telanta | ? | нет | — | adimit | **нет**: искал telant, take away/deprive (есть q. *nehta-* «лишать») |
| vello | ve² + -llo | q | us, we (inclusive) | nobis | ок |
| Anarva | Anar | q | — | Solis | ок |
| ehten | ehten | nq | outlook, sight, view, spectacle | prospectum | ок |
| Hinna | hinna | mq | still; *hither (to us) | tamen | см. ниже |
| moia | moia- | q | to labour, be afflicted (VT43/31) | patitur | ок по слову, точно |
| sinen | sinen | q | by this means, so | (aliquid) | «от этого» |
| nan | nan | mq | but, on the contrary | sed | ок |
| lá | lá¹ | q | no, not (есть и *lá²* «за, через, поверх») | nec | **отрицание перенесено**, см. ниже |

**Подозрение на обратный смысл.** В латыни: «nec tamen Sol patitur aliquid, sed Terra» — «однако Солнце ничего не претерпевает, а [претерпевает] Земля». Квенья: «Hinna Anar moia sinen nan lá Imbar».
- По словарю: hinna «всё ещё», Anar «Солнце», moia «страдает, претерпевает (be afflicted)», sinen «этим, от этого», nan «но», lá «не», Imbar «Земля». Получается: «Однако / всё ещё Солнце страдает от этого, но не Земля». **Это противоположно латыни**: отрицание стоит при Земле, а не при Солнце.
- Альтернативы, если разбирать честно:
  (a) Взять *moia* в старом активном значении «трудиться» (ᴹQ. *móta-* «трудиться»; Eldamo предлагает развести *moia-* «страдать» и *móta-* «трудиться» только в нq). Тогда: «Солнце по-прежнему трудится (светит), а Земля — нет». Смысл ближе к ситуации (свет теряет Земля), но расходится с латинским *patitur*, и *sinen* «от этого» так ложится плохо.
  (b) Взять *lá²* «за, поверх» — «но за пределами Земли»: синтаксически натянуто.
  (c) Взять *nan* как приставку «назад» — смысла не даёт.
- Вывод: при прямом словарном чтении это инверсия. Вероятная причина: переводчик понял *nec … sed* как «не … а» и поставил *lá* ко второму члену. Чтение (a) — единственное, при котором текст не ошибочен, но для него *moia* нужно взять в значении, которое Eldamo этому слову не приписывает.

### Prudentia (Incánusse)

| квенья | лемма | слой | глосса Eldamo | латынь | замечание |
|---|---|---|---|---|---|
| Incánusse | incánussë | q | mind mastership (PE17/088) | Prudentia | **ок, находка**: слово из имени Гэндальфа *Incánus* |
| oscene | os + cen- | nq + q | around + to see | circumspectat | **нет** как слово; прозрачная калька «осматривает» |
| ilqua | ilqa | mq | everything | omnia | ок |
| ve | ve¹ | q | as, like | ut | ок |
| lóce | lócë² | q | snake, serpent | Serpens | ок |
| munto | munta | nq/eq | *zero, naught, nothing | nihil | **морф.**: *munto* — это род. п. от *munta*; ожидался именительный *munta* |
| quete | quet- | q | to say, speak | loquitur | ок |
| sana | sana- | q | *to think, reflect | cogitat | ок |
| lustave | lustavë | nq | in vain, emptily | incassum | ок |
| Nócenes | nó¹ + cen- | q | before; at back (of place) + to see | Respicit | **нет** как слово; «смотрит назад» — правдоподобно |
| vanwienna | vanwie | mq | the past, past time | ad praeterita | ок |
| angalenna | angal | q | mirror | in Speculum | **ок, находка** (NM/350) |
| apacenes | apacen | q | foresight, *(lit.) after-sight | prospicit | **сдвиг части речи**: у Толкина это существительное, здесь оно глагол |
| tulurie | tulurya | mq | future, coming | Futura | **морф.**: форма на -ie не найдена; есть *tulurya* |
| metta | metta | q | ending, end | Finem | ок |
| palantírnen | palantír | q | far-seer | Telescopio | **ок, находка** |
| tuntas | tunta- | nq/eq | to notice, perceive | perspicit | ок |
| cárienwa | car- | q | — (*cárienwa* «уже сделанный», PE17/68) | quid egerit | ок |
| ancaruvaina | car- | q? | — | quid restet agendum | **морф.?**: будущее страд. причастие *caruvaina* (PE22/109) с приставкой an-; что даёт an-, неясно |
| Cardaryain | carda | q | deed | Actionibus suis | ок |
| ettulcas | et + tulca- | nq | to set up, establish | praefigit | ок |
| óripanta | óripanta | nq | sincere, honest, open | Honestum | ок |
| mára | mára | q/mq | good, useful, fit | Utilem | ок (в мQ значение «полезный») |
| nai | nai | q | maybe | si fieri potest | ок |
| alassea | alassëa | nq | joyful, happy | Jucundum | ок |
| induinen | indo | q | (state of) mind | (—) | добавлено «для умов» |
| Apa | apa¹ | q | after | (Fine prospecto) | ок |
| escenes | ? (et + cen-?) | нет | — | dispicit | **нет**: искал escen, es- |
| carmar | carma² | q | tool, implement, means | Media | **ок, точно** |
| tie | tië | q | path, road, way | Viam | ок |
| tulya | tulya- | q | to lead | ducit | ок |
| mettanna | metta | q | end | ad finem | ок |
| sinwe | sinwa | q | known, certain | certa | ок |
| ancárime | ancárima | q | easy, (lit.) very doable | facilia | **ок, точно** (PE22/155) |
| nótime | nótima | q | countable, limited in number | pauciora | ок |
| minome | minomë | nq | instead, in place of | potius quam | ок |
| line | ? (мQ. lia¹?) | ? | мQ. lia¹ «(not) a few, several»; мQ. líne «cobweb», eQ. líne «thread» | plura | **?**: разбор неясен; омоним «паутина» |
| tarastier | tarastië | nq | trouble | (impediat) | ок |
| avanevime | avanev- | nq | to avoid | ne … impediat | ок, пересказ |
| Cestas | cesta-¹ | q | to seek, search for | Attendit | ок, лёгкий сдвиг |
| ecesta | ecesta | nq | opportunity, chance | Occasioni | ок |
| finea | finëa | nq | downy, hairy | Capillata | ок |
| estirnë | estirnë | q | brow | Fronte | ок |
| parne | parnë | q | bald, bare, naked | calva | ок |
| casinga | cas + inga | q | head + top, highest point | vertice | **нет** как слово; составное «макушка» точное |
| ente | entë¹ | q | moreover, furthermore | adhaec | ок |
| rámaite | rámaitë | nq/eq | winged | alata | ок |
| aswanwaima | as(a)- + vanwa + -ima? | нет | asa-: «легко» (в *asamahte*, *asanótë*); vanwa: gone, lost | facile elabitur | **нет / ?**: возможно «легко исчезающий» (sv > sw); обратный поиск escape/fleeting дал только *us-*, *uswë*, eq. *luksima* |
| atesses | at- | nq | to catch, capture | captat | ок по корню; **морф.**: -sses не разбирается (может быть *ate-s* + *-se*) |
| Tienen | tië | q | path | In viâ | ок |
| menes | men- | q | to go, proceed | pergit | ок |
| ruave | rua + -ve | nq/eq | steady, still, tranquil | cautè | **сдвиг**: «спокойно, ровно», а не «осторожно» |
| cimbulave | cimba- + ? | nq? | cimba-: to care (нq); q. cimba: edge, brink | providè | **? / нет**: -ula- неясно; искал cimb, kimb, careful/heed |
| atáltiévas | atalta- | mq | to collapse, fall in, fall down | impingat | ок по смыслу; будущее совершенное |
| imístiévas | mista- | mq | to stray about | aberret | ок; будущее совершенное |

## Главное

1. **Будущее совершенное вместо простого будущего.** Это *utúliévan, atániévan, éstiévan, onóltiéva, minelélievamme, ecénievamme, atáltiévas, imístiévas*. Форма взята по курсу (QVS 1948, PE22/105): «-iéva — для действий, завершённых к другому будущему действию». Латинское простое будущее так получает оттенок «буду иметь показанным».
2. **utúliévan «ducam»** образовано от *tul-* «приходить», а не от *tulya-* «вести». Выходит «я приду / буду пришедшим», а не «поведу тебя».
3. **Затмение: «Hinna Anar moia sinen nan lá Imbar».** При словарном чтении сказано «Солнце страдает от этого, но не Земля», то есть обратное латыни. Безошибочное чтение возможно только при *moia* = «трудится», а этого значения Eldamo слову не даёт. Кроме того, *hinna* у Толкина значит «всё ещё», а не «однако».
4. **Точные находки переводчика из позднего Толкина:** *tornanga* «сталь» (PE17), *telpilini* «талеры = серебряные монеты» (QL), *ceula* «живой (о растениях)» = vegetativa, *vëa* «кажущийся» = apparens, *Incánussë* = Prudentia, *angal* «зеркало», *carma* «средство», *ancárima* «лёгкий», *nolmë* = scientia, *Esto* (двойственное число для Адама и Евы).
5. **Замены мира:** Quendeva «эльфийская» вместо «человеческой» речи, Melkor вместо Дьявола, Aman вместо рая, Atan («Человек») вместо Адама.
6. **Смысловые сдвиги:** námië «отдельное суждение» = Hypostasis; Ontar «родитель» = Creator; alacestaima «неисследимый» = inaccessa; nalanta «нападает» = incidit; lan «пока» = ut ut; lúta «проходит» = est; unqualë «предсмертная мука» = miseria; ruave «спокойно» = caute; apacen (существительное) как глагол.
7. **Морфология:** *urusenen* и *calasenen* образованы без учёта основ *urust-* и *calass-*; *munto* стоит вместо *munta*; *auquers* — усечённый аорист; *tulyavalye* смешивает будущее с повелительным; *térava* имеет окончание -va вместо -vë.
8. **Непоследовательности:** Луна — *Isil* и *Itil* (второго в квенья нет); «мы» — *estalme*/*mello* (исключающее) против *estalve*/*vello* (включающего).
9. **Ловушки поиска** (для меня самого): ᴹQ-слова надо искать в старом написании (ilqa, maksa, kelure, kalya-, tulko). *nastor* нашёлся только обратным поиском (мQ. *nasto*).

## Не найдены (статьи в Eldamo нет; искал основу и обратную глоссу)

- Прозрачные новообразования: lámea, alanomesse, oscene, nócenes, casinga, lícutulcor, ambaxollo, úreyulmar, súlea, óravinqua, anainima.
- Неясные: nelinqua, ermastar, maltastar, hilmittar, haninar, halatie/Halatier, halatter, nunurras, telanta, escenes, aswanwaima, cimbulave, Enwe, Itil, quenessen, line; фраза «telda neme nelnen».

Проверено около 300 вхождений по таблице (около 270 разных форм). Полностью не найдено 16 неясных и 11 прозрачных новообразований.
