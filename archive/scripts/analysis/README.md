> **Idioma / Language:** [Español](#español) | [English](#english)

# Analysis Scripts

## English

78 scripts for per-session deep analysis, validation, and report generation.

### Reusable Tools

| Script | Purpose |
|--------|---------|
| **`generate_library_guide.py`** | Generate wiki-ready Hellgate Library guide |
| `bookcase_narrative.py` | Reconstruct narrative by in-game bookcase location |
| `parse_bookcases.py` | Extract bookcase structure from raw data |
| `garbled_analysis.py` | Analyze failure modes in undecoded segments |
| `garbled_context_trace.py` | Trace context around garbled blocks |
| `code_suspicion.py` | Identify suspect code assignments via gap analysis |
| `digit_insertion_analysis.py` | Test digit insertion hypothesis on odd-length books |
| `iterative_corrections.py` | Automated correction feedback loops |
| `test_corrections.py` | Validate correction outcomes |
| `math_patterns.py` | Test mathematical encoding hypotheses |

### Session Scripts (68 files)

Scripts named `session{N}_*.py` contain deep analysis for specific sessions:

| Session | Scripts | Focus |
|---------|---------|-------|
| 18 | 3 | Code 20 investigation, MHG patterns, deep analysis |
| 19 | 6 | Boundary effects, word segmentation, narrative quality |
| 20-24 | 15 | Systematic garbled block attacks, word completion |
| 25-26 | 12 | Cross-boundary anagrams, mapping stability testing |
| 27 | 6 | Lore research integration, systematic attack |
| 28 | 8 | Letter-swap tolerant matching, BoLWP prototype |
| 29 | 10 | BoLWP full deployment, +10.1% coverage gain |
| 30 | 8 | CADST optimization, digit-split, final polish |

---

## Español

78 scripts para análisis profundo por sesión, validación y generación de reportes.

### Herramientas Reutilizables

| Script | Propósito |
|--------|-----------|
| **`generate_library_guide.py`** | Generar guía de la Biblioteca Hellgate para wiki |
| `bookcase_narrative.py` | Reconstruir narrativa por ubicación de estantería in-game |
| `parse_bookcases.py` | Extraer estructura de estanterías de datos crudos |
| `garbled_analysis.py` | Analizar modos de fallo en segmentos no decodificados |
| `garbled_context_trace.py` | Trazar contexto alrededor de bloques ilegibles |
| `code_suspicion.py` | Identificar asignaciones de códigos sospechosas |
| `digit_insertion_analysis.py` | Probar hipótesis de inserción de dígitos en libros impares |
| `iterative_corrections.py` | Ciclos automáticos de corrección |
| `math_patterns.py` | Probar hipótesis de codificación matemática |

### Scripts de Sesión (68 archivos)

Los scripts `session{N}_*.py` contienen análisis profundo para sesiones específicas (18-30). Cada sesión atacó un aspecto diferente del cifrado, desde investigación de códigos individuales hasta el despliegue completo de BoLWP.
