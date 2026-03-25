> **Idioma / Language:** [Español](#español) | [English](#english)

# Core Scripts

## English

14 canonical pipeline scripts for decoding, optimization, and cipher attacks.
Historical and exploratory scripts are in [`archive/scripts/`](../../archive/scripts/).

### Entry Point

```bash
python scripts/core/narrative_v3_clean.py   # decode all 70 books (94.6% coverage)
```

Or use the root [`Makefile`](../../Makefile):

```bash
make decode      # run narrative_v3_clean.py
make optimize    # re-run simulated annealing
make build       # full pipeline from scratch
```

### Scripts

| Script | Purpose |
|--------|---------|
| **`narrative_v3_clean.py`** | **CANONICAL decoder** — complete decode with all anagram resolutions |
| `narrative_translate.py` | Translation output (DE → EN/ES) |
| `build_v7_and_attack.py` | Full mapping builder + initial attack pipeline |
| `simulated_annealing_v8.py` | Simulated annealing optimizer |
| `constraint_solver_v8.py` | Constraint-satisfaction solver for code assignment |
| `test_combinations_v7.py` | Brute-force test all pairwise code reassignments |
| `anagram_bruteforce.py` | Single-word anagram matching with swap tolerance |
| `anagram_resolution.py` | Apply confirmed anagram resolutions (SALZBERG, etc.) |
| `geographic_anagram_attack.py` | Attack proper nouns as geographic anagrams |
| `deep_anagram_attack.py` | Deep anagram search across corpus |
| `comprehensive_attack.py` | Multi-vector attack combining all techniques |
| `crack_garbled_core.py` | BoLWP attack on garbled segments |
| `crib_garbled_attack.py` | Known-plaintext crib-drag on garbled segments |
| `gap_code_reassignment.py` | Reassign codes that only appear in garbled regions |

---

## Español

14 scripts canónicos para decodificación, optimización y ataques a la cifra.
Los scripts históricos y exploratorios están en [`archive/scripts/`](../../archive/scripts/).

### Punto de Entrada

```bash
python scripts/core/narrative_v3_clean.py   # decodifica los 70 libros (94.6% de cobertura)
```

### Scripts

| Script | Propósito |
|--------|-----------|
| **`narrative_v3_clean.py`** | **DECODIFICADOR CANÓNICO** — descifrado completo con resoluciones de anagramas |
| `narrative_translate.py` | Salida de traducción (DE → EN/ES) |
| `build_v7_and_attack.py` | Constructor de mapeo completo + pipeline de ataque inicial |
| `simulated_annealing_v8.py` | Optimizador de recocido simulado |
| `constraint_solver_v8.py` | Solver de restricciones para asignación de códigos |
| `test_combinations_v7.py` | Test exhaustivo de todas las reasignaciones posibles |
| `anagram_bruteforce.py` | Búsqueda de anagramas con tolerancia a intercambios |
| `anagram_resolution.py` | Aplicar resoluciones confirmadas (SALZBERG, etc.) |
| `geographic_anagram_attack.py` | Ataque a nombres propios como anagramas geográficos |
| `deep_anagram_attack.py` | Búsqueda profunda de anagramas en el corpus |
| `comprehensive_attack.py` | Ataque multi-vector combinando todas las técnicas |
| `crack_garbled_core.py` | Ataque BoLWP a segmentos ilegibles |
| `crib_garbled_attack.py` | Arrastre de crib en segmentos ilegibles |
| `gap_code_reassignment.py` | Reasignar códigos en regiones ilegibles |
