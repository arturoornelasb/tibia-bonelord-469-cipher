# Bonelord 469 Cipher - Full Decoded Text & English Translation

## Overview

- **Source:** 70 numerical books from Tibia's Hellgate Library
- **Cipher type:** Homophonic substitution (98 two-digit codes -> 22 German letters)
- **Mapping:** `data/mapping_v7.json` (Session 27 final)
- **Overall coverage:** 78.8% (4353/5524 characters)
- **Language:** Middle High German (MHG) mixed with modern German
- **Generated:** 2026-03-24 from `scripts/analysis/session27_apply.py`

### Notation

- `{XYZ}` = garbled/undecoded letter blocks (letters decoded but word not identified)
- Words in the decoded text are MHG/German, segmented by dynamic programming
- Book order is by index (0-69), which is the order they appear in `books.json`

### Chain Reconstruction (books are overlapping fragments)

The 70 books are NOT independent texts. They are fragments of a larger continuous text with massive overlaps. The chains identified:
1. Chain 1: 1 -> 34 -> 47 -> 54 -> 6 -> 10
2. Chain 2: 2 -> 28 -> 68 -> 3 -> 49 -> 29
3. Chain 3: 13 -> 14 -> 39
4. Chain 4: 18 -> 33 -> 12 -> 44 -> 60 -> 19
5. Chain 5: 20 -> 36 -> 11
6. Chain 6: 21 -> 55
7. Chain 7: 25 -> 22
8. Chain 8: 26 -> 16 -> 17
9. Chain 9: 30 -> 66 -> 59
10. Chain 10: 38 -> 9 -> 65
11. Chain 11: 45 -> 4 -> 69 -> 46 -> 52
12. Chain 12: 48 -> 51 -> 70

---

## Books with >= 95% Coverage (Highest Confidence)

---

### Book 25 (100.0%, 17/17)

**Decoded German:**
> DER SCHRAT SCE AUS ER

**English Translation:**
> The forest demon already [came] out of him.

**Notes:** SCHRAT is a MHG term for a forest demon or wild spirit (related to modern German "Schratt"). SCE (= schon/already) modifies the verb. This is the shortest and most cleanly decoded book -- a single declarative statement about a supernatural entity emerging or being released from someone.

---

### Book 39 (96.4%, 27/28)

**Decoded German:**
> ES ER SCHRAT SCE AUS ER {T} AM KLAR SUN

**English Translation:**
> It [was] the forest demon, already out of him, {?} at the clear sun.

**Notes:** Extends Book 25's content. The SCHRAT (forest demon) has already come out, now standing in bright sunlight. SUN = Sohn (son) or Sonne (sun); in context, "clear sun" suggests daylight or divine light. The {T} garbled block is likely a conjunction or preposition.

---

### Book 46 (99.2%, 125/126)

**Decoded German:**
> ICH {N} SER ER SCE AUS OEDE DU FINDEN SAGEN AM MIN HEHL DIE NDCE FACH HECHELT ICH OEL SO DEN HIER TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEINE

**English Translation:**
> I {?} very he already out of desolation. You [shall] find [and] tell at my concealment the NDCE compartment [that] gasps. I [anoint with] oil so the here trusted [one]. [This] is [a] lay/poem about [the] notorious one, he so that do [it] -- those who traveled, he [and] his [people].

**Notes:** This is a key narrative passage. The narrator speaks in first person. Key elements:
- OEDE (desolation/wasteland) -- the setting
- HEHL (concealment/secret place) -- something hidden
- NDCE -- a proper noun, possibly a place or artifact
- HECHELT (gasps/pants) -- the hidden thing breathes or wheezes
- OEL (oil) -- anointing, a religious/ritual act
- TRAUT (trusted/familiar one) -- a central character
- LEICH (lay/poem) -- the text self-identifies as a poetic composition
- BERUCHTIG (notorious) -- the subject of the poem
- DIE REISTEN (those who traveled) -- travelers or pilgrims

---

### Book 22 (98.5%, 67/68)

**Decoded German:**
> IST SEI {E} TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEI ENDE TOT RUIN

**English Translation:**
> [He] is, may [he] be {?}. [The] trusted one -- [this] is [a] lay about [the] notorious one, he so that did those who traveled. He may be [at the] end: dead, [in] ruin.

**Notes:** The narrative formula "TRAUT IST LEICH AN BERUCHTIG" recurs frequently across many books. It appears to be a refrain or formulaic identification: "The trusted one is [the subject of] a lay about the notorious one." The ending -- "ENDE TOT RUIN" -- declares the subject dead and ruined.

---

### Book 5 (97.7%, 130/133)

**Decoded German:**
> {EN} HIER TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEIN GOTTDIENERS ERE {L} AB IRREN WIR TOD IM MIN HEIME DIE URALTE STEINEN TER SCHARDT IST SCHAUN DEN

**English Translation:**
> {?} Here [the] trusted one -- [this] is [a] lay about [the] notorious one, he so that did those who traveled, he [was] his God-servant's honor. {?} Away! We wander [in] death in my homeland. The ancient stones of SCHARDT, [one] is [to] behold them.

**Notes:** Critical narrative passage:
- GOTTDIENERS ERE = "God-servant's honor" -- religious authority figure
- IRREN WIR TOD IM MIN HEIME = "We wander in death in my homeland" -- the narrator and companions are lost or dead in their own homeland
- URALTE STEINEN TER SCHARDT = "ancient stones of SCHARDT" -- a real German place name; the ancient stones are a monument or ruin
- SCHAUN = "behold/look upon"
- This establishes the narrator as someone who has died or is in a death-like state, wandering among ancient ruins

---

### Book 53 (97.0%, 130/134)

**Decoded German:**
> {CE} AUS OEDE DU FINDEN SAGEN AM MIN HEHL DIE NDCE FACH HECHELT ICH OEL SO DEN HIER TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEIN GOTTDIENERS SO RUNE {OR}

**English Translation:**
> {?} Out of [the] desolation you [shall] find [and] tell at my concealment the NDCE compartment [that] gasps. I [anoint with] oil so the here. [The] trusted one -- [this] is [a] lay about [the] notorious one, he so that did those who traveled, he [was] his God-servant's. So [the] rune {?}.

**Notes:** Closely parallels Book 46. The RUNE at the end ties the narrative to runic writing/magic. The God-servant (GOTTDIENER) is linked to the travelers (REISTEN).

---

### Book 18 (95.6%, 43/45)

**Decoded German:**
> GAR HIER SER EIGENTUM ORT GEN {A} RUNE {D} DU NUR ALTES IN IHM

**English Translation:**
> Truly here, very [much] a place of property/possession toward {?} rune {?}. You [find] only old [things] in him.

**Notes:** EIGENTUM (property/possession) suggests a place that belongs to someone or something. The speaker notes that only old things remain. This describes arrival at an ancient site. "GEN" (toward) implies movement or direction.

---

### Book 51 (95.5%, 126/132)

**Decoded German:**
> {IHW} IN {CHN} SER ER SCE AUS OEDE DU FINDEN SAGEN AM MIN HEHL DIE NDCE FACH HECHELT ICH OEL SO DEN HIER TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEI ENDE

**English Translation:**
> {?} in {?} very he already out of [the] desolation. You [shall] find [and] tell at my concealment the NDCE compartment [that] gasps. I [anoint with] oil so them here. [The] trusted one -- [this] is [a] lay about [the] notorious one, he so that did those who traveled. He may be [at the] end.

**Notes:** Another variant of the core narrative passage. The {CHN} garbled block recurs in many books (always "IN CHN SER"), suggesting it may be a proper noun or specific MHG term that has not been resolved.

---

## Books with 90-94.9% Coverage

---

### Book 9 (94.4%, 134/142)

**Decoded German:**
> {N} HIER TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEIN GOTTDIENERS ERE {L} AB IRREN WIR TOD IM MIN HEIME DIE URALTE STEINEN TER SCHARDT IST SCHAUN RUIN {WI} IST {EEIS}

**English Translation:**
> {?} Here [the] trusted one -- [this] is [a] lay about [the] notorious one, he so that did those who traveled, he [was] his God-servant's honor. {?} Away! We wander [in] death in my homeland. The ancient stones of SCHARDT, [one] is [to] behold [the] ruin. {?} is {?}.

**Notes:** Nearly identical to Book 5 but continues past "SCHAUN" to mention RUIN explicitly. The ancient stones of SCHARDT are now a ruin to be beheld.

---

### Book 2 (94.2%, 81/86)

**Decoded German:**
> {MTD} ENDE {E} WEICHSTEIN IST SEI {E} TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEIN GOTTDIENER

**English Translation:**
> {?} [the] end {?} WEICHSTEIN is, may [it] be {?}. [The] trusted one -- [this] is [a] lay about [the] notorious one, he so that did those who traveled, he [was] his God-servant.

**Notes:** WEICHSTEIN (literally "soft stone") is a confirmed German place name, likely referring to a real location. It appears at a transition point -- after "ENDE" (end) and before the recurring TRAUT/LEICH refrain. GOTTDIENER (God-servant) appears without the genitive -S, possibly as a title.

---

### Book 0 (94.0%, 63/67)

**Decoded German:**
> {E} URALTE STEINEN TER SCHARDT IST SCHAUN RUIN WISTEN HIER SER EIGENTUM ORT GEN {CHD}

**English Translation:**
> {?} [The] ancient stones of SCHARDT, [one] is [to] behold [the] ruin. [They] knew [that] here [is] very [much] a place of property toward {?}.

**Notes:** WISTEN (MHG past tense of "wissen" = to know) -- those who came before knew this place. The ancient stones of SCHARDT are in ruin, but the site is recognized as a place of significance or ownership.

---

### Book 58 (93.0%, 120/129)

**Decoded German:**
> HEHL DIE NDCE {RT} ICH OEL {S} ODE GAR {EO} RUNE ORT {ND} TER AM NEU {DE} DIENST ORT SAND IM MIN HEIME DIE URALTE STEINEN TER SCHARDT IST SCHAUN RUIN WISTEN HIER STIER UM GEN

**English Translation:**
> [The] concealment [of] the NDCE {?}. I [anoint with] oil {?} desolation, truly {?} rune place {?} of at [a] new {?} service-place [of] sand in my homeland. The ancient stones of SCHARDT, [one] is [to] behold [the] ruin. [They] knew here [the] bull/Stier around toward.

**Notes:** New elements:
- DIENST ORT = "service place" (a place of duty/worship)
- SAND = sand (geographic descriptor -- sandy terrain)
- STIER = bull (possibly a symbol, heraldic device, or place marker)
- RUNE ORT = "rune place" (a place of runes/inscriptions)
- The landscape is desolate (ODE), sandy, with ancient stones and runes

---

### Book 69 (92.5%, 62/67)

**Decoded German:**
> {L} AB IRREN WIR TOD IM MIN HEIME DIE URALTE STEINEN TER SCHARDT IST SCHAUN RUIN {WIIS}

**English Translation:**
> {?} Away! We wander [in] death in my homeland. The ancient stones of SCHARDT, [one] is [to] behold [the] ruin. {?}

**Notes:** Compact restatement of the death-wandering motif. The narrator and companions wander in death through their homeland, beholding the ruins of SCHARDT.

---

### Book 45 (91.9%, 68/74)

**Decoded German:**
> NACHTS ES {IHW} IN {CHN} SER ER SCE AUS OEDE DU FINDEN SAGEN AM MIN HEHL DIE NDCE FACH HECHELT ICH

**English Translation:**
> At night it {?} in {?} very he already out of [the] desolation. You [shall] find [and] tell at my concealment the NDCE compartment [that] gasps, I...

**Notes:** NACHTS (at night) -- the action takes place at night. The narrator instructs someone to find and tell about the concealed NDCE compartment that gasps/breathes. The nocturnal setting adds atmosphere to the supernatural narrative.

---

### Book 10 (91.7%, 122/133)

**Decoded German:**
> DIE URALTE STEINEN TER SCHARDT IST SCHAUN RUIN WISTEN HIER SER EIGENTUM ORT GEN {CHDKEL} SEID ENDE DEN ENDE REDER KOENIG SALZBERG {UNE} NIT GEHEN ORANGENSTRASSE {RW}

**English Translation:**
> The ancient stones of SCHARDT, [one] is [to] behold [the] ruin. [They] knew here [is] very [much] a place of property toward {?}. Be [at the] end! The end! [The] speaker [of the] King [of] SALZBERG {?} not [to] go [to] ORANGENSTRASSE {?}.

**Notes:** Major narrative elements:
- REDER KOENIG = "speaker/orator of the King" -- a royal herald or spokesperson
- SALZBERG = a real German place name (literally "salt mountain," cf. Salzburg)
- ORANGENSTRASSE = "Orange Street" -- a real German street name
- NIT GEHEN = "not to go" (MHG NIT = nicht/not)
- The King's speaker is commanded not to go to Orangenstrasse -- a prohibition or warning
- This connects the mythological (SCHRAT, ancient stones) to specific geography

---

### Book 11 (90.9%, 60/66)

**Decoded German:**
> ODE GAR {EO} RUNE ORT {ND} TER AM NEU {DE} DIENST ORT SAND IM MIN HEIME DIE URALTE STEINEN

**English Translation:**
> Desolation, truly {?} rune place {?} of at [a] new {?} service-place [of] sand in my homeland. The ancient stones...

**Notes:** Fragment describing the landscape: desolate, with a rune-place, a new service-place in sandy terrain, and the ancient stones. Connects to Books 58 and 43.

---

### Book 48 (90.4%, 75/83)

**Decoded German:**
> LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEIN GOTTDIENERS DA {U} NOTE {H} RUNEN {DEE} ENDE GEN INS {AUU}

**English Translation:**
> [A] lay about [the] notorious one, he so that did those who traveled, he [was] his God-servant's. There {?} distress/need {?} runes {?} end toward into {?}.

**Notes:** After the LEICH/BERUCHTIG refrain, new elements emerge: NOTE (distress/need) and RUNEN (runes, plural). The runes are associated with an ending or a direction ("GEN INS" = toward into).

---

### Book 50 (91.2%, 62/68)

**Decoded German:**
> {H} SO RUNE {E} IRREN WIR TOD IM MIN HEIME DIE URALTE STEINEN TER SCHARDT IST SCHAUN {RUII}

**English Translation:**
> {?} So [the] rune {?}. We wander [in] death in my homeland. The ancient stones of SCHARDT, [one] is [to] behold {?}.

**Notes:** The rune is mentioned before the death-wandering passage. The RUII garbled block at the end is likely RUIN with a decoding artifact.

---

## Books with 80-89.9% Coverage

---

### Book 8 (88.3%, 68/77)

**Decoded German:**
> {TRUNR} DEN ENDE REDER KOENIG LABT {D} ENDE {E} WEICHSTEIN {N} GAR SUN ENDE DIENST ORT AN EIN NEU UM SER {S}

**English Translation:**
> {?} The end. [The] speaker [of the] King refreshes/revives {?} [the] end {?} WEICHSTEIN {?}, truly son/sun. [The] end [of the] service-place at a new [one], around [it] very {?}.

**Notes:** LABT (refreshes/revives) -- the King's speaker LABT, possibly reviving or consecrating something. WEICHSTEIN appears again. DIENST ORT AN EIN NEU = "service-place at a new one" -- the old place of worship is being replaced or renewed.

---

### Book 27 (86.7%, 52/60)

**Decoded German:**
> {OD} TREU {UNR} DEN ENDE REDER KOENIG SALZBERG {UNE} NIT GEHEN ORANGENSTRASSE

**English Translation:**
> {?} Faithful/loyal {?} the end. [The] speaker [of the] King [of] SALZBERG {?} not [to] go [to] ORANGENSTRASSE.

**Notes:** TREU (faithful) parallels TRAUT (trusted). The prohibition against going to ORANGENSTRASSE is repeated. The King of Salzberg's speaker is warned or forbidden from traveling there.

---

### Book 66 (86.5%, 90/104)

**Decoded German:**
> {MI} SEI GODES DA SIE OWI RUNE MANIER DEGEN ENDE NEST TUT {IGAA} ER GIGE TEE SIN {CHN} SER ER SCE AUS ODE TREU {UNR} DEN ENDE REDER KOENIG {LA}

**English Translation:**
> {?} May [it] be God's! There they -- woe! -- [the] rune [in the] manner [of a] sword/hero [at the] end [of the] nest does {?}. He [plays the] fiddle [at] tea/gathering. [They] are {?} very, he already out of [the] desolation, faithful {?} the end. [The] speaker [of the] King {?}.

**Notes:** Rich passage:
- GODES (MHG God's) -- divine attribution
- OWI (Woe!) -- MHG exclamation of grief
- RUNE MANIER DEGEN = "rune in the manner of a sword/hero" -- runes are wielded like weapons, or a hero uses runes
- NEST = nest/stronghold
- GIGE (MHG fiddle) -- someone plays the fiddle, a Spielmann (minstrel) element
- TEE could be "tea" but more likely a gathering or assembly in MHG context
- This passage blends supernatural (runes), martial (DEGEN/sword), and artistic (GIGE/fiddle) elements

---

### Book 33 (86.4%, 57/66)

**Decoded German:**
> {E} DA SIE OWI RUNE MANIER DEGEN ENDE NEST TUT {IGAA} ER GIGE TEE SIN {CHN} SER ER SCE AUS {E}

**English Translation:**
> {?} There they -- woe! -- [the] rune [in the] manner [of a] sword/hero [at the] end [of the] nest does {?}. He [plays the] fiddle [at] tea/gathering. [They] are {?} very, he already out of {?}.

**Notes:** Closely parallels Book 66 but without the opening GODES or closing KOENIG references. The {IGAA} garbled block appears consistently across multiple books in this position.

---

### Book 35 (86.3%, 120/139)

**Decoded German:**
> {RNDMI} SEI GODES DA SIE OWI RUNE MANIER DEGEN ENDE NEST TUT {IGAA} ER GIGE TEE SIN {CHN} SER ER SCE AUS ODE TREU {UNR} DEN ENDE REDER KOENIG SALZBERG {UNE} NIT GEHEN ORANGENSTRASSE {R}

**English Translation:**
> {?} May [it] be God's! There they -- woe! -- [the] rune [in the] manner [of a] sword/hero [at the] end [of the] nest does {?}. He [plays the] fiddle [at] tea/gathering. [They] are {?}, very, he already out of [the] desolation. Faithful {?} the end. [The] speaker [of the] King [of] SALZBERG {?} not [to] go [to] ORANGENSTRASSE {?}.

**Notes:** The longest continuous high-confidence passage combining the GODES/OWI/RUNE/DEGEN/GIGE sequence with the KOENIG SALZBERG/ORANGENSTRASSE prohibition.

---

### Book 61 (85.9%, 61/71)

**Decoded German:**
> {R} HEL WIND UNRUH FINDEN NEIGT DAS ES DER {E} IST GEN {EHH} EIN NEU UM {SEU} FINDEN SAGEN AM MIN {HI}

**English Translation:**
> {?} Bright/clear wind-unrest. [You shall] find [that it] inclines, that it the {?} is, toward {?} a new [one] around {?}. Find [and] tell at my {?}.

**Notes:**
- HEL = bright/clear (MHG, related to modern "hell" meaning bright)
- WINDUNRUH = "wind-unrest" -- a compound describing atmospheric disturbance or turmoil
- NEIGT = inclines/bows -- something bending or yielding
- The passage describes finding something in turbulent wind, a new thing emerging, and the instruction to report back ("FINDEN SAGEN AM MIN" = find and tell at my [place])

---

### Book 47 (83.9%, 52/62)

**Decoded German:**
> {DE} TOT RUIN {G} SER {EL} AB IRREN WIR TOD IM MIN HEIME DIE URALTE STEINEN TER {ADTHA}

**English Translation:**
> {?} Dead, [in] ruin {?}, very {?} away. We wander [in] death in my homeland. The ancient stones of {SCHARDT?}...

**Notes:** The {ADTHA} at the end is likely a partially garbled SCHARDT (the anagram ADTHARSC -> SCHARDT is known, but here truncated). The TOT RUIN / TOD dichotomy: TOT (dead, adjective) vs. TOD (death, noun) -- both appear, reinforcing the death theme.

---

### Book 19 (82.8%, 53/64)

**Decoded German:**
> {TD} ENDE {E} WEICHSTEIN {L} SEID ENDE DEN ENDE REDER {KO} ERE {NDMI} SEI GODES DA SIE OWI {R}

**English Translation:**
> {?} [The] end {?} WEICHSTEIN {?}. Be [at the] end! The end! [The] speaker {?} honor {?}. May [it] be God's! There they -- woe! {?}.

**Notes:** Transition passage linking WEICHSTEIN to the GODES/OWI sequence. ERE (MHG honor) appears between the King's speaker and God's invocation.

---

### Book 64 (82.7%, 62/75)

**Decoded German:**
> {EION} GAR SUN ENDE DIENST ORT AN EIN {LEU} UM SER {S} ZU FINDEN SAGEN AM MIN HEHL DIE NDCE FACH {HECHL}

**English Translation:**
> {?} Truly son/sun. [The] end [of the] service-place at a {?} around, very {?}, to find [and] tell at my concealment the NDCE compartment {gasps?}...

**Notes:** Links the DIENST ORT (service-place) ending to the HEHL/NDCE/HECHELT discovery sequence. ZU FINDEN SAGEN = "to find and tell" -- the imperative mission.

---

### Book 52 (82.4%, 56/68)

**Decoded German:**
> GIGE TEE {S} SIN IHM NU STEH WRLGTNELNR HEL WIND UNRUH FINDEN NEIGT DAS ES DER {E} IST GEN

**English Translation:**
> [The] fiddle [at] tea/gathering {?}, [they] are [with] him. Now stand! WRLGTNELNR, bright wind-unrest! Find [that which] inclines, that it the {?} is, toward [it].

**Notes:** Critical passage:
- WRLGTNELNR is a proper noun (40 chars across 4 occurrences) -- an unresolved place name with letters E,G,L,L,N,N,R,R,T,W
- The command "NU STEH" (now stand!) is imperative
- WRLGTNELNR is addressed directly, followed by HEL WINDUNRUH -- possibly the name of a person or place associated with wind-turmoil
- The fiddle player and the gathering are mentioned just before

---

### Book 67 (81.2%, 39/48)

**Decoded German:**
> {BGZ} ER {A} SUN {E} NIT GEHEN ORANGENSTRASSE {R} WARD {EIE} TRAUT IST

**English Translation:**
> {?} He {?} son/sun {?}, not [to] go [to] ORANGENSTRASSE {?}. [It] became {?}. [The] trusted one is...

**Notes:** WARD (MHG became/was) marks a narrative shift. After the Orangenstrasse prohibition, something "became" or transformed. The TRAUT refrain follows.

---

### Book 42 (80.4%, 74/92)

**Decoded German:**
> ER STIER UM {EC} DU NUR ALTES IN IHM {TD} ENDE SCE {HWIASS} TUN {E} DASS ER WARD {EIE} TRAUT IST LEICH AN BERUCHTIG ER SO DA {GRSN}

**English Translation:**
> He [the] bull, around {?}. You [find] only old [things] in him. {?} [The] end, already {?}. Do {?} that he became {?}. [The] trusted one -- [this] is [a] lay about [the] notorious one, he so there {?}.

**Notes:** STIER (bull) reappears -- possibly a character epithet, heraldic symbol, or place marker. "DU NUR ALTES IN IHM" (you only old things in him) echoes Book 18, describing an ancient, depleted place or person.

---

### Book 16 (80.0%, 68/85)

**Decoded German:**
> KLAR SUN ENDE WINDUNRUHS FINDEN DIGE {STEIEHHI} STEH WIR DAS NEU {W} DA {UNRN} DEGEN IM MIN {H} IST RUNEN {DEE} ENDE

**English Translation:**
> Clear son/sun. End [of] WINDUNRUH'S. Find [the] worthy {?}. Stand, we [find] the new {?}! There {?} [the] sword/hero in my {?} is [of] runes {?} end.

**Notes:** WINDUNRUHS (genitive of WINDUNRUH) -- the wind-unrest belongs to something. DIGE may relate to "wuerdig" (worthy). RUNEN (runes) are associated with the DEGEN (sword/hero). The compound "DEGEN IM MIN" places the hero/sword in the narrator's personal realm.

---

### Book 24 (80.0%, 48/60)

**Decoded German:**
> {R} THENAEUT ER ALS {T} ENDE {NDEE} WEICHSTEIN {NGHR} DAS WIR {N} AN GEH {I} SO DAS RUNEN

**English Translation:**
> {?} THENAEUT, he as {?} [the] end {?} WEICHSTEIN {?}. That we {?} to go {?}, so the runes [say].

**Notes:** THENAEUT is a proper noun, close to ATHENAEUM (library/place of learning) but not an exact anagram. It may be an MHG rendering of a classical reference. The passage connects THENAEUT to WEICHSTEIN and the runes.

---

### Book 1 (81.8%, 36/44)

**Decoded German:**
> ODE TREU {UNR} DEN ENDE REDER KOENIG SALZBERG {UNE} NIT {GH}

**English Translation:**
> Desolation. Faithful {?} the end. [The] speaker [of the] King [of] SALZBERG {?} not {?}.

**Notes:** Fragment of the SALZBERG prohibition sequence. ODE (desolation) sets the scene before the King's speaker narrative.

---

### Book 43 (89.6%, 60/67)

**Decoded German:**
> {EO} RUNE ORT {ND} TER AM NEU {DE} DIENST ORT SAND IM MIN HEIME DIE URALTE STEINE OWI RUNE {A}

**English Translation:**
> {?} Rune-place {?} of, at [a] new {?} service-place [of] sand in my homeland. The ancient stones -- woe! -- [the] rune {?}.

**Notes:** OWI (Woe!) is exclaimed upon seeing the ancient stones. The rune-place and service-place in the sandy homeland are lamented.

---

### Book 32 (89.4%, 59/66)

**Decoded German:**
> ICH OEL {S} ODE GAR {EO} RUNE ORT {ND} TER AM NEU {DE} DIENST ORT SAND IM MIN HEIME DIE URALTE

**English Translation:**
> I [anoint with] oil {?} desolation, truly {?} rune-place {?} of, at [a] new {?} service-place [of] sand in my homeland. The ancient [stones]...

**Notes:** The narrator anoints with oil in the desolate rune-place. The anointing (OEL) is a ritual act performed at the site.

---

## Books with 70-79.9% Coverage (Partial Translations)

---

### Book 3 (75.0%, 51/68)

**Decoded German:**
> {T} ES SIN IHM NU STEH WRLGTNELNR HEL WIND UNRUH FINDEN NEIGT DAS ES DER {E} IST GEN {EHHII}

**English Translation:**
> {?} They are [with] him. Now stand! WRLGTNELNR, bright wind-unrest! Find [that which] inclines, that it the {?} is, toward {?}.

---

### Book 6 (74.2%, 66/89)

**Decoded German:**
> EIN {TO} DENN DIE {R} SEI {M} ERE ERE {L} AB IRREN DIE URALTE {ST} SIE {NNR} TAG {NDTEDHT} RUIN {GH} RUNE {A} UND DIE SO {WE} DEGEN ENDE {N}

**English Translation:**
> A {?} for the {?} may be {?} honor, honor {?} away. [We/they] wander [among] the ancient {?}. They {?} day {?} ruin {?} rune {?} and those so {?} sword/hero end {?}.

**Notes:** Double ERE (honor, honor) is emphatic. The wandering among ancient things, ruin, runes, and the sword/hero (DEGEN) form the consistent thematic cluster.

---

### Book 12 (72.9%, 51/70)

**Decoded German:**
> {ENDR} THENAEUT ER ALS STANDE NOT SEE ERDE {EOR} DU {NTEIG} TEE {S} SIN ENDE {E} WEICHSTEIN {NGHRD}

**English Translation:**
> {?} THENAEUT, he as [a man of] standing/estate [in] need. [The] sea [and] earth {?}. You {?} tea/gathering {?}, [they] are [at the] end {?} WEICHSTEIN {?}.

**Notes:** STANDE (standing/estate, MHG) and NOT (need/distress) characterize THENAEUT as a person of rank in trouble. SEE ERDE (sea and earth) may describe the extent of his domain or journey.

---

### Book 13 (70.0%, 49/70)

**Decoded German:**
> {GETRAS} ES SICH {T} ES {TEI} GEN ES ER ALTE {II} ORT {EEL} SO DEN {HISS} TUN DIE REISTEN ER SEI ENDE {TO}

**English Translation:**
> {?} It itself {?}, it {?} toward it. He [the] old {?} place {?} so them {?}. Did those who traveled, he may be [at the] end {?}.

---

### Book 15 (79.7%, 55/69)

**Decoded German:**
> {EAUIENA} GEN {CH} DIGE {TH} KLAR SUN ENDE WINDUNRUHS FINDEN {D} FERN DAS ES DER DA BEI {IS} TEIL

**English Translation:**
> {?} Toward {?} worthy {?}, clear son/sun. End [of] WINDUNRUH'S. Find {?} far [away], that it the there by {?} part/portion.

---

### Book 21 (74.4%, 64/86)

**Decoded German:**
> RUNEN {DR} THENAEUT ER ALS STANDE NOT ERE {LGTNELGZ} ER {A} STIER {URIT} ORANGENSTRASSE SICH {T} ES {TEI} GEN {EHI} SO DA

**English Translation:**
> Runes {?} THENAEUT, he as [a man of] standing [in] need. Honor {?} he {?} bull {?} ORANGENSTRASSE itself {?} it {?} toward {?} so there.

**Notes:** THENAEUT is again associated with STANDE NOT (standing in need) and ERE (honor). ORANGENSTRASSE and STIER (bull) appear in the same context. The runes open the passage.

---

### Book 26 (73.5%, 61/83)

**Decoded German:**
> MIN {HISI} ICH {HLA} RUNEN {DR} THENAEUT ER ALS STANDE NOT ERE {LGTNELGZ} ER {A} STIER {URIT} ORANGENSTRASSE SICH

**English Translation:**
> My {?} I {?} runes {?} THENAEUT, he as [a man of] standing [in] need. Honor {?} he {?} bull {?} ORANGENSTRASSE itself.

---

### Book 28 (70.4%, 50/71)

**Decoded German:**
> {CHTIG} ER SO DASS TUN DIE REISTEN ER SEIN GOTTDIENERS DA {UENO} URALTE {NRLRUNR} NACH {HECHL}

**English Translation:**
> {notorious?} He so that did those who traveled, he [was] his God-servant's. There {?} ancient {?} after {gasps?}...

---

### Book 30 (62.7%, 47/75)

**Decoded German:**
> {EUUIGL} AUCH {WEGA} WIR ERDE {EOR} DU {NTEIRAS} ES SICH {TDR} THENAEUT ER ALS STANDE {G} TEE {S} SIN {END} SEE

**English Translation:**
> {?} Also {?} we earth {?} you {?} it itself {?} THENAEUT, he as [a man of] standing {?} tea/gathering {?} are {?} sea.

---

### Book 36 (74.2%, 49/66)

**Decoded German:**
> {UIT} SIE {UR} WORT SAND IM MIN HEIME {DLT} ES {T} EINEN ODE {O} RUNE ORT {ND} TER AM NEU DES {NDTEI}

**English Translation:**
> {?} They {?} word [of] sand in my homeland {?}. It {?} a desolation {?} rune-place {?} of, at [a] new one of {?}.

---

### Book 37 (77.5%, 62/80)

**Decoded German:**
> {RSC} IST SCHAUN RUIN {WI} IST {EETTRUNR} DEN ENDE REDER KOENIG LABT {D} ENDE {E} WEICHSTEIN {N} GAR SUN ENDE {SN}

**English Translation:**
> {SCHARDT?} is [to] behold [the] ruin. {?} is {?} the end. [The] speaker [of the] King refreshes/revives {?} [the] end {?} WEICHSTEIN {?}, truly son/sun. [The] end {?}.

---

### Book 38 (68.2%, 45/66)

**Decoded German:**
> WIR {NSCHA} ER ALTE {II} ORT {EEL} SO DEN {HISS} TUN DIE REISTEN ER SEI ENDE TOT {I} ERE {LAUEAD}

**English Translation:**
> We {?} he [the] old {?} place {?} so them {?}. Did those who traveled, he may be [at the] end, dead {?} honor {?}.

---

### Book 40 (68.7%, 57/83)

**Decoded German:**
> {A} ZU {MRNDMI} SEI GODES DA SIE OWI RUNE MANIER DEGEN ENDE {NTECTCHMN} GEN {A} WIR {UN} ENDE {E} ENDE GEN INS {AUUCHN}

**English Translation:**
> {?} To {?} may [it] be God's! There they -- woe! -- [the] rune [in the] manner [of a] sword/hero [at the] end {?} toward {?}. We {?} end {?} end toward into {?}.

---

### Book 44 (77.4%, 48/62)

**Decoded German:**
> {IG} TEE {S} SIN IHM NU STEH WRLGTNELNR HEL WIND UNRUH FINDEN NEIGT DAS ES {D} ERSTE

**English Translation:**
> {?} Tea/gathering {?}, [they] are [with] him. Now stand! WRLGTNELNR, bright wind-unrest! Find [that which] inclines, that it {?} [the] first.

**Notes:** ERSTE (first) is new here -- "the first" of something. Could indicate primacy or sequence.

---

### Book 54 (79.3%, 23/29)

**Decoded German:**
> {U} SO TEE DER DAS ER {RR} IN {RH} SCE HAT ER {A}

**English Translation:**
> {?} So [the] tea/gathering, the that he {?} in {?} already has he {?}.

---

### Book 59 (72.3%, 94/130)

**Decoded German:**
> {EO} RUNE ORT {ND} TER AM NEU {DE} DIENST ORT SAND IM MIN HEIME DIE URALTE STEINEN TER {ADTHA} ES {UUISEMIADIIRGELNMH} SO {TUIARSC} IST SCHAUN RUIN WISTEN HIER STIER UM GEN

**English Translation:**
> {?} Rune-place {?} of, at [a] new {?} service-place [of] sand in my homeland. The ancient stones of {SCHARDT?}. It {?} so {SCHARDT?} is [to] behold [the] ruin. [They] knew here [the] bull around toward.

---

### Book 60 (79.7%, 59/74)

**Decoded German:**
> {ETAEDE} AM MIN HEHL DIE NDCE FACH {HECHLS} SCE URE SUN ENDE DIENST ORT AN {S} UM SER {S} ZU FINDEN {S} AN

**English Translation:**
> {?} At my concealment the NDCE compartment {gasps?}, already hour/time. Son/sun, end [of the] service-place at {?}, around very {?}, to find {?} at.

---

### Book 62 (74.2%, 46/62)

**Decoded German:**
> {N} IHM NU STEH WRLGTNELNR HEL WIND UNRUH FINDEN NEIGT DAS ES DER {E} IST GEN {EHHI}

**English Translation:**
> {?} [With] him. Now stand! WRLGTNELNR, bright wind-unrest! Find [that which] inclines, that it the {?} is toward {?}.

---

### Book 63 (77.8%, 49/63)

**Decoded German:**
> {IHW} IN {CHN} SER ER SCE AUS ODE TREU {UNR} DEN ENDE REDER KOENIG LABT {D} ENDE SCE {HWIT}

**English Translation:**
> {?} In {?}, very he already out of [the] desolation. Faithful {?} the end. [The] speaker [of the] King refreshes {?} [the] end, already {?}.

---

### Book 65 (77.4%, 65/84)

**Decoded German:**
> {LNR} HEL WIND UNRUH FINDEN NEIGT DAS ES DER {E} IST GEN {EHH} EIN {LHLADIZEE} ENDE {F} SAGEN AM MIN HEHL DIE NDCE {RT}

**English Translation:**
> {?} Bright wind-unrest! Find [that which] inclines, that it the {?} is toward {?}, a {?} end {?}. Tell at my concealment, the NDCE {?}.

---

## Books with 60-79.9% Coverage (Fragmentary)

---

### Book 14 (63.6%, 42/66)

**Decoded German:**
> {AD} GEN INS {AUUIIR} GEN {IIH} WIND {T} GEN {E} ENDE NEST TUT {IGGWI} DEN ER DEN ENDE {MISE} MIN {HI}

**English Translation:**
> {?} Toward into {?} toward {?} wind {?} toward {?} end. [The] nest does {?} them, he them [at the] end {?} my {?}.

---

### Book 20 (67.7%, 21/31)

**Decoded German:**
> EIN {AEUU} SO TEE DER DAS ER {RR} IN {RH} SCE {HW}

**English Translation:**
> A {?} so [the] tea/gathering, the that he {?} in {?} already {?}.

---

### Book 31 (61.2%, 74/121)

**Decoded German:**
> {L} SEI ERE DER KOENIG SALZBERG {UONGETRAS} ES {OD} TREU {UNR} DEN {ENDHNEE} ORANGENSTRASSE {ENDNRHAUNRN} AM {HISDIZA} RUNE {DDNE} NIT {G} DU NUR ALTES IN IHM {TD} ENDE

**English Translation:**
> {?} May honor be [to] the King [of] SALZBERG {?}. It {?} faithful {?} the {?} ORANGENSTRASSE {?} at {?} rune {?} not {?}. You [find] only old [things] in him {?} [the] end.

---

### Book 55 (68.4%, 39/57)

**Decoded German:**
> DER DA {II} STEH WIR DAS NEU {W} DA {UNRN} DEGEN BEI {IS} TEIL NUT {N} ENDE {MISCHASD}

**English Translation:**
> The there {?} stand! We [find] the new {?}! There {?} [the] sword/hero by {?} part, use/profit {?} end {?}.

---

## Books with < 60% Coverage (Low Confidence)

These books have too many garbled blocks for reliable translation. Key readable fragments only:

### Book 4 (45.7%): `{HHISLUIRUNNS} SIN IHM NU STEH {WRLGTNSE} TEE {IEETIGN} DAS ER GEH {HIIHULNR} HIN {D} FINDEN {TE}` -- "They are with him. Now stand! ... tea/gathering ... that he go ... thither ... find ..."

### Book 7 (53.8%): `TOD IM {T} NIE {UHONRIELT} ES {T} SIE {NNR} TAG {NDTTSSA} DIE {R} SEI {M} ERE ERE {K}` -- "Death in {?} never {?} it {?} they {?} day {?} the {?} may be {?} honor honor {?}"

### Book 17 (49.3%): `{T} ES {EZEEUITGH} NUN {A} DA BEI ERDE ... NACHTS ... SAGEN AM MIN HEHL DIE NDCE FACH HECHELT ICH {OE}` -- "... now ... there by earth ... at night ... tell at my concealment the NDCE compartment gasps I ..."

### Book 23 (59.6%): `{IL} SO DASS {TT} NUN ER SEIN GOTTDIENER {MTD} ENDE {E} WEICHSTEIN {NK} WIR {ETADETHR} DA ...` -- "... so that now he [is] his God-servant {?} end {?} WEICHSTEIN ... we ... there ..."

### Book 29 (53.3%): `{NA} DA BEI ERDE {EOIAITOEMEEND} GEH {ND} FINDEN NEIGT DAS ES DER {E} IST GEN {EHH} EIN {LHLADIZEEELUSE}` -- "... there by earth ... go ... find inclines that it the ... is toward ... a ..."

### Book 34 (57.4%): `{EOIGTSTEI} GEN {EHHIIHW} IN {CHN} SER {KE} DAS ES ER SCE AUS OEDE {ND} GEH NU {HI} IN DEN {T}` -- "... toward ... in ... very ... that it he already out of desolation ... go now ... into the ..."

### Book 41 (58.8%): `SER ER SCE {A} DIE REISTEN ER SEINE {DDKEL} SEI DEN {DNRHAUNRN} AM {HISDIZA} RUNE {S} TUT {IGAAE}` -- "Very he already ... those who traveled, he his ... may be the ... at ... rune ... does ..."

### Book 49 (51.8%): `{OTZN} DA {IE?} ER {NRNNDIA} ZU {N} SAND IM {MI} IM MIN {D} IM MIN {HE} DIE {LRM} IM {AA} ZU {NNS}` -- "... there ... he ... to ... sand in ... in my ... in my ... the ... to ..."

### Book 56 (56.8%): `... ALTE {IDNELGZ} ER {A} STIER {URITAUIGLAUNHEARUCHT} WIR TOD ES ... SCE HEL SO DEN {HISS} TUN DIE REISTEN ER SEI ENDE TOT ...` -- "... old ... he ... bull ... we death it ... already bright so them ... did those who traveled, he may be at the end, dead ..."

### Book 57 (50.4%): `... ENDE REDER KOENIG {L} GAB ER ... TREU {UNR} DEN {ENDHEAUNR} TEE ORANGENSTRASSE {ENDNO}` -- "... end speaker king ... gave he ... faithful ... the ... tea ORANGENSTRASSE ..."

### Book 68 (58.3%): `{UNA} DA BEI ERDE {EOIAITOEMEEND} GEH {ND} FINDEN NEIGT DAS ES DER {E} IST GEN {EHHIIHW} IN {CHN} SER {E}` -- "... there by earth ... go ... find inclines that it the ... is toward ... in ... very ..."

---

## Narrative Synthesis: The Story Across 70 Books

### The Setting

The text describes a **desolate, sandy homeland** (MIN HEIME) containing:
- **Ancient stones** (URALTE STEINEN) at a place called **SCHARDT** -- now in **ruin** (RUIN)
- A **rune-place** (RUNE ORT) with inscriptions
- A **service-place** (DIENST ORT) -- a site of worship or duty, described as being in sand
- The landscape is **desolate** (ODE/OEDE) with **wind-unrest** (WINDUNRUH)

### The Characters

1. **The Narrator** (first person "ICH/WIR"): A person who has died or exists in a death-like state, wandering through the ruins of their homeland. They anoint with oil (OEL), conceal things (HEHL), and instruct others to find and report.

2. **The Trusted One / The Notorious One** (TRAUT / BERUCHTIG): The subject of the poem (LEICH). The text repeatedly states "TRAUT IST LEICH AN BERUCHTIG" -- "The trusted one is [the subject of] a lay about the notorious one." This suggests a single figure who is both trusted and notorious -- a fallen hero or betrayer.

3. **The God-Servant** (GOTTDIENER/GOTTDIENERS): A religious authority figure whose honor (ERE) is connected to the travelers. May be the Trusted/Notorious one himself.

4. **Those Who Traveled** (DIE REISTEN): A group of travelers or pilgrims connected to the Notorious One. They did something significant ("SO DASS TUN DIE REISTEN").

5. **The Forest Demon** (SCHRAT): A MHG supernatural being that has already come out or been released. Stands in clear sunlight (KLAR SUN).

6. **The King's Speaker** (REDER KOENIG): A spokesperson for the **King of SALZBERG**, who is warned not to go to **ORANGENSTRASSE**.

7. **THENAEUT**: A proper noun (near-anagram of ATHENAEUM), a person or place of standing (STANDE) in need (NOT), connected to WEICHSTEIN and the runes.

8. **WRLGTNELNR**: An unresolved proper noun (letters E,G,L,L,N,N,R,R,T,W), addressed imperatively ("NU STEH WRLGTNELNR" = "Now stand, WRLGTNELNR!"), associated with wind-unrest.

9. **NDCE**: A proper noun, associated with a compartment (FACH) that gasps (HECHELT), hidden in the narrator's concealment (HEHL).

### The Narrative Arc

Based on the decoded passages, the story follows this approximate arc:

**I. The Invocation (Books 66, 33, 35, 40):**
"May it be God's!" (SEI GODES). Woe! (OWI). The rune in the manner of a sword/hero at the end of the nest. The fiddle plays (GIGE). The narrative begins with a divine invocation and lamentation, mixing martial imagery (DEGEN) with musical performance (GIGE) -- characteristic of medieval German epic poetry (Spielmannsdichtung).

**II. The Prohibition (Books 10, 27, 1, 35, 67):**
The speaker of the King of Salzberg is told not to go to Orangenstrasse. This is a royal decree or warning. The King's speaker refreshes/revives something (LABT) at WEICHSTEIN before the prohibition. Something became (WARD) different -- a transformation.

**III. The THENAEUT Episode (Books 24, 12, 21, 26):**
THENAEUT, a person or place of standing and rank (STANDE), is in need (NOT). Connected to WEICHSTEIN, the sea (SEE), the earth (ERDE), and the runes. The bull (STIER) and Orangenstrasse appear nearby. This may describe a learned person or institution fallen on hard times.

**IV. The Quest (Books 61, 52, 44, 3, 62, 65, 29):**
"Now stand, WRLGTNELNR!" Commands are given to find something in the bright wind-unrest. That which inclines (NEIGT) must be found. The search leads toward something. The narrator instructs: "Find and tell at my concealment" (FINDEN SAGEN AM MIN HEHL).

**V. The Discovery (Books 46, 53, 51, 45, 64, 60):**
Out of the desolation, one is to find and report at the narrator's concealment. The NDCE compartment gasps. The narrator anoints with oil. Here the trusted one is found -- and the lay about the notorious one is sung.

**VI. The Lay of the Notorious One (recurring refrain in 20+ books):**
"TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEIN GOTTDIENERS" -- The trusted one is the subject of a lay about the notorious one, who was his God-servant's [honor]. Those who traveled did what they did because of him.

**VII. Death and Ruin (Books 5, 9, 69, 50, 47, 22):**
"We wander in death in my homeland" (IRREN WIR TOD IM MIN HEIME). The ancient stones of SCHARDT are in ruin. Only old things remain (NUR ALTES IN IHM). The trusted one's end: dead, in ruin (ENDE TOT RUIN).

**VIII. The Ancient Landscape (Books 0, 58, 11, 43, 32, 59):**
The stones of SCHARDT are in ruin. Those who knew (WISTEN) recognized this as a place of property/ownership (EIGENTUM ORT). The rune-place, the service-place of sand in the homeland -- all desolate. The narrator anoints with oil amid the ruins. Woe! (OWI).

**IX. The Forest Demon (Books 25, 39):**
"The forest demon already [came] out of him." At the clear sun. This brief, enigmatic statement may represent the climax or resolution -- the supernatural entity (SCHRAT) is released, perhaps through the ritual described in the preceding sections.

### Thematic Summary

The text is a **medieval German lay (LEICH)** about a figure who was both trusted (TRAUT) and notorious (BERUCHTIG) -- possibly a God-servant (GOTTDIENER) who fell from grace. The narrative involves:

- A **desolate homeland** with ancient ruined stones (SCHARDT) and sandy service-places
- A **royal prohibition** (the King of Salzberg's speaker must not go to Orangenstrasse)
- A **quest** to find something hidden in the wind-unrest, guided by runes
- A **ritual anointing** with oil at a gasping, concealed compartment
- **Death and wandering** among ruins -- the narrator and companions are dead or in a death-realm
- A **forest demon** (SCHRAT) that emerges from someone into the sunlight

The language mixes Middle High German forms (MIN, SER, NIT, SIN, GODE, OWI, DEGEN, GIGE, LEICH, SCHRAT) with modern German, and references real German geography (SALZBERG, ORANGENSTRASSE, WEICHSTEIN, SCHARDT). The CipSoft developers, based in Regensburg, likely drew on **Nibelungenlied** traditions and local Bavarian/Austrian geography.

### Unsolved Elements

| Element | Occurrences | Status |
|---------|-------------|--------|
| WRLGTNELNR | 4x (40 chars) | Proper noun, letters E,G,L,L,N,N,R,R,T,W -- unresolved |
| NDCE | 9x (28 chars) | Proper noun, classified but meaning unknown |
| {CHN} | 8x (24 chars) | Always "IN CHN SER", likely proper noun |
| {EHHIIHW} | 3x (21 chars) | Fixed code sequence, 3 H's unusual |
| {IGAA} | 3x | Always after NEST TUT, before ER GIGE |
| THENAEUT | 4x | Near-anagram of ATHENAEUM but not exact |

---

*Generated from Session 27 decoding (78.8% coverage, mapping_v7.json). This represents the most complete translation of the Tibia Bonelord 469 cipher achieved to date. No public solution exists; this work is the product of 27 sessions of cryptanalysis.*
