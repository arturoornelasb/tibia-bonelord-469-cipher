## 18. Session 21: HEDDEMI Fix, SAND Cross-Boundary, Systematic Block Attack

**Coverage: 68.7% -> 69.7% (+1.0%, +36 chars)**

### 18.1 HEDDEMI Dead Code Fix (+22 chars)

The anagram map entry `HEDEMI -> HEIME` was dead code -- the raw text always has HEDDEMI (7 letters with double-D code 45), never HEDEMI (6 letters). The DP was falsely matching DEM from inside HEDDEMI, splitting it as HED(garbled) + DEM(known) + I(garbled).

**Fix:** Changed anagram map entry from `HEDEMI -> HEIME` to `HEDDEMI -> HEIME` (+2 pattern, unprecedented but validated).

**Before:** `IM MIN {HED} DEM {I} DIE URALTE` (4 garbled, 3 false-known)
**After:** `IM MIN HEIME DIE URALTE` (0 garbled, 5 known)

This is the first +2 anagram pattern (two extra letters DD). All previous were +1 or exact. The 11x consistent occurrence across all books validates this interpretation.

### 18.2 ANSD -> SAND Cross-Boundary Anagram (+14 chars)

Discovered that the garbled block {SD} (7x, always in context AN|SD|IM) forms a cross-boundary exact anagram: AN + SD = ANSD -> SAND.

**Before:** `DIENST ORT AN {SD} IM MIN HEIME` (2 garbled)
**After:** `DIENST ORT SAND IM MIN HEIME` (0 garbled)

"Service place sand in my homes" -- a geographic/location reference consistent with the narrative's place name pattern (SALZBERG, WEICHSTEIN, ORANGENSTRASSE, SCHARDT).

No collisions with existing anagram map entries. All 7 occurrences verified safe.

### 18.3 Systematic Garbled Block Census

Full census of 1771 garbled chars in 508 blocks (206 unique). Top targets by impact:

| Block | Length | Freq | Total | Context |
|-------|--------|------|-------|---------|
| WRLGTNELNRHELUIRUNNHWND | 23 | 4x | 92 | STEH..FINDEN |
| UTRUNR | 6 | 7x | 42 | ODE..DEN |
| HIHL | 4 | 9x | 36 | MIN..DIE |
| HECHLLT | 7 | 5x | 35 | FACH..ICH |
| HED (now HEIME) | 3 | 11x | 33 | MIN..DEM (FIXED) |
| NLNDEF | 6 | 5x | 30 | DU..SAGEN |
| NDCE | 4 | 7x | 28 | DIE..FACH |

### 18.4 Key Investigation Results

**NLNDEF = FINDEN if L=I**: NLNDEF (5x, "DU NLNDEF SAGEN") would be an exact anagram of FINDEN if code 96 mapped to I instead of L. But code 96 = L is confirmed by EILCH->LEICH (9x). Coincidence or intentional cipher obfuscation layer beyond anagramming.

**HIHL + NDCE + HECHLLT always appear together**: These three garbled blocks appear as a repeating unit: "SAGEN AM MIN HIHL DIE NDCE FACH HECHLLT ICH OEL". Identical codes across all occurrences. Combined 15 garbled chars, appears 5-9x. Remains unsolved.

**UTRUNR (7x)**: Always "ODE UTRUNR DEN ENDE REDER KOENIG". Codes always identical: 44 64 72 61 14 51 = U T R U N R. Split analysis found TUR+NUR but context doesn't support it well.

**Single-letter blocks**: {T} 23x (13x as ER|T|EIN, always code 78), {E} 31x, {D} 20x, {I} 17x (10x from HEDDEMI fix now resolved), {H} 9x (7x as IN|H|IM). These are structural artifacts of the cipher.

**NPC Noodles update**: Testing "schrat", "forest demon", "waldschrat", "Zathroth" = NO RESPONSE. But "runes of the forest demon" = SNIFF and "the trusted one is a corpse" = SNIFF. Confirms pattern: Noodles responds to English narrative phrases, not individual words. Zathroth (Tibia's evil god) gets no response, meaning Noodles' God-bark is specific to cipher-decoded references.

### 18.5 Updated Anagram Count: 23 confirmed

Added: HEDDEMI->HEIME (+2), ANSD->SAND (cross-boundary exact)

### 18.6 Data Files Created

- `scripts/analysis/session21_systematic_attack.py` — Full garbled block census and anagram scan
- `scripts/analysis/session21_deep_investigation.py` — Raw code analysis for top blocks
- `scripts/analysis/session21_coverage_gains.py` — Coverage impact testing
- `scripts/analysis/session21_pattern_chains.py` — Cross-boundary anagram discovery

---

