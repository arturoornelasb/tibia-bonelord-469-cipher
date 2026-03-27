# The Eye-Count Parsing Hypothesis

**Date:** 2026-03-26
**Status:** Active hypothesis, partially confirmed
**Authors:** Kardfon Dogon (in-game research), Claude (analysis)

---

## Core Thesis

The bonelord language 469 is not spoken or written — it is **blinked with eyes**. Each digit represents the state of one eye (0-9). The number of eyes a being has determines how it **parses** the same digit stream. This explains why the bonelord says the language can only be used by "entities with enough eyes to blink it."

This means:
1. **The same digit sequence means different things to different species**
2. **The number of digits per "word" = the number of eyes used**
3. **Two completely different encoding systems are actually ONE system** viewed through different eye counts

---

## Evidence

### Direct NPC Quotes Supporting This

| Quote | Source | Implication |
|-------|--------|-------------|
| "Only to be spoken by entities with enough eyes to blink it" | Wrinkled Bonelord on `469` | Language requires eyes, not mouth |
| "You pitiful two-eyed creatures" | Wrinkled Bonelord on `eyes` | Humans have insufficient eyes |
| "You can determine the value of a species by the number of its eyes" | Wrinkled Bonelord on `eyes` | More eyes = more capability |
| "The name of our race is not fixed but a **complex formula**, and as such it always **changes for the subjective viewer**" | Wrinkled Bonelord on `bonelord` | Same digits, different parsing per viewer |
| "Our language heavily relies on **mathemagic**" | Wrinkled Bonelord on `language` | Mathematical operations on eye-states |
| "Go and wash your eyes for using this obscene number!" | Wrinkled Bonelord on `0` | Eye-state 0 = closed/blind = taboo |
| "It's 1, not 'Tibia', silly" | Wrinkled Bonelord on `tibia` (wiki) | Single-digit words exist (1-eye expression) |
| "Their mages are so close to the truth" | Wrinkled Bonelord on `minotaurs` (wiki) | Minotaur mages (who study mathemagics) are approaching bonelord knowledge |

### The Honeminas Formula

From the Demona library book "The Honeminas Formula":
```
g[a_,x_] := a g[3,2] + (4,3,1,5,3)·(3,4,7,8,4)
```

Both vectors have exactly **5 elements** — one for each bonelord eye. The dot product operation IS the "mathemagic": each eye contributes a value, and the mathematical combination produces meaning.

Dot product: (4×3) + (3×4) + (1×7) + (5×8) + (3×4) = 12+12+7+40+12 = **83**

### A Prisoner's Mathemagics

A Prisoner in the Paradox Tower (Mintwallin = minotaur city) teaches that `1 + 1 = your_number`, where the result changes per player. This is the same concept: the same input produces different output depending on the viewer. The Wrinkled Bonelord uses the identical word "mathemagic."

### The "Beware of the Bonelords" Book

> "Their native tongue consists of a blinking code with each eye, where a blinking could mean some **syllable, letter or word**."
> "It is not only a language but also **some kind of mathematics**. This **combination** makes it tedious."

Explicit confirmation: variable-unit encoding (syllable/letter/word) through eye blinks, combined with mathematics.

---

## The Two Systems Are One

### Previously Identified as Two Separate Systems

| Property | "System 1" (Books) | "System 2" (NPC Speech) |
|----------|-------------------|------------------------|
| Format | Continuous digit stream, no spaces | Space-separated words |
| Unit size | Fixed 2-digit pairs | Variable 1-5+ digits |
| Decoded language | German | English |
| Coverage | 98 codes, 94.6% decoded | 7 known word-codes |

### Reinterpreted Under Eye-Count Hypothesis

| Property | 2-Eye Parsing (Books) | 5-Eye Parsing (NPC Speech) |
|----------|----------------------|---------------------------|
| Parser | Human (2 eyes) reads pairs | Bonelord (5 eyes) reads variable words |
| Unit | Always 2 digits (one per eye) | 1-5 digits (one per eye, variable eyes used) |
| Why different | Humans can only process 2 simultaneous eye-states | Bonelords use 1-5 eyes per expression |
| "Primitive" | Yes — bonelord called books "primitive storage" | Full language capability |

**The books are the same data viewed through 2-eye parsing.** The NPC speech is the same type of data viewed through 5-eye parsing. The underlying digit stream is the same language, but the parsing unit changes based on the perceiver's eye count.

---

## Eye-State Model

### Each Digit = One Eye's State

- Digits 1-9: valid eye states (open in various configurations)
- Digit 0: "obscene" — represents a closed/blind eye
- The state of each eye in a single moment encodes information
- A "word" is one simultaneous blink pattern across N eyes

### Word Length = Number of Eyes Used

| Eyes Used | Digit Length | Example Code | Known Translation |
|-----------|-------------|-------------|-------------------|
| 1 eye | 1 digit | `0` | A |
| 2 eyes | 2 digits | `67` | A (homophonic with `0`) |
| 3 eyes | 3 digits | `345` | FOOL |
| 4 eyes | 4 digits | `3478` | BE |
| 4 eyes | 4 digits | `3466` | BE (homophonic) |
| 5 eyes | 5 digits | `90871` | WIT |
| 5 eyes | 5 digits | `97664` | THAN |

Note: Homophonic encoding exists within the same eye-count level (3478 and 3466 both = BE with 4 eyes) AND across eye-counts (0 and 67 both = A, using 1 or 2 eyes).

### 486486: The Name That Changes

The bonelord's name `486486` parsed by different viewers:

| Viewer | Eyes | Parsing | Result |
|--------|------|---------|--------|
| Human | 2 | 48-64-86 | 3 two-digit codes → NTM |
| Cyclops | 1 | 4-8-6-4-8-6 | 6 single-digit codes |
| Unknown (3-eyed) | 3 | 486-486 | 2 three-digit codes (repeated = emphasis?) |
| Bonelord (5-eyed) | 5 | 48648-6 | 1 five-digit word + 1 single |
| Other | 6 | 486486 | 1 six-digit word |

The bonelord says "don't confuse your numbers" — because getting the parsing wrong changes the meaning entirely.

---

## Known Word-Level (5-Eye System) Vocabulary

### Confirmed Translations (from Knightmare crib)

| Code | Word | Digits | Source |
|------|------|--------|--------|
| 0 | A | 1 | Knightmare |
| 67 | A | 2 | Knightmare |
| 345 | FOOL | 3 | Knightmare, Wrinkled Bonelord |
| 3478 | BE | 4 | Knightmare |
| 3466 | BE | 4 | Knightmare |
| 90871 | WIT | 5 | Knightmare |
| 97664 | THAN | 5 | Knightmare |

**Knightmare full decode:** `3478 67 90871 97664 3466 0 345` = "BE A WIT THAN BE A FOOL"

### Unconfirmed Codes (shared across sources)

| Code | Digits | Sources | Candidates |
|------|--------|---------|------------|
| 677 | 3 | Avar Tar (2x), Wrinkled BL | IS, OF, TO, IN, IT? |
| 663 | 3 | CipSoft Poll, Wrinkled BL | THE, AND, FOR? |
| 67538 | 5 | CipSoft Poll, Avar Tar | Unknown |
| 25 | 2 | Wrinkled BL | Unknown |
| 4129 | 4 | Wrinkled BL | Unknown |
| 4382 | 4 | Wrinkled BL | Unknown |
| 12801 | 5 | Wrinkled BL | Unknown |
| 6639 | 4 | Wrinkled BL | Unknown |
| 35682 | 5 | Wrinkled BL | Unknown |

### All Known NPC 469 Texts (Word-Level System)

```
Knightmare:       3478 67 90871 97664 3466 0 345
                  = "BE A WIT THAN BE A FOOL"

Wrinkled BL:      4129 663 4382 12801 6639 677 35682 345 25
                  = "???? ??? ???? ????? ???? ??? ????? FOOL ??"

CipSoft Poll:     663 902073 7223 67538 467 80097
                  = "??? ?????? ???? ????? ??? ?????"

Avar Tar poem:    29639 46781! 9063376290 3222011 677 80322429 67538 14805394,
                  6880326 677 63378129 337011 72683 149630 4378!
                  453 639 578300 986372 2953639!

Elder Bonelord:   659978 54764!
Evil Eye:         653768764!

Honeminas:        43154 34784
```

### Note on Avar Tar Reliability

Avar Tar is described as "a chronic liar and boaster." His poem uses `4378` where the standard form is `3478` (reversed). His data may be deliberately inverted or fabricated. Use with caution.

---

## Implications for the Cipher

### Why Books Decode to German

The 70 Hellgate books are continuous digit streams with no spaces. When a 2-eyed human reads them (parsing as pairs), they decode to German text via homophonic substitution (our v7 mapping, 94.6% coverage). This is correct — it's the "primitive" 2-eye reading of the data.

### Why NPC Speech Doesn't Match Books

NPC speech uses the full 5-eye parsing (variable-length words with spaces). These are completely different "readings" of the bonelord number system. They decode to English, not German, because the word-level codes map to English words.

### The Real Challenge

The 2-eye (book) cipher is largely solved. The 5-eye (word-level) cipher has only 7 confirmed translations out of 30+ known codes. Cracking the word-level system requires:

1. More cribs (known plaintext-ciphertext pairs)
2. Identifying shared codes across sources to build vocabulary
3. Possibly mathematical relationships between codes (mathemagic)
4. The Knightmare NPC hint: encoding "excalibug" in word-level 469 might unlock a secret (but the NPC has been removed from the game)

### Open Questions

1. Can the same digit stream be meaningfully read BOTH as 2-eye pairs AND as 5-eye words? (Would prove the unified system)
2. Is there a mathematical relationship between codes of different eye-counts for the same word? (e.g., 0=A and 67=A — is 67 derived from 0 somehow?)
3. What determines how many eyes a bonelord uses for each word? (Complexity? Emphasis? Grammar?)
4. Code 32 appears in Avar Tar's poem but never in books — is it reserved for the 5-eye system?
5. Code 07 never appears anywhere — is it truly forbidden (related to 0 being obscene)?

---

## Testing This Hypothesis

### In-Game Tests (Priority)

1. **Test remaining Wrinkled Bonelord keywords:** `tibia`, `ab'dendriel`, `minotaurs`, `cyclops`, `humans`, `elves`, `orcs`, `excalibug` — these may trigger the word-level (spaced) 469 format
2. **Visit Avar Tar** — say `bonelord language` to get his poem, then try `469`, `poem`, `excalibug`
3. **Visit A Prisoner (Paradox Tower)** — his mathemagics formula may connect to the eye-state system
4. **Visit Evil Eye / Elder Bonelord creatures** — record all 469 utterances
5. **Try saying word-level codes to Wrinkled Bonelord:** `3478`, `345`, `90871` (with spaces between them)

### Analytical Tests

1. Check if book digit streams can be alternatively parsed as variable-length words (5-eye reading)
2. Look for mathematical relationships between same-meaning codes of different lengths
3. Analyze the Honeminas dot-product operation as an eye-state transformation
4. Test if digit-sum, digit-product, or modular arithmetic connects word-codes to their meanings

---

## Sources

- In-game NPC interaction log: `data/npc_wrinkled_bonelord_log.md`
- Complete findings: `FINDINGS.md` sections 13.1-13.14
- NPC research database: `docs/investigation/npc-research.md`
- Cipher paper: `papers/469_cipher/paper_469_cipher.md`
- TibiaWiki: Wrinkled Bonelord, Knightmare, Avar Tar transcripts
- "Beware of the Bonelords" book (in-game)
- "You Cannot Even Imagine How Old I Am" book (Isle of the Kings)
- "The Honeminas Formula" book (Demona Library)
