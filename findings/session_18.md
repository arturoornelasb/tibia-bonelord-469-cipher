## 15. Session 18: Complete Bookcase Mapping, Garbled Block Tracing, Anagram Discovery

### 15.1 Coverage Progress
- Start of session: 66.5% (3697/5559)
- End of session: **66.9% (3720/5559)** (+23 chars, +0.4%)
- Changes: Added IEB→BEI anagram, NU (MHG "now") to KNOWN words

### 15.2 Complete Hellgate Library Bookcase Mapping

User provided all 71 books organized across 40 physical bookcases. **All 71 books matched EXACTLY** to books.json entries. Key findings:

| Bookcase | Books (JSON idx) | Notes |
|----------|-----------------|-------|
| First | 12, 13, 14 | Starts with THENAEUT section |
| Second | 15, 16 | KLAR SUN ENDE, FINDEN |
| Third | 20, 21 | THENAEUT, LGTNELGZ, ORANGENSTRASSE |
| Fourth | 24, 25, 26 | THENAEUT, RUNEN DER THARSCR |
| Fifth | 30 | AUCH, THENAEUT |
| Sixth | 38, 39 | ALTE ORT, THARSCR SCE AUS |
| Seventh | 54, 55, 56 | Mixed garbled, HISS pattern |
| Eighth | 68, 69 | DA BEI ERDE, FINDEN NEIGT |
| Ninth | 57 | UTRUNR, ORANGENSTRASSE (garbled) |
| Tenth | **0, 1, 2** | **Classic opening: URALTE STEINEN** |
| Eleventh | 58, 59 | HIHL, NDCE, DIENST ORT |
| Twelfth | 3, 4 | NU STEH, WRLGTNELN..., FINDEN |
| Thirteenth | 40, 41, 42 | GODES, OWI RUNE MANIER |
| Fourteenth | 60 | HIHL, NDCE, DIENST ORT |
| Fifteenth | 22 | TRAUT IST LEICH |
| Sixteenth | 27 | UTRUNR, SALZBERG, ORANGENSTRASSE |
| Seventeenth | 31 | SALZBERG, ORANGENSTRASSE |
| Eighteenth | 43 | RUNE ORT, DIENST ORT |
| Nineteenth | **61** | FINDEN, SANG (DUPLICATE) |
| Twentieth | 44, 45 | NU STEH, NLNDEF SANG |
| Twenty-First | 62, 63, 64 | FINDEN, UTRUNR, DIENST ORT |
| Twenty-Second | 5, 6, 7 | TRAUT, GOTTDIENERS, MEERE |
| Twenty-Third | 28, 29 | GOTTDIENERS, DA BEI ERDE |
| Twenty-Fourth | 36 | WORT AN, RUNE ORT |
| Twenty-Fifth | 37 | LABT, WEICHSTEIN |
| Twenty-Sixth | **61** | Same as Nineteenth (DUPLICATE) |
| Twenty-Seventh | 46, 47 | NLNDEF SANG, HIHL, NDCE |
| Twenty-Eighth | 65 | FINDEN, SANG |
| Twenty-Ninth | 17 | DA BEI ERDE, HIHL, NDCE |
| Thirtieth | 32, 33 | OEL, RUNE ORT, OWI RUNE MANIER |
| Thirty-First | 48 | LEICH AN BERUCHTIG, NOTH |
| Thirty-Second | 66, 67 | OWI RUNE MANIER, UTRUNR |
| Thirty-Third | 18, 19 | EIGENTUM ORTEN, WEICHSTEIN |
| Thirty-Fourth | 34 | SCE AUS, GEH NU HI |
| Thirty-Fifth | 49 | Most garbled (48%) |
| Thirty-Sixth | 8, 9 | LABT, WEICHSTEIN, TRAUT |
| Thirty-Seventh | 23 | GOTTDIENER, WEICHSTEIN |
| Thirty-Eighth | 35 | GODES, OWI, UTRUNR |
| Thirty-Ninth | 10, 11 | URALTE STEINEN, SALZBERG |
| Fortieth | 50, 51, 52, 53 | Largest: 4 books |

**Book 61 is DUPLICATED** — appears on both Nineteenth and Twenty-Sixth Bookcases.

### 15.3 Bookcase Order vs Index Order

- Bookcase order coverage: 66.5% (3696/5560)
- Index order coverage: 66.6% (3701/5560)
- **Virtually identical** (-5 chars)
- The narrative is **circular** — same phrases repeat across bookcases regardless of physical order
- Books within the same bookcase sometimes chain (overlap at boundaries) but inconsistently

Book chaining within bookcases:
- First Bookcase: [12]→[13] overlap 26 chars
- Second Bookcase: [15]→[16] overlap 106 chars
- Eleventh Bookcase: [58]&[59] shared 50 chars
- Twenty-Second: [5]&[6] shared 26, [6]&[7] shared 35
- Thirty-Ninth: [11]→[10] overlap 32 chars
- Many bookcases show NO overlap between their books

### 15.4 New Anagram: IEB → BEI

**IEB = BEI** (exact anagram, 3 occurrences)

Context: "DA {IEB} ERDE" → "DA BEI ERDE" = "there at/by earth"

All 3 occurrences appear in the phrase "DA BEI ERDE EOIAITOEMEEND" which seems to describe a location near/at the earth.

### 15.5 New KNOWN Word: NU

**NU** = MHG for "now" (same as NUN, shorter variant). Appears ~5x.

Context: "IM NU STEH" = "in the now stand" = "stand now"
Also: "ENGE ENDE NU OD" and "GEH NU HI" = "go now here"

### 15.6 Garbled Block Code Tracing

All major garbled blocks traced to their raw digit codes. **Key finding: blocks are remarkably consistent** — the same garbled text always comes from the same digit codes, confirming the mapping is stable.

| Block | Codes | Consistency | Identity |
|-------|-------|-------------|----------|
| UTRUNR | 44-64-72-61-14-51 | 7/7 consistent | Unknown place |
| HIHL | 57-65-94-34 | 9/9 consistent | Unknown place (contains code 94) |
| NDCE | 60-42-18-30 | 9/9 consistent | Unknown (DEN+C?) |
| HECHLLT | 57-19-18-94-34-34-64 | 5/5 consistent | Unknown (contains code 94) |
| NLNDEF | 90-96-73-47-09-20 | 7/7 consistent | Unknown (close to FINDEN?) |
| UOD | 43-53-45 | 8/8 consistent | Unknown MHG word |
| HED | 57-74-45 | 12/12 consistent | HELD minus L? |
| LGTNELGZ | 96-84-75-60-19-96-84-77 | 2/2 consistent | Unknown |
| TIURIT | 78-16-70-51-21-64 | 3/3 consistent | Unknown |
| GCHD | 80-18-94-45 | 4/4 consistent | Unknown (contains code 94) |
| RRNI | 51-08-11-46 | 5/6 consistent | Unknown |
| RUI | 72-61-16 | 8/8 consistent | RUIN minus N? (extra I blocks match) |
| CHN | 18-00-14 | 10/10 consistent | Unknown |

### 15.7 Code 94 Analysis

Code 94 (currently H) has **100% garbled ratio** but is **locked** by the ADTHARSC→SCHARDT anagram. Testing 94:H→I, H→E, H→A all resulted in -46 to -49 coverage loss and broke the SCHARDT anagram. Code 94=H is confirmed correct.

Code 94 appears in: HIHL (H position), HECHLLT (H position), GCHD (H position), ADTHARSC/THARSCR (H position). All these blocks remain garbled, but the SCHARDT evidence is conclusive.

### 15.8 Code 20 Deep Investigation

Code 20 (currently F) was tested as F→N (+11 coverage). Full analysis of all 28 occurrences:

- 10 occurrences form **FINDEN** (to find) — a very strong contextual match
- 7 occurrences form **FACH** (compartment) — which would become NACH (after)
- 1 occurrence forms **FERN** (far)
- 10 occurrences in garbled **NLNDEF** — which would become NLNDEN (still garbled, but contains DEN)

**Verdict: Code 20=F is correct.** Reasons:
1. FINDEN is a semantically crucial word in context ("FINDEN NEIGT DAS ES" = "find, bow, that it...")
2. If 20=N, German text has zero F letters — suspicious even for MHG
3. The +11 gain comes from coincidental short-word matches (IN+DEN replacing FINDEN)
4. FACH→NACH doesn't improve narrative coherence

### 15.9 Recurring Garbled Patterns Summary

Most frequent garbled segments (after IEB→BEI and NU fixes):
- `{T}` single letter: 387 occurrences (all 5 T-codes), part of words like STEINEN**T**ER
- `{HED}` 11x: always codes 57-74-45, possibly MHG for HEID (heath/moor) or truncated HEDEM
- `{HIHL}` 8x: always codes 57-65-94-34, place name
- `{CHN}` 8x: always codes 18-00-14
- `{RUI}` 7x: always codes 72-61-16, followed by extra I (prevents RUIN match)
- `{UTRUNR}` 7x: always codes 44-64-72-61-14-51, place name
- `{SD}` 7x: variable codes (59-45, 13-45, 05-45), possibly part of "DES" or similar
- `{NDCE}` 7x: always codes 60-42-18-30
- `{HECHLLT}` 5x: always codes 57-19-18-94-34-34-64
- `{NLNDEF}` 5x: always codes 90-96-73-47-09-20

### 15.10 Data Files Created

- `data/bookcase_mapping.json` — Complete mapping of 71 library books to 40 bookcases
- `scripts/analysis/parse_bookcases.py` — Parser for Hellgate Library data
- `scripts/analysis/bookcase_narrative.py` — Bookcase-order narrative decoder
- `scripts/analysis/garbled_context_trace.py` — Garbled block code tracer
- `scripts/analysis/session18_deep_analysis.py` — Deep anagram/correction analysis
- `scripts/analysis/session18_code20_investigation.py` — Code 20 F/N investigation

