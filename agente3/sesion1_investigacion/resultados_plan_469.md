# Resultados: Plan de Resolución del Cifrado 469

> Ejecutado: 2026-03-23 | Agente 3

---

## Resumen Ejecutivo

Se ejecutaron **4 fases de ataque** con 20+ transformaciones distintas sobre los 70 libros de Hellgate (11,263 dígitos, 5,631 pares). **Ninguna transformación alternativa superó al mapeo base v4**. El cifrado homofónico de sustitución es confirmado como el enfoque correcto.

La Fase 2 logró una **mejora marginal** del 36.6% → 38.3% en parseo de palabras alemanas mediante reasignación de 3 códigos sospechosos.

---

## Fase 1: Hipótesis del Espejo 🪞

**Resultado: ❌ Descartada como mecanismo de nivel de caracter**

| Transformación | Word Parse | vs Baseline |
|:---|:---:|:---:|
| **Baseline (offset 0)** | **36.6%** | — |
| Baseline (offset 1) | 33.6% | -3.0% |
| 1A Reversal dígitos (o0) | 16.2% | -20.4% |
| 1A Reversal dígitos (o1) | 15.2% | -21.4% |
| 1B Swap adyacentes | 11.8% | -24.8% |
| 1C Superstring reverso | 15.9% | -20.7% |
| 1D Fórmula Facebook | 10.5% | -26.1% |
| 1D FB Inversa | 4.4% | -32.2% |

> **Conclusión**: Los espejos no aplican como transformación criptográfica directa sobre los pares de dígitos. El motivo del espejo es **temático/lore** (Paradox Tower, bonelords mirándose), no un paso mecánico del descifrado.

---

## Fase 2: Códigos Gap-Only 🔧

**Resultado: ✅ Mejora de 36.6% → 38.3% (+1.7%)**

### Gap-Only Codes encontrados (15 total, 555 ocurrencias):

| Código | Letra actual | Ocurrencias | En bigramas alemanes |
|:---:|:---:|:---:|:---:|
| [34] | L | 91 | 0 |
| [04] | M | 77 | 0 |
| [36] | W | 74 | 0 |
| [99] | O | 56 | 0 |
| [96] | L | 51 | 0 |
| [83] | V | 38 | 0 |
| [77] | Z | 35 | 0 |
| + 8 más | — | 206 total | 0 |

### Letras sub-representadas vs alemán esperado:
- **B**: -1.59% (más deficitaria)
- **F**: -1.30%
- **L**: -0.92%
- **C**: -0.86%
- **K**: -0.84%
- **P**: -0.79% (0 ocurrencias!)

### Reasignaciones que mejoraron:
1. `[83]` V → **A** (+0.78% WP)
2. `[96]` L → **A** (+0.57% WP)
3. `[99]` O → **A** (+0.39% WP)

> Mapeo mejorado guardado en `mapping_v5_agente3.json`

---

## Fase 3: Segmentación por Libros Pares 📖

**Resultado: ✅ Estructura confirmada**

### Datos numéricos:
- **31 relaciones de contención** (un libro dentro de otro)
- **164 solapamientos suffix-prefix** (≥10 dígitos)
- **8 cadenas reconstruidas**:

| Cadena | Libros | Dígitos | Secuencia |
|:---:|:---:|:---:|:---|
| 0 | 10 | ~1,644 | 17→32→11→43→59→18→67→2→48→28 |
| 1 | 8 | ~1,664 | 44→3→68→45→51→53→5→9 |
| 2 | 4 | ~570 | 24→21→13→38 |
| 3 | 4 | ~944 | 31→19→35→10 |
| 4 | 3 | ~352 | 25→15→16 |
| 5-7 | 2 c/u | ~120-307 | Pares menores |

- **33 libros aislados** (no conectados a ninguna cadena)
- Unidad repetida más frecuente: `EURALTESTEINENTERAD…` (30 dígitos, en 14 libros)

---

## Fase 4: Pistas No Exploradas 🔍

**Resultado: ❌ Ninguna alternativa supera al baseline**

| Test | Word Parse | vs Baseline |
|:---|:---:|:---:|
| **Baseline** | **36.6%** | — |
| FB sustitución | 16.4% | -20.2% |
| Tiveana add 13 | 16.2% | -20.4% |
| Tiveana add 49 | 15.7% | -20.9% |
| Vigenère "469" | 14.6% | -21.9% |
| Nihilista "469" | 9.0% | -27.6% |

### Hallazgo interesante del Facebook:
La fórmula R = 0.593L + 25.28 mapea letras a otras letras. Del análisis:
- `N(11)→?(32)`, `S(12)→?(32)` — el código 32 no tiene asignación
- `I(15)→L(34)`, `R(24)→E(39)`, `D(42)→I(50)`, `U(43)→R(51)`
- Hay un patrón `D→I, U→R, I→L, K→K (fijo)` que recuerda a una permutación

---

## Conclusiones Generales

1. **El mapeo v4 es fundamentalmente correcto** — ninguna transformación global lo mejora
2. **El espejo es lore, no criptografía** — el motivo aparece en la narrativa pero no en la mecánica de cifrado
3. **El camino es la mejora incremental del mapeo**: reasignar los 15 gap-only codes (555 ocurrencias) es la mayor oportunidad
4. **Las cadenas 0 y 1 son el texto principal**: 18 libros, ~3,300 dígitos — el núcleo del mensaje
5. **Letras B, F, P** prácticamente ausentes sugieren que varios gap-only codes pertenecen a estas letras
6. **33 libros aislados** podrían ser variantes o fragmentos que necesitan offset distinto

---

## Archivos Generados

| Archivo | Contenido |
|:---|:---|
| `scripts/utils_469.py` | Módulo de utilidades compartidas |
| `scripts/fase1_espejos.py` | Tests de 4 transformaciones espejo |
| `scripts/fase2_gap_analysis.py` | Análisis de códigos gap-only |
| `scripts/fase3_word_segmentation.py` | Segmentación + cadenas |
| `scripts/fase4_nuevas_pistas.py` | Vigenère, Nihilista, Tiveana |
| `scripts/fase[1-4]_resultados.txt` | Salida cruda de cada fase |
| `mapping_v5_agente3.json` | Mapeo mejorado (3 reasignaciones) |
| `plan_resolucion_469.md` | Plan original documentado |
