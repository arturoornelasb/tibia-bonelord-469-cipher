> **Idioma / Language:** [Español](#español) | [English](#english)

# Scripts

## English

| Folder | Scripts | Description |
|--------|---------|-------------|
| [`core/`](core/) | 14 | Canonical pipeline: decoder, optimizer, attacks, anagram tools |

Historical and exploratory scripts are preserved in [`archive/scripts/`](../archive/scripts/):

| Folder | Scripts | Description |
|--------|---------|-------------|
| `archive/scripts/sessions/` | 43 | Per-round crack scripts from Sessions 9–12 |
| `archive/scripts/core_misc/` | 27 | One-off investigation scripts |
| `archive/scripts/experimental/` | 79 | Early-hypothesis scripts |
| `archive/scripts/analysis/` | 81 | Per-session analysis scripts (Sessions 18–31) |

### Quick Start

```bash
# Decode all 70 books (uses committed data/mapping_v7.json)
python scripts/core/narrative_v3_clean.py

# Or via Makefile
make decode
```

See [`core/README.md`](core/README.md) for the full script catalog.

---

## Español

| Carpeta | Scripts | Descripción |
|---------|---------|-------------|
| [`core/`](core/) | 14 | Pipeline canónico: decodificador, optimizador, ataques, herramientas de anagramas |

Los scripts históricos y exploratorios están en [`archive/scripts/`](../archive/scripts/):

| Carpeta | Scripts | Descripción |
|---------|---------|-------------|
| `archive/scripts/sessions/` | 43 | Scripts de ataque por ronda (Sesiones 9–12) |
| `archive/scripts/core_misc/` | 27 | Scripts de investigación puntuales |
| `archive/scripts/experimental/` | 79 | Scripts de hipótesis tempranas |
| `archive/scripts/analysis/` | 81 | Scripts de análisis por sesión (Sesiones 18–31) |

### Inicio Rápido

```bash
python scripts/core/narrative_v3_clean.py
```

Ver [`core/README.md`](core/README.md) para el catálogo completo de scripts.
