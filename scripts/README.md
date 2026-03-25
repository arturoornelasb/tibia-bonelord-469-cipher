> **Idioma / Language:** [Español](#español) | [English](#english)

# Scripts

## English

This directory contains **255 Python scripts** developed across 31 sessions of cryptanalysis. All scripts are preserved as-is — they document the complete research journey from initial frequency analysis to 94.6% decode.

### Directory Structure

| Directory | Scripts | Purpose |
|-----------|---------|---------|
| `core/` | 98 | Main decryption pipeline, cipher attacks, and mapping builders |
| `analysis/` | 78 | Per-session analysis, validation, and statistics |
| `experimental/` | 79 | Early hypotheses: base-5, bigram, checkerboard, DNA alignment |

### Key Entry Points

| Script | What it does |
|--------|-------------|
| `core/narrative_v3_clean.py` | **START HERE** — Decodes all 70 books with v7 mapping (94.6%) |
| `core/build_v7_and_attack.py` | Builds mapping v7 and runs final attacks |
| `core/anagram_resolution.py` | Resolves anagrammed proper nouns (SALZBERG, etc.) |
| `analysis/generate_library_guide.py` | Generates the wiki-ready Hellgate Library guide |

### Quick Start

```bash
python scripts/core/narrative_v3_clean.py
```

See each subdirectory's README for detailed script catalogs.

---

## Español

Este directorio contiene **255 scripts de Python** desarrollados a lo largo de 31 sesiones de criptoanálisis. Todos los scripts se conservan tal cual — documentan el recorrido completo de investigación desde el análisis de frecuencia inicial hasta el 94.6% de decodificación.

### Estructura de Directorios

| Directorio | Scripts | Propósito |
|------------|---------|-----------|
| `core/` | 98 | Pipeline principal de descifrado, ataques y constructores de mapeo |
| `analysis/` | 78 | Análisis por sesión, validación y estadísticas |
| `experimental/` | 79 | Hipótesis tempranas: base-5, bigramas, checkerboard, alineación DNA |

### Puntos de Entrada Clave

| Script | Qué hace |
|--------|----------|
| `core/narrative_v3_clean.py` | **EMPIEZA AQUÍ** — Decodifica los 70 libros con mapeo v7 (94.6%) |
| `core/build_v7_and_attack.py` | Construye el mapeo v7 y ejecuta ataques finales |
| `core/anagram_resolution.py` | Resuelve nombres propios anagramados (SALZBERG, etc.) |
| `analysis/generate_library_guide.py` | Genera la guía de la Biblioteca Hellgate para wiki |

### Inicio Rápido

```bash
python scripts/core/narrative_v3_clean.py
```

Ver el README de cada subdirectorio para catálogos detallados de scripts.
