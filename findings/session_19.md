## 16. Session 19: Cross-Boundary Anagrams, NPC Investigation, Deep Garbled Analysis

### 16.1 Coverage Progress

- **Session start:** 66.9% (3720/5559)
- **Session end:** 68.2% (3793/5559)
- **Delta:** +73 chars (+1.3%)
- **Total confirmed anagrams:** 20 (16 from v7 + 4 new)
- **New KNOWN words:** STANDE, NACHTS, NIT, TOT

### 16.2 Cross-Boundary Anagram Discovery (NEW TECHNIQUE)

Previous anagrams were all found within DP-segmented garbled blocks. Session 19 discovered
that some anagrams **span word boundaries** — the DP segments a string as {garbled}+KNOWN_WORD
but the actual MHG word spans both parts.

| Raw | DP Parse | True Word | Type | Occurrences | Coverage |
|-----|----------|-----------|------|-------------|----------|
| TNEDAS | {TNE} DAS | STANDE | exact | 4x | +12 |
| NSCHAT | {NSC} HAT | NACHTS | exact | 2x | +6 |
| SANGE | SANG {E} | SAGEN | exact | 8x | +8 |

**TNEDAS → STANDE**: MHG subjunctive of "stan" (to stand). Phrase: "THENAEUT ER ALS STANDE [E] NOT"
= "THENAEUT, he who stood as/in need/distress". Sorted letters: ADENST = ADENST. Perfect match.

**NSCHAT → NACHTS**: "at night" (genitive). Context: "WIR NACHTS EMNET ENGE MI ORTEN"
= "we at night [?] narrow [?] places". Sorted: ACHNST = ACHNST.

**SANGE → SAGEN**: "to say/tell" or "legends/sagas". Context: "DU NLNDEF SAGEN AM MIN HIHL"
= "you [?] tell/say at my HIHL". Already in KNOWN. Sorted: AEGNS = AEGNS.

### 16.3 Candidate: ANSD → SAND (NOT APPLIED)

ANSD appears 7x (sorted ADNS = ADNS, exact anagram of SAND). Would give +14 chars.
Context: "DIENST ORT AN{SD} IM MIN" → "DIENST ORT SAND IM MIN".
**Not applied** because it destroys the preposition AN which is grammatically valid in all contexts.
One occurrence shows "WORT ANSD" where SAND makes less sense than "WORT AN [?]".

### 16.4 NPC Investigation: Noodles (Dog NPC)

User tested decoded cipher words on Noodles (dog NPC in Tibia):

| Keyword | Response | Notes |
|---------|----------|-------|
| bone | `<wiggle>` | 5x consistent |
| bonelord | `<wiggle>` | Recognized |
| book | `<wiggle>` | Recognized |
| thenaeut | `<sniff>` | Different from wiggle! |
| **gottdiener** | **`Woof! Woof!`** | **Unique bark response!** |
| HWND, FINDEN, UTRUNR, HIHL | (none) | No reaction |
| leich, reder, salzberg, weichstein | (none) | No reaction |
| schardt, orangenstrasse, curst | (none) | No reaction |
| hund, dog, food, library, hellgate | (none) | No reaction |
| 659978, 54764 | (none) | Elder Bonelord numbers |

**Key finding:** GOTTDIENER ("God's Servant") triggered a unique bark response, different from
the wiggle (bone/book) and sniff (thenaeut) patterns. This is the only cipher-decoded word
that got a bark. In the narrative, GOTTDIENER is the central role/title of the protagonist.

### 16.5 Big Garbled Block: WRLGTNELNRHELUIRUNNHWND

23-char block appearing 4x between "IM NU STEH" and "FINDEN NEIGT DAS".
A shorter 7-char variant (WRLGTNE) also appears in similar context.

Raw codes (Book 3): 36-24-96-84-75-60-19-96-58-55-06-49-96-70-46-72-61-14-58-00-36-90-42

Anagram-DP decomposition found fragments: GEN(+T), RUHE(+L), RUIN inside the block.
HWND (last 4 chars) consistently uses codes 00-36-90-42 across all books.

### 16.6 NLNDEF vs FINDEN: Different Code Sequences

NLNDEF appears 5x before SAGEN. Comparison with FINDEN:
- NLNDEF codes: `90→N 96→L 73→N 47→D 09→E 20→F` (sorted letters: DEFLNN)
- FINDEN codes: `20→F 46→I 48→N 45→D 19→E 11→N` (sorted letters: DEFINN)
- Only difference: L (code 96) vs I (code 46). Different code sequences entirely.
- NLNDEF is NOT a mis-mapped FINDEN — it's a genuinely different word.
- Context: "DU NLNDEF SAGEN AM MIN HIHL" = "you [?] tell at my [?]"

### 16.7 Remaining Garbled Block Summary

No anagram matches found for: UTRUNR, HIHL, NDCE, HECHLLT, RRNI, TTUIGAA, TIURIT.
These are likely proper nouns (place names) or words not in our German/MHG lexicon.
UTRUNR and HIHL are consistently described as place names by narrative context.

### 16.8 UNENITGHNEE Decomposition (BREAKTHROUGH)

The 11-letter block UNENITGHNEE (4x, always between SALZBERG and ORANGENSTRASSE) was
finally decomposed using NIT as a word boundary:

```
UNENITGHNEE = {UNE} + NIT + GHNEE
                       ^^^   ^^^^^
                     "not"   GEHEN (to go, exact anagram)
```

Result: "KOENIG SALZBERG {UNE} NIT GEHEN ORANGENSTRASSE"
= "King Salzberg [?] not go [to] Orange Street"

NIT is MHG "not" (variant of "niht"), confirmed by 6 occurrences (+18 coverage).
GHNEE → GEHEN is an exact anagram (sorted EEGHN = EEGHN), 4 occurrences (+20 coverage).

### 16.9 TOT Discovery

TOT ("dead/death") found 3x in "SEINE {DE} TOT" phrases (+9 coverage).
Context: "ER SEINE {DE} TOT {NIURIL}" = "he his [?] death/dead [?]"
Thematically linked to "TRAUT IST LEICH" (the trusted one is a corpse) narrative.

### 16.10 NPC Investigation Results

**Noodles (dog NPC):**
- "gottdiener" → `Woof! Woof!` (unique bark, only cipher word with this response)
- "thenaeut" → `<sniff>` (different from wiggle)
- "bone/bonelord/book" → `<wiggle>` (standard positive)
- All other cipher words → no reaction

**Bozo (jester NPC):**
- "bonelord" → joke ("Why are bonelords so ugly?")
- All cipher words → no reaction (only knows his own keywords)

### 16.11 Data Files Created

- `scripts/analysis/session19_cross_boundary.py` — Cross-boundary anagram scanner
- `scripts/analysis/session19_validate_apply.py` — Candidate validation and testing
- `scripts/analysis/session19_garbled_fast.py` — Deep garbled block analysis
- `scripts/analysis/session19_narrative_structure.py` — Narrative structure and hidden word scan
- `scripts/analysis/session19_quick_words.py` — Mass 3-letter word scan
- `scripts/analysis/session19_ghnee_test.py` — GHNEE→GEHEN verification

---

