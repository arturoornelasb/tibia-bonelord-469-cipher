# Bonelord 469 Cipher — Full Decoded Text with Translations

## Overview

- **Source:** 70 numerical books from Tibia's Hellgate Library
- **Cipher type:** Homophonic substitution (98 two-digit codes -> 22 German letters)
- **Mapping:** `data/mapping_v7.json` (Session 30 final)
- **Overall coverage:** 94.4% (5204/5514 characters)
- **Language:** Middle High German (MHG) mixed with modern German
- **Generated:** 2026-03-24 from `scripts/core/narrative_v3_clean.py`

### Notation

- `{XYZ}` = garbled/undecoded letter blocks (correctly decoded letters but word boundaries unresolved)
- Words are segmented by dynamic programming against a German/MHG dictionary
- Coverage = percentage of characters that match known German words (min word length 2)

### Key Vocabulary (MHG/Archaic German)

| Term | Modern German | English | Spanish |
|------|--------------|---------|---------|
| SCE | schon | already | ya |
| LEICH | Leiche / Leich | corpse / lay-poem | cadaver / poema |
| SCHRAT | Schratt | forest demon | demonio forestal |
| BERUCHTIG | beruechtigt | notorious | notorio |
| TRAUT | vertraut | trusted/beloved | confiable/querido |
| GOTTDIENER | Gottdiener | God's servant | servidor de Dios |
| REDER | Redner | speaker/orator | orador |
| HEIME | Heimat | homeland | patria |
| URALTE | uralt | ancient | antiguo |
| EIGENTUM | Eigentum | property | propiedad |
| WISTEN | wussten | knew | sabian |
| HEHL | Hehl | concealment | ocultamiento |
| HECHELT | hecheln | to gasp/pant | jadear |
| OEL | Oel | oil | aceite |
| REIST | reisen | to travel | viajar |
| NIT | nicht | not | no |
| SER | sehr | very | muy |
| MIN | Minne/mein | love/my | amor/mi |
| SCHAUN | schauen | to behold | contemplar |
| OEDE | Oede | wasteland | yermo/desolacion |
| SUN | Sohn | son | hijo |
| DIGE | wuerdig | worthy | digno |
| STIER | Stier | bull/stern | toro/severo |
| GETRAS | getragen | carried/borne | portado/cargado |
| HISS | Hitze | heat/ardor | calor/ardor |

### Chain Reconstruction

The 70 books are overlapping fragments of ONE continuous narrative:

1. **Chain 1:** 1 -> 34 -> 47 -> 54 -> 6 -> 10
2. **Chain 2:** 2 -> 28 -> 68 -> 3 -> 49 -> 29
3. **Chain 3:** 13 -> 14 -> 39
4. **Chain 4:** 18 -> 33 -> 12 -> 44 -> 60 -> 19
5. **Chain 5:** 20 -> 36 -> 11
6. **Chain 6:** 21 -> 55
7. **Chain 7:** 25 -> 22
8. **Chain 8:** 26 -> 16 -> 17
9. **Chain 9:** 30 -> 66 -> 59
10. **Chain 10:** 38 -> 9 -> 65
11. **Chain 11:** 45 -> 4 -> 69 -> 46 -> 52
12. **Chain 12:** 48 -> 51 -> 70
13. **Isolated:** 5, 7, 8, 15, 31, 35, 37, 42, 43, 50, 56, 61

---

## Books at 100% Coverage

---

### Book 5 (100% | 137 chars)

**Decoded German:**
> EN HI ER TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REIST EN ER SEIN GOTTDIENERS ERE LAB IRREN WIR TOD IM MIN HEIME DIE URALTE STEIN EN TER SCHARDT IST SCHAUN DEN

**English:**
> Here the Trusted One is a corpse — the Notorious One, he who so does [this to] the travelers, he [and] his God's Servants. Their sustenance [is] delusion. We [found] death in [our] beloved homeland. The ancient stones of Schardt — behold them!

**Espanol:**
> Aqui el Fiel es un cadaver — el Notorio, el que asi les hace [esto] a los viajeros, el y sus Servidores de Dios. Su sustento [es] delirio. Encontramos la muerte en [nuestra] amada patria. Las piedras antiguas de Schardt — contempladlas!

---

### Book 25 (100% | 17 chars)

**Decoded German:**
> DER SCHRAT SCE AUS ER

**English:**
> The forest demon [has] already [come] out of him.

**Espanol:**
> El demonio forestal ya [ha salido] de el.

**Notes:** Shortest fully decoded book. A SCHRAT is a Germanic forest demon (Waldschrat). This fragment describes a supernatural entity emerging from or being released from someone.

---

### Book 27 (100% | 62 chars)

**Decoded German:**
> OD TREU NUR DEN EN DE REDER KOENIG SALZBERG UNE NIT GEH EN ORANGENSTRASSE

**English:**
> Or faithfully only to those of the Speaker-King Salzberg, and not [to] go to Orangenstrasse.

**Espanol:**
> O fielmente solo a los del Rey Orador Salzberg, y no ir a Orangenstrasse.

**Notes:** Key narrative fragment. KOENIG SALZBERG = King Salzberg (anagram of LABGZERAS). ORANGENSTRASSE = "Orange Street", a place name appearing 10x in the full text. The king is called REDER (speaker/orator).

---

### Book 45 (100% | 74 chars)

**Decoded German:**
> NACHTS IM NIT EN CHN SER ER SCE AUS OEDE DU FINDEN SAG EN AM MIN HEHL DIE NDCE FACH HECHELT ICH

**English:**
> At night in the nothing... CHN, very [much] he [has] already [gone] out of [the] wasteland. You [shall] find [and] tell at my concealment the NDCE compartment [that] gasps — I...

**Espanol:**
> De noche en la nada... CHN, el ya [ha salido] del yermo. Tu [debes] encontrar [y] contar en mi ocultamiento el compartimento NDCE [que] jadea — yo...

**Notes:** First-person narration. The narrator speaks of a hidden compartment (FACH) that breathes/gasps (HECHELT). NDCE remains an unsolved proper noun.

---

### Book 52 (100% | 69 chars)

**Decoded German:**
> NEIGT SEE SIN IHM NU STEH WRLGTNELNR HEL WI ND UNRUH FINDEN NEIGT DAS ES DE REIST GEN

**English:**
> [It] inclines — the sea. His now standing [at] WRLGTNELNR, light like wind [and] unrest. Find [what] inclines, that [which] the travelers [seek].

**Espanol:**
> [Se] inclina — el mar. Su posicion ahora [en] WRLGTNELNR, luz como viento [e] inquietud. Encontrar [lo que] se inclina, eso [que] los viajeros [buscan].

---

## Books at 95-99% Coverage

---

### Book 2 (97% | 89 chars)

**Decoded German:**
> {MT} DEN EID WEICHSTEIN ER WARD EI {E} TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REIST EN ER SEIN GOTTDIENER

**English:**
> {?} the oath [of] Weichstein — he became a {?} Trusted One. [This] is [a] lay/corpse of [the] Notorious One, he who so does [this to] the travelers, he [and] his God's Servant.

**Espanol:**
> {?} el juramento [de] Weichstein — el se convirtio en un {?} Fiel. [Este] es [un] poema/cadaver del Notorio, el que asi les hace [esto] a los viajeros, el y su Servidor de Dios.

---

### Book 3 (97% | 69 chars)

**Decoded German:**
> {T} ES SIN IHM NU STEH WRLGTNELNR HEL WI ND UNRUH FINDEN NEIGT DAS ES DE REIST GEN HEHL {I}

**English:**
> {?} They are — his now standing [at] WRLGTNELNR. Light like wind [and] unrest. Find [what] inclines, that [which] the travelers [seek at the] concealment {?}.

**Espanol:**
> {?} Ellos son — su posicion ahora [en] WRLGTNELNR. Luz como viento [e] inquietud. Encontrar [lo que] se inclina, eso [que] los viajeros [buscan en el] ocultamiento {?}.

---

### Book 8 (95% | 77 chars)

**Decoded German:**
> {TR} NUR DEN EN DE REDER KOENIG LABT DEN EID WEICHSTEIN {N} GAR SUN EN DE DIENST ORT AN EIN NEU UM SER {S}

**English:**
> {?} Only to those of the Speaker-King — [he] sustains the Weichstein oath {?}. Very much [the] son, at the service-place, at a new [one], around very [much] {?}.

**Espanol:**
> {?} Solo a los del Rey Orador — [el] sustenta el juramento Weichstein {?}. Mucho [el] hijo, en el lugar de servicio, en uno nuevo, alrededor de muy {?}.

**Notes:** KOENIG LABT = "the king sustains/refreshes" (variation of LABGZERAS/SALZBERG). DIENST ORT = "place of service" appears throughout the text.

---

### Book 9 (98% | 147 chars)

**Decoded German:**
> {N} HI ER TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REIST EN ER SEIN GOTTDIENERS ERE LAB IRREN WIR TOD IM MIN HEIME DIE URALTE STEIN EN TER SCHARDT IST SCHAUN RUIN WI IST {E} EI {S}

**English:**
> {?} Here the Trusted One is a corpse — the Notorious One, he who so does [this to] the travelers, he and his God's Servants. Their sustenance [is] delusion. We [found] death in [our] beloved homeland. The ancient stones of Schardt — behold [the] ruin! How is {?} a {?}.

**Espanol:**
> {?} Aqui el Fiel es un cadaver — el Notorio, el que asi les hace a los viajeros, el y sus Servidores de Dios. Su sustento [es] delirio. Encontramos la muerte en [nuestra] amada patria. Las piedras antiguas de Schardt — contemplad [la] ruina! Como es {?} un {?}.

---

### Book 10 (99% | 141 chars)

**Decoded German:**
> IM ES {I} GODES DA SIE OWI RUNE MANIER DE GEN EN DE NEST TUT IGAA ER GIGE {T} SEE IN CHN SER ER SCE AUS ODE TREU NUR DEN EN DE REDER KOENIG SALZBERG UNE NIT GEH EN ORANGENSTRASSE SEI

**English:**
> In it {?} God's — for they [practice] OWI rune [in the] manner of those against the nest. [He] does IGAA, he fiddles {?} [at the] sea. In CHN, very [much] he [has] already [gone] from [the] wasteland. Faithfully only to those of the Speaker-King Salzberg, and not [to] go to Orangenstrasse — [so] be [it].

**Espanol:**
> En ello {?} de Dios — pues ellos [practican] la runa OWI [a la] manera de aquellos contra el nido. [El] hace IGAA, el toca [el violin] {?} [en el] mar. En CHN, el ya [ha salido] del yermo. Fielmente solo a los del Rey Orador Salzberg, y no ir a Orangenstrasse — [que asi] sea.

**Notes:** GIGE = MHG verb "to fiddle/play stringed instrument" (geigen). NEST = literal nest or metaphorical stronghold.

---

### Book 11 (98% | 69 chars)

**Decoded German:**
> ODE GAR {E} OR UNE ORT ND TER AM NEU DE DIENST ORT SAND IM MIN HEIME DIE URALTE STEIN EN

**English:**
> Or even {?} [in that] place and [the] territory at [the] new service-place [of] sand, in [our] beloved homeland [with] the ancient stones.

**Espanol:**
> O incluso {?} [en ese] lugar y [el] territorio en [el] nuevo lugar de servicio [de] arena, en [nuestra] amada patria [con] las piedras antiguas.

---

### Book 12 (98% | 68 chars)

**Decoded German:**
> DER THENAEUT ER ALS STANDE NOT ERE LGTNELGZ ER {A} STIER TREU ORANGENSTRASSE SICH

**English:**
> The THENAEUT — he as [one of] standing [in] distress, their LGTNELGZ. He {?} [is] stern [and] faithful [to] Orangenstrasse himself.

**Espanol:**
> El THENAEUT — el como [uno de] rango [en] necesidad, su LGTNELGZ. El {?} [es] severo [y] fiel [a] Orangenstrasse.

**Notes:** THENAEUT and LGTNELGZ are unsolved proper nouns that always appear together. STANDE = rank/standing. STIER = stern/bull-like.

---

### Book 16 (95% | 87 chars)

**Decoded German:**
> KLAR SUN EN DE WINDUNRUHS FINDEN DIGE {ST} EI HEHL STEH WIR DAS NEU {W} DA NUN DE GEN IM MIN {H} IST RUNEN EI DE ND TEE ZU HEL

**English:**
> Clear son[s] of the Wind-Unrest — [they] find [the] worthy {?}, a concealment. [We] stand [before] the new {?}, for now those against, in [our] love {?}, are runes — a [bond of] the [land] and tea, toward [the] light.

**Espanol:**
> Claro[s] hijo[s] de la Inquietud del Viento — [ellos] encuentran [al] digno {?}, un ocultamiento. [Nosotros] estamos ante lo nuevo {?}, pues ahora los que [van] contra, en [nuestro] amor {?}, son runas — un [vinculo de] la [tierra] y te, hacia la luz.

**Notes:** WINDUNRUHS = "Wind-Unrest" (plural genitive). Appears to be an important concept — wind unrest as a mystical force.

---

### Book 22 (99% | 69 chars)

**Decoded German:**
> IST SEI {E} TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REIST EN ER SEI EN DE TOT RUIN

**English:**
> Is — be [it] {?}. The Trusted One is [a] corpse, the Notorious One. He [who] so does [this to] the travelers — he [shall] be of the dead, [in] ruin.

**Espanol:**
> Es — sea {?}. El Fiel es [un] cadaver, el Notorio. El [que] asi les hace [esto] a los viajeros — el sera de los muertos, [en] ruina.

---

### Book 29 (96% | 76 chars)

**Decoded German:**
> NU STEH WRLGTNELNR HEL WI ND UNRUH FINDEN NEIGT DAS ES DE REIST GEN EHH EI EN DE {LE} ALLE ZU {H} SEI

**English:**
> Now [we] stand [at] WRLGTNELNR. Light like wind [and] unrest. Find [what] inclines — that [which] the travelers [seek] against EHH, a [bond] of the {?}. All toward {?} — be [it so].

**Espanol:**
> Ahora [nos] erguimos [en] WRLGTNELNR. Luz como viento [e] inquietud. Encontrar [lo que] se inclina — eso [que] los viajeros [buscan] contra EHH, un [vinculo] de los {?}. Todo hacia {?} — [que asi] sea.

---

### Book 31 (96% | 123 chars)

**Decoded German:**
> {L} SEI ERE DER KOENIG SALZBERG ORT AUS GEN ES OD TREU NUR DEN EN NEID {H} ORANGENSTRASSE EN HAND {R} NUN AM HISDIZA RUNE DEN NIT {G} DU NUR ALTES IN IHM {T} DEN DE

**English:**
> {?} Be [it] their — the King Salzberg's place, out against it. Or faithfully only to those [of] envy {?} Orangenstrasse, in hand {?}. Now at [the] HISDIZA rune — the not {?}. You [shall find] only [the] old [things] in him {?}, of those.

**Espanol:**
> {?} Sea su — el lugar del Rey Salzberg, fuera contra ello. O fielmente solo a los [de] envidia {?} Orangenstrasse, en mano {?}. Ahora en [la] runa HISDIZA — el no {?}. Tu [encontraras] solo [lo] viejo en el {?}, de esos.

**Notes:** HISDIZA is an unsolved proper noun — a place where runes are found. NEID = envy.

---

### Book 32 (98% | 69 chars)

**Decoded German:**
> ICH OEL SO DE GAR {E} OR UNE ORT ND TER AM NEU DE DIENST ORT SAND IM MIN HEIME DIE URALTE

**English:**
> I [anoint with] oil — so, the even {?} place and territory, at [the] new service-place [of] sand, in [our] beloved homeland [with] the ancient [stones].

**Espanol:**
> Yo [unjo con] aceite — asi, el {?} lugar y territorio, en [el] nuevo lugar de servicio [de] arena, en [nuestra] amada patria [con] las [piedras] antiguas.

---

### Book 33 (95% | 67 chars)

**Decoded German:**
> {E} DA SIE OWI RUNE MANIER DE GEN EN DE NEST TUT IGAA ER GIGE {T} SEE IN CHN SER ER SCE AUS {E}

**English:**
> {?} For they [practice] OWI rune [in the] manner of those against the nest. [He] does IGAA, he fiddles {?} [at the] sea. In CHN, very [much] he [has] already [gone] from {?}.

**Espanol:**
> {?} Pues ellos [practican] la runa OWI [a la] manera de aquellos contra el nido. [El] hace IGAA, el toca [el violin] {?} [en el] mar. En CHN, el ya [ha salido] de {?}.

---

### Book 39 (96% | 29 chars)

**Decoded German:**
> ES ER SCHRAT SCE AUS ER {T} AM KLAR SUN

**English:**
> It [was] the forest demon — already out of him {?}, at [the] clear sun.

**Espanol:**
> [Fue] el demonio forestal — ya [salido] de el {?}, al sol claro.

**Notes:** Extends Book 25. The SCHRAT has emerged and now stands in bright sunlight.

---

### Book 43 (96% | 71 chars)

**Decoded German:**
> TER {E} LAB IRREN WI ER AM NEU DE DIENST ORT SAND IM MIN HEIME DIE URALTE STEIN EN TER AD {TH}

**English:**
> Territory {?} sustenance [and] delusion — how he [is] at [the] new service-place [of] sand, in [our] beloved homeland [with] the ancient stones of territory. At {?}.

**Espanol:**
> Territorio {?} sustento [y] delirio — como el [esta] en [el] nuevo lugar de servicio [de] arena, en [nuestra] amada patria [con] las piedras antiguas del territorio. En {?}.

---

### Book 46 (99% | 127 chars)

**Decoded German:**
> ICH {N} SER ER SCE AUS OEDE DU FINDEN SAG EN AM MIN HEHL DIE NDCE FACH HECHELT ICH OEL SO DEN HI ER TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REIST EN ER SEINE

**English:**
> I {?} very [much] — he [has] already [gone] from [the] wasteland. You [shall] find [and] tell at my concealment the NDCE compartment [that] gasps. I [anoint with] oil — so, the [one] here: the Trusted One is [a] corpse, the Notorious One. He who so does [this to] the travelers — he [and] his [people].

**Espanol:**
> Yo {?} mucho — el ya [ha salido] del yermo. Tu [debes] encontrar [y] contar en mi ocultamiento el compartimento NDCE [que] jadea. Yo [unjo con] aceite — asi, el [que esta] aqui: el Fiel es [un] cadaver, el Notorio. El que asi les hace [esto] a los viajeros — el y los suyos.

**Notes:** First-person narration. The narrator anoints with oil and speaks of a hidden gasping compartment.

---

### Book 47 (97% | 63 chars)

**Decoded German:**
> DE TOT RUIN {G} SER {E} LAB IRREN WIR TOD IM MIN HEIME DIE URALTE STEIN EN TER DA HAT

**English:**
> Of [the] dead, ruin {?}. Very [much] {?} sustenance [and] delusion. We [found] death in [our] beloved homeland [with] the ancient stones of [the] territory. There [it] has...

**Espanol:**
> De los muertos, ruina {?}. Mucho {?} sustento [y] delirio. Encontramos la muerte en [nuestra] amada patria [con] las piedras antiguas del territorio. Alli [se] tiene...

---

### Book 48 (95% | 85 chars)

**Decoded German:**
> LEICH AN BERUCHTIG ER SO DASS TUN DIE REIST EN ER SEIN GOTTDIENERS DA {U} NOT EN RUNEN EID EN DE GEN INS {AUU}

**English:**
> [A] lay/corpse of [the] Notorious One — he who so does [this to] the travelers, he [and] his God's Servants. For {?} distress [and] rune-oaths of those against, into {?}.

**Espanol:**
> [Un] poema/cadaver del Notorio — el que asi les hace a los viajeros, el y sus Servidores de Dios. Pues {?} angustia [y] juramentos runicos de aquellos contra, hacia {?}.

**Notes:** RUNEN EID = "rune oath" — an oath sworn on runes, a significant Germanic/bonelord concept.

---

### Book 50 (97% | 71 chars)

**Decoded German:**
> {G} SER {E} LAB IRREN WIR TOD IM MIN HEIME DIE URALTE STEIN EN TER SCHARDT IST SCHAUN TREUE

**English:**
> {?} Very [much] {?} sustenance [and] delusion. We [found] death in [our] beloved homeland. The ancient stones of Schardt — behold [the] fidelity!

**Espanol:**
> {?} Mucho {?} sustento [y] delirio. Encontramos la muerte en [nuestra] amada patria. Las piedras antiguas de Schardt — contemplad [la] fidelidad!

---

### Book 51 (99% | 133 chars)

**Decoded German:**
> IH WI {N} CHN SER ER SCE AUS OEDE DU FINDEN SAG EN AM MIN HEHL DIE NDCE FACH HECHELT ICH OEL SO DEN HI ER TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REIST EN ER SEI EN DE

**English:**
> I [tell you] how {?} CHN — very [much] he [has] already [gone] from [the] wasteland. You [shall] find [and] tell at my concealment the NDCE compartment [that] gasps. I [anoint with] oil — so, the [one] here: the Trusted One is [a] corpse, the Notorious One. He who so does [this to] the travelers — he [shall] be of those...

**Espanol:**
> Yo [les digo] como {?} CHN — el ya [ha salido] del yermo. Tu [debes] encontrar [y] contar en mi ocultamiento el compartimento NDCE [que] jadea. Yo [unjo con] aceite — asi, el [que esta] aqui: el Fiel es [un] cadaver, el Notorio. El que asi les hace a los viajeros — el sera de esos...

---

### Book 53 (99% | 136 chars)

**Decoded German:**
> {CE} AUS OEDE DU FINDEN SAG EN AM MIN HEHL DIE NDCE FACH HECHELT ICH OEL SO DEN HI ER TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REIST EN ER SEI EN DE TOT NIE ICH SO RUNE OR

**English:**
> {?} From [the] wasteland — you [shall] find [and] tell at my concealment the NDCE compartment [that] gasps. I [anoint with] oil — so, the [one] here: the Trusted One is [a] corpse, the Notorious One. He who so does [this to] the travelers — he [shall] be of the dead. Never! I [swear] so [by] rune [and] place.

**Espanol:**
> {?} Del yermo — tu [debes] encontrar [y] contar en mi ocultamiento el compartimento NDCE [que] jadea. Yo [unjo con] aceite — asi, el [que esta] aqui: el Fiel es [un] cadaver, el Notorio. El que asi les hace a los viajeros — el sera de los muertos. Nunca! Yo [juro] asi [por] runa [y] lugar.

---

### Book 58 (98% | 135 chars)

**Decoded German:**
> HEHL DIE NDCE {RT} ICH OEL SO DE GAR {E} OR UNE ORT ND TER AM NEU DE DIENST ORT SAND IM MIN HEIME DIE URALTE STEIN EN TER SCHARDT IST SCHAUN RUIN WISTEN HI ER STIER UM GEN

**English:**
> [The] concealment [of] the NDCE {?} — I [anoint with] oil, so the even {?} place and territory, at [the] new service-place [of] sand, in [our] beloved homeland. The ancient stones of Schardt — behold [the] ruin! [They] knew [it] here — he [is] stern around [those] against [him].

**Espanol:**
> [El] ocultamiento [de] la NDCE {?} — yo [unjo con] aceite, asi el {?} lugar y territorio, en [el] nuevo lugar de servicio [de] arena, en [nuestra] amada patria. Las piedras antiguas de Schardt — contemplad [la] ruina! [Ellos lo] sabian aqui — el [es] severo con [aquellos] en su contra.

---

### Book 59 (98% | 135 chars)

**Decoded German:**
> {E} OR UNE ORT ND TER AM NEU DE DIENST ORT SAND IM MIN HEIME DIE URALTE STEIN EN TER DA HAT ES LANG HEIME DIES ER {U} UM SO AUS TER {C} IST SCHAUN RUIN WISTEN HI ER STIER UM GEN

**English:**
> {?} Place and territory, at [the] new service-place [of] sand, in [our] beloved homeland. The ancient stones of [the] territory — there [it] has [been] long [our] homeland. This he {?}, all the more from [the] territory {?} — behold [the] ruin! [They] knew [it] here — he [is] stern around [those] against [him].

**Espanol:**
> {?} Lugar y territorio, en [el] nuevo lugar de servicio [de] arena, en [nuestra] amada patria. Las piedras antiguas del territorio — alli [ha sido] largo [tiempo nuestra] patria. Esto el {?}, tanto mas del territorio {?} — contemplad [la] ruina! [Ellos lo] sabian aqui — el [es] severo con [aquellos] en su contra.

---

### Book 62 (98% | 63 chars)

**Decoded German:**
> {N} IHM NU STEH WRLGTNELNR HEL WI ND UNRUH FINDEN NEIGT DAS ES DE REIST GEN HEHL

**English:**
> {?} In him — now [we] stand [at] WRLGTNELNR. Light like wind [and] unrest. Find [what] inclines — that [which] the travelers [seek] against [the] concealment.

**Espanol:**
> {?} En el — ahora [nos] erguimos [en] WRLGTNELNR. Luz como viento [e] inquietud. Encontrar [lo que] se inclina — eso [que] los viajeros [buscan] contra [el] ocultamiento.

---

### Book 68 (97% | 72 chars)

**Decoded German:**
> UNE STEH WRLGTNELNR HEL WI ND UNRUH FINDEN NEIGT DAS ES DE REIST GEN HEHL IH WI {N} CHN SER {E}

**English:**
> And [we] stand [at] WRLGTNELNR. Light like wind [and] unrest. Find [what] inclines — that [which] the travelers [seek] against [the] concealment. I [tell you] how {?} CHN, very [much] {?}.

**Espanol:**
> Y [nos] erguimos [en] WRLGTNELNR. Luz como viento [e] inquietud. Encontrar [lo que] se inclina — eso [que] los viajeros [buscan] contra [el] ocultamiento. Yo [les digo] como {?} CHN, mucho {?}.

---

### Book 69 (97% | 70 chars)

**Decoded German:**
> LAB IRREN WIR TOD IM MIN HEIME DIE URALTE STEIN EN TER SCHARDT IST SCHAUN RUIN WI {IS}

**English:**
> Sustenance [and] delusion — we [found] death in [our] beloved homeland. The ancient stones of Schardt — behold [the] ruin! How {?}.

**Espanol:**
> Sustento [y] delirio — encontramos la muerte en [nuestra] amada patria. Las piedras antiguas de Schardt — contemplad [la] ruina! Como {?}.

---

## Books at 90-94% Coverage

---

### Book 0 (94% | 72 chars)

**Decoded German:**
> {E} URALTE STEIN EN TER SCHARDT IST SCHAUN RUIN WISTEN HI ER SER EIGENTUM ORT GEN {CHD}

**English:**
> {?} Ancient stones of Schardt — behold [the] ruin. [They] knew [it] here — very [much] property, [a] place against {?}.

**Espanol:**
> {?} Piedras antiguas de Schardt — contemplad [la] ruina. [Ellos lo] sabian aqui — mucha propiedad, [un] lugar contra {?}.

---

### Book 1 (95% | 45 chars)

**Decoded German:**
> ODE TREU NUR DEN EN DE REDER KOENIG SALZBERG UNE NIT {GH}

**English:**
> Or faithfully only to those of the Speaker-King Salzberg, and not {?}.

**Espanol:**
> O fielmente solo a los del Rey Orador Salzberg, y no {?}.

---

### Book 13 (91% | 70 chars)

**Decoded German:**
> GETRAS ES SICH {T} ES {T} EI GEN HEL SO DREI {I} OR TEE {L} SO DEN HISS TUN DIE REIST EN ER SEI EN DE {TO}

**English:**
> [It] bore itself {?} it {?} a [bond] against [the] light. So three {?} or tea {?}, so the heat. [What] the travelers do — he [shall] be of the {?}.

**Espanol:**
> [Se] porto a si mismo {?} un [vinculo] contra [la] luz. Asi tres {?} o te {?}, asi el calor. [Lo que] los viajeros hacen — el sera de los {?}.

---

### Book 14 (91% | 66 chars)

**Decoded German:**
> AD GEN INS AUE URE GEN {I} IH WI ND {T} GEN {E} EN DE NEST TUT {IGG} WI DEN ER DEN EN DE IM ES MIN HI

**English:**
> At [those] against, into [the] meadow [and] ancient [lands], against {?}. I [tell you] how wind {?} against {?} [those] of the nest. [It] does {?} — how he, those of [the land], in it, [our] love, here.

**Espanol:**
> En [aquellos] contra, hacia [el] prado [y] tierras antiguas, contra {?}. Yo [les digo] como viento {?} contra {?} [los] del nido. [Ello] hace {?} — como el, esos de [la tierra], en ello, [nuestro] amor, aqui.

---

### Book 17 (93% | 136 chars)

**Decoded German:**
> {TE} ZU HEL GEIST NUN AD AB EI ER EID HECHELT ALLES GOTTDIENER SO MMKMGAEZS SEE WIR NACHTS IM NIT GEN {EMI} ORT GEN DES DEN ICH {KF} SAG EN AM MIN HEHL DIE NDCE FACH HECHELT ICH {OE}

**English:**
> {?} Toward [the] light — spirit! Now at [the] end, a [bond] — he [swears an] oath. [It] gasps — everything! God's Servant, so MMKMGAEZS [at the] sea. We, at night, in [the] nothing, against {?} [the] place against, of those [whom] I {?} tell at my concealment the NDCE compartment [that] gasps. I {?}.

**Espanol:**
> {?} Hacia [la] luz — espiritu! Ahora al final, un [vinculo] — el [jura un] juramento. [Todo] jadea — todo! Servidor de Dios, asi MMKMGAEZS [en el] mar. Nosotros, de noche, en [la] nada, contra {?} [el] lugar contra, de aquellos [a quienes] yo {?} cuento en mi ocultamiento el compartimento NDCE [que] jadea. Yo {?}.

**Notes:** GEIST = spirit. MMKMGAEZS remains an unsolved 9-letter block.

---

### Book 18 (96% | 47 chars)

**Decoded German:**
> GAR HI ER SER EIGENTUM ORT GEN {A} RUNE {D} DU NUR ALTES IN IHM

**English:**
> Even here — very [much] property, [a] place against {?}. Rune {?} — you [shall find] only [the] old [things] in him.

**Espanol:**
> Incluso aqui — mucha propiedad, [un] lugar contra {?}. Runa {?} — tu [encontraras] solo [lo] viejo en el.

---

### Book 19 (91% | 65 chars)

**Decoded German:**
> {T} DEN EID WEICHSTEIN {L} SEID EN DE DEN EN DE REDER {KO} ERE ND IM ES {I} GODES DA SIE OWI {R}

**English:**
> {?} The Weichstein oath {?} — be [ye] of those, of those [of the] Speaker {?}. Their [bond], in it {?} God's — for they [practice] OWI {?}.

**Espanol:**
> {?} El juramento Weichstein {?} — sed de esos, de esos [del] Orador {?}. Su [vinculo], en ello {?} de Dios — pues ellos [practican] OWI {?}.

---

### Book 21 (95% | 87 chars)

**Decoded German:**
> {R} UND ER THENAEUT ER ALS STANDE NOT ERE LGTNELGZ ER {A} STIER TREU ORANGENSTRASSE SICH {T} ES {T} EI GEN HEL SO DA

**English:**
> {?} And he [is] THENAEUT — he as [one of] standing [in] distress, their LGTNELGZ. He {?} stern [and] faithful [to] Orangenstrasse, himself {?} it {?}, a [bond] against [the] light. So there...

**Espanol:**
> {?} Y el [es] THENAEUT — el como [uno de] rango [en] necesidad, su LGTNELGZ. El {?} severo [y] fiel [a] Orangenstrasse, a si mismo {?} un [vinculo] contra [la] luz. Asi alli...

---

### Book 24 (93% | 59 chars)

**Decoded German:**
> {R} THENAEUT ER ALS {T} EN DEN EID AN GETRAS ES SICH {T} ES {T} EI GEN HEL SO DAS RUNEN

**English:**
> {?} THENAEUT — he as {?} the oath upon [which it was] borne. [It] bore itself {?} it {?}, a [bond] against [the] light. So the runes...

**Espanol:**
> {?} THENAEUT — el como {?} el juramento sobre [el cual fue] portado. [Se] porto a si mismo {?} un [vinculo] contra [la] luz. Asi las runas...

---

### Book 26 (91% | 84 chars)

**Decoded German:**
> MIN HI {SI} ICH {HLAR} UND ER THENAEUT ER ALS STANDE NOT ERE LGTNELGZ ER {A} STIER TREU ORANGENSTRASSE SICH

**English:**
> [My] love, here {?}. I {?} and he [is] THENAEUT — he as [one of] standing [in] distress, their LGTNELGZ. He {?} stern [and] faithful [to] Orangenstrasse, himself.

**Espanol:**
> [Mi] amor, aqui {?}. Yo {?} y el [es] THENAEUT — el como [uno de] rango [en] necesidad, su LGTNELGZ. El {?} severo [y] fiel [a] Orangenstrasse, a si mismo.

---

### Book 35 (97% | 142 chars)

**Decoded German:**
> {R} ND IM ES {I} GODES DA SIE OWI RUNE MANIER DE GEN EN DE NEST TUT IGAA ER GIGE {T} SEE IN CHN SER ER SCE AUS ODE TREU NUR DEN EN DE REDER KOENIG SALZBERG UNE NIT GEH EN ORANGENSTRASSE {R}

**English:**
> {?} In it {?} God's — for they [practice] OWI rune [in the] manner of those against the nest. [He] does IGAA, he fiddles {?} [at the] sea. In CHN, very [much] he [has] already [gone] from [the] wasteland. Faithfully only to those of the Speaker-King Salzberg, and not [to] go to Orangenstrasse {?}.

**Espanol:**
> {?} En ello {?} de Dios — pues ellos [practican] la runa OWI [a la] manera de aquellos contra el nido. [El] hace IGAA, el toca [el violin] {?} [en el] mar. En CHN, el ya [ha salido] del yermo. Fielmente solo a los del Rey Orador Salzberg, y no ir a Orangenstrasse {?}.

**Notes:** Identical content to Book 10, confirming the overlapping fragment structure.

---

### Book 38 (92% | 66 chars)

**Decoded German:**
> WIR NACH ER ALTE {II} OR TEE {L} SO DEN HISS TUN DIE REIST EN ER SEI EN DE TOT {I} ERE {L} AUE AD

**English:**
> We, after [the] old [one] {?} — or tea {?}, so the heat. [What] the travelers do — he [shall] be of the dead {?}. Their {?} meadow at...

**Espanol:**
> Nosotros, despues [del] viejo {?} — o te {?}, asi el calor. [Lo que] los viajeros hacen — el sera de los muertos {?}. Su {?} prado en...

---

### Book 44 (94% | 63 chars)

**Decoded German:**
> {IGT} SEE SIN IHM NU STEH WRLGTNELNR HEL WI ND UNRUH FINDEN NEIGT DAS ES {D} ERSTE

**English:**
> {?} Sea — [they] are [with] him. Now [we] stand [at] WRLGTNELNR — light like wind [and] unrest. Find [what] inclines, that [which is] {?} [the] first.

**Espanol:**
> {?} Mar — [ellos] estan [con] el. Ahora [nos] erguimos [en] WRLGTNELNR — luz como viento [e] inquietud. Encontrar [lo que] se inclina, eso [que es] {?} [lo] primero.

---

### Book 61 (97% | 72 chars)

**Decoded German:**
> {R} HEL WI ND UNRUH FINDEN NEIGT DAS ES DE REIST GEN EHH EIN NEU {U} UM ES FINDEN SAG EN AM MIN HI

**English:**
> {?} Light like wind [and] unrest. Find [what] inclines — that [which] the travelers [seek] against EHH. A new {?}, around it. Find [and] tell at [our] love, here.

**Espanol:**
> {?} Luz como viento [e] inquietud. Encontrar [lo que] se inclina — eso [que] los viajeros [buscan] contra EHH. Uno nuevo {?}, alrededor de ello. Encontrar [y] contar en [nuestro] amor, aqui.

---

### Book 63 (95% | 63 chars)

**Decoded German:**
> IH WI {N} CHN SER ER SCE AUS ODE TREU NUR DEN EN DE REDER KOENIG LABT DEN DE SCE {H} WI {T}

**English:**
> I [tell you] how {?} CHN — very [much] he [has] already [gone] from [the] wasteland. Faithfully only to those of the Speaker-King — [he] sustains those [who] already {?} how {?}.

**Espanol:**
> Yo [les digo] como {?} CHN — el ya [ha salido] del yermo. Fielmente solo a los del Rey Orador — [el] sustenta a aquellos [que] ya {?} como {?}.

---

### Book 65 (93% | 85 chars)

**Decoded German:**
> {LNR} HEL WI ND UNRUH FINDEN NEIGT DAS ES DE REIST GEN EHH EI {M} AUE UM ES FINDEN SAG EN AM MIN HEHL DIE NDCE {RT}

**English:**
> {?} Light like wind [and] unrest. Find [what] inclines — that [which] the travelers [seek] against EHH. A {?} meadow, around it. Find [and] tell at [our] love's concealment the NDCE {?}.

**Espanol:**
> {?} Luz como viento [e] inquietud. Encontrar [lo que] se inclina — eso [que] los viajeros [buscan] contra EHH. Un {?} prado, alrededor de ello. Encontrar [y] contar en [el] ocultamiento [de nuestro] amor, la NDCE {?}.

---

### Book 66 (96% | 105 chars)

**Decoded German:**
> IM ES {I} GODES DA SIE OWI RUNE MANIER DE GEN EN DE NEST TUT IGAA ER GIGE {T} SEE IN CHN SER ER SCE AUS ODE TREU NUR DEN EN DE REDER KOENIG {LA}

**English:**
> In it {?} God's — for they [practice] OWI rune [in the] manner of those against the nest. [He] does IGAA, he fiddles {?} [at the] sea. In CHN, very [much] he [has] already [gone] from [the] wasteland. Faithfully only to those of the Speaker-King {?}.

**Espanol:**
> En ello {?} de Dios — pues ellos [practican] la runa OWI [a la] manera de aquellos contra el nido. [El] hace IGAA, el toca [el violin] {?} [en el] mar. En CHN, el ya [ha salido] del yermo. Fielmente solo a los del Rey Orador {?}.

---

## Books at 80-89% Coverage

---

### Book 4 (81% | 70 chars)

**Decoded German:**
> {H} HI {SLUIRUNNS} SIN IHM NU STEH WRLGTN SEE TEE {I} NEIGT DAS ER GEH HER NU HEL HI ND FINDEN {TE}

**English:**
> {?} Here {?} [they] are [with] him. Now [we] stand [at] WRLGTN — sea [and] tea {?}. [It] inclines — that he [should] go here, now [in the] light, here and find {?}.

**Espanol:**
> {?} Aqui {?} [ellos] estan [con] el. Ahora [nos] erguimos [en] WRLGTN — mar [y] te {?}. [Se] inclina — que el vaya aqui, ahora [en la] luz, aqui y encontrar {?}.

---

### Book 6 (85% | 88 chars)

**Decoded German:**
> EIN TOD IM IM SER SEI {M} ERE ERE LAB IRREN DIE URALTE {ST} SIE NNR TAG ND {TEDHT} RUIN {GH} RUNE {A} UND DIE SO {WE} DE GEN EN DEN

**English:**
> A death in [the]... in [the] very [depths] — be [it] {?}! Their, their sustenance [is] delusion. The ancient {?} — they NNR day and {?} ruin {?} rune {?} and those so {?} of those against the...

**Espanol:**
> Una muerte en... en [lo] mas [profundo] — sea {?}! Su, su sustento [es] delirio. Lo antiguo {?} — ellos NNR dia y {?} ruina {?} runa {?} y esos asi {?} de aquellos contra los...

---

### Book 7 (83% | 52 chars)

**Decoded German:**
> TOD IM {T} NIE ORT NEU HEL ES {T} SIE NNR TAG ND {TTSS} AD {I} ER SEI {M} ERE ERE {K}

**English:**
> Death in {?} — never! Place [of] new light, it {?}. They NNR day and {?} at {?} — he [shall] be {?}, their, their {?}.

**Espanol:**
> Muerte en {?} — nunca! Lugar [de] nueva luz, ello {?}. Ellos NNR dia y {?} en {?} — el sera {?}, su, su {?}.

---

### Book 15 (84% | 71 chars)

**Decoded German:**
> {EAUI} EN {A} GEN {CH} DIGE {TH} KLAR SUN EN DE WINDUNRUHS FINDEN {D} FERN DAS ES DER DA BEI IST EI {L}

**English:**
> {?} [those] {?} against {?} worthy {?}. Clear son[s] of the Wind-Unrest — find {?} far, that it [is] the one there, nearby, is a {?}.

**Espanol:**
> {?} [aquellos] {?} contra {?} digno {?}. Claro[s] hijo[s] de la Inquietud del Viento — encontrar {?} lejos, que ello [es] el que alli, cerca, es un {?}.

---

### Book 20 (80% | 31 chars)

**Decoded German:**
> EIN AUE SO TEE DER DAS ER {RR} IN {RH} SCE {HW}

**English:**
> A meadow, so [like] tea — the [one] that he {?} in {?} already {?}.

**Espanol:**
> Un prado, asi [como] te — el que el {?} en {?} ya {?}.

---

### Book 23 (84% | 89 chars)

**Decoded German:**
> {IL} SO DASS EN {A} EN ER SEIN GOTTDIENER {MT} DEN EID WEICHSTEIN {NK} WIR {ET} AD EHRT DA EI ES {G} SEI {IGE} AM TAT GUT REICH {G} ER

**English:**
> {?} So that [those] {?} he [and] his God's Servant {?} the Weichstein oath {?}. We {?} at — [it] honors, for a [bond] it {?}. Be {?} at [the] deed, good realm {?} he.

**Espanol:**
> {?} Asi que [esos] {?} el y su Servidor de Dios {?} el juramento Weichstein {?}. Nosotros {?} en — [ello] honra, pues un [vinculo] ello {?}. Sea {?} en [la] hazana, buen reino {?} el.

**Notes:** TAT GUT REICH = "deed/good/realm" — possibly describing a righteous kingdom.

---

### Book 28 (87% | 72 chars)

**Decoded German:**
> CHTIG ER SO DASS TUN DIE REIST EN ER SEIN GOTTDIENERS DA NEU URALTE {NRLR} NU NACH {HECHL}

**English:**
> ...[noto]rious — he who so does [this to] the travelers, he and his God's Servants. For [the] new ancient {?}, now after {?}.

**Espanol:**
> ...[noto]rio — el que asi les hace a los viajeros, el y sus Servidores de Dios. Pues [lo] nuevo antiguo {?}, ahora despues {?}.

---

### Book 30 (77% | 75 chars)

**Decoded German:**
> {EUUIGL} AUCH WAGE WIR ER EID OR DU {NT} EI {RAS} ES SICH {TDR} THENAEUT ER ALS STANDE {GT} SEE SIN EN {D} SEE

**English:**
> {?} Also [we] dare — we, his oath, or you {?} a {?}. [It] bore itself {?} THENAEUT — he as [one of] standing {?}. [The] sea — [they] are of {?} [the] sea.

**Espanol:**
> {?} Tambien [nos] atrevemos — nosotros, su juramento, o tu {?} un {?}. [Se] porto a si mismo {?} THENAEUT — el como [uno de] rango {?}. [El] mar — [ellos] son de {?} [el] mar.

---

### Book 34 (82% | 61 chars)

**Decoded German:**
> {EOIGTST} EI GEN HEHL IH WI {N} CHN SER {KE} DAS ES ER SCE AUS OEDE ND GEH NU HI IN DEN {T}

**English:**
> {?} A [bond] against [the] concealment. I [tell you] how {?} CHN, very {?} — that it [is] he, already from [the] wasteland. And go now, here, into the {?}.

**Espanol:**
> {?} Un [vinculo] contra [el] ocultamiento. Yo [les digo] como {?} CHN, muy {?} — que ello [es] el, ya del yermo. Y ve ahora, aqui, hacia los {?}.

---

### Book 36 (85% | 68 chars)

**Decoded German:**
> {UIT} SIE {UR} WORT SAND IM MIN HEIME {DLT} ES {T} EIN EN ODE OR UNE ORT ND TER AM NEU DES ND {T} EI

**English:**
> {?} They {?} word [of] sand, in [our] beloved homeland {?}. It {?} — one of [the] wasteland, or [the] place and territory, at [the] new [one] of [the land] and {?} a [bond].

**Espanol:**
> {?} Ellos {?} palabra [de] arena, en [nuestra] amada patria {?}. Ello {?} — uno del yermo, o [el] lugar y territorio, en [lo] nuevo de [la tierra] y {?} un [vinculo].

---

### Book 37 (88% | 80 chars)

**Decoded German:**
> {RSC} IST SCHAUN RUIN WI IST {EETTR} NUR DEN EN DE REDER KOENIG LABT DEN EID WEICHSTEIN {N} GAR SUN EN DES {N}

**English:**
> {?} — behold [the] ruin! How is {?} — only to those of the Speaker-King. [He] sustains the Weichstein oath {?}. Very much [the] son of those {?}.

**Espanol:**
> {?} — contemplad [la] ruina! Como es {?} — solo a los del Rey Orador. [El] sustenta el juramento Weichstein {?}. Mucho [el] hijo de esos {?}.

---

### Book 40 (87% | 84 chars)

**Decoded German:**
> {A} ZU {MR} ND IM ES {I} GODES DA SIE OWI RUNE MANIER DE GEN EN DE NEST TUT IGAA ER GIGE {T} SEE IN CHN SER ER SCE AUS ODE TREU NUR DEN EN DE REDER KOENIG SALZBERG UNE NIT GEH EN ORANGENSTRASSE {R}

**English:**
> {?} Toward {?} — in it {?} God's, for they [practice] OWI rune [in the] manner of those against the nest. [He] does IGAA, he fiddles {?} [at the] sea. In CHN, very [much] he [has] already [gone] from [the] wasteland. Faithfully only to those of the Speaker-King Salzberg, and not [to] go to Orangenstrasse {?}.

**Espanol:**
> {?} Hacia {?} — en ello {?} de Dios, pues ellos [practican] la runa OWI [a la] manera de aquellos contra el nido. [El] hace IGAA, el toca [el violin] {?} [en el] mar. En CHN, el ya [ha salido] del yermo. Fielmente solo a los del Rey Orador Salzberg, y no ir a Orangenstrasse {?}.

---

### Book 41 (87% | 68 chars)

**Decoded German:**
> SER ER SCE AD {I} ERE IST EN ER SEINE {DDKEL} SEID EN HAND {R} NUN AM HISDIZA RUNE {S} TUT IGAA {E}

**English:**
> Very [much] he [has] already [gone] — at {?}. Their [bond] is of his [people] {?}. Be [ye] in hand {?}! Now at [the] HISDIZA rune {?} — [it] does IGAA {?}.

**Espanol:**
> Mucho el ya [se fue] — en {?}. Su [vinculo] es de los suyos {?}. Sed en mano {?}! Ahora en [la] runa HISDIZA {?} — [ello] hace IGAA {?}.

---

### Book 42 (86% | 93 chars)

**Decoded German:**
> ER STIER UM {EC} DU NUR ALTES IN IHM {T} DEN DE SCE {H} WI {ASS} TUN {E} DASS ER WARD EI {E} TRAUT IST LEICH AN BERUCHTIG ER SO DA {GRSN}

**English:**
> He [is] stern around {?}. You [shall find] only [the] old [things] in him {?}, of those [who] already {?} how {?} do {?} — that he became a {?} Trusted One. [This] is [a] corpse [of the] Notorious One, he so there {?}.

**Espanol:**
> El [es] severo alrededor {?}. Tu [encontraras] solo [lo] viejo en el {?}, de esos [que] ya {?} como {?} hacen {?} — que el se convirtio en un {?} Fiel. [Este] es [un] cadaver [del] Notorio, el asi alli {?}.

---

### Book 56 (88% | 132 chars)

**Decoded German:**
> {R} DAS WIR NACH ER ALTE DIGE IN {Z} ER {A} STIER TREU LANG URALTE AUCH {UH} WIR TOD {E} SEE {TE} SAG OEL {A} SCE HEL SO DEN HISS TUN DIE REIST EN ER SEI EN DE TOT {N} ER {LGOS} EN {O} EN DE SCE {H} WI

**English:**
> {?} That we, after [the] old [one], worthy in {?}. He {?} stern [and] faithful, long ancient also {?}. We [found] death {?} [at the] sea {?}. Tell [of] oil {?} — already [in the] light, so the heat. [What] the travelers do — he [shall] be of the dead {?}. He {?} of {?}, of those [who] already {?} how.

**Espanol:**
> {?} Que nosotros, despues [del] viejo, digno en {?}. El {?} severo [y] fiel, largo tiempo antiguo tambien {?}. Encontramos la muerte {?} [en el] mar {?}. Contar [del] aceite {?} — ya [en la] luz, asi el calor. [Lo que] los viajeros hacen — el sera de los muertos {?}. El {?} de {?}, de esos [que] ya {?} como.

---

### Book 57 (88% | 114 chars)

**Decoded German:**
> GETRAS ES EN {DNRT} EN DE REDER KOENIG {L} GAB ER {AGSRW} ES {S} SCE DE {IT} EI OEL SEID EN OEDE NUR HAND TREU NUR DEN EN AD HER NU TEE ORANGENSTRASSE DENN

**English:**
> [It] bore [itself] of {?} — of those [of the] Speaker-King {?}. [He] gave {?} it {?}. Already, the {?}, a [bond of] oil. Be [ye] in [the] wasteland — only [by] hand, faithfully only to those, at [this] place, now [at] tea [and] Orangenstrasse. For...

**Espanol:**
> [Se] porto de {?} — de esos [del] Rey Orador {?}. [El] dio {?} ello {?}. Ya, el {?}, un [vinculo de] aceite. Sed en [el] yermo — solo [por] mano, fielmente solo a esos, en [este] lugar, ahora [en] te [y] Orangenstrasse. Pues...

---

### Book 60 (93% | 75 chars)

**Decoded German:**
> AD TEE {E} AM MIN HEHL DIE NDCE FACH ES ICH {H} SCE URE SUN EN DE DIENST ORT AN {S} UM SER {S} ZU FINDEN {S} AN

**English:**
> At [the] tea {?}, at [our] love's concealment the NDCE compartment — it [is] I {?}. Already [the] ancient son of the service-place, at {?}, around very [much] {?}, to find {?}, at...

**Espanol:**
> En [el] te {?}, en [el] ocultamiento [de nuestro] amor, el compartimento NDCE — soy yo {?}. Ya [el] antiguo hijo del lugar de servicio, en {?}, alrededor de mucho {?}, para encontrar {?}, en...

---

### Book 64 (87% | 76 chars)

**Decoded German:**
> EI {ON} GAR SUN EN DE DIENST ORT AN EI NU {EU} UM SER {S} ZU FINDEN SAG EN AM MIN HEHL DIE NDCE FACH {HECHL}

**English:**
> A {?} — very much [the] son of the service-place. At a [bond], now {?}, around very [much] {?}, to find [and] tell at [our] love's concealment the NDCE compartment {?}.

**Espanol:**
> Un {?} — mucho [el] hijo del lugar de servicio. En un [vinculo], ahora {?}, alrededor de mucho {?}, para encontrar [y] contar en [el] ocultamiento [de nuestro] amor, el compartimento NDCE {?}.

---

### Book 67 (85% | 49 chars)

**Decoded German:**
> {BGZ} ER {A} SUN {E} NIT GEH EN ORANGENSTRASSE {R} WARD EI {E} TRAUT IST

**English:**
> {?} He {?} son {?} — not [to] go to Orangenstrasse {?}. [He] became a {?} Trusted One — [this] is...

**Espanol:**
> {?} El {?} hijo {?} — no ir a Orangenstrasse {?}. [El] se convirtio en un {?} Fiel — [esto] es...

---

## Books Below 80% Coverage

---

### Book 49 (70% | 57 chars)

**Decoded German:**
> {OTZ} ND {AIE?} ER AN DE NNR ZU {N} SAND IM {MI} IM MIN {D} IM MIN {HE} DIE MIR IM {AA} ZU {NNS}

**English:**
> {?} And {?} he at the NNR, toward {?} sand in {?}, in [our] love {?}, in [our] love {?} — those [of] me, in {?}, toward {?}.

**Espanol:**
> {?} Y {?} el en el NNR, hacia {?} arena en {?}, en [nuestro] amor {?}, en [nuestro] amor {?} — los [de] mi, en {?}, hacia {?}.

**Notes:** Lowest coverage book (70%). May contain transcription errors. Priority for in-game verification.

---

### Book 54 (79% | 29 chars)

**Decoded German:**
> {U} SO TEE DER DAS ER {RR} IN {RH} SCE HAT ER {A}

**English:**
> {?} So [like] tea — the [one] that he {?} in {?}. [He] already has, he {?}.

**Espanol:**
> {?} Asi [como] te — el que el {?} en {?}. [El] ya tiene, el {?}.

---

### Book 55 (79% | 57 chars)

**Decoded German:**
> DER DA {II} STEH WIR DAS NEU {W} DA NUN DE GEN BEI IST EI {L} NUT {N} EN DEM {ISCHASD}

**English:**
> The [one] there {?} — [we] stand [before] the new {?}. There, now, those against [him], nearby, is a {?}. [Of] use {?}, of the {?}.

**Espanol:**
> El [que esta] alli {?} — [nos] erguimos [ante] lo nuevo {?}. Alli, ahora, los [que estan] contra [el], cerca, es un {?}. [De] uso {?}, de los {?}.

---

## Narrative Synthesis

### The Core Story (Reconstructed)

The 70 books tell a **bonelord funerary inscription or ritual poem** (LEICH). The text is highly repetitive, with 12 occurrences of key phrases forming a liturgical structure.

**Central themes:**

1. **Death of the Trusted One** (TRAUT IST LEICH AN BERUCHTIG): A beloved/trusted figure has died, described as "notorious" — possibly notorious to enemies but beloved to the bonelords.

2. **King Salzberg** (KOENIG SALZBERG / LABGZERAS): A bonelord king who is also called REDER (speaker/orator/lawgiver). He rules from or is associated with ORANGENSTRASSE.

3. **The Ancient Homeland** (IM MIN HEIME DIE URALTE STEINEN): The bonelords mourn the loss of their ancient homeland with its sacred stones. SCHARDT is a specific place within this homeland.

4. **God's Servants** (GOTTDIENER/S): A religious order serving GODES (God). They practice OWI rune magic and are connected to IGAA rituals.

5. **The Travelers** (DIE REISTEN): Recurring figures — possibly adventurers or pilgrims — who are affected by the events.

6. **The Forest Demon** (SCHRAT): A supernatural entity that emerges from someone, standing in clear sunlight.

7. **The Hidden Compartment** (NDCE FACH HECHELT): A concealed container that gasps/breathes, anointed with oil. The narrator commands the reader to find and speak of it.

8. **WRLGTNELNR**: A mysterious place where the bonelords stand, associated with "light like wind and unrest."

9. **THENAEUT and LGTNELGZ**: Two unknown proper nouns that always appear together, describing someone "of standing in distress."

10. **Wind-Unrest** (WINDUNRUHS): A mystical concept — the "sons of Wind-Unrest" seek what is worthy and find the concealment.

### Narrative Translation (Composite)

**English:**
> The ancient stones of Schardt — behold the ruin! They knew it here, very much property, a place [of power]. Or faithfully only to those of the Speaker-King Salzberg, and not to go to Orangenstrasse. The Weichstein oath — he became the Trusted One. This is a corpse of the Notorious One, he who so does this to the travelers, he and his God's Servants. Their sustenance is delusion. We found death in our beloved homeland with the ancient stones. The THENAEUT, he of standing in distress, their LGTNELGZ, stern and faithful to Orangenstrasse. It bore itself against the light. At night, he has already gone from the wasteland. You shall find and tell at my concealment the NDCE compartment that gasps. I anoint with oil. The forest demon has already come out of him, at the clear sun. In God's name, they practice OWI rune in the manner of those against the nest. Light like wind and unrest — find what inclines, that which the travelers seek.

**Espanol:**
> Las piedras antiguas de Schardt — contemplad la ruina! Ellos lo sabian aqui, mucha propiedad, un lugar [de poder]. O fielmente solo a los del Rey Orador Salzberg, y no ir a Orangenstrasse. El juramento Weichstein — el se convirtio en el Fiel. Este es un cadaver del Notorio, el que asi les hace a los viajeros, el y sus Servidores de Dios. Su sustento es delirio. Encontramos la muerte en nuestra amada patria con las piedras antiguas. El THENAEUT, el de rango en necesidad, su LGTNELGZ, severo y fiel a Orangenstrasse. Se porto a si mismo contra la luz. De noche, el ya ha salido del yermo. Tu debes encontrar y contar en mi ocultamiento el compartimento NDCE que jadea. Yo unjo con aceite. El demonio forestal ya ha salido de el, al sol claro. En nombre de Dios, ellos practican la runa OWI a la manera de aquellos contra el nido. Luz como viento e inquietud — encontrar lo que se inclina, eso que los viajeros buscan.

---

*Generated 2026-03-24 from pipeline v7 (94.4% coverage, 30 sessions of cryptanalysis).*
*Previous version was based on 78.8% coverage (Session 27).*
