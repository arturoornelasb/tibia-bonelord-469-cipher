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
| 92 of 98 codes mapped to 22 letters | Confirmed |
| 70 books = overlapping fragments of **ONE continuous narrative** | Proven |
| ~50% of decoded text parses as German words | Current |
| Narrative about King LABGZERAS, ancient stones, runes | Partial |
| Code 05 likely = S, not C (never appears before H) | Hypothesis |

### The Mapping (92 codes -> 22 letters)

```
E (14 codes): 95 56 19 26 76 01 41 30 86 67 27 03 09 17 29 49 39
N (10 codes): 60 11 14 48 58 13 93 53 73 90
I  (7 codes): 21 15 46 71 65 16 50 24
S  (7 codes): 92 91 52 59 12 23 [05?]
R  (6 codes): 72 51 55 08 68 10
D  (5 codes): 45 42 47 63 28
A  (5 codes): 31 85 35 89 66
T  (6 codes): 88 78 64 75 81 98
H  (4 codes): 06 00 57 94
U  (4 codes): 61 43 70 44
G  (3 codes): 80 97 84
K  (2 codes): 38 22
O  (4 codes): 99 82 25 79
W  (2 codes): 36 87
C  (1-2 codes): 18 [05?]
M  (2 codes): 04 54
L  (2 codes): 34 96
F  (1 code):  20
B  (1 code):  62
Z  (1 code):  77
V  (1 code):  83
Unknown (6):  74(19x) 37(8x) 40(7x) 02(4x) 33(1x) 69(1x)
```

No P, J, Q, X, or Y found in the text.

### Decoded Sample (main fragment, 292 chars)

```
...FINDEN...DAS ES DER STEINEN... → "find that it the stones"
...ICH...AUS ENDE...             → "I...from the end"
...HIER...STEIL...AN HEARUCHTIGER → "here...steep...at Hearuchtiger"
...DASS TUN DIES ER...TOTNIURG   → "that this he does...Totniurg"
...WIR UND...DIE URALTE STEINEN  → "we and...the ancient stones"
...DEN ENDE REDE R KOENIG LABGZERAS → "the concluding speech of King Labgzeras"
```

## Repository Structure

```
.
├── README.md              # This file
├── FINDINGS.md            # Complete research log (89 sections, 6 sessions)
├── data/
│   ├── books.json         # Source data: all 70 books as digit strings
│   ├── best_mapping.json  # Current best code-to-letter mapping
│   └── ...
├── scripts/
│   ├── core/              # Key scripts that produced results
│   │   ├── decode_tier14.py        # Final 92-code decoder
│   │   ├── raw_superstring.py      # Raw-digit superstring assembly
│   │   ├── narrative_v2.py         # Comprehensive narrative parser
│   │   ├── formula_analysis.py     # Proved ONE narrative structure
│   │   ├── comprehensive_decode.py # Code 16 I/O test + full decode
│   │   ├── audit_segments.py       # Unrecognized segment analysis
│   │   ├── investigate_c_ende.py   # C anomaly + ENDE investigation
│   │   ├── dp_parse.py             # DP word segmentation
│   │   ├── find_repeats.py         # Repeating pattern analysis
│   │   └── superstring_v2.py       # Superstring assembly
│   └── experimental/      # 79 exploratory scripts from 6 sessions
└── docs/
    ├── 01-books.md         # Book transcriptions
    └── README-469.md       # Early research notes
```

## Open Questions

- **SCHWITEIO**: Appears 10 times, always same encoding. Proper noun? Compound word?
- **AUNRSONGETRASES**: Most common unrecognized phrase (11 books). Name?
- **6 unknown codes**: What letters do 74, 37, 40, 02, 33, 69 represent?
- **Code 05**: Is it S or C? Evidence points to S.
- **Second cipher layer?**: Could the proper nouns be anagrammed/reversed?
- **IIIWII**: Secondary cipher or just "III W II"?

## How to Contribute

The cipher text is in `data/books.json`. The complete research log is in `FINDINGS.md`. If you know Tibia lore (especially about Bonelords, the Hellgate Library, King LABGZERAS, TOTNIURG), your knowledge could help crack the remaining ~35%.

Key areas where help is needed:
- **Tibia lore cross-reference**: Do LABGZERAS, TOTNIURG, HEARUCHTIGER, THARSC, SCHWITEIO match any known in-game entities?
- **Archaic German vocabulary**: Some unrecognized segments might be Middle High German
- **NPC dialogue analysis**: The 469 cipher appears in NPC dialogues too — additional data could constrain the solution

## Methodology

This research uses crib-based incremental decryption:
1. Identify the cipher type via Index of Coincidence
2. Use frequency analysis to get initial E/N assignments
3. Progressively assign codes through 14 tiers of evidence
4. Validate using German bigram/trigram statistics
5. Parse decoded text with DP word segmentation
6. Use book overlap structure to verify assignments

Blind statistical attacks (Simulated Annealing) were tested and do **not** converge on this text — it's too short for 98-symbol homophonic cipher cracking without cribs.
