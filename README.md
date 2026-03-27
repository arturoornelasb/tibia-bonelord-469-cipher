> **Idioma / Language:** [Español](README.es.md) | English

[![DOI](https://zenodo.org/badge/1188959183.svg)](https://doi.org/10.5281/zenodo.19262987)

# Tibia Bonelord 469 Cipher — SOLVED (94.6%)

Computational cryptanalysis of the **Bonelord Language** from the MMORPG [Tibia](https://www.tibia.com). **First known solution** to a 25-year-old cipher.

## The Mystery

The Hellgate Library in Tibia contains **70 books written entirely in digit sequences** — 11,263 digits total. The community calls this the "469 cipher" after the Wrinkled Bonelord's dialogue: *"Our books are written in 469."*

No public solution has existed in 25+ years of community effort.

## Solution

| Result | Value |
|--------|-------|
| **Cipher type** | Homophonic substitution (98 two-digit codes → 22 German letters) |
| **Plaintext language** | German (with Middle High German vocabulary) |
| **Word-level coverage** | **94.6%** (5219/5514 characters) |
| **Letter-level coverage** | **100%** (all codes mapped) |
| **Codes mapped** | 98/100 (codes 07 and 32 never appear in any book) |
| **Sessions** | 31 sessions of systematic cryptanalysis |
| **Content** | Bonelord funerary inscription (LEICH) — King Salzberg, God's Servants, ancient stone ruins, rune magic |

### The Mapping (v7 — 98 codes → 22 letters)

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
Never appear: 07, 32
```

### Key Decoded Phrases

```
"TUN DIE REIST EN ER"              (12x) — "What the travelers do, he..."
"IM MIN HEIME DIE URALTE STEIN"   (11x) — "In my beloved homeland, the ancient stones"
"TRAUT IST LEICH AN BERUCHTIG"     (9x) — "The Trusted One is a corpse, the Notorious"
"DEN EN DE REDER KOENIG"          (10x) — "Of those of the Speaker-King"
"SALZBERG"                         (5x) — "Salt Mountain" (= Salzburg)
"ORANGENSTRASSE"                   (3x) — "Orange Street"
"GOTTDIENER"                       (4x) — "God's Servant"
"WEICHSTEIN"                       (4x) — "Soft Stone"
```

### Confirmed Proper Nouns (Anagram Resolutions)

| Cipher Form | Resolution | Meaning | Pattern |
|------------|-----------|---------|---------|
| LABGZERAS | SALZBERG | "Salt Mountain" (Salzburg) | anagram + 1 letter |
| SCHWITEIONE | WEICHSTEIN | "Soft Stone" | anagram + 1 letter |
| AUNRSONGETRASES | ORANGENSTRASSE | "Orange Street" | anagram + 1 letter |
| EDETOTNIURG | GOTTDIENER | "God's Servant" | anagram + 1 letter |
| ADTHARSC | SCHARDT | Place name | anagram + 1 letter |
| HEDEMI/HEDDEMI | HEIME | "Homeland" (MHG) | anagram |

### Unsolved Proper Nouns

| Name | Freq | Context |
|------|------|---------|
| THENAEUT | 7x | "ER THENAEUT ER ALS STANDE NOT" |
| LGTNELGZ | 7x | Always paired with THENAEUT |
| WRLGTNELNR | 4x | "STEH _ HEL" (stand _ light) |
| NDCE | 9x | "HEHL DIE NDCE FACH" (concealment the _ compartment) |
| HISDIZA | 2x | "NUN AM _ RUNE" (now at _ rune) |

## Novel Techniques

This research produced three novel cryptanalytic techniques, described in a [separate technical paper](papers/bag_of_letters/paper_bag_of_letters.md):

1. **Bag-of-Letters Word Partition (BoLWP)** — Combinatorial multi-word decomposition of garbled cipher blocks with systematic letter-swap tolerance. Largest single-session gain: +10.1% coverage.

2. **Context-Aware Anagram Resolution (CAAR)** — Phrase-boundary-sensitive string replacement that avoids breaking valid compound words during anagram substitution.

3. **Concatenation-Aware Digit-Split Testing (CADST)** — Global validation of per-fragment modifications in fragmented ciphertext, detecting cross-boundary regressions invisible to local testing.

## Repository Structure

```
.
├── README.md / README.es.md           # Bilingual overview (EN/ES)
├── LICENSE                            # MIT License
├── CREATORS.md / .es.md               # Content creator media kit
├── papers/
│   ├── 469_cipher/                    # Main research paper (EN/ES) + PDF
│   ├── bag_of_letters/                # BoLWP technique paper (EN/ES) + PDF
│   └── shared/                        # Shared LaTeX preamble
├── data/
│   ├── mapping_v7.json                # THE mapping (98 codes → 22 letters)
│   ├── books.json                     # 70 books as digit strings
│   ├── bookcase_mapping.json          # Library book → bookcase mapping
│   └── archive/                       # Historical mapping versions (v1-v6)
├── scripts/
│   ├── core/                          # Decryption pipeline & cipher attacks
│   ├── analysis/                      # Per-session analysis & validation
│   └── experimental/                  # Early hypotheses & exploratory work
├── docs/
│   ├── INDEX.md                       # Documentation index (EN/ES)
│   ├── findings.md                    # Complete 31-session research log (7000+ lines)
│   ├── narrative_translation.md       # All 70 books translated (DE/EN/ES)
│   ├── hellgate_library_guide.md      # Wiki-ready library guide (71 books)
│   ├── investigation/                 # In-game research & NPC data
│   └── archive/                       # Legacy community data
└── archive/                           # Internal agent work artifacts
```

> See [docs/INDEX.md](docs/INDEX.md) for the complete documentation index.

## Quick Start

```bash
# Decode all 70 books with 94.6% word coverage
python scripts/core/narrative_v3_clean.py
```

## Why Was This Unsolved for 25 Years?

1. **Homophonic substitution** (98 codes for 22 letters) defeats frequency analysis
2. **No spaces** in the encoded text — no word boundaries
3. **German plaintext** — most attackers assumed English
4. **CipSoft removed digits** from 37/70 books to break pair alignment
5. **Short text** — 5,515 unique chars is marginal for blind homophonic cracking
6. **Anagrammed proper nouns** with +1 extra letter
7. **"Mathemagic" red herring** — NPC dialogue misdirects toward math, not language

## License

**MIT License** — Use freely for any purpose.

Game data (`books.json`) contains community-transcribed content from Tibia, which is the intellectual property of CipSoft GmbH. Included for research purposes.

See [CREATORS.md](CREATORS.md) for a content creator media kit.

## Acknowledgments

- **CipSoft GmbH** for creating and maintaining Tibia since 1997
- **s2ward/469** repository for community-transcribed book data
- **TibiaSecrets** and **Tales of Tibia** for prior analysis

---

*This research was conducted independently. CipSoft GmbH owns all intellectual property related to Tibia and its in-game content.*

---

## Disclaimer — by kardfon dogon

**I cannot confirm that the decoded content is the actual intended plaintext.**

The mapping passes every computational validation test we threw at it: Index of Coincidence confirms German + 2-digit encoding (independent of any mapping), 164 book overlaps decode with zero inconsistencies, letter frequencies match German within 2%, and the mapping outperforms all 200 random permutations tested (p < 0.005). The math is solid.

But math alone doesn't prove CipSoft wrote these words.

### How we got here

The Hellgate Library books are 70 digit sequences totaling 11,263 digits. We treated them as a **homophonic substitution cipher**: each pair of two digits encodes one of 22 German letters, with multiple codes per letter (E alone has 20 codes). The attack combined:

- **Frequency analysis** to establish code-to-letter proportions
- **NPC dialogue cribs** (known phrases from the Wrinkled Bonelord) as anchors for known-plaintext attacks
- **Book overlap chains** — books share suffix-prefix overlaps, letting us reconstruct 12 chains from the 70 fragments
- **Bag-of-Letters Word Partition (BoLWP)** — a novel technique that decomposes garbled letter blocks into valid German word combinations, tolerating systematic letter swaps
- **Concatenation-Aware Digit-Split Testing** — CipSoft removed a single digit from 37/70 books to break pair alignment; we brute-forced the optimal insertion for each
- **Context-Aware Anagram Resolution** — proper nouns are anagrammed with +1 extra letter (LABGZERAS = SALZBERG + A), matching CipSoft's known pattern (Ferumbras, Vladruc, Dallheim)

### The overfitting concern

With 98 codes mapped to 22 letters and a 5,515-character corpus, there are enough degrees of freedom that a determined optimizer *could* force plausible-looking German text out of random data. Our 94.6% word coverage is measured against a German dictionary — but the 5.4% gap consists of consonant clusters and undecoded proper nouns, not random noise. That's either evidence of a real archaic German text with bonelord-specific vocabulary... or evidence of a very convincing overfit.

### Books vs NPCs: two different cipher systems

This is critical and often overlooked:

- **The 70 library books** use a clean **two-digit homophonic substitution** — pairs of digits map to letters, no spaces, no punctuation. This is what we solved.
- **NPC dialogue** (Avar Tar's poem, Evil Eye utterances) uses a **completely different encoding** — variable-length digit groups separated by spaces, with patterns that don't match the book cipher at all. Avar Tar's poem has groups like `29639`, `46781`, `9063376290` — these are NOT two-digit pairs.

We solved the books. We have NOT solved the NPC cipher. They may use the same underlying language but a different encoding scheme, or they may be entirely separate systems. **Until someone cracks the NPC encoding independently and finds it consistent with the book solution, the two systems remain unlinked.**

### What we tested in-game

I went back to Tibia after years away and tested decoded keywords (`SALZBERG`, `RUNE`, `STEIN`, `LEICH`, `GOTTDIENER`, `SCHARDT`) with the Wrinkled Bonelord. **No results.** No new dialogue, no reactions, nothing. This is strange, but it doesn't necessarily disprove the solution — my theory is that bonelord *written* language and bonelord *spoken* language may be fundamentally different systems. Bonelords communicate by blinking their eyes in patterns, which could explain why the NPC's spoken dialogue uses a completely different encoding than the library books. The books are *written* records — perhaps in a formal or archaic register that doesn't map to how a living bonelord "speaks" through eye-blinks.

### What the community can help with

- **Avar Tar in Edron** — This NPC recites a poem in 469 and could be critical for obtaining more data. His poem uses variable-length digit groups (not two-digit pairs like the books), suggesting a different encoding layer. Cracking his poem independently and finding consistency with the book narrative would be the smoking gun.
- **Cross-reference with Tibia lore** — Do "King Salzberg", "Orangenstrasse", "Weichstein", or "Gottdiener" appear anywhere else in the game? Any wiki reference, any NPC dialogue, any book outside Hellgate?
- **More cipher texts** — Are there 469-encoded texts outside Hellgate? Isle of Kings? Ferumbras Citadel? The more data, the stronger (or weaker) the solution becomes.
- **Native German speakers** — The decoded text appears to be Middle High German. A native speaker or MHG scholar reviewing the text could confirm whether it reads as coherent archaic German or as statistical noise that happens to look like words.

The statistical evidence says this mapping is real. The decoded text reads like archaic German with a coherent funeral narrative. But I've spent enough hours staring at these digits to know that pattern recognition is a hell of a drug, and the human brain is disturbingly good at finding meaning in noise.

I retired from Tibia years ago and came back to fulfill my dream of reaching level 100. I found a completely different game — one that no longer motivates me to play. But this bonelord enigma always intrigued me, and I'll remain available to the community to keep exploring.

I just hope this isn't another door like the one at level 999.
