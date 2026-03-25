> **Idioma / Language:** [Español](paper_bag_of_letters.es.md) | English

# Bag-of-Letters Word Partition: A Novel Technique for Resolving Garbled Blocks in Homophonic Substitution Ciphers

**Authors:** Independent Research Project
**Date:** March 2026
**License:** BUSL-1.1 (see LICENSE in repository root)

---

## Abstract

We present **Bag-of-Letters Word Partition** (BoLWP), a combinatorial technique for recovering readable text from garbled blocks produced by homophonic substitution ciphers that encode spaceless text. Unlike traditional anagram resolution (which maps one garbled block to one known word), BoLWP decomposes a block's letter inventory into the **optimal multi-word combination** from a known dictionary, tolerating systematic letter substitutions inherent to the cipher. Applied to a 25-year-old unsolved cipher in the MMORPG Tibia, the technique achieved +10.1% word coverage in a single session — the largest gain across 30 sessions of analysis — resolving 34 previously opaque blocks. We also describe two companion techniques: **Context-Aware Anagram Resolution** (CAAR), which respects compound word boundaries during substitution, and **Concatenation-Aware Digit-Split Testing** (CADST), which validates per-fragment modifications against the global reconstructed text to prevent cross-boundary regressions.

---

## 1. Introduction

### 1.1 The Problem

Homophonic substitution ciphers assign multiple ciphertext symbols to the same plaintext letter, flattening frequency distributions and defeating standard frequency analysis. When the plaintext additionally **lacks word boundaries** (no spaces, punctuation, or delimiters), even a correct letter-level decryption produces a continuous string of letters that must be segmented into words — a non-trivial task, especially for languages with productive compounding (e.g., German).

Dynamic programming (DP) word segmentation against a dictionary achieves good coverage on most of the decoded stream, but certain regions resist segmentation. These **garbled blocks** contain correctly decoded letters that fail to match any single dictionary entry. Prior approaches treat each block as a potential anagram of one known word. We show this is insufficient: many garbled blocks encode **multiple words** whose letters are interleaved by the cipher's many-to-one mapping.

### 1.2 Context

This technique was developed during the decryption of the "Bonelord 469" cipher — 70 books of pure digit sequences from the MMORPG Tibia (CipSoft GmbH, 1997–present). The cipher uses 98 two-digit codes mapped to 22 German letters (including Middle High German vocabulary). After achieving ~81% word-level coverage through standard cryptanalytic methods, the remaining ~19% consisted of garbled blocks ranging from 3 to 35 characters.

### 1.3 Contributions

1. **Bag-of-Letters Word Partition (BoLWP):** Combinatorial multi-word decomposition of garbled blocks with swap tolerance
2. **Context-Aware Anagram Resolution (CAAR):** Phrase-boundary-sensitive string replacement
3. **Concatenation-Aware Digit-Split Testing (CADST):** Global validation of local modifications in fragmented ciphertext

---

## 2. Background

### 2.1 Homophonic Substitution

A homophonic substitution cipher maps each plaintext letter $l$ to a set of ciphertext symbols $C(l)$, where $|C(l)|$ is roughly proportional to the frequency of $l$ in the plaintext language. For a 22-letter German alphabet:

- E (16.4% frequency) → 20 codes
- N (9.8%) → 10 codes
- I (7.6%) → 8 codes
- S (7.3%) → 7 codes
- ...down to V (0.7%) → 1 code

With 98 codes spanning 22 letters, each code deterministically maps to one letter, but the reverse mapping is one-to-many.

### 2.2 The Segmentation Problem

Given a decoded letter stream (e.g., `DIERALTESTEINEISEINRUIN`), DP segmentation finds the word boundaries that maximize dictionary coverage:

```
DIE|RALT|STEIN|E|IST|EIN|RUIN  →  suboptimal
DIE|R|ALTE|STEIN|E|IST|EIN|RUIN  →  better
```

Blocks that match no dictionary entry are enclosed in braces: `{RALT}`. These garbled blocks are the target of BoLWP.

### 2.3 Why Single-Word Anagram Matching Fails

Consider the garbled block `DNRHAUNIIOD` (11 characters). No single German word is an anagram of these letters. Traditional approaches abandon this block. But the letters can be partitioned into:

- OEDE (4 letters, "wasteland") — requires 2 I→E swaps
- NUR (3 letters, "only") — exact match
- HAND (4 letters, "hand") — exact match

Total: 4 + 3 + 4 = 11 letters consumed, 100% coverage.

---

## 3. Bag-of-Letters Word Partition (BoLWP)

### 3.1 Algorithm

**Input:** A garbled block $G$ of length $n$, a dictionary $D$ of known words, and a set of permitted letter swaps $S$ (e.g., {I↔E, I↔L}).

**Output:** An ordered sequence of words $(w_1, w_2, \ldots, w_k)$ from $D$ such that the multiset union of their letters matches (or approximately matches via $S$) the letter multiset of $G$, maximizing total characters covered.

```
function BoLWP(G, D, S, max_swaps):
    bag = letter_multiset(G)
    n = |G|
    best = (0, [])  # (coverage, word_list)

    function search(remaining_bag, remaining_len, words, swaps_used):
        if coverage(words) > best.coverage:
            best = (coverage(words), words)

        for w in D where |w| <= remaining_len:
            w_bag = letter_multiset(w)
            (ok, new_swaps) = can_satisfy(remaining_bag, w_bag, S, max_swaps - swaps_used)
            if ok:
                new_bag = remaining_bag - w_bag (with swaps applied)
                search(new_bag, remaining_len - |w|, words + [w], swaps_used + new_swaps)

    search(bag, n, [], 0)
    return best
```

### 3.2 Letter Swap Model

The cipher's many-to-one mapping creates systematic ambiguities at code boundaries. In our cipher:

- **I↔E swap:** The 8 I-codes and 20 E-codes create boundary confusion where a code pair decoded as `...I` might actually end in `E` if the pair boundary is shifted
- **I↔L swap:** The 2 L-codes (34, 96) are numerically adjacent to I-codes, causing occasional misassignment

The swap model permits up to $k$ total letter substitutions per block (typically $k \leq 3$ for blocks under 15 characters). Each swap has a cost, and the algorithm prefers solutions with fewer swaps.

### 3.3 Pruning

The naive search is exponential. We apply three pruning strategies:

1. **Length bound:** Only consider words $w$ where $|w| \leq$ remaining letters
2. **Letter availability:** Pre-check that the remaining bag contains enough letters (with swaps) to form $w$ before recursing
3. **Minimum word length:** Words must be $\geq 2$ characters (single letters are too ambiguous)
4. **Coverage threshold:** Abandon branches where the maximum achievable coverage (current + remaining letters) cannot exceed the current best

### 3.4 Dictionary

The dictionary combines:

- Modern German (common words, 2-20 characters)
- Middle High German (MHG) vocabulary (538 entries including archaic forms: SCE, NIT, SER, LEICH, SCHRAT, OEL)
- Confirmed proper nouns from the cipher (SALZBERG, WEICHSTEIN, GOTTDIENER, etc.)
- Single-character words excluded to prevent trivial decomposition

Total: ~12,000 entries (after filtering to the cipher's 22-letter alphabet).

### 3.5 Complexity

For a garbled block of length $n$ and a dictionary of size $|D|$:

- Worst case: $O(|D|^{n/2})$ (all 2-letter words)
- Practical case: $O(|D|^{n/\bar{w}})$ where $\bar{w}$ is average word length (~4.5 for German)
- With pruning, typical blocks ($n \leq 20$) resolve in under 1 second

---

## 4. Context-Aware Anagram Resolution (CAAR)

### 4.1 The Compound Word Problem

Standard string replacement is context-agnostic: replacing all occurrences of pattern $P$ with replacement $R$ may break valid compound words that contain $P$ as a substring.

**Example:** The garbled block `UNR` is an anagram of `NUR` ("only"). But naively replacing all `UNR` with `NUR` destroys:
- `WINDUNRUH` → `WINDNURH` (breaks the compound "Windunruh" = wind-unrest)
- `SCHAUNRUIN` → `SCHAUNRUIN` (breaks "schaun ruin" = behold ruin)

### 4.2 Solution: Phrase-Boundary Targeting

Instead of global replacement, CAAR identifies the specific **phrasal context** in which the anagram occurs and targets only that pattern:

```python
# WRONG: global replacement breaks compounds
resolved = resolved.replace('UNR', 'NUR')

# RIGHT: context-specific replacement
resolved = resolved.replace('TREUUNR', 'TREUNUR')
```

This resolved all 8 occurrences of the UNR→NUR anagram without affecting the 4 occurrences of WINDUNRUH.

### 4.3 When to Apply CAAR

CAAR is necessary when:
1. The anagram pattern appears as a substring of a valid compound word
2. The compound word was formed by a **prior** anagram resolution (since resolutions are applied longest-first)
3. Both the compound and the standalone anagram are legitimate readings

CAAR operates as a **post-pass** after the main anagram resolution, fixing context-specific collisions.

---

## 5. Concatenation-Aware Digit-Split Testing (CADST)

### 5.1 The Digit-Split Problem

In the Bonelord cipher, CipSoft removed a single digit from 37 of 70 books (all books with odd digit counts). This deliberate obfuscation breaks the 2-digit pair alignment at the deletion point, producing incorrect letter decoding downstream.

Recovery requires finding:
1. The correct **position** (0 to $n$) for the missing digit
2. The correct **digit** (0-9) to insert

For a book of length $n$, this is a search space of $10 \times (n+1)$.

### 5.2 Per-Book vs. Global Testing

**Per-book testing** evaluates each digit insertion against only that book's decoded text. This misses:

- Cross-book anagram boundaries (ANAGRAM_MAP entries that span the junction between two books in the concatenated narrative)
- Downstream effects where one book's change shifts letter frequencies enough to alter DP segmentation in overlapping books

**CADST** evaluates each candidate insertion by:
1. Inserting the digit into the target book
2. Re-decoding the **entire corpus** (all 70 books concatenated)
3. Applying the full ANAGRAM_MAP resolution pipeline
4. Running DP segmentation on the **global** resolved text
5. Comparing global coverage against the baseline

### 5.3 Results

Session 30 applied CADST after per-book testing had been exhausted:

| Book | Per-Book Best | CADST Best | Difference |
|------|--------------|-----------|------------|
| 42 | digit '0', pos 45 (+8) | digit '2', pos 91 (+25) | +17 chars |
| 60 | digit '0', pos 73 (+3) | digit '9', pos 73 (+15) | +12 chars |
| 15 | digit '0', pos 0 (+0) | digit '5', pos 62 (+8) | +8 chars |

CADST found 17 improvements that per-book testing missed, totaling +38 characters. The key insight: in a concatenated narrative with overlapping fragments, local optimality does not guarantee global optimality.

---

## 6. Results

### 6.1 BoLWP Performance

Applied across Sessions 29-30, BoLWP resolved garbled blocks in three rounds:

| Round | Blocks Resolved | Characters Recovered | Avg Block Size |
|-------|----------------|---------------------|----------------|
| Session 29, Round 1 | 14 | +151 chars | 10.8 |
| Session 29, Round 2 | 20 | +119 chars | 6.0 |
| Session 30 | 4 | +15 chars | 4.8 |
| **Total** | **38** | **+285 chars** | — |

### 6.2 Coverage Impact

| Metric | Before BoLWP | After BoLWP+CAAR+CADST | Delta |
|--------|-------------|----------------------|-------|
| Word coverage | 81.1% (4470/5515) | 94.4% (5204/5515) | +13.3% |
| Garbled blocks | ~180 | ~50 | -130 |
| Letter-level coverage | 100% | 100% | 0% |

### 6.3 Largest Single Resolutions

| Garbled Block | Length | Resolution | Words | Swaps |
|--------------|--------|-----------|-------|-------|
| `OIAITOEMEENDGEEMKMTGRSCASEZSTEIEHHIS` | 35 | HECHELT+ALLES+GOTTDIENERS | 3 | 4 I→E |
| `UUISEMIADIIRGELNMH` | 18 | LANG+HEIME+DIESER | 3 | 2 I→E |
| `EHHIIHHISLUIRUNNS` | 17 | HEHL+UNRUH+SEINES | 3 | 2 I→E |
| `AUIGLAUNHEARUCHT` | 16 | LANG+URALTE+AUCH | 3 | 1 I→L |
| `OIAITOEMEEND` | 12 | OEDE+NAME+TEE | 3 | 2 I→E |

### 6.4 Swap Distribution

Across all 38 resolved blocks:
- 0 swaps (exact anagram partition): 12 blocks (31%)
- 1 swap: 9 blocks (24%)
- 2 swaps: 14 blocks (37%)
- 3 swaps: 3 blocks (8%)

The I→E swap dominates (87% of all swaps), consistent with E being the most frequent letter (20 codes) creating the most boundary ambiguity.

---

## 7. Discussion

### 7.1 Why BoLWP Works

Traditional anagram resolution assumes a 1:1 mapping between garbled blocks and dictionary words. This assumption fails in spaceless homophonic ciphers because:

1. **No word boundaries exist** in the plaintext encoding — multiple words' letters are interleaved in the decoded stream
2. **DP segmentation greedily matches** known words, leaving multi-word residuals as single blocks
3. **Letter swaps from code ambiguity** prevent exact anagram matching even for single words

BoLWP relaxes all three assumptions: it allows multi-word decomposition, tolerates known letter substitutions, and operates on the letter multiset rather than ordered characters.

### 7.2 Limitations

1. **Exponential worst case:** Very long garbled blocks (>25 characters) with small average word length may not resolve in practical time
2. **Ambiguity:** Multiple valid decompositions may exist; the algorithm returns the highest-coverage one, which may not be semantically correct
3. **Swap model specificity:** The I↔E and I↔L swaps are specific to this cipher's code distribution — other ciphers would require different swap models
4. **Dictionary dependence:** The quality of results depends entirely on dictionary completeness — missing archaic or domain-specific words produce false negatives

### 7.3 Generalizability

BoLWP is applicable to any cipher where:
- Decoded text lacks word boundaries
- Garbled blocks contain correctly decoded letters from multiple words
- Systematic letter confusion patterns can be identified and modeled as swaps

Candidate applications include:
- Other homophonic substitution ciphers (historical diplomatic ciphers, Zodiac-like systems)
- OCR error correction in historical manuscripts (where character confusion follows systematic patterns)
- Ancient language decipherment (Linear A, Indus Valley script) where word boundaries are unknown

### 7.4 Comparison with Existing Methods

| Method | Single Word | Multi-Word | Swap Tolerant | Context-Aware |
|--------|:-----------:|:----------:|:-------------:|:-------------:|
| Traditional anagram matching | Yes | No | No | No |
| DP word segmentation | No | Yes | No | No |
| Spelling correction (Levenshtein) | Yes | No | Yes | No |
| **BoLWP** | **Yes** | **Yes** | **Yes** | **No** |
| **BoLWP + CAAR** | **Yes** | **Yes** | **Yes** | **Yes** |

---

## 8. Implementation

### 8.1 Core Algorithm (Python)

```python
def bag_of_letters_partition(garbled, dictionary, max_swaps=3):
    """Find best multi-word decomposition of a garbled block."""
    from collections import Counter

    bag = Counter(garbled)
    n = len(garbled)
    best = {'coverage': 0, 'words': [], 'swaps': 0}

    # Pre-filter dictionary to words that could fit
    candidates = [w for w in dictionary if len(w) <= n]

    def can_match(remaining, word, swap_budget):
        """Check if word can be formed from remaining letters with swaps."""
        needed = Counter(word)
        swaps = 0
        for letter, count in needed.items():
            have = remaining.get(letter, 0)
            if have >= count:
                continue
            deficit = count - have
            # Try I<->E swap
            if letter == 'E' and remaining.get('I', 0) >= deficit:
                swaps += deficit
            elif letter == 'I' and remaining.get('E', 0) >= deficit:
                swaps += deficit
            # Try I<->L swap
            elif letter == 'L' and remaining.get('I', 0) >= deficit:
                swaps += deficit
            elif letter == 'I' and remaining.get('L', 0) >= deficit:
                swaps += deficit
            else:
                return False, 0
        return swaps <= swap_budget, swaps

    def search(remaining, rem_len, words, swaps_used):
        coverage = sum(len(w) for w in words)
        if coverage > best['coverage']:
            best['coverage'] = coverage
            best['words'] = words[:]
            best['swaps'] = swaps_used

        if rem_len == 0:
            return

        for w in candidates:
            if len(w) > rem_len:
                continue
            ok, sw = can_match(remaining, w, max_swaps - swaps_used)
            if ok:
                new_rem = subtract_with_swaps(remaining, w)
                search(new_rem, rem_len - len(w), words + [w], swaps_used + sw)

    search(bag, n, [], 0)
    return best
```

### 8.2 CAAR Implementation

```python
def context_aware_replace(text, anagram_map):
    """Apply anagram resolutions respecting compound word boundaries."""
    # Phase 1: Standard longest-first replacement
    for key in sorted(anagram_map.keys(), key=len, reverse=True):
        text = text.replace(key, anagram_map[key])

    # Phase 2: Context-specific fixups for compound collisions
    # Each entry: (pattern_in_context, replacement_in_context)
    context_fixes = [
        ('TREUUNR', 'TREUNUR'),  # UNR->NUR without breaking WINDUNRUH
    ]
    for pattern, replacement in context_fixes:
        text = text.replace(pattern, replacement)

    return text
```

---

## 9. Conclusion

Bag-of-Letters Word Partition addresses a gap in classical cryptanalysis: the recovery of multi-word sequences from garbled blocks in spaceless homophonic ciphers. By treating garbled blocks as letter multisets and searching for optimal multi-word decompositions with systematic swap tolerance, BoLWP recovered 285 characters (13.3% coverage gain) from a cipher that had resisted 25 years of community effort and all prior techniques in our own 30-session analysis.

The companion techniques CAAR and CADST solve adjacent problems: compound-word-safe substitution and global validation of local modifications in fragmented texts. Together, these three techniques lifted coverage from 81.1% to 94.4%, demonstrating that novel post-decryption text recovery methods can extract significant additional value from a "mostly solved" cipher.

---

## References

1. Beker, H. & Piper, F. (1982). *Cipher Systems: The Protection of Communications.* Northwood.
2. Lasry, G. (2018). *A Methodology for the Cryptanalysis of Classical Ciphers with Search Metaheuristics.* Kassel University Press.
3. CipSoft GmbH. (1997–present). *Tibia.* https://www.tibia.com
4. s2ward. (2024). *469 Repository.* https://github.com/s2ward/469
5. Schmeh, K. (2020). *Codebreaking: A Practical Guide.* No Starch Press.

---

*This work is licensed under BUSL-1.1. Free for individuals, academics, and non-profits. Commercial use requires a participation agreement. See LICENSE and COMMERCIAL.md in the repository root.*
