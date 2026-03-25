## 30. Session 31: Post-Resolution Fixups + DIGIT_SPLIT Re-optimization (94.4% → 94.6%)

### Post-ANAGRAM_MAP Fixup: EETTR → TRETE (+5)

EETTR is an artifact created by prior ANAGRAM_MAP resolutions — it doesn't exist in the raw decoded text. In the resolved text it appears uniquely in the context "IST EETTR NUR", which is an exact anagram of TRETE (1st person singular of *treten* = to step/tread). Rearranging gives "IST TRETE NUR" = "is step only". Added as a `resolved_text.replace()` fixup alongside the existing TREUUNR→TREUNUR pattern.

### DIGIT_SPLIT Re-optimization (+8)

Full-pipeline brute-force search over all positions × digits for each of the 37 odd-length books. Found 6 books where alternative splits improve coverage in the concatenated pipeline context:

| Book | Old Split | New Split | Gain |
|------|-----------|-----------|------|
| 15 | (98, '0') | (36, '6') | +1 |
| 14 | (98, '1') | (47, '8') | +3 |
| 65 | (94, '0') | (94, '1') | +1 |
| 36 | (78, '0') | (63, '3') | +1 |
| 29 | (151, '1') | (120, '1') | +1 |
| 19 | (52, '0') | (32, '0') | +1 |

Per-book analysis suggested +13 total, but full-pipeline verification (accounting for ANAGRAM_MAP interactions and chain overlaps) confirmed +8.

### KNOWN Addition: GE (+2)

Added `GE` (common MHG prefix *ge-*) to the KNOWN set. Appears as standalone fragment due to CipSoft's anagram obfuscation splitting prefixes from stems. Absorbs garbled `{IGE}` block at one position.

### Updated Coverage Progress
| Metric | Ses.30 | Ses.31 | Delta |
|--------|--------|--------|-------|
| Coverage | 94.4% | 94.6% | +0.2% |
| Chars | 5204 | 5219 | +15 |
| Techniques | DIGIT_SPLIT, BoLWP, anagrams | Post-resolution fixups, DIGIT_SPLIT re-opt, KNOWN expansion | 3 new |

### Remaining Garbled (5.4%, ~295 chars)

- **Single-letter residues** (~117 blocks): Isolated letters between recognized words, unmatchable by DP (min wlen=2)
- **Two-char blocks** (~44 blocks): Mostly consonant clusters (ST, RR, RH, GT, RT) — not German words
- **Multi-char blocks** (~24 blocks): SEUUIGL(7), TEDHT(5), DDKEL(5), AGSRW(5), GHMT(4), HLAR(4), etc. — no German word anagrams found (with I↔E/I↔L swap tolerance)

The remaining gap appears to be the irreducible noise floor of the cipher: boundary artifacts from anagram obfuscation, single-letter residues, and consonant clusters that don't form recognizable words in any arrangement.

### New Scripts
- `scripts/analysis/session31_attack.py` — BoLWP analysis on garbled blocks
- `scripts/analysis/session31_anagram_scan.py` — German word anagram scan with swap tolerance
- `scripts/analysis/session31_rescan.py` — Post-optimization garbled block rescan
