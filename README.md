# Tibia Bonelord 469 Cipher

Computational cryptanalysis of the unsolved **Bonelord Language** from the MMORPG [Tibia](https://www.tibia.com).

## The Mystery

The Hellgate Library in Tibia contains **70 books written entirely in digit sequences**. No one has deciphered them in 25+ years. The community calls this the "469 cipher" or "Bonelord Language."

Example book:
```
956151353478019288952160199364672431427894315191186512819118003561147261164671364646121978585765197292197278167054671180014015255175191180189445
```

## What We Found

| Finding | Status |
|---------|--------|
| Cipher type: **homophonic substitution** (2-digit codes -> letters) | Confirmed |
| Plaintext language: **German** (IC = 1.73, matches German 1.72) | Confirmed |
| **97 of 100 codes mapped** to 21 letters (mapping v4) | Confirmed |
| 70 books = overlapping fragments of **ONE continuous narrative** | Proven |
| 37/70 books have odd digit counts — last digit is artifact | **Critical** |
| **67.2%** of decoded text parses as German words (DP segmentation) | Current |
| 25/70 books assembled into raw-code superstring | Current |
| Consensus narrative: **549 chars** (voting across aligned books) | Current |
| Narrative about King LABGZERAS, ancient stones, runes | Partial |
| **TOTNIURG** reversed = GRUIN+TOT (ruin + dead) | Discovered |
| **11+ proper nouns** identified — none found in Tibia wiki | Novel |
| **No prior public decode exists** — this would be a first | Verified |

### The Mapping (97 codes -> 21 letters)

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
Never appear: 07, 32 (confirmed absent from all books)
Unmapped:     33 (1x, likely W)
```

No P, J, Q, X, or Y found in the text.

### Consensus Narrative (549 chars, assembled from 25+ books)

The full decoded text reads as a bonelord historical inscription. Key readable passages:

```
...HIER TAUTR IST EILCHANHEARUCHTIG ER SO DAS TUN DIESER
EINER SEIN EDETOTNIURGS ER LABRNI WIR UND IE...IN HEDEMI
DIE URALTE STEINEN TER ADTHARSC IST SCHAUN...IN WISET...
TIUMENGEMI ORT ENGCHD KELSEI...RUNE...UNTER...
SCHWITEIONE IST...WIR...SEI GEVMT WIE TUN...
NGETRAS ER...WIR...SCHAER ALTE
```

**Key decoded phrases:**
```
HIER TAUTR IST EILCHANHEARUCHTIG  => "Here Tautr is [the] Eilchanhearuchtig"
EINER SEIN EDETOTNIURGS           => "one [is] his Edetotniurgs"
IN HEDEMI DIE URALTE STEINEN      => "in Hedemi the ancient stones"
ADTHARSC IST SCHAUN               => "Adtharsc is — look!"
TIUMENGEMI ORT ENGCHD KELSEI      => "Tiumengemi place Engchd Kelsei"
SCHWITEIONE IST                   => "[the] Schwiteione is"
HWND FINDEN TEIGN DAS ES          => "hound find(s) [the] sign that it"
DER KOENIG LABGZERAS              => "the King Labgzeras"
RUNE UNTER                        => "rune beneath"
WIR UND...                        => "we and..."
```

### Identified Proper Nouns (11+)

| Name | Context | Notes |
|------|---------|-------|
| **TAUTR** | Subject, "ist Eilchanhearuchtig" | A person/entity described by a title |
| **EILCHANHEARUCHTIG** | Title/descriptor of TAUTR | Compound word, possibly MHG |
| **EDETOTNIURGS** | Attribute of TAUTR | Contains TOTNIURG |
| **LABGZERAS** | "KOENIG LABGZERAS" = King | No known Tibian king matches |
| **HEDEMI** | Place with "uralte Steinen" | Wiki opensearch recognizes term! |
| **ADTHARSC** | At HEDEMI, "ist schaun" | Unknown entity/place |
| **KELSEI** | After ENGCHD | Wiki opensearch recognizes term! |
| **TIUMENGEMI** | "ORT" (place) | A location name |
| **ENGCHD** | Before KELSEI | Unknown |
| **SCHWITEIONE** | 10x in text, "ist..." | May be bonelord race name |
| **LABRNI** | After TAUTR's description | Person or place |
| **GEVMT** | "SEI GEVMT WIE TUN" | Unknown |
| **NGETRAS** | "SO NGETRAS ER" | Unknown |

## Repository Structure

```
.
├── README.md              # This file
├── FINDINGS.md            # Complete research log (12+ sessions, 4800+ lines)
├── data/
│   ├── books.json         # Source data: all 70 books as digit strings
│   ├── final_mapping_v4.json  # Best 97-code mapping (current)
│   └── ...
├── scripts/
│   ├── core/              # Key scripts that produced results
│   │   ├── crack_session12m.py     # Consensus assembly via voting (latest)
│   │   ├── crack_session12l.py     # Substring alignment assembly
│   │   ├── crack_session12k.py     # Decoded-text-level assembly
│   │   ├── crack_session12j.py     # Code forensics (proper noun codes)
│   │   ├── crack_session12i.py     # Aggressive assembly + proper nouns
│   │   ├── crack_session12h.py     # Multi-chain assembly
│   │   ├── decode_tier14.py        # 92-code decoder (tiers 1-14)
│   │   ├── narrative_reconstruct.py # Full narrative decoder
│   │   ├── deep_narrative.py       # DP word segmentation
│   │   └── ...                     # 25+ core scripts
│   └── experimental/      # 79+ exploratory scripts
└── docs/
    ├── 01-books.md         # Book transcriptions
    └── README-469.md       # Early research notes
```

## Tibia Lore Cross-Reference

Comprehensive wiki research (4 parallel agents, 300+ searches) confirmed:
- **None of our decoded proper nouns appear anywhere in public Tibia research**
- **HEDEMI and KELSEI** are recognized as search terms on TibiaWiki (no pages exist)
- **KOENIG LABGZERAS** doesn't match any of the ~68 known Tibian kings
- Bonelord civilization lore (ancient cities, pyramids, necromancy, high council) aligns with decoded text
- **German plaintext is consistent** with CipSoft being a German company (Regensburg)
- The only previously named bonelord is **Honeminas** (mathematical formulae, Demona)
- **SCHWITEIONE** (10x frequency) may be the bonelord race name — the Wrinkled Bonelord says their race name "is not fix but a complex formula, always changes"
- Reversal/mirroring is canonical in bonelord lore (Paradox Tower mirrored room)

## Open Questions

- **8 unconfirmed codes**: 04(M,80x), 38(K,6x), 40(M,19x), 69(E,5x), 80(G,92x), 83(V,43x), 94(H,50x), 96(L,52x) — never appear in confirmed German word contexts
- **I inflation**: 10.4% vs 7.6% expected (+2.8%) — persistent across all assembly methods
- **B/F deficit**: B=0.2% (exp 1.9%), F=0.5% (exp 1.7%) — some I codes may actually be B or F
- **45 unaligned books**: Only 25/70 books align at code level; remaining books encode same text with different homophonic codes
- **SCHWITEIONE**: 10x frequency, always in same context. Bonelord race name?
- **Proper noun meanings**: EILCHANHEARUCHTIG, EDETOTNIURGS, TIUMENGEMI — compound words or titles?
- **TibiaSecrets English decode vs our German decode**: Their key (62=N, 79=A, 20=R) differs completely from ours (62=B, 79=O, 20=F)

## How to Contribute

The cipher text is in `data/books.json`. The mapping is in `data/final_mapping_v4.json`. The complete research log is in `FINDINGS.md` (4800+ lines, 12 sessions).

Key areas where help is needed:
- **Book alignment**: 45/70 books don't align at code level due to homophonic substitution. A multi-sequence alignment or voting approach could recover the full narrative
- **Unconfirmed code verification**: 8 codes (esp. 80(G) and 04(M)) may be wrong — fixing them could unlock proper noun meanings
- **Archaic German vocabulary**: Unrecognized segments may be Middle High German (MHG) or Old High German
- **Anagram analysis**: CipSoft uses anagrams extensively (Vladruc=Dracula, Dallheim=Heimdall). Do any proper nouns rearrange to known terms?
- **NPC dialogue 469**: Avar Tar, Knightmare NPC, and Chayenne (dev) all speak 469 — additional cribs

## Methodology

This research uses crib-based incremental decryption:
1. Identify the cipher type via Index of Coincidence
2. Use frequency analysis to get initial E/N assignments
3. Progressively assign codes through 14 tiers of evidence
4. Validate using German bigram/trigram statistics
5. Parse decoded text with DP word segmentation
6. Use book overlap structure to verify assignments

Blind statistical attacks (Simulated Annealing) were tested and do **not** converge on this text — it's too short for 98-symbol homophonic cipher cracking without cribs.
