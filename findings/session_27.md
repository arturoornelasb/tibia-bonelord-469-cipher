## 24. Session 27: Systematic Garbled Attack + Lore Research — 76.9% → 78.7%

**Date:** 2026-03-24

### Methodology
- Systematic 2-5 char garbled block resolution via anagram matching
- Cross-boundary word formation (merging garbled chars with adjacent known words)
- Code 18 (C) anomaly investigation — exhaustive reassignment testing
- Code 96 (L→I) hypothesis testing — definitive rejection
- Parallel Tibia lore research agent for proper noun identification

### Key Discoveries

**1. GIGE - MHG Fiddle/Viola (+16 chars)**
- GEIG → GIGE: anagram, 4 occurrences
- GIGE is the Middle High German word for fiddle (modern German: Geige)
- Context: "ER GIGE TEE SIN" — adds musical element to narrative

**2. TOD - Death (+16 chars)**
- UOD → TOD: anagram, 5 occurrences
- Always "WIR TOD IM MIN HEIME" = "we death in my homeland"
- Strong narrative fit: death theme alongside RUIN, ENDE, LEICH

**3. ODE - Desolation (+12 chars)**
- EOD → ODE: anagram, 3x in "AUS ODE TREU" (from desolation, faithful)

**4. Cross-Boundary Absorptions:**
- EODE → OEDE (wasteland, +5), EER → ERE (MHG honor, +5)
- WRDA → WARD (became, +4), ENOT → NOTE (need/distress, +3)
- ETE → TEE (+3), EES → SEE (sea, +2), ABG → GAB (gave, +1), UER → URE (+1)
- ENG → GEN (toward, +6)

**5. NDCE = Proper Noun (+32 chars)**
- Fixed code sequence [60, 42, 18, 30] = N,D,C,E
- Always in "DIE NDCE FACH" (the NDCE compartment)
- 9 occurrences across 9 books, always identical codes
- Added to KNOWN set as proper noun

### Code Investigation Results

**Code 96 (L→I): DEFINITIVELY REJECTED**
- Coverage drops -44 chars (76.9% → 76.1%)
- 16 books worsen, only 2 improve
- Destroys LEICH (9x), LEICHANBERUCHTIG (9x)
- Frequency score worsens by +1.38

**Code 18 (C): CONFIRMED CORRECT**
- Only 1 code maps to C (expected for rare letter)
- 71% of C appears as CH, 25% as SCH — correct German pattern
- Every alternative letter (A-Z) causes massive drops (-400 to -485 chars)
- C is NOT misassigned; NDCE and CHN genuinely contain C

### Tibia Lore Research (Agent)

**Key findings from wiki/fandom research:**
- Cipher uses REAL German geographic names (SALZBERG, ORANGENSTRASSE, WEICHSTEIN, SCHARDT), NOT Tibia location names
- CipSoft is based in Regensburg (near Nibelungenbrücke) — cipher may draw from Nibelungenlied tradition
- No Tibia NPC/location names match garbled proper nouns
- THENAEUT close to ATHENAEU(M) but NOT exact anagram (T/A count mismatch)
- The text is an original medieval-German-style composition, likely by developer Knightmare

### Fixed Code Sequences Identified
| Sequence | Codes | Letter | Freq | Classification |
|----------|-------|--------|------|---------------|
| WRLGTNELNR | (varies) | E,G,L,L,N,N,R,R,T,W | 4x | Proper noun (place) |
| NDCE | 60,42,18,30 | N,D,C,E | 9x | Proper noun |
| EHHIIHW | 03,57,57,65,46,00,36 | E,H,H,H,I,I,W | 3x | Unknown (3 H's unusual) |
| CHN | (varies) | C,H,N | 8x | Fragment, always "IN CHN SER" |

### Coverage Progress
| Metric | Session 26 | Session 27 | Delta |
|--------|-----------|-----------|-------|
| Coverage | 76.9% | 78.7% | +1.8% |
| Chars covered | 4247 | 4348 | +101 |
| Anagrams | 50+ | 63+ | +13 |
| Books >= 90% | 14 | 18 | +4 |
| Books >= 80% | 28 | 35 | +7 |

### Highest-Confidence Books (Session 27)

**Book 25 (100%):** "DER SCHRAT SCE AUS ER" = The forest demon SCE from him

**Book 46 (99%):** "ICH SER ER SCE AUS OEDE DU FINDEN SAGEN AM MIN HEHL DIE NDCE FACH HECHELT ICH OEL SO DEN HIER TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEINE"

**Book 22 (99%):** "IST SEI TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEI ENDE TOT RUIN"

**Book 5 (98%):** "HIER TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEIN GOTTDIENERS ERE AB IRREN WIR TOD IM MIN HEIME DIE URALTE STEINEN TER SCHARDT IST SCHAUN DEN"

### Remaining Garbled (21.3%)
- **WRLGTNELNR** (40 chars, 4x) — proper noun, letters E,G,L,L,N,N,R,R,T,W
- **NDCE** (32 chars, 9x) — proper noun, now in KNOWN
- **CHN** (24 chars, 8x) — always "IN CHN SER"
- **UNR** (21 chars, 7x) — =NUR causes regressions, needs context-specific fix
- **EHHIIHW** (21 chars, 3x) — unknown, 3 H's unusual, fixed codes
- **ND** (18 chars, 9x) — short garbled, various contexts

### New Scripts
- `scripts/analysis/session27_comprehensive.py` — Full garbled block attack
- `scripts/analysis/session27_targeted.py` — High-impact pattern analysis
- `scripts/analysis/session27_apply.py` — Final coverage validation
- `scripts/analysis/session27_c_anomaly.py` — Code 18 (C) investigation
- `scripts/analysis/session26_code96_test.py` — Code 96 (L→I) rejection

---

