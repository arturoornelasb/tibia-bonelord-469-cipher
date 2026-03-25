## 19. Session 22: MHG Word Discovery, CHIS→SICH, HEL Breakdown

### 19.1 Coverage Progress

| Metric | Start | End |
|--------|-------|-----|
| Word coverage | 69.7% (3820/5557) | 71.9% (3976/5528) |
| Confirmed anagrams | 23 | 24 (+ CHIS→SICH) |
| New MHG words added | — | +6 (HEL, RIT, EWE, SIN, MIS, AUE) |
| New chars matched | — | +156 |

### 19.2 MHG (Middle High German) Words Discovered

Systematic MHG lexicon scan identified 6 new words with confirmed positive coverage gain and plausible context:

| Word | Gain | Contexts | Meaning |
|------|------|----------|---------|
| **HEL** | +21 | STEH .. HEL .. FINDEN; {C} HEL SO DEN | MHG "bright, clear" / Norse underworld |
| **RIT** | +9 | SER {TIU} RIT ORANGENSTRASSE | MHG "ride, journey" |
| **EWE** | +8 | ENDE EWE ICH STEIN (5x) | MHG "eternity, law" (OHG: ewa) |
| **SIN** | +6 | ES SIN {H} IM NU (6x) | MHG "his / to be" |
| **MIS** | +6 | DEN ENDE MIS {E} MIN; ZU {MRND} MIS {EI} GODES | MHG "with, together" |
| **AUE** | +5 | context varies | MHG "meadow, water-meadow" |

Total from new MHG words: **+55 chars**

### 19.3 CHIS → SICH Anagram (anagram #24, +7 chars)

CHIS is an exact anagram of SICH (German reflexive pronoun "oneself/itself").

- Contexts: `ORANGENSTRASSE CHIS TESTEIENGE`, `ORANGENSTRASSE CHIS ODE UTRUNR`
- Appears 4x, always after ORANGENSTRASSE in the phrase `SER {TIU} RIT ORANGENSTRASSE SICH`
- Reading: "SER [?] RIT(e) ORANGENSTRASSE SICH" = "[he] journeys Orange Street himself"

### 19.4 HEL inside the Big Block WRLGTNELNRHELUIRUNNHWND

Key structural discovery: the 23-character block WRLGTNELNRHELUIRUNNHWND contains **HEL** at the center, splitting it into three parts:

```
WRLGTNELNR  |  HEL  |  UIRUNNHWND
  (10 chars)    (3)    (10 chars)
```

All 6 occurrences of this block use identical codes:
- `WRLGTNELNR`: codes 36-24-96-84-75-60-19-96-58-55 (W-R-L-G-T-N-E-L-N-R)
- `HEL`: codes 06-49-96 (H-E-L) — confirmed valid codes
- `UIRUNNHWND`: codes 70-46-72-61-14-58-00-36-90-42 (U-I-R-U-N-N-H-W-N-D)

Context: always appears as `STEH {WRLGTNELNR} HEL {UIRUNNHWND} FINDEN`

So the phrase reads: **"STEH [?10?] HEL [?10?] FINDEN"** = "stand [?] HEL [?] find/finds"

Both flanking 10-char blocks remain unsolved.

### 19.5 ENG Inside ENGE (No New Standalone ENG)

Analysis confirmed ENG only appears as part of ENGE (30 occurrences total). No standalone ENG exists that can be used as a separate word. The few "standalone" cases are part of larger garbled blocks.

### 19.6 ER {T} EIN = REITEN Ruled Out

ERTEIN is an exact anagram of REITEN (to ride), appearing 13x in `DIES ER {T} EIN ER SEIN GOTTDIENER`. However, using REITEN would break narrative structure — the {T} is a single-code garbled letter between ER and EIN. Context analysis confirms ER+TEIN is not a German reading; the correct parse is `DIES ER (tut) EIN ER SEIN GOTTDIENER`.

### 19.7 RUIIN → RUIN Confirmed (+1 anagram, already in map)

RUIIN appears in text as a 5-char sequence where DP adds an extra I. Already handled by RUIIN → RUIN in the anagram map. No new discovery needed.

### 19.8 Data Files Created

- `scripts/analysis/session22_deeper_blocks.py` — UNE, ENG, EO, ERTEIN investigation
- `scripts/analysis/session22_ruiin_and_patterns.py` — RUIIN, IGAA, EO patterns
- `scripts/analysis/session22_hel_verify.py` — HEL occurrence analysis, big block decomposition
- `scripts/analysis/session22_sin_chis_verify.py` — MHG word testing, CHIS→SICH, batch scan

---

