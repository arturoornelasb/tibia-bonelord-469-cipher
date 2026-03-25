# Tibia 469 Bonelord Language — Pipeline
# Run `make help` to see available targets.
#
# Prerequisites: Python 3.8+, no external dependencies.
# All scripts read from data/ and write to data/ or stdout.

PYTHON := python3
MAPPING := data/mapping_v7.json
BOOKS   := data/books.json

.PHONY: help decode decode-verbose optimize anagram-scan verify clean

# ─────────────────────────────────────────────────────────────────────────────
# Main targets
# ─────────────────────────────────────────────────────────────────────────────

## help       : Show this help message
help:
	@grep -E '^## ' Makefile | sed 's/## /  /'

## decode     : Decode all 70 books with the canonical mapping (94.6% coverage)
decode:
	$(PYTHON) scripts/core/narrative_v3_clean.py

## decode-verbose : Decode with per-book coverage stats printed to stdout
decode-verbose:
	$(PYTHON) scripts/core/narrative_v3_clean.py --verbose

## optimize   : Re-run the simulated annealing optimizer on the current mapping
##              Output: data/mapping_v7.json (overwrites if improved)
optimize:
	$(PYTHON) scripts/core/simulated_annealing_v8.py

## constrain  : Re-run the constraint solver (alternative optimizer)
constrain:
	$(PYTHON) scripts/core/constraint_solver_v8.py

## build      : Re-run the full V7 mapping builder + attack pipeline
##              (slow — runs build_v7_and_attack.py)
build:
	$(PYTHON) scripts/core/build_v7_and_attack.py

## anagram    : Run the anagram bruteforcer on current garbled blocks
anagram:
	$(PYTHON) scripts/core/anagram_bruteforce.py

## anagram-geo: Run the geographic anagram attack
anagram-geo:
	$(PYTHON) scripts/core/geographic_anagram_attack.py

## crib       : Run the crib-drag attack on garbled segments
crib:
	$(PYTHON) scripts/core/crib_garbled_attack.py

## gap        : Re-assign gap codes
gap:
	$(PYTHON) scripts/core/gap_code_reassignment.py

## translate  : Generate human-readable narrative translation
translate:
	$(PYTHON) scripts/core/narrative_translate.py

## verify     : Quick verification — print mapping stats and coverage summary
verify:
	@$(PYTHON) -c "\
import json; \
m = json.load(open('$(MAPPING)')); \
b = json.load(open('$(BOOKS)')); \
codes = sum(len(v) for v in m.values()); \
print(f'Mapping: {codes} codes across {len(m)} letters'); \
print(f'Books: {len(b)} entries in corpus'); \
"

## clean      : Remove generated output files (keeps source data)
clean:
	@rm -f data/decoded_text.txt data/decoded_narrative.json data/master_text.txt
	@echo "Cleaned generated output files."

# ─────────────────────────────────────────────────────────────────────────────
# Pipeline order (for full reproduction from scratch)
# ─────────────────────────────────────────────────────────────────────────────
#
#  1. build       — build initial mapping from frequency analysis
#  2. optimize    — refine with simulated annealing
#  3. constrain   — further refine with constraint solver
#  4. anagram     — resolve anagrammed proper nouns
#  5. anagram-geo — geographic-context anagram attack
#  6. gap         — assign gap/residual codes
#  7. crib        — crib-drag on remaining garbled segments
#  8. decode      — produce final decoded output
#  9. translate   — generate human-readable translation
#
# Or simply run `make decode` to reproduce the final result using
# the committed mapping_v7.json (skips steps 1–7).
# ─────────────────────────────────────────────────────────────────────────────
