> **Idioma / Language:** [Español](README.es.md) | English

# Tibia Bonelord 469 Cipher — SOLVED (94.4%)

Computational cryptanalysis of the **Bonelord Language** from the MMORPG [Tibia](https://www.tibia.com). **First known solution** to a 25-year-old cipher.

## The Mystery

The Hellgate Library in Tibia contains **70 books written entirely in digit sequences** — 11,263 digits total. The community calls this the "469 cipher" after the Wrinkled Bonelord's dialogue: *"Our books are written in 469."*

No public solution has existed in 25+ years of community effort.

## Solution

| Result | Value |
|--------|-------|
| **Cipher type** | Homophonic substitution (98 two-digit codes → 22 German letters) |
| **Plaintext language** | German (with Middle High German vocabulary) |
| **Word-level coverage** | **94.4%** (5204/5515 characters) |
| **Letter-level coverage** | **100%** (all codes mapped) |
| **Codes mapped** | 98/100 (codes 07 and 32 never appear in any book) |
| **Sessions** | 30 sessions of systematic cryptanalysis |
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

This research produced three novel cryptanalytic techniques, described in a [separate technical paper](docs/paper_bag_of_letters.md):

1. **Bag-of-Letters Word Partition (BoLWP)** — Combinatorial multi-word decomposition of garbled cipher blocks with systematic letter-swap tolerance. Largest single-session gain: +10.1% coverage.

2. **Context-Aware Anagram Resolution (CAAR)** — Phrase-boundary-sensitive string replacement that avoids breaking valid compound words during anagram substitution.

3. **Concatenation-Aware Digit-Split Testing (CADST)** — Global validation of per-fragment modifications in fragmented ciphertext, detecting cross-boundary regressions invisible to local testing.

## Repository Structure

```
.
├── README.md / README.es.md           # Bilingual overview (EN/ES)
├── LICENSE                            # BUSL-1.1 (free for individuals/academics/non-profits)
├── COMMERCIAL.md / .es.md             # Commercial participation guidelines
├── CREATORS.md / .es.md               # Content creator guidelines & media kit
├── TERMS.md / .es.md                  # Terms of use & contribution obligation
├── FINDINGS.md                        # Complete 30-session research log (7000+ lines)
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
│   ├── paper_469_cipher.md / .es.md   # Research paper (EN/ES)
│   ├── paper_bag_of_letters.md / .es.md # BoLWP technique paper (EN/ES)
│   ├── narrative_translation.md       # All 70 books translated (DE/EN/ES)
│   ├── hellgate_library_guide.md      # Wiki-ready library guide (71 books)
│   ├── roadmap_ingame.md              # In-game verification roadmap
│   ├── npc-research.md                # NPC dialogue research
│   └── archive/                       # Legacy community data
└── agente3/                           # Spanish-language investigation phases
```

> See [docs/INDEX.md](docs/INDEX.md) for the complete documentation index.

## Quick Start

```bash
# Decode all 70 books with 94.4% word coverage
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

**Business Source License 1.1 (BUSL-1.1)**

- **Free for:** individuals, academics, researchers, non-profits
- **Commercial use:** requires participation agreement (see [COMMERCIAL.md](COMMERCIAL.md))
- **Contribution obligation:** improvements must be shared back (see [TERMS.md](TERMS.md))
- **Change date:** 2030-03-24 (auto-converts to AGPL-3.0)
- **Game data:** CipSoft GmbH intellectual property, included under fair use for research

See [LICENSE](LICENSE) for full terms.

**Content creators:** You can monetize freely — no license needed. See [CREATORS.md](CREATORS.md) for attribution guidelines and media kit.

## Acknowledgments

- **CipSoft GmbH** for creating and maintaining Tibia since 1997
- **s2ward/469** repository for community-transcribed book data
- **TibiaSecrets** and **Tales of Tibia** for prior analysis

---

*This research was conducted independently. CipSoft GmbH owns all intellectual property related to Tibia and its in-game content.*
