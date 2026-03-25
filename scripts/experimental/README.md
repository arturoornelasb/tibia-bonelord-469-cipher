> **Idioma / Language:** [Español](#español) | [English](#english)

# Experimental Scripts

## English

79 scripts from the exploratory phase (approximately Sessions 1-8), before the homophonic substitution model was confirmed. These represent hypotheses that were tested and either validated or discarded.

### Frequency & Statistical Analysis

| Script | Purpose |
|--------|---------|
| `analyze_469.py` | Initial frequency analysis of digit sequences |
| `analyze_decoded.py` | Analyze decoded output quality |
| `bigram_audit.py` / `bigram_decode.py` / `bigram_validate.py` | Bigram hypothesis testing |
| `base5_and_residuals.py` | Test base-5 encoding hypothesis |
| `digit9_and_differential.py` | Differential analysis of digit patterns |
| `score_solutions.py` | Score candidate solutions |

### Cipher Attack Approaches

| Script | Approach | Result |
|--------|----------|--------|
| `checkerboard_search.py` / `deep_checkerboard.py` | Polybius checkerboard hypothesis | Discarded |
| `crack_homophonic.py` | Early homophonic attack (pre-v7) | Superseded |
| `known_plaintext_attack.py` | Known plaintext attack | Evolved into core crib attacks |
| `crib_attack.py` / `crib_constrained.py` / `crib_fast.py` | Crib-based attacks | Evolved into core |
| `paradox_key.py` | Paradox Tower key hypothesis | Discarded |
| `constraint_crack.py` / `constrained_decode.py` | Constraint-based cracking | Evolved into core |

### Tier-Based Decoding (historical progression)

`decode_tier4.py` through `decode_tier13.py` — Progressive tier assignments from early sessions. Superseded by `core/build_v7_and_attack.py`.

### Pattern Tracing & Investigation

| Script | Purpose |
|--------|---------|
| `trace_codes.py` / `trace_pairs.py` / `trace_doubles.py` | Trace code patterns |
| `trace_iii.py` / `trace_mystery.py` | Investigate anomalous patterns |
| `investigate_16.py` | Code 16 investigation |
| `find_bkzom.py` | Search for specific patterns |
| `pattern_brute.py` | Brute-force pattern search |
| `transition_filter.py` | Filter by transition probability |

### Decode & Text Processing

| Script | Purpose |
|--------|---------|
| `decode_attempt.py` / `fast_decode.py` / `full_decode.py` | Various decode attempts |
| `master_decode.py` / `master_text.py` / `joint_decode.py` | Master text assembly |
| `pair_decode.py` / `pairs_hypothesis.py` | Pair-based decoding tests |
| `superstring.py` / `superstring_parse.py` / `read_superstring.py` | Superstring operations |
| `parse_narrative.py` / `parse_text.py` | Text parsing utilities |
| `word_derive.py` / `word_diff_test.py` / `word_optimize.py` | Word-level optimization |
| `refine_mapping.py` / `refined_decode.py` | Mapping refinement |
| `swap_io_test.py` / `swap_optimize.py` | I/O swap testing |
| `context_derive.py` | Context-based derivation |

---

## Español

79 scripts de la fase exploratoria (aproximadamente Sesiones 1-8), antes de que el modelo de sustitución homofónica fuera confirmado. Representan hipótesis que fueron probadas y validadas o descartadas.

### Análisis Estadístico y de Frecuencia
Scripts como `analyze_469.py`, `bigram_*.py`, `base5_and_residuals.py` — análisis inicial que confirmó la codificación de 2 dígitos.

### Enfoques de Ataque
Scripts como `checkerboard_search.py` (descartado), `crack_homophonic.py` (superado), `crib_attack.py` (evolucionó al core), `paradox_key.py` (descartado).

### Decodificación por Tiers (progresión histórica)
`decode_tier4.py` a `decode_tier13.py` — Asignaciones progresivas de las sesiones tempranas. Superados por `core/build_v7_and_attack.py`.

### Rastreo de Patrones
Scripts de `trace_*.py` e `investigate_*.py` — investigación de patrones anómalos y códigos individuales.

Estos scripts son un registro histórico. Para el pipeline actual, usar `core/narrative_v3_clean.py`.
