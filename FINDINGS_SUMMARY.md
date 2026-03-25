# Research Findings — Executive Summary

> **Full log:** [`findings/`](findings/README.md) (25 session files, 7425 lines)
> **Complete log:** [`FINDINGS.md`](FINDINGS.md) (single file, 320 KB)

---

## Result

The Tibia 469 / Bonelord Language cipher has been **solved at 94.6% word-level coverage** across 5,514 characters in 70 books.

| Metric | Value |
|--------|-------|
| Cipher type | Homophonic substitution |
| Plaintext language | German (with Middle High German vocabulary) |
| Codes in mapping | 98 two-digit codes → 22 German letters |
| Word-level coverage | **94.6%** (5,219 / 5,514 characters) |
| Unresolved | ~5.4% (295 chars — proper nouns with no known referent) |
| Research sessions | 31 |
| Codes never appearing | 07, 32 (unused in corpus) |

---

## The Mapping (v7)

```
E (20 codes): 95 56 19 26 76 01 41 30 86 67 27 03 09 17 29 49 39 74 37 69
N (10 codes): 60 11 14 48 58 13 93 53 73 90
I  (8 codes): 21 15 46 71 65 16 50 24
S  (7 codes): 92 91 52 59 12 23 05
T  (6 codes): 88 78 64 75 81 98
D  (6 codes): 45 42 47 63 28 02
R  (6 codes): 72 51 55 08 68 10
A  (5 codes): 31 85 35 89 66
H  (4 codes): 06 00 57 94
U  (4 codes): 61 43 70 44
O  (4 codes): 99 82 25 79
M  (3 codes): 04 54 40
G  (3 codes): 80 97 84
L  (2 codes): 34 96
W  (2 codes): 36 87
K  (2 codes): 22 38
C  (1 code):  18
F  (1 code):  20
B  (1 code):  62
Z  (1 code):  77
V  (1 code):  83
```

Canonical mapping file: [`data/mapping_v7.json`](data/mapping_v7.json)

---

## Content Summary

The 70 books form a **funerary inscription (LEICH)** — a poetic/religious text commemorating
a Bonelord king. Recurring themes:

- **King Salzberg** (KOENIG LABGZERAS → anagram of SALZBERG + 1 letter)
- **Ancient stone ruins** (URALTE STEINE / STEIN) — a sacred site
- **"God's Servants"** (GOTTDIENER) — a religious order or title
- **The Speaker-King** (DER REDER KOENIG) — a recurring epithet
- **Homeland** (HEIME / HEDEMI) — the Bonelords' ancestral place

### Most Frequent Phrases

| German | English | Occurrences |
|--------|---------|-------------|
| TUN DIE REIST EN ER | "What the travelers do, he..." | 12× |
| IM MIN HEIME DIE URALTE STEIN | "In my beloved homeland, the ancient stones" | 11× |
| DEN EN DE REDER KOENIG | "Of those of the Speaker-King" | 10× |
| TRAUT IST LEICH AN BERUCHTIG | "The Trusted One is a corpse, the Notorious" | 9× |

### Resolved Proper Nouns

| Cipher Form | Resolution | Meaning |
|------------|-----------|---------|
| LABGZERAS | SALZBERG | "Salt Mountain" (= Salzburg) |
| SCHWITEIONE | WEICHSTEIN | "Soft Stone" |
| AUNRSONGETRASES | ORANGENSTRASSE | "Orange Street" |
| EDETOTNIURG | GOTTDIENER | "God's Servant" |
| ADTHARSC | SCHARDT | Place name |
| HEDEMI / HEDDEMI | HEIME | "Homeland" (MHG) |

### Still-Unresolved Proper Nouns (5.4%)

| Name | Freq | Context |
|------|------|---------|
| THENAEUT | 7× | "ER THENAEUT ER ALS STANDE NOT" |
| LGTNELGZ | 7× | Paired with THENAEUT |
| WRLGTNELNR | 4× | "STEH _ HEL" |
| NDCE | 9× | "HEHL DIE NDCE FACH" |
| HISDIZA | 2× | "NUN AM _ RUNE" |

---

## Why It Was Unsolved for 25 Years

1. **Homophonic substitution** — 98 codes for 22 letters defeats standard frequency analysis
2. **No word boundaries** — no spaces in encoded text
3. **German plaintext** — community assumed English
4. **CipSoft added noise digits** to 37/70 books to break pair alignment
5. **Short corpus** — 5,515 chars is marginal for blind homophonic cracking
6. **Anagrammed proper nouns** with +1 extra letter obscure known words
7. **NPC "Mathemagic" dialogue** misdirects toward mathematics

---

## Novel Techniques Developed

Three techniques were developed during this research and described in a
[separate paper](papers/bag_of_letters/paper_bag_of_letters.md):

**1. Bag-of-Letters Word Partition (BoLWP)**
Combinatorial multi-word decomposition of garbled cipher blocks with systematic
letter-swap tolerance. Largest single-session gain: **+10.1% coverage** (Session 29:
81.1% → 89.1%).

**2. Context-Aware Anagram Resolution (CAAR)**
Phrase-boundary-sensitive string replacement that avoids breaking valid compound
words during anagram substitution.

**3. Concatenation-Aware Digit-Split Testing (CADST)**
Global validation of per-fragment modifications in fragmented ciphertext, detecting
cross-boundary regressions invisible to local testing.

---

## Coverage Progression

| Session(s) | Coverage | Key Event |
|-----------|----------|-----------|
| 1–4 | 0% → ~40% | 2-digit encoding confirmed; URALTE STEINE crib |
| 5–9 | 40% → ~55% | Systematic tier assignments (T,A,G,R,F,L,O,E,C,N...) |
| 10–13 | 55% → ~60% | Deep pattern attack; geographic anagram breakthrough |
| 14–15 | 60% → ~65% | Constraint solver V8; simulated annealing |
| 16–19 | 65% → ~70% | Bookcase mapping; cross-boundary anagrams |
| 20–25 | 70% → ~81% | Systematic block attacks; proper noun confirmations |
| 26–28 | 76% → ~81% | Swap-tolerant attacks |
| **29** | 81.1% → **89.1%** | **BoLWP breakthrough** |
| 30 | 91.2% → 93.3% | DIGIT_SPLIT optimization |
| 31 | 94.4% → **94.6%** | Final fixups — current state |

---

## Files

| File | Description |
|------|-------------|
| [`data/mapping_v7.json`](data/mapping_v7.json) | The solution — 98 codes → 22 letters |
| [`data/books.json`](data/books.json) | 70 books as digit strings |
| [`data/decoded_narrative.json`](data/decoded_narrative.json) | Full decoded text with coverage tracking |
| [`data/decoded_text.txt`](data/decoded_text.txt) | Human-readable German plaintext output |
| [`docs/narrative_translation.md`](docs/narrative_translation.md) | All 70 books translated (DE/EN/ES) |
| [`scripts/core/narrative_v3_clean.py`](scripts/core/narrative_v3_clean.py) | Canonical decoder script |

---

*See [`findings/README.md`](findings/README.md) for the full session-by-session log.*
