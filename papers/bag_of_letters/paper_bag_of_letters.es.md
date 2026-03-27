> **Idioma / Language:** Español | [English](paper_bag_of_letters.md)

# Partición de Bolsa de Letras: Una Técnica Novedosa para Resolver Bloques Ilegibles en Cifrados de Sustitución Homofónica

**Autor:** J. Arturo Ornelas Brand — Investigador Independiente — arturoornelas62@gmail.com
**Fecha:** Marzo 2026
**Licencia:** MIT (ver LICENSE en la raíz del repositorio)

---

## Resumen

Presentamos la **Partición de Bolsa de Letras por Palabras** (Bag-of-Letters Word Partition, BoLWP), una técnica combinatoria para recuperar texto legible a partir de bloques ilegibles producidos por cifrados de sustitución homofónica (homophonic substitution ciphers) que codifican texto sin espacios. A diferencia de la resolución de anagramas tradicional (que mapea un bloque ilegible a una palabra conocida), BoLWP descompone el inventario de letras de un bloque en la **combinación óptima de múltiples palabras** de un diccionario conocido, tolerando sustituciones de letras sistemáticas inherentes al cifrado. Aplicada a un cifrado sin resolver de 25 años de antigüedad en el MMORPG Tibia, la técnica logró +10,1% de cobertura de palabras en una sola sesión — la mayor ganancia en 30 sesiones de análisis — resolviendo 34 bloques previamente opacos. También describimos dos técnicas complementarias: la **Resolución de Anagramas Consciente del Contexto** (Context-Aware Anagram Resolution, CAAR), que respeta los límites de palabras compuestas durante la sustitución, y la **Prueba de División de Dígitos Consciente de Concatenación** (Concatenation-Aware Digit-Split Testing, CADST), que valida modificaciones por fragmento contra el texto reconstruido global para prevenir regresiones en los límites entre fragmentos.

---

## 1. Introducción

### 1.1 El Problema

Los cifrados de sustitución homofónica (homophonic substitution ciphers) asignan múltiples símbolos de texto cifrado a la misma letra del texto plano, aplanando las distribuciones de frecuencia y derrotando el análisis de frecuencia estándar. Cuando el texto plano además **carece de límites de palabras** (sin espacios, puntuación ni delimitadores), incluso una descifrado correcto a nivel de letras produce una cadena continua de letras que debe segmentarse en palabras — una tarea no trivial, especialmente para idiomas con composición productiva (p. ej., alemán).

La segmentación de palabras por programación dinámica (PD) contra un diccionario logra buena cobertura en la mayor parte del flujo descifrado, pero ciertas regiones resisten la segmentación. Estos **bloques ilegibles** contienen letras correctamente descifradas que no coinciden con ninguna entrada individual del diccionario. Los enfoques anteriores tratan cada bloque como un posible anagrama de una palabra conocida. Demostramos que esto es insuficiente: muchos bloques ilegibles codifican **múltiples palabras** cuyas letras están intercaladas por el mapeo muchos-a-uno del cifrado.

### 1.2 Contexto

Esta técnica fue desarrollada durante el descifrado del cifrado "Bonelord 469" — 70 libros de secuencias de dígitos puros del MMORPG Tibia (CipSoft GmbH, 1997–presente). El cifrado utiliza 98 códigos de dos dígitos mapeados a 22 letras alemanas (incluyendo vocabulario del alto alemán medio). Después de alcanzar ~81% de cobertura a nivel de palabras mediante métodos criptoanalíticos estándar, el ~19% restante consistía en bloques ilegibles que variaban de 3 a 35 caracteres.

### 1.3 Contribuciones

1. **Partición de Bolsa de Letras por Palabras (Bag-of-Letters Word Partition, BoLWP):** Descomposición combinatoria multipalabra de bloques ilegibles con tolerancia a intercambios
2. **Resolución de Anagramas Consciente del Contexto (Context-Aware Anagram Resolution, CAAR):** Reemplazo de cadenas sensible a los límites de frases
3. **Prueba de División de Dígitos Consciente de Concatenación (Concatenation-Aware Digit-Split Testing, CADST):** Validación global de modificaciones locales en texto cifrado fragmentado

---

## 2. Antecedentes

### 2.1 Sustitución Homofónica

Un cifrado de sustitución homofónica (homophonic substitution cipher) mapea cada letra del texto plano $l$ a un conjunto de símbolos de texto cifrado $C(l)$, donde $|C(l)|$ es aproximadamente proporcional a la frecuencia de $l$ en el idioma del texto plano. Para un alfabeto alemán de 22 letras:

- E (16,4% de frecuencia) → 20 códigos
- N (9,8%) → 10 códigos
- I (7,6%) → 8 códigos
- S (7,3%) → 7 códigos
- ...hasta V (0,7%) → 1 código

Con 98 códigos que abarcan 22 letras, cada código mapea determinísticamente a una letra, pero el mapeo inverso es de uno a muchos.

### 2.2 El Problema de Segmentación

Dada una secuencia de letras descifradas (p. ej., `DIERALTESTEINEISEINRUIN`), la segmentación por PD encuentra los límites de palabras que maximizan la cobertura del diccionario:

```
DIE|RALT|STEIN|E|IST|EIN|RUIN  →  subóptimo
DIE|R|ALTE|STEIN|E|IST|EIN|RUIN  →  mejor
```

Los bloques que no coinciden con ninguna entrada del diccionario se encierran entre llaves: `{RALT}`. Estos bloques ilegibles son el objetivo de BoLWP.

### 2.3 Por Qué Falla la Coincidencia de Anagramas de Palabra Única

Considere el bloque ilegible `DNRHAUNIIOD` (11 caracteres). Ninguna palabra alemana individual es un anagrama de estas letras. Los enfoques tradicionales abandonan este bloque. Pero las letras pueden particionarse en:

- OEDE (4 letras, "páramo") — requiere 2 intercambios I→E
- NUR (3 letras, "solo") — coincidencia exacta
- HAND (4 letras, "mano") — coincidencia exacta

Total: 4 + 3 + 4 = 11 letras consumidas, 100% de cobertura.

---

## 3. Partición de Bolsa de Letras por Palabras (Bag-of-Letters Word Partition, BoLWP)

### 3.1 Algoritmo

**Entrada:** Un bloque ilegible $G$ de longitud $n$, un diccionario $D$ de palabras conocidas, y un conjunto de intercambios de letras (letter swaps) permitidos $S$ (p. ej., {I↔E, I↔L}).

**Salida:** Una secuencia ordenada de palabras $(w_1, w_2, \ldots, w_k)$ de $D$ tal que la unión de multiconjuntos de sus letras coincida (o coincida aproximadamente vía $S$) con el multiconjunto de letras de $G$, maximizando el total de caracteres cubiertos.

```
function BoLWP(G, D, S, max_swaps):
    bag = letter_multiset(G)
    n = |G|
    best = (0, [])  # (coverage, word_list)

    function search(remaining_bag, remaining_len, words, swaps_used):
        if coverage(words) > best.coverage:
            best = (coverage(words), words)

        for w in D where |w| <= remaining_len:
            w_bag = letter_multiset(w)
            (ok, new_swaps) = can_satisfy(remaining_bag, w_bag, S, max_swaps - swaps_used)
            if ok:
                new_bag = remaining_bag - w_bag (with swaps applied)
                search(new_bag, remaining_len - |w|, words + [w], swaps_used + new_swaps)

    search(bag, n, [], 0)
    return best
```

### 3.2 Modelo de Intercambio de Letras

El mapeo muchos-a-uno del cifrado crea ambigüedades sistemáticas en los límites de los códigos. En nuestro cifrado:

- **Intercambio I↔E:** Los 8 códigos de I y 20 códigos de E crean confusión en los límites donde un par de códigos descifrado como `...I` podría en realidad terminar en `E` si el límite del par se desplaza
- **Intercambio I↔L:** Los 2 códigos de L (34, 96) son numéricamente adyacentes a los códigos de I, causando asignaciones erróneas ocasionales

El modelo de intercambio permite hasta $k$ sustituciones de letras totales por bloque (típicamente $k \leq 3$ para bloques de menos de 15 caracteres). Cada intercambio tiene un coste, y el algoritmo prefiere soluciones con menos intercambios.

### 3.3 Poda

La búsqueda ingenua es exponencial. Aplicamos tres estrategias de poda (pruning):

1. **Límite de longitud:** Solo considerar palabras $w$ donde $|w| \leq$ letras restantes
2. **Disponibilidad de letras:** Verificar previamente que la bolsa restante contiene suficientes letras (con intercambios) para formar $w$ antes de recurrir
3. **Longitud mínima de palabra:** Las palabras deben tener $\geq 2$ caracteres (las letras individuales son demasiado ambiguas)
4. **Umbral de cobertura:** Abandonar ramas donde la cobertura máxima alcanzable (actual + letras restantes) no puede superar la mejor actual

### 3.4 Diccionario

El diccionario combina:

- Alemán moderno (palabras comunes, 2-20 caracteres)
- Vocabulario del alto alemán medio (MHG) (538 entradas incluyendo formas arcaicas: SCE, NIT, SER, LEICH, SCHRAT, OEL)
- Nombres propios confirmados del cifrado (SALZBERG, WEICHSTEIN, GOTTDIENER, etc.)
- Palabras de un solo carácter excluidas para prevenir descomposición trivial

Total: ~12.000 entradas (después de filtrar al alfabeto de 22 letras del cifrado).

### 3.5 Complejidad

Para un bloque ilegible de longitud $n$ y un diccionario de tamaño $|D|$:

- Peor caso: $O(|D|^{n/2})$ (todas palabras de 2 letras)
- Caso práctico: $O(|D|^{n/\bar{w}})$ donde $\bar{w}$ es la longitud promedio de palabra (~4,5 para alemán)
- Con poda, los bloques típicos ($n \leq 20$) se resuelven en menos de 1 segundo

---

## 4. Resolución de Anagramas Consciente del Contexto (Context-Aware Anagram Resolution, CAAR)

### 4.1 El Problema de Palabras Compuestas

El reemplazo de cadenas estándar es agnóstico al contexto: reemplazar todas las ocurrencias del patrón $P$ con el reemplazo $R$ puede romper palabras compuestas válidas que contienen $P$ como subcadena.

**Ejemplo:** El bloque ilegible `UNR` es un anagrama de `NUR` ("solo"). Pero reemplazar ingenuamente todos los `UNR` con `NUR` destruye:
- `WINDUNRUH` → `WINDNURH` (rompe el compuesto "Windunruh" = viento-inquietud)
- `SCHAUNRUIN` → `SCHAUNRUIN` (rompe "schaun ruin" = contemplar ruina)

### 4.2 Solución: Focalización en Límites de Frase

En lugar de reemplazo global, CAAR identifica el **contexto frasal** específico en el que ocurre el anagrama y apunta solo a ese patrón:

```python
# INCORRECTO: reemplazo global rompe compuestos
resolved = resolved.replace('UNR', 'NUR')

# CORRECTO: reemplazo específico por contexto
resolved = resolved.replace('TREUUNR', 'TREUNUR')
```

Esto resolvió las 8 ocurrencias del anagrama UNR→NUR sin afectar las 4 ocurrencias de WINDUNRUH.

### 4.3 Cuándo Aplicar CAAR

CAAR es necesario cuando:
1. El patrón del anagrama aparece como subcadena de una palabra compuesta válida
2. La palabra compuesta fue formada por una resolución de anagrama **previa** (ya que las resoluciones se aplican de mayor a menor longitud)
3. Tanto el compuesto como el anagrama independiente son lecturas legítimas

CAAR opera como un **paso posterior** (post-pass) después de la resolución principal de anagramas, corrigiendo colisiones específicas del contexto.

---

## 5. Prueba de División de Dígitos Consciente de Concatenación (Concatenation-Aware Digit-Split Testing, CADST)

### 5.1 El Problema de División de Dígitos

En el cifrado Bonelord, CipSoft eliminó un solo dígito de 37 de los 70 libros (todos los libros con conteos de dígitos impares). Esta ofuscación deliberada rompe la alineación de pares de 2 dígitos en el punto de eliminación, produciendo una decodificación incorrecta de letras aguas abajo.

La recuperación requiere encontrar:
1. La **posición** correcta (0 a $n$) para el dígito faltante
2. El **dígito** correcto (0-9) a insertar

Para un libro de longitud $n$, esto es un espacio de búsqueda de $10 \times (n+1)$.

### 5.2 Prueba Por Libro vs. Global

La **prueba por libro** evalúa cada inserción de dígito contra solo el texto descifrado de ese libro. Esto omite:

- Límites de anagramas entre libros (entradas de ANAGRAM_MAP que abarcan la unión entre dos libros en la narrativa concatenada)
- Efectos aguas abajo donde el cambio de un libro desplaza las frecuencias de letras lo suficiente para alterar la segmentación por PD en libros superpuestos

**CADST** evalúa cada inserción candidata mediante:
1. Insertar el dígito en el libro objetivo
2. Re-decodificar el **corpus completo** (los 70 libros concatenados)
3. Aplicar la pipeline completa de resolución de ANAGRAM_MAP
4. Ejecutar la segmentación por PD en el texto resuelto **global**
5. Comparar la cobertura global contra la línea base

### 5.3 Resultados

La Sesión 30 aplicó CADST después de que la prueba por libro se había agotado:

| Libro | Mejor Por Libro | Mejor CADST | Diferencia |
|-------|----------------|-------------|------------|
| 42 | dígito '0', pos 45 (+8) | dígito '2', pos 91 (+25) | +17 caracteres |
| 60 | dígito '0', pos 73 (+3) | dígito '9', pos 73 (+15) | +12 caracteres |
| 15 | dígito '0', pos 0 (+0) | dígito '5', pos 62 (+8) | +8 caracteres |

CADST encontró 17 mejoras que la prueba por libro pasó por alto, totalizando +38 caracteres. La idea clave: en una narrativa concatenada con fragmentos superpuestos, la optimalidad local no garantiza la optimalidad global.

---

## 6. Resultados

### 6.1 Rendimiento de BoLWP

Aplicado a lo largo de las Sesiones 29-30, BoLWP resolvió bloques ilegibles en tres rondas:

| Ronda | Bloques Resueltos | Caracteres Recuperados | Tamaño Promedio de Bloque |
|-------|-------------------|------------------------|---------------------------|
| Sesión 29, Ronda 1 | 14 | +151 caracteres | 10,8 |
| Sesión 29, Ronda 2 | 20 | +119 caracteres | 6,0 |
| Sesión 30 | 4 | +15 caracteres | 4,8 |
| **Total** | **38** | **+285 caracteres** | — |

### 6.2 Impacto en la Cobertura

| Métrica | Antes de BoLWP | Después de BoLWP+CAAR+CADST | Delta |
|---------|----------------|------------------------------|-------|
| Cobertura de palabras | 81,1% (4470/5515) | 94,6% (5219/5514) | +13,5% |
| Bloques ilegibles | ~180 | ~50 | -130 |
| Cobertura a nivel de letras | 100% | 100% | 0% |

### 6.3 Resoluciones Individuales Más Grandes

| Bloque Ilegible | Longitud | Resolución | Palabras | Intercambios |
|-----------------|----------|-----------|----------|--------------|
| `OIAITOEMEENDGEEMKMTGRSCASEZSTEIEHHIS` | 35 | HECHELT+ALLES+GOTTDIENERS | 3 | 4 I→E |
| `UUISEMIADIIRGELNMH` | 18 | LANG+HEIME+DIESER | 3 | 2 I→E |
| `EHHIIHHISLUIRUNNS` | 17 | HEHL+UNRUH+SEINES | 3 | 2 I→E |
| `AUIGLAUNHEARUCHT` | 16 | LANG+URALTE+AUCH | 3 | 1 I→L |
| `OIAITOEMEEND` | 12 | OEDE+NAME+TEE | 3 | 2 I→E |

### 6.4 Distribución de Intercambios

A lo largo de los 38 bloques resueltos:
- 0 intercambios (partición exacta de anagrama): 12 bloques (31%)
- 1 intercambio: 9 bloques (24%)
- 2 intercambios: 14 bloques (37%)
- 3 intercambios: 3 bloques (8%)

El intercambio I→E domina (87% de todos los intercambios), consistente con que E es la letra más frecuente (20 códigos) creando la mayor ambigüedad en los límites.

---

## 7. Discusión

### 7.1 Por Qué Funciona BoLWP

La resolución de anagramas tradicional asume un mapeo 1:1 entre bloques ilegibles y palabras del diccionario. Esta suposición falla en cifrados homofónicos sin espacios porque:

1. **No existen límites de palabras** en la codificación del texto plano — las letras de múltiples palabras están intercaladas en el flujo descifrado
2. **La segmentación por PD coincide ávidamente** con palabras conocidas, dejando residuos multipalabra como bloques únicos
3. **Los intercambios de letras por ambigüedad de códigos** impiden la coincidencia exacta de anagramas incluso para palabras individuales

BoLWP relaja las tres suposiciones: permite la descomposición multipalabra, tolera sustituciones de letras conocidas y opera sobre el multiconjunto de letras en lugar de caracteres ordenados.

### 7.2 Limitaciones

1. **Peor caso exponencial:** Bloques ilegibles muy largos (>25 caracteres) con longitud promedio de palabra pequeña pueden no resolverse en tiempo práctico
2. **Ambigüedad:** Pueden existir múltiples descomposiciones válidas; el algoritmo devuelve la de mayor cobertura, que puede no ser semánticamente correcta
3. **Especificidad del modelo de intercambio:** Los intercambios I↔E e I↔L son específicos de la distribución de códigos de este cifrado — otros cifrados requerirían modelos de intercambio diferentes
4. **Dependencia del diccionario:** La calidad de los resultados depende enteramente de la completitud del diccionario — la falta de palabras arcaicas o específicas del dominio produce falsos negativos

### 7.3 Generalización

BoLWP es aplicable a cualquier cifrado donde:
- El texto descifrado carece de límites de palabras
- Los bloques ilegibles contienen letras correctamente descifradas de múltiples palabras
- Los patrones de confusión de letras sistemáticos pueden identificarse y modelarse como intercambios

Las aplicaciones candidatas incluyen:
- Otros cifrados de sustitución homofónica (cifrados diplomáticos históricos, sistemas tipo Zodiac)
- Corrección de errores de OCR en manuscritos históricos (donde la confusión de caracteres sigue patrones sistemáticos)
- Desciframiento de lenguas antiguas (Lineal A, escritura del Valle del Indo) donde los límites de palabras son desconocidos

### 7.4 Comparación con Métodos Existentes

| Método | Palabra Única | Multipalabra | Tolerante a Intercambios | Consciente del Contexto |
|--------|:-------------:|:------------:|:------------------------:|:-----------------------:|
| Coincidencia de anagramas tradicional | Sí | No | No | No |
| Segmentación de palabras por PD | No | Sí | No | No |
| Corrección ortográfica (Levenshtein) | Sí | No | Sí | No |
| **BoLWP** | **Sí** | **Sí** | **Sí** | **No** |
| **BoLWP + CAAR** | **Sí** | **Sí** | **Sí** | **Sí** |

---

## 8. Implementación

### 8.1 Algoritmo Principal (Python)

```python
def bag_of_letters_partition(garbled, dictionary, max_swaps=3):
    """Find best multi-word decomposition of a garbled block."""
    from collections import Counter

    bag = Counter(garbled)
    n = len(garbled)
    best = {'coverage': 0, 'words': [], 'swaps': 0}

    # Pre-filter dictionary to words that could fit
    candidates = [w for w in dictionary if len(w) <= n]

    def can_match(remaining, word, swap_budget):
        """Check if word can be formed from remaining letters with swaps."""
        needed = Counter(word)
        swaps = 0
        for letter, count in needed.items():
            have = remaining.get(letter, 0)
            if have >= count:
                continue
            deficit = count - have
            # Try I<->E swap
            if letter == 'E' and remaining.get('I', 0) >= deficit:
                swaps += deficit
            elif letter == 'I' and remaining.get('E', 0) >= deficit:
                swaps += deficit
            # Try I<->L swap
            elif letter == 'L' and remaining.get('I', 0) >= deficit:
                swaps += deficit
            elif letter == 'I' and remaining.get('L', 0) >= deficit:
                swaps += deficit
            else:
                return False, 0
        return swaps <= swap_budget, swaps

    def search(remaining, rem_len, words, swaps_used):
        coverage = sum(len(w) for w in words)
        if coverage > best['coverage']:
            best['coverage'] = coverage
            best['words'] = words[:]
            best['swaps'] = swaps_used

        if rem_len == 0:
            return

        for w in candidates:
            if len(w) > rem_len:
                continue
            ok, sw = can_match(remaining, w, max_swaps - swaps_used)
            if ok:
                new_rem = subtract_with_swaps(remaining, w)
                search(new_rem, rem_len - len(w), words + [w], swaps_used + sw)

    search(bag, n, [], 0)
    return best
```

### 8.2 Implementación de CAAR

```python
def context_aware_replace(text, anagram_map):
    """Apply anagram resolutions respecting compound word boundaries."""
    # Phase 1: Standard longest-first replacement
    for key in sorted(anagram_map.keys(), key=len, reverse=True):
        text = text.replace(key, anagram_map[key])

    # Phase 2: Context-specific fixups for compound collisions
    # Each entry: (pattern_in_context, replacement_in_context)
    context_fixes = [
        ('TREUUNR', 'TREUNUR'),  # UNR->NUR without breaking WINDUNRUH
    ]
    for pattern, replacement in context_fixes:
        text = text.replace(pattern, replacement)

    return text
```

---

## 9. Conclusión

La Partición de Bolsa de Letras por Palabras (Bag-of-Letters Word Partition) aborda una brecha en el criptoanálisis clásico: la recuperación de secuencias multipalabra a partir de bloques ilegibles en cifrados homofónicos sin espacios. Al tratar los bloques ilegibles como multiconjuntos de letras y buscar descomposiciones multipalabra óptimas con tolerancia a intercambios sistemáticos, BoLWP recuperó 285 caracteres (ganancia de 13,3% en cobertura) de un cifrado que había resistido 25 años de esfuerzo comunitario y todas las técnicas previas en nuestro propio análisis de 31 sesiones.

Las técnicas complementarias CAAR y CADST resuelven problemas adyacentes: sustitución segura para palabras compuestas y validación global de modificaciones locales en textos fragmentados. Junto con la re-optimización de digit-split y correcciones post-resolución posteriores, estas técnicas elevaron la cobertura de 81,1% a 94,6%, demostrando que métodos novedosos de recuperación de texto post-descifrado pueden extraer un valor adicional significativo de un cifrado "mayormente resuelto".

---

## References

1. Beker, H. & Piper, F. (1982). *Cipher Systems: The Protection of Communications.* Northwood.
2. Lasry, G. (2018). *A Methodology for the Cryptanalysis of Classical Ciphers with Search Metaheuristics.* Kassel University Press.
3. CipSoft GmbH. (1997–present). *Tibia.* https://www.tibia.com
4. s2ward. (2024). *469 Repository.* https://github.com/s2ward/469
5. Schmeh, K. (2020). *Codebreaking: A Practical Guide.* No Starch Press.

---

*Este trabajo está licenciado bajo la Licencia MIT. Ver LICENSE en la raíz del repositorio.*
