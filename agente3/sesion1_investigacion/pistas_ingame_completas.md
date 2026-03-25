# Pistas In-Game Completas del 469 (Documentación Consolidada)

> Compilado por Agente 3. Fecha: 2026-03-23.
> Fuente: docs/README-469.md, FINDINGS.md secciones 3, 18, 21, 24.

---

## 1. NPC: A Wrinkled Bonelord (Hellgate)

Guardián de la biblioteca. Sus saludos numéricos aparecen DENTRO de los libros.

### Saludos
```
Saludo 1: 485611800364197          → Encontrado en Libro 31
Saludo 2: 78572611857643646724     → Encontrado en Libros 13, 22, 25, 27, 31, 57
```

### Diálogos clave
| Keyword | Respuesta | Importancia |
|---------|-----------|-------------|
| `books` | "Our books are written in 469, of course you can't understand them." | Confirmación directa |
| `469` | "The language of my kind. Superior to any other language and only to be spoken by entities with enough eyes to blink it." | El lenguaje requiere múltiples ojos |
| `language` | "It heavily relies on mathemagic. Your brain is not suited for the mathemagical processing necessary..." | **Matemagia** es clave |
| `numbers` | "Numbers are essential. They are the secret behind the scenes. If you are a master of mathematics you are a master over life and death." | Matemáticas = vida y muerte |
| `name` | "I'm 486486 and NOT 'Blinky' as some people called me..." | 486486 = 486 repetido. 486/1001=486 exacto |
| `Tibia` | "It's 1, not 'Tibia', silly." | ¿Tibia = 1 en 469? |
| `0` | "Go and wash your eyes for using this obscene number!" | El 0 es obsceno para bonelords |
| `bonelord` | "The term bonelord sticks to us... In our language the name of our race is not fix but a complex formula, and as such it always changes for the subjective viewer." | El nombre de la raza es una fórmula cambiante |

---

## 2. NPC: Knightmare (CipSoft Dev NPC)

```
Cifrado:  3478 67 90871 97664 3466 0 345!
Texto:    BE   A  WIT   THAN  BE   A FOOL
```

### Análisis crítico
- `3478` = BE y `3466` = BE → **Homofónico** (múltiples códigos por palabra)
- `67` = A y `0` = A → Confirma homofonía
- `345` = FOOL → **0.75 dígitos/letra**, IMPOSIBLE para codificación letra-por-letra
- **Conclusión**: Los NPCs podrían usar codificación a nivel de PALABRA, mientras los libros usan parejas de 2 dígitos

### Versiones del crib
- README (autoritativa): `3478 67 90871 97664 3466 0 345!` (24 dígitos)
- Versión anterior: `347867090871097664346600345` (27 dígitos, ceros extra)
- La versión README da **0 soluciones** para sustitución a nivel de letra → refuerza hipótesis de nivel de palabra

---

## 3. Chayenne (Diseñadora de Contenido CipSoft)

Entrevista de 2009:
> Q: "What about the Beholder language?"
> A: "114514519485611451908304576512282177 :) 6612527570584 xD"

**Esta frase aparece en 11 libros diferentes** (2, 9, 11, 20, 28, 32, 36, 38, 42, 64, 67).
Esto PRUEBA que los libros y los diálogos NPC comparten la misma secuencia codificada.

---

## 4. Otros NPCs

### Elder Bonelord / The Evil Eye
```
659978 54764!        → "Let me take a look at you!" (¿?)
653768764!           → "Inferior creatures, bow before my power!" (¿?)
```
- NO encontrados en los libros de Hellgate.

### Avar Tar (NPC mentiroso)
```
29639 46781! 9063376290 3222011 677 80322429 67538 14805394...
```
> Avar Tar: "I know it's rather short, but still, this poem I like best."
- No parece ser 469 verdadero. Avar Tar es conocido por mentir.

### The Gate Keeper (Spirit Grounds)
```
"The nearest you may come to is Zg'!kch of Cthle-ZüuKh'lkrlxchwr."
Player: Zg'!kch → "Really! No need to be rude."
```
- Posible conexión con la fonética del 469.

---

## 5. Encuesta del 15.04.2020

> "When the veils of shrouded truths are lifted, who can stand?"

| Opción | Contenido | Significado |
|--------|-----------|-------------|
| A | Binario | "These aren't the words you're looking for." |
| B | Deepling | "Nonbelievers defy the narrow path to undersea!" |
| **C** | `663 902073 7223 67538 467 80097` | **Sin traducción conocida — ¡469 verdadero!** |

Análisis de Opción C:
- `663`: 0 ocurrencias en libros
- `902073`: 0 ocurrencias en libros
- `467`: **110 ocurrencias** en libros
- `80097`: **1 ocurrencia** en libros
- Los códigos de la encuesta que NO aparecen en libros apoyan la hipótesis de codificación a nivel de palabra para NPCs.

---

## 6. Fórmula de Honeminas (Demona)

Warlocks de Demona tenían un bonelord llamado "honeminas" (único bonelord nombrado en el lore).

```
g[a_,x_] := a g[3,2] + (4,3,1,5,3).(3,4,7,8,4)
e=3m*2g+3p
```

- Producto punto: (4,3,1,5,3)·(3,4,7,8,4) = 12+12+7+40+12 = **83**
- Los vectores como strings: `43153` NO aparece, pero `4315` aparece **14 veces**; `3478` aparece **24 veces**
- Cada vector tiene **5 números** — ¿uno por ojo al "parpadear"?

---

## 7. Facebook Post Oficial de CipSoft

Imagen espejada con pares de números. Cuando se invierte:
- **26/28 pares** siguen la relación lineal perfecta: `R = 0.593 × L + 25.28` (R² = 0.990)
- Coeficiente 0.593 ≈ **3/5** (¡cinco ojos!)
- Intercepción ~25 (¿tamaño del alfabeto - 1?)
- El par que no cuadra: (1280, 625) — el único donde L termina en 0

---

## 8. Libro de la Secret Library

```
74032 45331
```
- Otra vez en pares, con el número izquierdo mayor que el derecho.
- Consistente con el patrón del Facebook post y Honeminas.

---

## 9. Libros de la Paradox Tower (Posible Clave del Cifrado)

### Libro 1 (26 secciones = ¡tamaño del alfabeto!)
```
ljkhbl nilse jfpce ojvco ld
slcld ylddiv dnolsd dd sd
sdcp cppcs cccpc cpsc
awdp cpcw cfw ce
cpvc ev vcemmev vrvf
cp fd vmfpm xcv
```
- 104 caracteres totales.
- Dominado por: c (20%), d (12%), p (11%).
- 5 letras ausentes: g, q, t, u, z.

### Libro 2 (9 filas, 11 secciones)
```
dtjfhg jhfvzk bbliiug bkjjjjjjj xhvuo fffff zkkbk h lbhiovz klhi igbb
```

- **Teoría**: Estos libros podrían ser tablas de búsqueda (lookup tables) para el cifrado.
- Están en el cuarto espejado de la Paradox Tower, creada por el mismo creador del 469.

---

## 10. Matemagia (Paradox Tower Quest)

Las "matemáticas mágicas" enseñadas por el Mad Mage:
```
1 + 1 = 1
1 + 1 = 13
1 + 1 = 49
1 + 1 = 94
```
- Esta secuencia aparece en la secuencia tetranacci.
- La Paradox Tower tiene un teletransporte directo a Hellgate.

### Wydrin NPC
> "Could the language of bonelords be the invention of some madman?"
- Referencia directa al Mad Mage como posible creador del lenguaje.

---

## 11. Matriz de Hellgate

En Hellgate existe una matriz 4×4 de cráneos:
```
[1, 1, 1, 1]
[1, 3, 6, 1]
[1, 1, 4, 1]
[4, 6, 1, 1]
```
- Contiene 4, 6, 1 — nota: contiene los dígitos del "469".
- CipSoft cambió los números de cráneos después de especulación de jugadores.

---

## 12. Kharos Library (Ferumbras Citadel)

```
51595646114145190584521765219727830464879636612527578967212778894388727857261185764217614588952196180031651288899751121615127215196805970
```
- Este libro es una **reorganización por bloques** de un libro de Hellgate.
- 7 subcadenas comunes de 13-24 dígitos en posiciones diferentes.
- Cada OTRO bloque de 10 dígitos de Hellgate aparece en Kharos (patrón alternante).
- **Transposición de bloques**, no un cifrado diferente.

---

## 13. Libro "You Cannot Even Imagine"

> "It was me who assisted the great calculator to assemble the bonelords language."

- **"The great calculator"** es un ser, no una máquina (probablemente A Wrinkled Bonelord).
- El autor se cree que es el Mad Mage.
