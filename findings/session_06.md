## Session 6

### 81. Raw-Digit Superstring Assembly

Assembled superstring at the raw digit level (before decoding) for exact overlaps.

**Results:**
- 20 of 70 books are completely contained in other books (literal digit substrings)
- 50 unique (non-contained) books remain
- Assembled into **29 fragments** (vs 33 from decoded-level assembly)
- Largest fragment: **349 chars** (Fragment 1, from 6 books)
- Total: 3,701 codes assembled

**Containment examples (raw-level, exact digit match):**
```
Bk0 contained in Bk10, Bk35, Bk66
Bk11 contained in Bk58
Bk46 contained in Bk51
Bk47 contained in Bk5, Bk9
Bk66 contained in Bk10, Bk35
```

**Top overlaps:**
```
Bk46 -> Bk53: 234 digits (117 codes)
Bk66 -> Bk10: 210 digits (105 codes)
Bk48 -> Bk28: 146 digits (73 codes)
Bk26 -> Bk21: 144 digits (72 codes)
```

Fragment word coverage (DP parse):
| Fragment | Chars | Books | Coverage |
|----------|-------|-------|----------|
| Frag 4   | 175   | 2     | 70.9%    |
| Frag 21  | 69    | 1     | 63.8%    |
| Frag 0   | 278   | 2     | 62.2%    |
| Frag 6   | 136   | 1     | 61.8%    |
| Frag 18  | 75    | 1     | 61.3%    |
| Frag 1   | 349   | 6     | 54.2%    |

### 82. CRITICAL FINDING: Code 05 May Not Be C

**Code 18 = C is SOLID.** All valid German CH/SCH/ICH/ACH patterns exclusively use code 18.

**Code 05 NEVER appears before H.** It produces only non-German C patterns:

| Pattern | Code 05 | Code 18 |
|---------|---------|---------|
| CH      | 0       | ~49     |
| SCH     | 0       | ~31     |
| CO      | 10      | 0       |
| CE      | 5       | 13      |
| CI      | 7       | 10      |
| CG      | 7       | 0       |
| CS      | 5       | 1       |
| CT      | 1       | 1       |

**Word hit test for code 05 alternatives:**
```
05=S: 1682 hits (+28)  <-- BEST
05=E: 1681 hits (+27)
05=N: 1671 hits (+17)
05=R: 1671 hits (+17)
05=I: 1666 hits (+12)
05=C: 1654 hits (baseline)
```

**05=S evidence:**
- HEARUCHTIGERCO -> HEARUCHTIGER**SO** DASS = "Hearuchtiger so that" (perfect German!)
- All 10 CO occurrences = code 05+79(O); if 05=S these become "SO" (German "thus/so")
- HEARUCHTIGER SO DASS TUN DIESER = "Hearuchtiger, so that this one does..." — natural German

**05=S problems:**
- OELCO -> OELSO (unclear)
- GETECSIN -> GETESSIN (unclear)
- UOEHCGSEI -> UOEHSGSEI (no improvement)
- TOTNIURGCE -> TOTNIURGSE (possibly possessive?)

**Status:** Code 05 is likely S, not C. This would reduce C to just code 18 (113 occurrences, ~2% of text — matching German 2.73% when combined with current frequency). Needs further verification, especially in the ECG/ECS contexts.

### 83. Code 18 Reassignment Test

For code 18 (113 occurrences, definitely participates in CH/SCH):
```
18=E: 1697 hits (+43)  <-- mathematically best
18=O: 1674 hits (+20)
18=C: 1654 hits (baseline, 3rd best)
```
But 18=E or 18=O would DESTROY all SCH/CH patterns (SCHAUN, ICH, FACH, HEARUCHTIGER etc.). **Code 18=C is confirmed and cannot be changed.** The higher word hits from E/O are illusory — they come from forming spurious short words at the expense of breaking all CH/SCH words.

### 84. ENDE Frequency Analysis

41 total ENDE occurrences across all books (many overlapping):

**Four different homophonic encodings of ENDE:**
```
56-11-45-19 -> ENDE: 26x
56-11-47-26 -> ENDE: 6x
29-53-45-27 -> ENDE: 6x
26-11-45-19 -> ENDE: 3x
```

**ENDE is often part of longer words:**
- ENDEN (ends): 6x — "IENERDENGE**ENDEN**TENTTUIGA"
- ENDER (in DENENDEREDER): 8x — "DENEND**ERED**ERKOENIGLABGZERAS"
- ENDES: 4x — "SUNENDES NDTEI"
- SENDE: 6x — "RERSCEAUSENDE" = "R ER SCE AUS ENDE"

**Key context: DEN ENDE REDE R KOENIG LABGZERAS**
= "the end speech of King Labgzeras" — REDE (speech/discourse) confirms this is narrative about a king's speech.

**Letter before ENDE:** N:18, E:9, D:8, S:6
**Letter after ENDE:** E:16, N:6, R:6, S:4, U:3

### 85. SCHWITEIO Pattern Analysis

SCHWITEIO appears repeatedly in a fixed context:
```
...D ENDE E SCHWITEIO N/S/L...
```

Raw codes: S(91) C(18) H(00) W(36) I(46) T(88) E(95) I(21) O(99) + varying suffix

All 10 SCHWITEIO occurrences share the exact same codes 91-18-00-36-46-88-95-21-99.

**Context variations after SCHWITEIO:**
- SCHWITEION (most common, then diverges: EISTLRSZTH, ELS?, GHRDASWIRN, GARSUNENDES)
- SCHWITEIOILS? (with unknown code 74)

This is either a proper noun or an unrecognized German compound. No parse as standard German.
If code 05=S (finding #82), then we'd need to re-examine if any SCHWITEIO contexts change — but code 05 is not involved here (all C's in SCHWI use code 18).

### 86. C Pattern Distribution

Out of 152 total C occurrences in the text:
```
SCH: 31 (20.4%) — valid German
CH:  49 (32.2%) — valid German (includes SCH as subset)
CK:   0 (0.0%)  — ZERO! Unusual — CK is common in German
CE:  18 (11.8%) — non-standard
CI:  17 (11.2%) — non-standard
CO:  10 (6.6%)  — non-standard
CA:   4 (2.6%)  — non-standard
CS:   6 (3.9%)  — non-standard
other: 17 (11.2%)
```

**47% of C occurrences are NOT in standard German patterns.**
If code 05 is reassigned to S (removing 39 of those non-standard C's), the remaining code 18 would have 113 C's with a much healthier German pattern ratio.

### 87. SA Decoder Results (Blind Attack)

Several Simulated Annealing decoders were run from scratch (no cribs):
- Unconstrained bigram SA: converged poorly, score -700 (inconsistent mapping)
- Constrained SA (fixed codes/letter): score -0.59 (very different from our mapping)
- Constrained SA with unigram+bigram: score -3.55 (different mapping again)
- Crib-constrained SA: failed (implementation errors)
- Crib overlap analysis: ran but parity issues detected

**Conclusion:** Blind SA attack on 5,597 codes with 98 unique symbols does NOT converge to the correct mapping. The text is too short and the cipher has too many symbols for statistical methods alone. Our crib-based, incremental approach (sessions 1-5) is the right methodology.

### 88. Session 6 Summary

**Key findings:**
1. Raw-digit assembly: 29 fragments, 20 contained books, better than decoded-level assembly
2. **Code 05 likely = S, not C** — never appears before H, best word hit alternative, makes HEARUCHTIGER SO DASS (perfect German)
3. Code 18 = C confirmed (all SCH/CH patterns)
4. ENDE appears in multiple forms (ENDEN, ENDER, ENDES, SENDE) — DEN ENDE REDE R KOENIG = "the end speech of King"
5. SCHWITEIO = uncracked repeated pattern (10 exact occurrences)
6. CK=0 in entire text (unusual for German)
7. Blind SA attacks don't converge — crib-based approach validated

**If code 05=S is correct, the updated mapping would be:**
- 91 codes assigned to 22 letters (plus 05=S, making 7 total S codes)
- C would have only 1 code (18) with 113 occurrences = 2.0% (close to expected 2.73%)
- S would have 7 codes: 92, 91, 52, 59, 12, 23, 05 = total ~191 occurrences = 3.4% (still below expected 7.3%)
- The C overrepresentation anomaly in unrecognized text would be RESOLVED

### 89. Pending Ideas for Future Sessions

**High priority (updated):**
1. **Verify code 05=S** — Test this hypothesis thoroughly. Check each of the 39 code-05 positions to see if S makes more contextual sense than C. Especially: what does GETESSIN, OELSO, UOEHSGSEI become?
2. **Crack SCHWITEIO** — This appears 10 times. It's key to the narrative. Try: compound splits, Tibia lore lookup, anagram analysis, alternate word boundaries
3. **Raw-digit level cross-fragment joining** — The 29 fragments may still overlap at the decoded level; try merging decoded fragments that overlap when homophone differences are ignored
4. **Tibia lore cross-reference** — Look up LABGZERAS, TOTNIURG, HEARUCHTIGER, THARSC, SCHWITEIO, AUNRSONGETRASES in TibiaWiki
5. **ENDE structural analysis** — With 41 occurrences, is ENDE a structural marker? Count distance between ENDEs. Could be verse/stanza breaks.

**Medium priority:**
6. Code 74 (19 occ) systematic testing — most frequent unknown
7. Compound word splitting for DP parser (RUNEORT, KOENIGSREDE, etc.)
8. CK absence investigation — why zero CK? Could mean K codes are wrong
9. Trigram analysis vs German reference
10. NPC dialogue cross-reference

**Speculative:**
11. IIIWII as secondary cipher
12. Positional cipher hypothesis
13. Word-level anagram on proper nouns
14. Rosetta Stone approach (find known Tibia text matching a passage)

### Files Created Session 6

| File | Purpose | Session |
|------|---------|---------|
| `raw_superstring.py` | Raw-digit superstring assembly + DP parse | 6 |
| `investigate_c_ende.py` | C code analysis, ENDE frequency, SCHWITEIO | 6 |
| `sa_decoder.py` | Blind SA homophonic decoder (multiple variants) | 6 |
| `sa_decoder_constrained.py` | Constrained SA with fixed code counts | 6 |
| `sa_decoder_unibigram.py` | SA with unigram+bigram scoring | 6 |
| `sa_crib_constrained.py` | Crib-constrained SA (failed) | 6 |
| `crib_attack.py` | Book overlap crib analysis (partial) | 6 |

---

