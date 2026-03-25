# Estado Actual de la Investigación del Cifrado 469 (Bonelord Language)

> Compilado por Agente 3. Fecha: 2026-03-23.
> Fuente: Repositorio `tibia-research`, `FINDINGS.md`, `README.md`, `agente2/FINDINGS_SESSION3.md`, `data/`, `docs/`.

---

## 1. ¿Qué es el 469?

El **lenguaje 469** (o "Bonelord Language") es un misterio no resuelto del MMORPG Tibia que lleva 25+ años sin solución. Consiste en **70 libros escritos completamente en secuencias numéricas** ubicados en la biblioteca de Hellgate, más diálogos de NPCs que también usan números.

- Total de dígitos: **11,263** distribuidos en 70 libros.
- Los libros van de **35 dígitos** (Libro 26) a **294 dígitos** (Libro 10).
- También existen copias en Isle of Kings y Kharos Library.

---

## 2. Tipo de Cifrado Identificado

### CONFIRMADO: Sustitución Homofónica de 2 Dígitos → Texto en Alemán

| Evidencia | Detalle |
|-----------|---------|
| Índice de Coincidencia (IC) | IC a nivel de parejas = **1.73** (alemán esperado: 1.72) — coincidencia casi perfecta |
| Bigramas | 17 de los 25 bigramas más frecuentes del texto decodificado coinciden con los bigramas alemanes |
| Palabras encontradas | EINEN (14,860x sobre el azar), EINE (735x), SIND (653x), RUNE (163x), DER (66x), ICH (44x), IST (22x) |
| Consistencia CipSoft | CipSoft es una empresa alemana de Regensburg |

### El mapeo actual (v4): 97 de 100 códigos asignados a 21 letras

```
E (20 códigos): 95 56 19 26 76 01 41 30 86 67 27 03 09 17 29 49 39 74 37 69
N (10 códigos): 60 11 14 48 58 13 93 53 73 90
I  (8 códigos): 21 15 46 71 65 16 50 24
S  (7 códigos): 92 91 52 59 12 23 05
T  (6 códigos): 88 78 64 75 81 98
D  (6 códigos): 45 42 47 63 28 02
R  (6 códigos): 72 51 55 08 68 10
A  (5 códigos): 31 85 35 89 66
H  (4 códigos): 06 00 57 94
U  (4 códigos): 61 43 70 44
O  (4 códigos): 99 82 25 79
M  (3 códigos): 04 54 40
G  (3 códigos): 80 97 84
L  (2 códigos): 34 96
W  (2 códigos): 36 87
K  (2 códigos): 22 38
C  (1 código):  18
F  (1 código):  20
B  (1 código):  62
Z  (1 código):  77
V  (1 código):  83
Nunca aparecen: 07, 32
Sin asignar:    33 (1x, probablemente W)
```

---

## 3. Estructura de los Libros

### Los 70 libros son fragmentos de UN SOLO texto continuo

- **164 solapamientos** sufijo-prefijo de ≥10 dígitos.
- **31 relaciones de contención** (libros enteros dentro de otros).
- El mayor solapamiento: Libro 36 → Libro 11 = **279 dígitos** (¡de 286!).
- Los 70 libros se ensamblan en un **superstring de 5,902 dígitos**.
- ~55% del texto total es duplicado.

### 12 cadenas reconstruidas

Los libros se encadenan en 12 grupos + 12 libros aislados. Las dos cadenas más importantes:
- **Cadena 0** (8 libros, 291 chars): Contiene URALTE STEINE, NO contiene KOENIG.
- **Cadena 2** (7 libros, 283 chars): Contiene KOENIG, NO contiene URALTE.
- Estas cadenas cubren **secciones diferentes** de la inscripción.

---

## 4. Texto Parcialmente Decodificado

### Fragmentos legibles clave

```
HIER TAUTR IST EILCHANHEARUCHTIG     → "Aquí Tautr es [el] Eilchanhearuchtig"
EINER SEIN EDETOTNIURGS               → "uno [es] su Edetotniurgs"
IN HEDEMI DIE URALTE STEINEN          → "en Hedemi las piedras antiguas"
ADTHARSC IST SCHAUN                   → "Adtharsc es — ¡mira!"
TIUMENGEMI ORT ENGCHD KELSEI          → "lugar Tiumengemi Engchd Kelsei"
SCHWITEIONE IST                       → "[la] Schwiteione es"
DER KOENIG LABGZERAS                  → "el Rey Labgzeras"
RUNE UNTER                            → "runa debajo"
WIR UND...                            → "nosotros y..."
```

### 11+ Nombres propios descubiertos (NINGUNO existe en la wiki de Tibia)

| Nombre | Contexto | Notas |
|--------|----------|-------|
| **TAUTR** | Sujeto central, "ist Eilchanhearuchtig" | Persona o entidad |
| **EILCHANHEARUCHTIG** | Título/descriptor de TAUTR | Palabra compuesta, ¿alemán antiguo? |
| **EDETOTNIURGS** | Atributo de TAUTR, contiene TOTNIURG | TOTNIURG invertido = GRUIN+TOT (ruina+muerte) |
| **LABGZERAS** | "KOENIG LABGZERAS" = Rey | No coincide con ninguno de los ~68 reyes tibiaques conocidos |
| **HEDEMI** | Lugar con "uralte Steinen" | TibiaWiki lo reconoce como término de búsqueda |
| **ADTHARSC** | En HEDEMI, "ist schaun" | Entidad o lugar desconocido |
| **KELSEI** | Después de ENGCHD | TibiaWiki lo reconoce |
| **TIUMENGEMI** | "ORT" (lugar) | Nombre de ubicación |
| **SCHWITEIONE** | 10x en el texto | ¿Nombre de la raza bonelord? |
| **LABRNI** | Después de la descripción de TAUTR | Persona o lugar |
| **GEVMT** | "SEI GEVMT WIE TUN" | Desconocido |

---

## 5. Pistas Clave In-Game

### Diálogos del NPC "A Wrinkled Bonelord"
- Dice que el 469 es "superior a cualquier otro lenguaje".
- Requiere "matemagia" y "suficientes ojos para parpadearlo".
- El nombre de su raza "no es fijo sino una fórmula compleja, siempre cambia".
- El 0 es "obsceno" para los bonelords.
- Su nombre personal es 486486 (486 repetido).

### Crib de Knightmare (texto plano conocido)
```
Cifrado:  3478 67 90871 97664 3466 0 345!
Texto:    BE   A  WIT   THAN  BE   A FOOL
```
- Codificación a **nivel de palabra** (345 = FOOL con 0.75 dígitos/letra, imposible a nivel de letra).
- Posiblemente los NPCs codifican a nivel de palabra pero los libros a nivel de pareja de dígitos.

### Fórmula de Honeminas (Demona)
```
g[a_,x_] := a g[3,2] + (4,3,1,5,3).(3,4,7,8,4)
```
- Producto punto = **83**.
- `3478` aparece **24 veces** en los libros.

### Facebook Post de CipSoft
- Imagen espejada con pares de números que siguen la relación lineal: `R = 0.593 * L + 25.28` (R² = 0.990).
- Coeficiente 0.593 ≈ 3/5 (¡cinco ojos!).

### Encuesta 2020
- Respuesta C: `663 902073 7223 67538 467 80097` — sin traducción conocida.

### Libros de la Paradox Tower
- Un libro tiene **26 secciones** (coincide con el tamaño del alfabeto).
- Letras mezcladas, podrían ser tablas de búsqueda para el cifrado.

---

## 6. Problemas Abiertos Críticos (Sesión 3, Agente 2)

### 20 códigos "gap-only" (nunca aparecen en palabras alemanas confirmadas)
- **[64]=T (124x)**, [97]=G (58x), [80]=G (79x), [96]=Z (53x), [70]=U (48x)
- **700+ ocurrencias** que NUNCA aparecen en ninguna palabra alemana reconocida.
- Son las asignaciones más sospechosas de estar mal.

### Desequilibrios de frecuencia
- Sobre-representados: N(+2.5%), I(+3.0%), R(+1.8%), D(+1.8%)  
- Sub-representados: M(-1.4%), O(-1.1%), B(-1.4%), F(-1.3%), P(-0.8%), V(-0.8%)
- P y V tienen **0 ocurrencias** — ¿La inscripción genuinamente evita estas letras o sus códigos están mal asignados?

### DERKOENIG siempre seguido por "LAL"
- El patrón `DERKOENIGLAL` siempre se repite, con dos variantes a continuación.
- "LAL" podría ser parte de un nombre propio (LABGZERAS).

### HEARUCHTIG usa códigos idénticos en los 8 libros donde aparece
- Si U(pos4)→I, daría HEA**RICHTIG** ("correcto" en alemán).
- Pero [61]=U está firmemente confirmado con 121 usos en URALTE.

---

## 7. Metodología Utilizada

1. **Análisis estadístico**: IC, frecuencias, matriz de transición, entropía condicional.
2. **Cripto-análisis con texto plano conocido (cribs)**: Knightmare NPC, Chayenne, Wrinkled Bonelord.
3. **Asignación progresiva en 14+ tiers**: Desde frecuencias simples hasta patrones de palabras.
4. **Ensamblaje narrativo**: Superstring de 5,902 dígitos + votación por consenso.
5. **Segmentación de palabras con DP** (programación dinámica): 67.2% del texto se parsea como alemán.
6. **Simulated Annealing**: Probado pero NO converge en textos tan cortos con cifrado homofónico de 98 símbolos.

---

## 8. Recursos del Repositorio

| Archivo | Contenido |
|---------|-----------|
| `data/books.json` | Los 70 libros como cadenas de dígitos |
| `data/final_mapping_v4.json` | El mapeo actual de 97 códigos → 21 letras |
| `data/decoded_text.txt` | Texto decodificado por libro y ensamblado por piezas |
| `data/master_text.txt` | Superstring de 5,902 dígitos |
| `FINDINGS.md` | Log completo de investigación (5,000 líneas, 35 secciones) |
| `docs/README-469.md` | Pistas de la comunidad, NPCs, Facebook post, Paradox Tower |
| `docs/01-books.md` | Transcripción de los 72 libros (Hellgate + IoK + Kharos) |
| `scripts/core/` | 25+ scripts que produjeron resultados |
| `scripts/experimental/` | 79+ scripts exploratorios |
| `agente2/` | 40 scripts de análisis + hallazgos de sesión 3 |
