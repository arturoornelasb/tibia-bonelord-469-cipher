> **Idioma / Language:** [Español](#español) | [English](#english)

# Core Scripts

## English

98 scripts forming the main decryption pipeline, cipher attacks, and mapping tools.

### Pipeline (decode chain)

| Script | Purpose |
|--------|---------|
| **`narrative_v3_clean.py`** | **CANONICAL** — Complete decryption with all anagram resolutions |
| `narrative_v2.py` | Earlier narrative generation (superseded) |
| `narrative_assembly.py` | Book chain assembly into continuous text |
| `narrative_extraction.py` | Extract narrative segments from decoded output |
| `narrative_final.py` | Final narrative formatting pass |
| `narrative_reconstruct.py` | Reconstruct narrative from chain fragments |
| `narrative_translate.py` | Translation pipeline (DE → EN/ES) |

### Mapping & Optimization

| Script | Purpose |
|--------|---------|
| `build_v7_and_attack.py` | Build mapping v7 and run attacks |
| `constraint_solver_v8.py` | Constraint satisfaction solver for code assignment |
| `simulated_annealing_v8.py` | Blind SA attack (negative result — useful as baseline) |
| `test_combinations_v7.py` | Brute-force test all code reassignments |
| `test_global_reassignments.py` | Global reassignment validation |
| `freq_constrained_optimization.py` | Frequency-constrained mapping optimization |

### Cipher Attacks

| Script | Purpose |
|--------|---------|
| `comprehensive_attack.py` | Multi-vector attack combining all techniques |
| `crack_garbled_core.py` | Attack garbled blocks using BoLWP |
| `crib_garbled_attack.py` | Known-plaintext attack on garbled segments |
| `tibia_lore_attack.py` | Attack using Tibia lore as cribs |
| `deep_anagram_attack.py` | Deep anagram search with swap tolerance |
| `geographic_anagram_attack.py` | Attack proper nouns as geographic anagrams |
| `gap_code_reassignment.py` | Reassign codes that only appear in garbled regions |
| `garbled_segment_attack.py` | Targeted segment-by-segment attack |
| `attack_i_codes.py` | Investigate I-code boundary confusion |

### Anagram Resolution

| Script | Purpose |
|--------|---------|
| `anagram_bruteforce.py` | Brute-force single-word anagram matching |
| `anagram_resolution.py` | Confirmed anagram resolutions (SALZBERG, etc.) |

### Analysis & Utilities

| Script | Purpose |
|--------|---------|
| `decode_v6.py` | Decode with v6 mapping (historical) |
| `comprehensive_decode.py` | Full decode with detailed statistics |
| `dp_parse.py` / `mhg_dp_parse.py` | Dynamic programming word segmentation |
| `word_boundaries.py` | Word boundary detection |
| `raw_superstring.py` / `superstring_v2.py` | Build master superstring from book chains |
| `audit_segments.py` | Audit decoded segments for errors |
| `code_reassign.py` | Code reassignment utilities |
| `formula_analysis.py` | Analyze mathematical patterns in codes |
| `find_missing_letters.py` | Identify unmapped codes |
| `find_repeats.py` | Find repeating patterns across books |
| `doubled_letters.py` | Analyze doubled-letter patterns |
| `investigate_patterns.py` / `investigate_c_ende.py` | Pattern investigation |
| `deep_46.py` / `deep_narrative.py` / `deep_crack_v2.py` | Deep analysis |
| `knightmare_decode.py` | Decode Knightmare NPC dialogue |
| `ruin_discovery.py` | RUIN pattern discovery |
| `sentence_reading.py` | Human-readable sentence extraction |
| `crack_hwnd.py` / `crack_remaining.py` / `crack_short_patterns.py` | Targeted attacks |
| `test_code15.py` / `test_i_codes.py` | Code-specific investigations |
| `final_crack.py` / `crack_codes_v3.py` / `crack_unknowns_v2.py` | Final attack rounds |
| `decode_tier14.py` | Tier 14 residual code assignment |
| `deep_candidate_analysis.py` | Candidate analysis for uncertain codes |

### Session Scripts (43 files)

Scripts named `crack_session{N}{letter}.py` are chronological attack rounds from Sessions 10-12. Each represents one attempt within a session — a research journal in code form.

- `crack_session10b.py` through `crack_session10q.py` (16 scripts)
- `crack_session11b.py` through `crack_session11n.py` (13 scripts)
- `crack_session12b.py` through `crack_session12o.py` (14 scripts)

---

## Español

98 scripts que forman el pipeline principal de descifrado, ataques y herramientas de mapeo.

### Pipeline (cadena de decodificación)

| Script | Propósito |
|--------|-----------|
| **`narrative_v3_clean.py`** | **CANÓNICO** — Descifrado completo con todas las resoluciones de anagramas |
| `narrative_v2.py` | Generación narrativa anterior (superada) |
| `narrative_assembly.py` | Ensamblaje de cadenas de libros en texto continuo |
| `narrative_extraction.py` | Extraer segmentos narrativos de la salida decodificada |
| `narrative_final.py` | Paso final de formato narrativo |
| `narrative_reconstruct.py` | Reconstruir narrativa desde fragmentos de cadenas |
| `narrative_translate.py` | Pipeline de traducción (DE → EN/ES) |

### Mapeo y Optimización

| Script | Propósito |
|--------|-----------|
| `build_v7_and_attack.py` | Construir mapeo v7 y ejecutar ataques |
| `constraint_solver_v8.py` | Solver de satisfacción de restricciones para asignación de códigos |
| `simulated_annealing_v8.py` | Ataque ciego SA (resultado negativo — útil como línea base) |
| `test_combinations_v7.py` | Test de fuerza bruta de todas las reasignaciones |
| `test_global_reassignments.py` | Validación global de reasignaciones |

### Ataques a la Cifra

| Script | Propósito |
|--------|-----------|
| `comprehensive_attack.py` | Ataque multi-vector combinando todas las técnicas |
| `crack_garbled_core.py` | Ataque a bloques ilegibles usando BoLWP |
| `crib_garbled_attack.py` | Ataque de texto plano conocido en segmentos ilegibles |
| `geographic_anagram_attack.py` | Ataque a nombres propios como anagramas geográficos |
| `gap_code_reassignment.py` | Reasignar códigos que solo aparecen en regiones ilegibles |

### Scripts de Sesión (43 archivos)

Los scripts `crack_session{N}{letra}.py` son rondas cronológicas de ataque de las Sesiones 10-12. Cada uno representa un intento dentro de una sesión — un diario de investigación en código.
