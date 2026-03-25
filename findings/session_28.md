## 25. Session 28: Letter-Swap Tolerant Attack (78.7% → 81.1%)

### Key Discovery: I↔E and I↔L Swaps are Real Cipher Patterns

The cipher doesn't just scramble letters within blocks — it also substitutes similar-looking
letters. Confirmed swap patterns:
- **I↔E swap**: Letters I and E are interchanged in some anagram blocks
- **I↔L swap**: Letters I and L are interchanged in some anagram blocks

These swaps are consistent across multiple books and make linguistic sense after correction.

### New Resolutions (+123 chars)

**I↔E swaps:**
- DEE → EID (oath, +28), URIT → TREU (faithful, +12), RUIT → TREU (+4), NTEIG → NEIGT (+5)

**I↔L swaps:**
- EHI → HEL (bright, +3), LRM → MIR (to me, +3)

**Block splits (garbled block = 2 concatenated words):**
- ADTHA → DA+HAT (there has, +10), MISE → IM+ES (in it, +5)

**+1 pattern (extra letter removed):**
- UNRN → NUN (+14), NDMI → MIN (+9), NSCHA → NACH (+8), AEUU → AUE (+7)
- ENDNO → DENN (+4), ENDR → DER (+3), TOAD → TOD (+3), DDNE → DEN (+3), UENO → NEU (+2)

### Coverage Progress
| Metric | Session 27 | Session 28 | Delta |
|--------|-----------|-----------|-------|
| Coverage | 78.7% | 81.1% | +2.4% |
| Chars covered | 4348 | 4470 | +122 |
| Anagrams | 63+ | 80+ | +17 |

### New Scripts
- `scripts/analysis/session28_swap_attack.py` — Letter-swap tolerant attack (4 strategies)
- `scripts/analysis/session28_round2.py` — Full 70-book decode at 81.1% baseline

---

