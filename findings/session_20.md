## 17. Session 20: Garbled Block Census, TER Discovery, SCHRAT Anagram

### 17.1 Coverage Progress

| Metric | Start | End |
|--------|-------|-----|
| Word coverage | 68.2% (3793/5559) | 68.7% (3820/5557) |
| Confirmed anagrams | 20 | 21 (+ THARSCR→SCHRAT) |
| KNOWN words | ~190 | ~192 (+ TER, SCHRAT) |
| New chars matched | — | +27 |

### 17.2 TER Discovery (+15 chars)

TER is a Middle High German dialectal variant of "der" (the/of the). All 9 occurrences are in the phrase **"DIE URALTE STEINEN TER SCHARDT IST SCHAUN"** = "The ancient stones of Schardt are to behold [as ruin]".

Previously parsed as `STEINEN {T} ER SCHARDT`, now correctly as `STEINEN TER SCHARDT`. The DP prefers longer words (UNTER, RICHTER) over TER where they overlap, so no conflicts.

### 17.3 THARSCR → SCHRAT (+12 chars, anagram #21)

**SCHRAT** = MHG "forest demon, wild man" (Waldschrat). The word appears in medieval German folklore as a supernatural forest creature.

- THARSCR sorted: ACHRRST
- SCHRAT + R sorted: ACHRRST (exact +1 match, extra R)
- 2 occurrences in text
- Context: **"RUNEN DER SCHRAT SCE AUS ER"** = "Runes of the Schrat (forest-demon), from him"

This adds a new mythological creature to the narrative — the text references both GOD (Gottdiener, Godes) and DEMONIC (Schrat) forces.

### 17.4 HEDEMI Anagram Map Entry is Dead Code

Critical discovery: the anagram entry HEDEMI→HEIME never fires because the raw decoded text has **HEDDEMI** (7 letters with double-D), not HEDEMI (6 letters). The codes are consistently 57-74-45-45-19-04-50 across all 11 occurrences — code 45 (D) appears twice, producing the double-D.

HEDDEMI sorted = DDEEHIM. No German/MHG word match found yet. The +2 pattern (HEIME + DD) is unusual compared to all other anagrams which are exact or +1.

### 17.5 Code 96 (L) Confirmed Correct

Testing code 96 as I instead of L showed +13 chars gain, but **breaks the EILCH→LEICH anagram** (9x) and EILCHANHEARUCHTIG→LEICHANBERUCHTIG (9x). The frequency analysis also confirms: L is already underrepresented (-1.00%) and I is overrepresented (+2.32%). Code 96 must remain L.

### 17.6 Garbled Block Census

478 total garbled blocks (195 unique), comprising 1767 chars (31.8% of text).

**Highest-frequency blocks:**
| Block | Count | Chars | Notes |
|-------|-------|-------|-------|
| {T} | 30x | 30 | Single letter before ER, EIN, ES |
| {E} | 30x | 30 | Single letter before URALTE, WEICHSTEIN |
| {D} | 19x | 19 | Single letter before ERSTE, FINDEN |
| {HED} | 11x | 33 | In HEDDEMI, between MIN and DEM |
| {CHN} | 8x | 24 | Recurring pattern |
| {HIHL} | 8x | 32 | Place name, unresolved |
| {UTRUNR} | 7x | 42 | Place name, unresolved |
| {NDCE} | 7x | 28 | After DIE, unresolved |
| {SD} | 7x | 14 | Always between AN and IM |
| {HECHLLT} | 5x | 35 | After FACH, codes 57-19-18-94-34-34-64 |
| {NLNDEF} | 5x | 30 | Before SAGEN, NOT variant of FINDEN |
| WRLGTNELNRHELUIRUNNHWND | 4x | 92 | Biggest block, codes identical all 4x |

### 17.7 Letter Distribution Anomaly: H

H is **62.3% garbled** vs 31.8% average — the most overrepresented letter in garbled zones (+30.5 points above average). L is second most overrepresented (64.2%).

4 H codes: 00 (90x, 83% known), 06 (34x, 32% known), 57 (100x, 48% known), 94 (42x, 52% known).

Code 06 is most suspicious (only 32% in known word contexts) but testing alternatives for all H codes showed no significant coverage gains. The overrepresentation is largely because unsolved blocks (HIHL, HECHLLT, HWND, CHN, HEDDEMI) all contain H.

### 17.8 NPC Noodles Response Pattern (Updated)

Three distinct response types correlate with cipher content:

| Response | Trigger | Interpretation |
|----------|---------|----------------|
| **BARK** ("Woof! Woof!") | "gottdiener", "God's Servant", "godes" | God-related words |
| **SNIFF** | "THENAEUT", "The trusted one", "ancient stones of SCHARDT" | Narrative proper nouns/phrases |
| **WIGGLE** | "bone", "bonelord", "book", "are to behold as ruin" | Generic bone/book keywords |

**Key insight**: Noodles responds to SEMANTIC MEANING, not individual cipher words. "TRAUT" alone = nothing, but "The trusted one" (its meaning) = sniff. This suggests the NPC recognizes English translations of cipher concepts.

**Recommended next tests on Noodles:**
1. "schrat" / "forest demon" / "waldschrat" (newly decoded)
2. "Zathroth" (evil god from Tibia lore)
3. "the trusted one is a corpse" (TRAUT IST LEICH)
4. "runes of the forest demon"
5. "king salzberg" (separate words)

### 17.9 Data Files Created

- `scripts/analysis/session20_garbled_census.py` — Complete garbled block inventory
- `scripts/analysis/session20_pattern_attack.py` — High-frequency pattern analysis
- `scripts/analysis/session20_code96_ter.py` — Code 96 and TER investigation
- `scripts/analysis/session20_apply_gains.py` — Word candidate testing and validation
- `scripts/analysis/session20_big_blocks.py` — Big block decomposition attempts
- `scripts/analysis/session20_validate_schrat.py` — THARSCR→SCHRAT validation
- `scripts/analysis/session20_npc_h_analysis.py` — H code analysis and NPC patterns

