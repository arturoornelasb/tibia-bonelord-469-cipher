## 23. Session 26: Massive Coverage Leap — 72.3% → 76.9%

**Date:** 2026-03-23

### Methodology
- Parallel agent attack: block decomposition + hypothesis testing + single-letter absorption
- Fixed code sequence discovery (identical 10-pair blocks appearing 13x across books)
- Brute-force optimization of all 64 anagram combinations
- CipSoft developer text cross-validation (Chayenne's reply, voice lines)

### Key Discoveries

**1. WINDUNRUH (Wind-Unrest, +74 chars)**
- UIRUNNHWND → WINDUNRUH: +1 pattern (extra N), compound noun WIND+UNRUH
- 8 occurrences, always in "HEL WINDUNRUH FINDEN" = "brightly find the wind-unrest"
- Follows established +1 extra letter pattern (SALZBERG+A, WEICHSTEIN+O, etc.)

**2. Fixed 10-Pair Block DIESERTEIN (+13 chars)**
- Pairs `45 21 76 52 19 72 78 30 46 48` appear identically 13 times
- Decodes to DIESERTEIN, anagram of DIE REISTEN (those who traveled)
- Resolves the persistent {T} in "DIES ER {T} EIN ER" pattern

**3. DEGEN - Sword/Hero (+7 chars)**
- DENGE → DEGEN: single-letter absorption MANIER+{D}+ENGE
- "RUNE MANIER DEGEN" = "rune manner of the sword/hero" — adds martial element

**4. Hypothesis Confirmations:**
- HIHL → HEHL (concealment, MHG): +36 chars, 9 occurrences
- HECHLLT → HECHELT (pants/gasps, MHG): +35 chars, 5 occurrences
- NLNDEF → FINDEN (to find): +39 chars, 7 occurrences (L→I issue noted)
- RRNI → IRREN (to err): +28 chars, 6 occurrences

**5. CipSoft Developer Text Analysis:**
- Chayenne's 2009 reply `114514519485611451908304576512282177` found in Book 1 (pos 16)
- Second part `6612527570584` found in Book 2 (pos 111)
- Voice lines also sourced from books: Voice 1 in Book 30, Voice 2 in Book 12
- Confirms books are the authoritative cipher source

**6. KOENIG (King) in 12 Books:**
- Always in context "NENDEREDERKOENIGLAB" — fixed code sequence
- "DEN ENDE REDER KOENIG" = "the end speaker/speech [of the] king"

### Coverage Progress
| Metric | Session 25 | Session 26 | Delta |
|--------|-----------|-----------|-------|
| Coverage | 72.3% | 76.9% | +4.6% |
| Chars covered | 3999 | 4247 | +248 |
| Anagrams | 39 | 50+ | +11 |
| Best book | 97% (Book 22) | 99% (Book 22) | +2% |

### Highest-Confidence Book Readings (Session 26)

**Book 22 (99%):**
"IST SEI TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEI ENDE TOT RUIN"
= "It is... the trusted one is a corpse, of notoriety, he so that those who traveled, he is at the end, dead, ruin."

**Book 46 (95%):**
"ICH SER ER SCE AUS ODE DU FINDEN SAGEN AM MIN HEHL DIE NDCE FACH HECHELT ICH OEL SO DEN HIER TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIE REISTEN ER SEINE"
= "I very he SCE out, or you find legends at my concealment, the NDCE compartment gasps, I anoint with oil, so the here... the trusted is corpse of notoriety..."

### Remaining Garbled (23.1%)
- **Proper nouns**: WRLGTNELNR (10 chars, place), UTRUNR (6 chars, king's place), NDCE (4 chars)
- **Unresolved**: CHN (10x), UOD (8x, possibly "old" in MHG/Dutch)
- **Single-letter remnants**: reduced from 126 to ~80 instances

### New Scripts
- `scripts/analysis/session26_block_decomposition.py` — Big block anagram attack
- `scripts/analysis/session26_hypothesis_test.py` — Coverage impact testing
- `scripts/analysis/session26_diesertein.py` — Fixed code sequence analysis
- `scripts/analysis/session26_single_letter_attack.py` — Single-letter absorption
- `scripts/analysis/session26_optimal_combo.py` — Brute-force combination optimizer
- `scripts/analysis/session26_cumulative_test.py` — Cumulative validation
- `scripts/analysis/session25_cipsoft_decode.py` — CipSoft developer text decoding

