## 22. Session 25: Cross-Boundary Anagram Breakthrough, Parallel Attack

### 22.1 Coverage Progress

| Metric | Start | End |
|--------|-------|-----|
| Word coverage | 71.9% (3974/5528) | 72.9% (4030/5528) |
| Confirmed anagrams | 33 | 39 (+6 cross-boundary) |
| New chars matched | — | +56 |

### 22.2 Methodology: 5-Agent Parallel Attack

Session 25 used 5 parallel analysis agents:
1. **Web Research**: No new public breakthroughs; s2ward/469 last active Dec 2024 (DNA sequence alignment approach by elkolorado)
2. **Code Error Detection**: Brute-force tested all 34 unconfirmed codes × 20 letters. Only 3 marginal candidates found (Code 39: E→H +6, Code 69: E→H +3, Code 02: D→B +1). Mapping v7 confirmed solid.
3. **Cross-Boundary Anagram Discovery**: Found 9 candidates, 6 validated (+56 chars)
4. **Big Block Decomposition**: Blocked by permissions, deferred
5. **Vocabulary Mining**: Confirmed garbled blocks are the main coverage barrier, not missing vocabulary

### 22.3 Six New Cross-Boundary Anagrams

| # | Source | Resolution | Gain | Freq | Meaning |
|---|--------|-----------|------|------|---------|
| 1 | SERTI | STIER | +12 | 9x | bull/steer (German) |
| 2 | ESR | SER | +11 | 14x | very (MHG, word boundary fix) |
| 3 | NEDE | ENDE | +10 | 14x | end (word boundary fix) |
| 4 | NTES | NEST | +8 | 4x | nest (German) |
| 5 | HIM | IHM | +8 | 8x | him/to him (dative) |
| 6 | EUTR | TREU | +7 | 7x | faithful/loyal |

**Rejected candidates:**
- ERT → TER: -13 chars (breaks existing word boundaries, harmful)
- ESD → DES: -8 chars (harmful)
- HHE → HEH: 0 gain (neutral)

### 22.4 Key Narrative Discoveries

**STIER (bull/steer)** appears 9x in context:
```
ER {A} STIER {URIT} ORANGENSTRASSE SICH
```
Reading: "he [?] bull/steer [?] Orange Street himself" — possibly a title or attribute.
Always appears near ORANGENSTRASSE and the THENAEUT phrases.

**IHM (to him)** resolves 8 garbled {H} blocks:
```
GOTTDIENER {T} ES SIN IHM NU STEH WRLGTNELNR HEL UIRUNNHWND FINDEN
```
Reading: "God's-servant, it is to-him now stand [?] bright [?] find" — the Gottdiener receives/stands before something.

**TREU (faithful)** appears 7x:
```
ODE TREU {UNR} DEN ENDE REDER KOENIG SALZBERG
```
Reading: "or faithful [?] the end-speaker King Salzberg" — loyalty/faithfulness tied to the king.

**NEST** appears 4x:
```
ENGE ENDE NEST TUT {IGAA} ER GEIGET
```
Reading: "narrow end nest does [?] he fiddles" — a compressed ritual description.

### 22.5 Updated Anagram Count: 39 confirmed

Session 25 additions: SERTI→STIER, ESR→SER, NEDE→ENDE, NTES→NEST, HIM→IHM, EUTR→TREU

### 22.6 Mapping v7 Stability Confirmed

Brute-force testing of all 34 unconfirmed codes against 20 possible letter assignments found no significant improvements. The maximum possible gain from any single code change is +6 chars (Code 39: E→H), affecting only 2 occurrences — too marginal to justify the change without additional evidence.

### 22.7 Community Research Summary

- s2ward/469 GitHub: last activity Dec 2024 (elkolorado contributor, DNA alignment approach)
- No public solution or breakthrough in 2025-2026
- TibiaWiki confirmed: Wrinkled Bonelord NPC script has 20+ keyword responses
- "Circular Canon of Eternal Darkness" in Drefia uses symbol-based (not numeric) encoding — separate system
- Tales of Tibia articles theorize 469 as coordinate/location system (not confirmed by our analysis)

### 22.8 Per-Book Coverage Highlights

| Book | Coverage | Key Text |
|------|----------|----------|
| Book 22 | **97%** | "TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIES ER {T} EIN ER SEI ENDE TOT RUIN" |
| Book 39 | **96%** | "ES ER SCHRAT SCE AUS ER {T} AM KLAR SUN" |
| Book  2 | **94%** | "TRAUT IST LEICH AN BERUCHTIG...GOTTDIENER" |
| Book  0 | **93%** | "URALTE STEINEN TER SCHARDT IST SCHAUN RUIN" |
| Book 18 | **93%** | "GAR HIER SER EIGENTUM ORTEN...DU NUR ALTES IN IHM" |

### 22.9 Remaining Garbled Blocks (27.1%)

Top blocks by total chars:
| Block | Freq | Total chars | Status |
|-------|------|-------------|--------|
| {UIRUNNHWND} | 6x | 60 | Proper noun (WINDUNRUH+N hypothesis) |
| {HIHL} | 8x | 32 | Proper noun (HEHL hypothesis) |
| {NDCE} | 7x | 28 | Proper noun |
| {T} | 25x | 25 | Single-letter structural artifact |
| {CHN} | 8x | 24 | Inside larger blocks |
| {D} | 22x | 22 | Single-letter artifact |
| {UNR} | 7x | 21 | Unresolved 3-char block |
| {HECHLLT} | 5x | 35 | Proper noun (HECHELT hypothesis) |
| {E} | 20x | 20 | Single-letter artifact |
| {RRNI} | 5x | 20 | Proper noun |

### 22.10 Data Files Created

- `scripts/analysis/session25_code_errors.py` — Garbled rate per code analysis
- `scripts/analysis/session25_code_errors_v2.py` — Brute-force all unconfirmed codes
- `scripts/analysis/session25_cross_boundary.py` — Cross-boundary anagram discovery
- `scripts/analysis/session25_vocab_mining.py` — Aggressive vocabulary mining
- `scripts/analysis/session25_validate_and_apply.py` — Validation and application of new anagrams

