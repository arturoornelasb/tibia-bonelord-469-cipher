# Research Findings Log

This directory contains the session-by-session research log for the Tibia 469 cipher investigation.
The complete log is also available in `FINDINGS.md` at the repository root.

## Session Index

| File | Sessions | Content |
|------|----------|---------|
| [session_01_04_early.md](session_01_04_early.md) | 1–4 | Initial analysis, statistical fingerprinting, 2-digit pair encoding breakthrough |
| [session_05.md](session_05.md) | 5 | Structural analysis, narrative reconstruction |
| [session_06.md](session_06.md) | 6 | Tier 5–6 code assignments (T, A, G, R, F, L, O) |
| [session_07.md](session_07.md) | 7 | Tier 7 assignments, full narrative decode attempt |
| [session_08.md](session_08.md) | 8 | Tier 8 assignments (S, E, A, D, I, K, Z) |
| [session_09.md](session_09.md) | 9 | Narrative assembly, deep pattern analysis |
| [session_10_13.md](session_10_13.md) | 10–13 | Deep pattern attack, colophon discovery, V7 mapping, geographic anagram breakthrough |
| [session_14.md](session_14.md) | 14 | Constraint solving (V8), anagram resolution, narrative reconstruction |
| [session_15.md](session_15.md) | 15 | Statistical validation, garbled segment deep analysis |
| [session_16.md](session_16.md) | 16 | Two encoding systems, lore connections |
| [session_17.md](session_17.md) | 17 | Mapping correction, digit insertions, bookcase mapping |
| [session_18.md](session_18.md) | 18 | Complete bookcase mapping, garbled block tracing, anagram discovery |
| [session_19.md](session_19.md) | 19 | Cross-boundary anagrams, NPC investigation, deep garbled analysis |
| [session_20.md](session_20.md) | 20 | Garbled block census, TER discovery, SCHRAT anagram |
| [session_21.md](session_21.md) | 21 | HEDDEMI fix, SAND cross-boundary, systematic block attack |
| [session_22.md](session_22.md) | 22 | MHG word discovery, CHIS→SICH, HEL breakdown |
| [session_23.md](session_23.md) | 23 | Code fingerprinting, big block attack, proper noun confirmation |
| [session_24.md](session_24.md) | 24 | Deep multi-language research — garbled text confirmed as German |
| [session_25.md](session_25.md) | 25 | Cross-boundary anagram breakthrough, parallel attack |
| [session_26.md](session_26.md) | 26 | Massive coverage leap: 72.3% → 76.9% |
| [session_27.md](session_27.md) | 27 | Systematic garbled attack + lore research: 76.9% → 78.7% |
| [session_28.md](session_28.md) | 28 | Letter-swap tolerant attack: 78.7% → 81.1% |
| [session_29.md](session_29.md) | 29 | Bag-of-Letters Word Partition: 81.1% → 89.1% |
| [session_30.md](session_30.md) | 30 | DIGIT_SPLIT optimization + UNR fix: 91.2% → 93.3% |
| [session_31.md](session_31.md) | 31 | Post-resolution fixups + DIGIT_SPLIT re-optimization: 94.4% → 94.6% |

## Coverage Progression

```
Session  1–4:   ~0% → ~40%   (initial breakthrough, 2-digit encoding confirmed)
Session  5–9:   40% → ~55%   (systematic tier assignments)
Session 10–13:  55% → ~60%   (deep pattern attack, V7 mapping)
Session 14–15:  60% → ~65%   (constraint solving, statistical validation)
Session 16–19:  65% → ~70%   (bookcase mapping, cross-boundary anagrams)
Session 20–25:  70% → ~81%   (systematic block attacks, BoLWP technique)
Session 26–28:  76% → ~81%   (swap attacks, coverage leaps)
Session 29:     81% → 89%    (Bag-of-Letters Word Partition — key breakthrough)
Session 30:     91% → 93%    (DIGIT_SPLIT optimization)
Session 31:     94.4% → 94.6% (final fixups — current state)
```

## Key Breakthroughs

1. **Session 3** — Confirmed homophonic substitution cipher (98 two-digit codes → 22 German letters)
2. **Session 4** — URALTE STEINE crib attack gave first anchor points
3. **Session 13** — Geographic anagram resolution (SALZBERG, WEICHSTEIN confirmed)
4. **Session 14** — Constraint solver (V8) + simulated annealing reached 60%+ coverage
5. **Session 29** — Bag-of-Letters Word Partition (BoLWP) jumped from 81% to 89%
6. **Session 30** — DIGIT_SPLIT operator reached 93%+ coverage
