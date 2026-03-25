## 13. Session 16: Two Encoding Systems & Lore Connections

### 13.1 CRITICAL FINDING: Two Separate Encoding Systems

The 469 cipher uses **two completely different encoding systems**:

| Property | System 1: Books | System 2: NPC Dialogues |
|---|---|---|
| **Encoding** | 2-digit pair homophonic substitution | Word-level variable-length codes |
| **Unit size** | Fixed 2 digits → 1 letter | 1-10 digits → 1 word |
| **Language** | German (MHG vocabulary) | English |
| **Delimiters** | None (continuous digit string) | Spaces between word codes |
| **Coverage** | 98 codes → 22 letters (v7) | 7 known: 3478=BE, 67=A, etc. |

**Evidence:**
- NONE of Avar Tar's 20 poem word-codes appear in the 70 books
- Digit frequency differs: books peak at digit 1 (16.6%), poem peaks at digit 3 (18.3%)
- Knightmare decodes to English: "BE A WIT THAN BE A FOOL"
- Books decode to German: URALTE STEINEN, KOENIG, GOTTDIENER

### 13.2 Avar Tar's Bonelord Poem

NPC Avar Tar (Isle of the Kings prisoner NPC) speaks bonelord language when asked:

```
29639 46781! 9063376290 3222011 677 80322429 67538 14805394,
6880326 677 63378129 337011 72683 149630 4378!
453 639 578300 986372 2953639!
```

"I know it's rather short, but still, this poem I like best."

**Structure:** 20 word-codes in 3 sentences (exclamation marks):
- Sentence 1: 2 words (exclamation/title)
- Sentence 2: 13 words with comma after word 6 (two clauses)
- Sentence 3: 5 words (conclusion)

**Key code: 67538** appears in BOTH this poem AND the CipSoft Facebook poll — confirms shared encoding across all NPC sources.

### 13.3 Shared Word Codes Across NPC Sources

| Code | Sources | Known Translation |
|---|---|---|
| 677 | Avar Tar (2x), Wrinkled Bonelord | ??? (common short word: IS, OF, TO, IN?) |
| 663 | CipSoft Poll, Wrinkled Bonelord | ??? (appears early in sentences) |
| 345 | Knightmare, Wrinkled Bonelord | FOOL |
| 67538 | CipSoft Poll, Avar Tar | ??? (5 digits ≈ 3 letters) |
| 3478 | Knightmare | BE |

**All known NPC bonelord texts:**
- Knightmare: `3478 67 90871 97664 3466 0 345` = "BE A WIT THAN BE A FOOL"
- Wrinkled Bonelord: `4129 663 4382 12801 6639 677 35682 345 25`
- CipSoft Poll: `663 902073 7223 67538 467 80097`
- Avar Tar poem: (20 word-codes, see above)
- Honeminas: `43154 34784` (2 codes)
- Bonelord name: `486486`

### 13.4 Isle of the Kings ↔ Decoded Book Text

The island's primary purpose is **burying ancient leaders of the Thaian empire**. Direct connections:

| Decoded Book Text | Isle of the Kings Lore |
|---|---|
| URALTE STEINEN (ancient stones) | Burial of ancient Thaian leaders |
| KOENIG (king) | King Zelos buried in deepest catacombs |
| LEICH (corpse) | Catacombs floors -1 to -6 with undead |
| GOTTDIENER (God's servant) | Monks studying books and Tibia history |
| BERUCHTIG (infamous) | "Great evil lurking beneath this isle" |
| RUNE (rune) | Ancient magical symbols |
| OEL (oil) | Religious anointing rituals |
| DEN ENDE REDE (final speech) | Last rites / funerary orations |
| LABRRNI ≈ LIBRARI | Bonelord = "the great librarian" |

**Avar Tar confirms:** "There is a great evil lurking beneath this isle... and beneath the Plains of Havoc, and in the ancient necropolis" — directly names locations where bonelord content exists (Hellgate is under Plains of Havoc).

### 13.5 Paradox Tower Quest Connection

The Paradox Tower Quest (created by Knightmare, same creator as 469) routes players **directly through Hellgate** where the 70 bonelord books are:

1. Riddler calls player "FOOL" (345 = FOOL in bonelord language)
2. Wrong answer → teleported to Hellgate (bonelord library location!)
3. A Prisoner in Mintwallin uses "surreal numbers" and "mathemagics"
4. A Prisoner's formula: `1 + 1 = your_number` (personalized mathematical transformation based on color choice)
5. Paradox Tower contains garbled letter books (see Section 24) — 26 sections matching alphabet size

**Connection to cipher:** A Prisoner's "mathemagics" demonstrates CipSoft's concept of digit→letter transformation where the mapping depends on context. The 70 books likely use a fixed mapping (our v7), while NPC texts use a different word-level system.

### 13.6 DRTHENAEUT Deep Analysis

The recurring garbled segment DRTHENAEUT (appears 3x, always identical digit sequence `45727857261185764364`):
- Contains THENA root (cf. ATHENA/THAIA?)
- Always followed by: ER ALS TNE DAS ENOT ER LGTNELGZ ER A SER TIURIT ORANGENSTRASSE
- The entire phrase block repeats identically → formulaic passage, likely a fixed expression or proper noun + title

**Full recurring phrase:** "...RUNEN DRTHENAEUT ER ALS TNE DAS ENOT ER LGTNELGZ ER A SER TIURIT ORANGENSTRASSE..."

This 40+ character block appears 3x verbatim. The garbled parts (DRTHENAEUT, TNE, ENOT, LGTNELGZ, TIURIT) likely form a coherent passage with wrong word boundaries in our segmenter.

### 13.7 THENAEUT Bridges Books and NPC Systems

**CRITICAL DISCOVERY:** The Wrinkled Bonelord's wiki description number `78572611857643646724` decodes with V7 pair mapping as THENAEUTER. This shares a 16-digit core `7857261185764364` = THENAEUT with the books' DRTHENAEUT sequence `45727857261185764364`.

```
Books:  [45-72] [78-57-26-11-85-76-43-64]
         DR      THENAEUT
NPC:            [78-57-26-11-85-76-43-64] [67-24]
                 THENAEUT                  ER
```

**Implications:**
1. The pair encoding (V7) works on NPC "written" text, not just books
2. THENAEUT is a real word/name in the cipher, not a mapping artifact
3. It likely functions as a proper noun (always followed by ER = "he")
4. Letter inventory A,E,E,H,N,T,T,U — possible ATHENE connection (remove T: ATHENE+U)

### 13.8 Written vs Spoken Bonelord Language

The Wrinkled Bonelord uses BOTH encoding systems:
- **Written format** (wiki/description, no spaces): `485611800364197. 78572611857643646724.` → pair encoding (same as 70 books)
- **Spoken format** (dialogue, space-separated): `4129 663 4382 12801 6639 677 35682 345 25` → word-level encoding

Other NPC spoken bonelord texts all use word-level encoding:
- Knightmare: `3478 67 90871 97664 3466 0 345`
- Avar Tar poem: 20 word-codes with spaces
- CipSoft Poll: `663 902073 7223 67538 467 80097`

### 13.9 Elder Bonelord and Evil Eye Codes

New bonelord dialogue data:
- **Elder Bonelord**: `659978 54764! 653768764!` (3 word-codes)
- **The Evil Eye**: `653768764!` (same code as Elder Bonelord's third word)

Code `653768764` is shared between Elder Bonelord and The Evil Eye — appears to be a bonelord aristocracy expression. None of these codes appear in the 70 books.

### 13.10 Bonelord Lore Connections

From wiki lore, bonelords are:
- An **ancient race that once ruled vast parts of the world** → URALTE STEINEN
- Created by gods as **counterweight to another race** in god wars
- Masters of **necromantic arts** using undead minions → LEICH, GOTTDIENER
- Have **dark pyramids** in their cities
- See themselves as **superior conqueror race** → KOENIG
- Planning to **raise an unstoppable undead army** to reconquer
- The Wrinkled Bonelord calls itself "**the great librarian**" → LABRRNI

### 13.11 "You Cannot Even Imagine" Book — The Great Calculator

The book "You Cannot Even Imagine How Old I Am" (Isle of the Kings, Dawnport) contains the most important lore clue about the cipher:

> "It was me who assisted **the great calculator** to **assemble** the bonelords language."

The narrator is the last of their race, witnessed creation wars, and helped build the bonelord language. Key word: **assemble** — the language was constructed, not just encoded.

Other witnessed events mention: Rorak slew Tingil, Riik fled north, betrayal of Asric, the last Frdai, Ss'rar becoming serpent god, first elves with lightbearers.

### 13.12 "Beware of the Bonelords" — Variable Encoding Units

> "Their native tongue consists of a blinking code with each eye, where a blinking could mean some **syllable, letter or word**."
> "It is not only a language but also **some kind of mathematics**. This **combination** makes it tedious."

**Explicit confirmation of variable-unit encoding:** syllable, letter, OR word — matching our discovery of pair-level (books) vs word-level (NPC dialogue) encoding.

**"Not only a language but also some kind of mathematics"** — the cipher involves mathematical operations, not just substitution.

### 13.13 Wrinkled Bonelord Complete Transcripts — Game-Changing Clues

Full NPC transcript reveals critical information:

**CRIB: Tibia = 1**
> "It's 1, not 'Tibia', silly."

The world Tibia is represented as "1" in bonelord language. In the books, digit 1 is the most common (16.59%).

**MATHEMAGIC = Paradox Tower Connection**
> "Our language heavily relies on **mathemagic**."
> "To decipher even our most basic texts, it would need a genius that can **calculate numbers** within seconds."

The word "mathemagic" is IDENTICAL to the Paradox Tower quest term. A Prisoner in Mintwallin teaches "the secret of **mathemagics**" with a personalized formula: "1 + 1 = your_number". This is a DIRECT connection between the Paradox Tower quest and the 469 cipher.

**Race Name = Complex Formula**
> "The name of our race is not fix but a **complex formula**, and as such it always **changes** for the subjective viewer."

486486 is just ONE evaluation. The name changes depending on who views it — like A Prisoner's personalized numbers. This suggests the encoding involves a viewer-dependent mathematical transformation.

**5 Eyes = 5 Channels**
> "Only to be spoken by entities with enough eyes to blink it."
> "You can determine the value of a species by the number of its eyes."

Bonelords have 5 eyes. The language may use 5 parallel channels (5-digit vectors?). This connects to the Honeminas formula: `(4,3,1,5,3).(3,4,7,8,4)` — two 5-vectors.

**Minotaur Mages Close to Truth**
> "Their mages are so close to the truth. Closer than they know and closer than it's good for them."

A Prisoner who teaches mathemagics is in Mintwallin — the MINOTAUR city. Is A Prisoner a minotaur mage who got "too close" to bonelord secrets?

**Other key quotes:**
- "Numbers are essential. They are the secret behind the scenes."
- "If you are a master of mathematics you are a master over life and death." (= necromancy)
- "Our books are written in 469"
- "0 is obscene" (but in Knightmare encoding, 0 = A)
- "Gods destroyed our empire... but our race is proficient in the return from death"

### 13.14 REDER KOENIG Discovery

REDER (speaker/orator) appears 6x in decoded text, always in the phrase:
```
DEN ENDE REDER KOENIG LAB...
```
Previously parsed as "REDE {R} KOENIG", the correct reading is **REDER KOENIG** = "speaker-king" or "the king who gives speeches". This fits the narrative context of royal proclamations about ancient places.

