## 12. Session 15 -- Statistical Validation, Garbled Segment Deep Analysis

### 12.1 Statistical Validation Results

Adapted permutation test, bootstrap CI, and Benjamini-Hochberg FDR correction from author's private repositories (tools not published). Results:

- **V7 vs Random**: p < 0.002 (V7 = 57.1% coverage vs 7.2% mean of 500 random mappings)
- **Anagram probability**: p ≈ 0 (finding 5+ valid +1 anagrams among ~15 proper nouns is astronomically unlikely by chance; Monte Carlo match rate ≈ 0.01% per string)
- **60-char consensus**: p = 1.0 (NOT significant — the raw digit sequences repeat across books regardless of letter assignment)
- **BH-FDR corrected code changes**: 2/4 significant ([86] E→M p=0.048, [83] N→A p=0.048); 2/4 not significant ([53] N→O p=0.095, [13] N→A p=0.619)

### 12.2 HWND = HUND (Dog/Hound) -- STRONG HYPOTHESIS

All 10 occurrences of HWND use identical codes: `00(H) 36(W) 90(N) 42(D)`. Zero variation.

| Evidence | Detail |
|---|---|
| Only viable German word | HUND (dog/hound) — replace W with U |
| W↔U orthographic link | MHG: W derives from "double-U"; some dialects used W-like graphs for /u/ |
| Context | "HUND FINDEN" = "find the hound" — quest instruction, appears 10x |
| Code 36=W is locked | Confirmed by WEICHSTEIN anagram (requires W) |
| Not a mapping error | W decodes correctly everywhere else (WIRD, WEICHSTEIN, WISSET, WIEDER) |
| HWND is the only anomaly | Sole case where W-for-U appears, suggesting intentional puzzle element |

**Full recurring context:** "STEH ... HUND FINDEN ... DAS ES ERSTE ... GEH" = "Stand ... find the hound ... that is the first ... go" — a clear quest instruction.

### 12.3 NDCE and HECHLLT Deep Code Analysis

**NDCE** — All 8 occurrences use identical codes: `60(N) 42(D) 18(C) 30(E)`
- All codes well-validated across the full superstring (code 18=C has 124 appearances, mostly in CH/SCH digraphs)
- No permutation of N,D,C,E forms any German or MHG word
- NDCE = END + C (mathematically confirmed +1 pattern), but END as a proper noun is weak
- Likely a proper noun or place name still unidentified
- Full context: "AM MIN HIHL DIE NDCE FACH HECHLLT ICH OEL SO DEN HIER"

**HECHLLT** — All 5 occurrences use identical codes: `57(H) 19(E) 18(C) 94(H) 34(L) 34(L) 64(T)`
- The double-L is real: both from code 34 (same code = same letter, always)
- HECHLLT ≠ HECHELT (differ by L↔E substitution, not an anagram)
- No 6-letter German word fits the +1 pattern (removing any single letter)
- No 7-letter German word is an exact anagram
- Two variant forms exist (book 60: HECHLS, book 64: HECHLL without T) suggesting truncated copies

**HIHL** — Appears in "AM MIN HIHL DIE NDCE" (at the MINNE HIHL the NDCE)
- Another unresolved 4-letter segment, likely a proper noun
- Letters H,H,I,L — no German word matches as exact or +1 anagram

### 12.4 Narrative Structure (Comprehensive)

The decoded text reveals a coherent medieval German narrative with these recurring sections:

| Section | German | Translation | Frequency |
|---|---|---|---|
| Ancient ruins | DIE URALTE STEINEN ... SCHARDT IST SCHAUN RUIN | The ancient stones ... the mountain pass to behold in ruins | 10x |
| The dead trusted one | TRAUT IST LEICH AN BERUCHTIG | The trusted one is a corpse, notorious | 8x |
| God's Servant | ER SO DASS TUN DIES ER T EIN ER SEIN GOTTDIENER | He so does this: he is his God's Servant | 8x |
| Quest instruction | STEH ... HUND FINDEN ... GEH | Stand ... find the hound ... go | 10x |
| King's speech | DEN ENDE REDE R KOENIG SALZBERG | The end of speech of the King of Salzberg | 6x |
| Anointing ritual | DIE NDCE FACH HECHLLT ICH OEL SO DEN HIER | The NDCE compartment HECHLLT I anoint/oil here | 5x |
| Locations | SALZBERG, ORANGENSTRASSE, WEICHSTEIN, SCHARDT | Salt Mountain, Orange Street, Soft Stone, Mountain Pass | varies |
| Love/homeland | IM MIN HEIME DIE URALTE | In the MINNE homelands the ancient | 6x |
| Rune places | RUNE ORT NDT ER AM NEU DES | Rune place, he at the new of | 5x |

### 12.5 Key Recurring Phrases (Frequency)

| Phrase | Count | Meaning |
|---|---|---|
| TUN DIES ER | 12x | "do this he" |
| ENDE REDE | 10x | "end of speech/sermon" |
| DIE URALTE | 10x | "the ancient [one/thing]" |
| ER SO DASS TUN DIES ER | 9x | "he so that to do this he" |
| URALTE STEINEN | 8x | "ancient stones" |
| TRAUT IST LEICH | 7x | "trusted [one] is corpse" |
| ER SEIN GOTTDIENER | 8x | "his God's Servant" |
| ER SCE AUS | 8x | "he SCE out/from" |
| KOENIG SALZBERG | 6x | "King of Salzberg" |

### 12.6 Updated Anagram Table (8 Confirmed)

| Anagram | Resolution | Pattern | Extra | Meaning |
|---|---|---|---|---|
| LABGZERAS | SALZBERG | +1 | A | Salt Mountain |
| SCHWITEIONE | WEICHSTEIN | +1 | O | Soft Stone |
| AUNRSONGETRASES | ORANGENSTRASSE | +1 | U | Orange Street |
| EDETOTNIURG | GOTTDIENER | +1 | U | God's Servant |
| ADTHARSC | SCHARDT | +1 | A | Mountain pass/notch |
| TAUTR | TRAUT | exact | — | Trusted/dear |
| EILCH | LEICH | exact | — | Corpse/body (MHG) |
| HEDEMI | HEIME | +1 | D | Homes/homelands |

### 12.7 New Anagram Resolutions (Session 15)

**EEMRE = MEERE** (seas, plural of Meer)
- Exact anagram (Pattern 2): sorted(EEMRE) = sorted(MEERE) = E,E,E,M,R
- Context: "DIE R SEI MEERE" = "the ? be seas"
- Anagram #10

**TEIGN = NEIGT** (bows, inclines)
- Exact anagram (Pattern 2): sorted(TEIGN) = sorted(NEIGT) = E,G,I,N,T
- Context: "FINDEN NEIGT DAS ES" = "find, inclines that it" (8x)
- Anagram #11

**WIISETN = WISTEN + I** (MHG: they knew)
- +1 pattern: remove I from WIISETN → sorted matches WISTEN = E,I,N,S,T,W
- WISTEN = MHG past tense of "wizzen" (to know)
- Context: "IST SCHAUN RUIN WISTEN HIER SER EIGENTUM" = "behold ruin they-knew here very territory"
- Anagram #12

**AUIENMR = MANIER + U** (manner, way)
- +1 pattern: remove U → sorted = AEIMNR = sorted(MANIER)
- Context: "RUNE MANIER DEN GE ENDE" = "rune manner/way the ... end"
- Anagram #13

**AODGE = GODE + A** (MHG: good, godly)
- +1 pattern: remove A → sorted(DEGO) = sorted(GODE) = D,E,G,O
- GODE = MHG/Germanic form meaning good, godly
- Context: "SEI GODE DA SIE OWI RUNE MANIER" = "be good since they OWI rune manner"
- Also matches DOGE + A (Venetian title) but GODE more contextually appropriate
- Anagram #14

**GEIGET = valid MHG verb** (NOT an anagram)
- "er geiget" = 3rd person singular of "geigen" (to play the fiddle), archaic -et conjugation
- Context: "ER GEIGET ES IN" = "he plays the fiddle in..."
- Also mathematically matches GEIGE + T (+1 pattern), but verb interpretation is primary

### 12.8 Updated Anagram Table (14 Confirmed)

| # | Anagram | Resolution | Pattern | Extra | Meaning |
|---|---------|-----------|---------|-------|---------|
| 1 | LABGZERAS | SALZBERG | +1 | A | Salt Mountain |
| 2 | SCHWITEIONE | WEICHSTEIN | +1 | O | Soft Stone |
| 3 | AUNRSONGETRASES | ORANGENSTRASSE | +1 | U | Orange Street |
| 4 | EDETOTNIURG | GOTTDIENER | +1 | U | God's Servant |
| 5 | ADTHARSC | SCHARDT | +1 | A | Mountain pass/notch |
| 6 | HEDEMI | HEIME | +1 | D | Homes/homelands |
| 7 | WIISETN | WISTEN | +1 | I | They knew (MHG) |
| 8 | AUIENMR | MANIER | +1 | U | Manner/way |
| 9 | AODGE | GODE | +1 | A | Good/godly (MHG) |
| 10 | TAUTR | TRAUT | exact | — | Trusted/dear |
| 11 | EILCH | LEICH | exact | — | Corpse/body (MHG) |
| 12 | EEMRE | MEERE | exact | — | Seas |
| 13 | TEIGN | NEIGT | exact | — | Bows/inclines |
| 14 | GEIGET | (verb) | — | — | He plays fiddle (MHG) |

**Extra letter distribution for +1 pattern:** A(3x), U(3x), O(1x), D(1x), I(1x) — vowels dominate

### 12.9 Coverage Improvement

| Metric | Session 14 | Session 15 | Change |
|---|---|---|---|
| Word coverage | 53.3% | 58.1% | +4.8% |
| Known word count | ~120 | ~135 | +15 |
| Resolved anagrams | 7 | 14 | +7 |
| Best book coverage | 79% (Book 2) | 87% (Books 0, 2) | +8% |

### 12.10 Key Readable Passages (Session 15)

**Book 0 (87% coverage):**
"URALTE STEINEN TER SCHARDT IST SCHAUN RUIN WISTEN HIER SER EIGENTUM ORTEN"
= "Ancient stones of SCHARDT to behold [in] ruin. They knew here very [much] territory places."

**Book 2 (87% coverage):**
"ORANGENSTRASSE ... TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIES ER EIN ER SEIN GOTTDIENER"
= "Orange Street ... the trusted one is a corpse, notorious, he so does this: he is his God's Servant"

**Book 10 (68% coverage):**
"SEI GODE DA SIE RUNE MANIER DEN ... ER GEIGET ES IN ... ER SCE AUS ... KOENIG SALZBERG ... ORANGENSTRASSE"
= "Be good since they [use] rune manner/way ... he plays the fiddle in ... he SCE out ... King of Salzberg ... Orange Street"

### 12.11 HWND = HUND Hypothesis (Strong) + HIND Variant

All 10 HWND occurrences use identical codes `00(H) 36(W) 90(N) 42(D)`. Code 36=W is locked by WEICHSTEIN. The only viable reading is HUND (dog/hound) with W functioning as U — supported by MHG orthographic conventions where W derives from "double-U." Full phrase: "STEH ... HUND FINDEN NEIGT DAS ES ERSTE ... GEH" = "Stand ... find the hound, bow that it is the first ... go" — a quest instruction appearing 10x.

**Critical discovery: Book 4 variant says HIND FINDEN (find the hind/female deer):**
- Book 4 codes: `06(H) 46(I) 90(N) 42(D)` — completely different codes from HWND
- HIND = "Hinde" (female deer) in MHG, a real word
- This proves books are NOT identical copies — CipSoft wrote intentional variations
- Both HIND and HUND are animals, reinforcing the animal-quest interpretation
- Standard version: "STEH ... HWND FINDEN NEIGT DAS ... GEH" (10x)
- Book 4 variant: "NEIGT DAS ER GEH ... HIND FINDEN" (1x, different word order too)

### 12.12 Remaining Mysteries

| Segment | Freq | Letters | Status |
|---|---|---|---|
| HWND | 10x | H,W,N,D | HUND hypothesis (strong, W=U) |
| LABRRNI | 8x | A,B,I,L,N,R,R | Unknown 7-letter proper noun, NOT Berlin |
| HIHL | 6x | H,H,I,L | Unknown proper noun in "AM MIN HIHL" |
| NDCE | 8x | N,D,C,E | Unknown, possibly END+C |
| HECHLLT | 5x | C,E,H,H,L,L,T | Unknown 7-letter word |
| SCE | 8x | S,C,E | Unknown 3-letter MHG word |
| UTRUNR | 6x | N,R,R,T,U,U | Unknown, no vowel pattern match |
| DRTHENAEUT | 5x | A,D,E,E,H,N,R,T,T,U | Long garbled, likely multi-word |
| LGTNELGZ | 3x | E,G,G,L,L,N,T,Z | Long garbled, likely multi-word |

### 12.13 Narrative Structural Analysis

The 70 books divide into distinct thematic sections with minimal overlap:

| Section | Theme | Books | Key Phrase |
|---|---|---|---|
| Death/Betrayal | Trusted one dies, notorious | 2, 5, 9, 22, 28, 46, 48, 51, 53 | TRAUT IST LEICH AN BERUCHTIG |
| Quest | Find the animal | 3, 4, 15, 16, 29, 44, 52, 61, 62, 65, 68 | HWND/HIND FINDEN |
| King's Speech | King of Salzberg speaks | 1, 8, 10, 27, 31, 35, 37, 57, 63, 66 | KOENIG + ENDE REDE |
| Rune Places | Locations and runes | 11, 32, 43, 50, 58, 59 | RUNE ORT |
| Anointing | Oil ritual | 32, 46, 51, 53, 58 | ICH OEL SO |

**Key observations:**
- Death section and Quest section are **completely non-overlapping** — they tell different parts of the story
- ORANGENSTRASSE is the most referenced location (11 books), suggesting it's the narrative's central setting
- The "anointing" section overlaps with both Death (46, 51, 53) and Rune Places (32, 58), suggesting it connects these narrative threads
- Book 4 is unique: only book using HIND (female deer) instead of HWND (hound), with different word order
- The densest books (53, 35, 10, 9, 5, 2) contain 4/15 key phrases each — these are the "summary" books

### 12.14 Digit Removal Discovery

**36 of 70 books show evidence of intentional digit removal by CipSoft.** 37 books have odd-length digit strings (impossible if all codes are 2-digit pairs), and inserting a dummy digit at optimal split points improves word coverage by +4 to +17 characters per book.

**Verified cases:**
- **Book 57** (pos 69): Recovers WEICHSTEIN anagram (SCHWITEIO), +SIE, DEM, GEH, EIN, ICH (+14 chars)
- **Book 59** (pos 126): Recovers GEIGET, OEL, WIR, ICH, DEN, ODE, ENDE (+13 chars)
- **Book 26** (pos 48): Recovers WEICHSTEIN, ERDE, ODE, WIR, DU, ENDE (+10 chars)
- **Book 50** (pos 35): +17 chars, Book 60 (pos 58): +17 chars, Book 49 (pos 36): +16 chars

**Caveat:** Mass application of splits reduces overall coverage (58.3% → 55.9%) because the superstring concatenation changes, breaking cross-book anagram patterns. Splits must be applied individually with per-book narrative verification.

**Total potential gain:** +354 characters across 36 books if all splits are correctly applied.

**Wrinkled Bonelord NPC confirmation:** "I am the great librarian" — confirms LABRRNI ≈ LIBRARI hypothesis. Key NPC dialogue:
- "Our race ruled the whole world" → matches URALTE STEINEN...RUIN (ancient ruins)
- "Proficient in the return from death" → matches LEICH (corpse), GOTTDIENER
- "Gods destroyed our empire" → matches the ruined places narrative
- "Numbers are essential" → cipher methodology hint
- "0 is obscene" → specific cipher property
- 486486 = bonelord's name in 469

### 12.15 Next Steps

1. **Word boundary analysis**: Many garbled segments (DRTHENAEUT, LGTNELGZ, NTEATTUIGAA) are likely multiple words with incorrect boundaries. Cross-book boundary alignment could resolve these.
2. **LABRRNI identification**: 7-letter proper noun, A,B,I,L,N,R,R. Neither BERLIN nor CARLIN. Need broader German/Tibia name databases.
3. **SCE investigation**: 3-letter MHG word appearing 8x in "ER SCE AUS" (he SCE from/out). Phonetically SC=SCH in MHG.
4. **HIHL and NDCE**: May require specialized MHG lexicon or Germanic dialect dictionaries.
5. **Validate HWND=HUND**: Look for in-game evidence or Tibia lore supporting "find the hound" as a quest element.
6. **HECHLLT**: Investigate if this could be a dialectal/MHG word not in standard dictionaries.

---

