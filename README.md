> **Idioma / Language:** [Español](README.es.md) | English

# Tibia Bonelord 469 Cipher — Solved (94.6%)

Computational cryptanalysis of the **Bonelord Language** from the MMORPG [Tibia](https://www.tibia.com).
**First known solution** to a 25-year-old unsolved cipher.

---

## The Mystery

The Hellgate Library in Tibia contains **70 books written entirely in digit sequences** — 11,263
digits total. The community calls this the "469 cipher" after the Wrinkled Bonelord's dialogue:
*"Our books are written in 469."*

No public solution has existed in 25+ years of community effort.

---

## Solution

| Result | Value |
|--------|-------|
| **Cipher type** | Homophonic substitution (98 two-digit codes → 22 German letters) |
| **Plaintext language** | German (with Middle High German vocabulary) |
| **Word-level coverage** | **94.6%** (5,219 / 5,514 characters) |
| **Codes mapped** | 98 / 100 (codes 07 and 32 never appear) |
| **Research sessions** | 31 |
| **Content** | Bonelord funerary inscription — King Salzberg, ancient ruins, rune magic |

### The Mapping (v7)

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
C  (1 code):  18    F (1 code): 20    B (1 code): 62
Z  (1 code):  77    V (1 code): 83
Never appear: 07, 32
```

Machine-readable: [`data/mapping_v7.json`](data/mapping_v7.json)

### Key Decoded Phrases

```
"TUN DIE REIST EN ER"             (12×)  "What the travelers do, he..."
"IM MIN HEIME DIE URALTE STEIN"  (11×)  "In my beloved homeland, the ancient stones"
"TRAUT IST LEICH AN BERUCHTIG"    (9×)  "The Trusted One is a corpse, the Notorious"
"DEN EN DE REDER KOENIG"         (10×)  "Of those of the Speaker-King"
"SALZBERG"                         (5×)  "Salt Mountain" (= Salzburg)
```

### Confirmed Proper Nouns (Anagram Resolutions)

| Cipher Form | Resolution | Meaning | Method |
|------------|-----------|---------|--------|
| LABGZERAS | SALZBERG | "Salt Mountain" (Salzburg) | anagram + 1 letter |
| SCHWITEIONE | WEICHSTEIN | "Soft Stone" | anagram + 1 letter |
| AUNRSONGETRASES | ORANGENSTRASSE | "Orange Street" | anagram + 1 letter |
| EDETOTNIURG | GOTTDIENER | "God's Servant" | anagram + 1 letter |
| ADTHARSC | SCHARDT | Place name | anagram + 1 letter |
| HEDEMI / HEDDEMI | HEIME | "Homeland" (MHG) | anagram |

---

## Quick Start

```bash
# Decode all 70 books with the canonical mapping
make decode
# or directly:
python scripts/core/narrative_v3_clean.py
```

See the [Makefile](Makefile) for the full pipeline (build → optimize → anagram → decode).

---

## Novel Techniques

Three cryptanalytic techniques were developed during this research:

**Bag-of-Letters Word Partition (BoLWP)**
Combinatorial multi-word decomposition of garbled cipher blocks with letter-swap tolerance.
Single-session gain: +10.1% (Session 29: 81.1% → 89.1%).

**Context-Aware Anagram Resolution (CAAR)**
Phrase-boundary-sensitive anagram substitution that avoids breaking valid compound words.

**Concatenation-Aware Digit-Split Testing (CADST)**
Global cross-boundary validation of per-fragment changes in fragmented ciphertext.

Described formally in [`papers/bag_of_letters/`](papers/bag_of_letters/).

---

## Repository Structure

```
tibia-research/
│
├── README.md / README.es.md          Bilingual overview (this file)
├── FINDINGS_SUMMARY.md               Executive summary of all results
├── FINDINGS.md                       Complete 31-session research log (320 KB)
├── Makefile                          Pipeline entry points
├── LICENSE                           BUSL-1.1
│
├── data/                             Corpus and solution files
│   ├── mapping_v7.json               THE SOLUTION — 98 codes → 22 letters
│   ├── books.json                    70 books as digit strings (11,263 digits)
│   ├── decoded_text.txt              Human-readable German plaintext output
│   ├── decoded_narrative.json        Full decoded text with coverage tracking
│   ├── bookcase_mapping.json         Book → physical bookcase location
│   ├── chain_info.json               12 narrative chains + 12 isolated books
│   ├── master_text.txt               Reconstructed continuous narrative
│   └── archive/                      Historical mapping versions v1–v6
│
├── scripts/
│   └── core/                         14 canonical pipeline scripts
│       ├── narrative_v3_clean.py     ← MAIN DECODER (run this)
│       ├── build_v7_and_attack.py    Mapping builder
│       ├── simulated_annealing_v8.py Optimization
│       ├── constraint_solver_v8.py   Constraint-based solver
│       ├── anagram_bruteforce.py     Anagram resolution
│       ├── anagram_resolution.py     Anagram resolution (alternate)
│       ├── geographic_anagram_attack.py  Geographic context attack
│       ├── deep_anagram_attack.py    Deep anagram search
│       ├── comprehensive_attack.py   Combined attack
│       ├── crib_garbled_attack.py    Crib-drag attack
│       ├── crack_garbled_core.py     Garbled segment attack
│       ├── gap_code_reassignment.py  Gap code handling
│       ├── test_combinations_v7.py   Combination testing
│       └── narrative_translate.py    Translation output
│
├── findings/                         Session-by-session research log
│   ├── README.md                     Session index + coverage progression
│   ├── session_01_04_early.md        Sessions 1–4: initial breakthrough
│   ├── session_05.md ... session_31.md
│   └── (25 files total)
│
├── papers/                           Research papers
│   ├── 469_cipher/                   Main paper (EN/ES, MD + PDF + LaTeX)
│   └── bag_of_letters/               BoLWP technique paper (EN/ES, MD + PDF + LaTeX)
│
├── docs/                             Documentation
│   ├── INDEX.md                      Documentation index
│   ├── narrative_translation.md      All 70 books translated (DE/EN/ES)
│   ├── hellgate_library_guide.md     Wiki-ready library guide (71 books)
│   ├── investigation/                In-game research & NPC data
│   └── archive/                      Legacy community data
│
└── archive/                          Historical research artifacts
    ├── README.md
    ├── scripts/experimental/         79 early-hypothesis scripts
    ├── scripts/sessions/             43 per-session crack scripts (Sessions 9–12)
    ├── scripts/core_misc/            27 one-off investigation scripts
    ├── scripts/analysis/             81 per-session analysis scripts (Sessions 18–31)
    └── agente3/                      Spanish-language investigation phase
```

---

## Reproducing Results

### From the committed mapping (fastest)

```bash
# Prerequisites: Python 3.8+, no external packages
python scripts/core/narrative_v3_clean.py
# Output: data/decoded_text.txt, data/decoded_narrative.json
```

### Full pipeline (re-derives mapping from scratch)

```bash
make build       # frequency analysis + initial mapping
make optimize    # simulated annealing refinement
make constrain   # constraint-solver pass
make anagram     # anagram resolution
make anagram-geo # geographic anagram attack
make gap         # gap code reassignment
make crib        # crib-drag on garbled segments
make decode      # final decode
make translate   # human-readable translation output
```

---

## Why Was This Unsolved for 25 Years?

1. **Homophonic substitution** — 98 codes for 22 letters defeats frequency analysis
2. **No word boundaries** — no spaces anywhere in the ciphertext
3. **German plaintext** — most attackers assumed English
4. **Noise digits inserted** — CipSoft removed digits from 37/70 books to misalign pairs
5. **Short corpus** — 5,515 chars is marginal for blind homophonic cracking
6. **Anagrammed proper nouns** with +1 extra letter obscure recognizable words
7. **NPC "Mathemagic" misdirection** — dialogue steers solvers toward mathematics

---

## Papers

| Paper | Description |
|-------|-------------|
| [papers/469_cipher/](papers/469_cipher/) | Main paper: full cipher analysis, methodology, results (EN/ES + PDF) |
| [papers/bag_of_letters/](papers/bag_of_letters/) | BoLWP / CAAR / CADST technique descriptions (EN/ES + PDF) |

---

## License

**Business Source License 1.1 (BUSL-1.1)**

- **Free for:** individuals, academics, researchers, non-profits
- **Commercial use:** requires participation agreement (see [COMMERCIAL.md](COMMERCIAL.md))
- **Contribution obligation:** improvements must be shared back (see [TERMS.md](TERMS.md))
- **Change date:** 2030-03-24 (converts automatically to AGPL-3.0)
- **Game data:** CipSoft GmbH intellectual property, included under fair use for research

**Content creators:** No license required for videos/articles — see [CREATORS.md](CREATORS.md).

---

## Acknowledgments

- **CipSoft GmbH** for creating and maintaining Tibia since 1997
- **[s2ward/469](https://github.com/s2ward/469)** for community-transcribed book data
- **TibiaSecrets** and **Tales of Tibia** for prior analysis work

---

*Independent research. CipSoft GmbH owns all intellectual property related to Tibia.*
