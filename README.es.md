> **Idioma / Language:** Español | [English](README.md)

[![DOI](https://zenodo.org/badge/1188959183.svg)](https://doi.org/10.5281/zenodo.19262987)

# Cifra Bonelord 469 de Tibia — RESUELTA (94.6%)

Criptoanálisis computacional del **Lenguaje Bonelord** del MMORPG [Tibia](https://www.tibia.com). **Primera solución conocida** de una cifra de 25 años de antigüedad.

## El Misterio

La Biblioteca de Hellgate en Tibia contiene **70 libros escritos enteramente en secuencias de dígitos** — 11,263 dígitos en total. La comunidad llama a esto la "cifra 469" por el diálogo del Wrinkled Bonelord: *"Our books are written in 469."*

Ninguna solución pública ha existido en más de 25 años de esfuerzo comunitario.

## Solución

| Resultado | Valor |
|-----------|-------|
| **Tipo de cifra** | Sustitución homofónica (98 códigos de 2 dígitos → 22 letras alemanas) |
| **Idioma del texto plano** | Alemán (con vocabulario del alto alemán medio) |
| **Cobertura a nivel de palabras** | **94.6%** (5219/5514 caracteres) |
| **Cobertura a nivel de letras** | **100%** (todos los códigos mapeados) |
| **Códigos mapeados** | 98/100 (los códigos 07 y 32 nunca aparecen en ningún libro) |
| **Sesiones** | 31 sesiones de criptoanálisis sistemático |
| **Contenido** | Inscripción funeraria bonelord (LEICH) — Rey Salzberg, Siervos de Dios, ruinas de piedra antiguas, magia rúnica |

### El Mapeo (v7 — 98 códigos → 22 letras)

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
```

### Frases Clave Decodificadas

```
"TUN DIE REIST EN ER"              (12x) — "Lo que hacen los viajeros, él..."
"IM MIN HEIME DIE URALTE STEIN"   (11x) — "En mi tierra querida, las piedras antiguas"
"TRAUT IST LEICH AN BERUCHTIG"     (9x) — "El de Confianza es un cadáver, el Notorio"
"DEN EN DE REDER KOENIG"          (10x) — "De los del Rey Orador"
"SALZBERG"                         (5x) — "Montaña de Sal" (= Salzburgo)
"ORANGENSTRASSE"                   (3x) — "Calle de la Naranja"
"GOTTDIENER"                       (4x) — "Siervo de Dios"
"WEICHSTEIN"                       (4x) — "Piedra Blanda"
```

### Nombres Propios Confirmados (Resoluciones de Anagramas)

| Forma Cifrada | Resolución | Significado | Patrón |
|---------------|-----------|-------------|--------|
| LABGZERAS | SALZBERG | "Montaña de Sal" (Salzburgo) | anagrama + 1 letra |
| SCHWITEIONE | WEICHSTEIN | "Piedra Blanda" | anagrama + 1 letra |
| AUNRSONGETRASES | ORANGENSTRASSE | "Calle de la Naranja" | anagrama + 1 letra |
| EDETOTNIURG | GOTTDIENER | "Siervo de Dios" | anagrama + 1 letra |
| ADTHARSC | SCHARDT | Topónimo | anagrama + 1 letra |
| HEDEMI/HEDDEMI | HEIME | "Tierra natal" (AAM) | anagrama |

### Nombres Propios Sin Resolver

| Nombre | Frec. | Contexto |
|--------|-------|----------|
| THENAEUT | 7x | "ER THENAEUT ER ALS STANDE NOT" |
| LGTNELGZ | 7x | Siempre emparejado con THENAEUT |
| WRLGTNELNR | 4x | "STEH _ HEL" (permanecer _ luz) |
| NDCE | 9x | "HEHL DIE NDCE FACH" (ocultar el _ compartimiento) |
| HISDIZA | 2x | "NUN AM _ RUNE" (ahora en _ runa) |

## Técnicas Novedosas

Esta investigación produjo tres técnicas criptoanalíticas novedosas, descritas en un [artículo técnico aparte](papers/bag_of_letters/paper_bag_of_letters.es.md):

1. **Partición de Bolsa de Letras (BoLWP)** — Descomposición combinatoria multipalabra de bloques ilegibles con tolerancia sistemática a intercambio de letras. Mayor ganancia en una sesión: +10.1% de cobertura.

2. **Resolución de Anagramas Sensible al Contexto (CAAR)** — Reemplazo de cadenas sensible a límites de frase que evita romper palabras compuestas válidas durante la sustitución de anagramas.

3. **Testing de Digit-Split con Conciencia de Concatenación (CADST)** — Validación global de modificaciones por fragmento en texto cifrado fragmentado, detectando regresiones entre límites invisibles al testing local.

## Estructura del Repositorio

```
.
├── README.md / README.es.md           # Vista general bilingüe
├── LICENSE                            # Licencia MIT
├── CREATORS.md / .es.md               # Media kit para creadores de contenido
├── papers/
│   ├── 469_cipher/                    # Artículo principal (EN/ES) + PDF
│   ├── bag_of_letters/                # Artículo técnico BoLWP (EN/ES) + PDF
│   └── shared/                        # Preámbulo LaTeX compartido
├── data/
│   ├── mapping_v7.json                # EL mapeo (98 códigos → 22 letras)
│   ├── books.json                     # 70 libros como cadenas de dígitos
│   ├── bookcase_mapping.json          # Mapeo libro → estantería
│   └── archive/                       # Versiones históricas del mapeo (v1-v6)
├── scripts/
│   ├── core/                          # Pipeline de descifrado + ataques
│   ├── analysis/                      # Análisis por sesión
│   └── experimental/                  # Hipótesis tempranas
├── docs/
│   ├── INDEX.md                       # Índice maestro de documentación
│   ├── findings.md                    # Registro de investigación de 31 sesiones (7000+ líneas)
│   ├── narrative_translation.md       # Los 70 libros (DE/EN/ES)
│   ├── hellgate_library_guide.md      # Guía de biblioteca para wiki
│   ├── investigation/                 # Investigación in-game y datos NPC
│   └── archive/                       # Datos comunitarios legacy
└── archive/                           # Artefactos de trabajo interno
```

## Inicio Rápido

```bash
# Decodificar los 70 libros con 94.6% de cobertura
python scripts/core/narrative_v3_clean.py
```

## ¿Por Qué Estuvo Sin Resolver 25 Años?

1. **Sustitución homofónica** (98 códigos para 22 letras) derrota el análisis de frecuencia
2. **Sin espacios** en el texto codificado — sin límites de palabras
3. **Texto plano en alemán** — la mayoría de los atacantes asumieron inglés
4. **CipSoft eliminó dígitos** de 37/70 libros para romper la alineación de pares
5. **Texto corto** — 5,515 caracteres únicos es marginal para cracking homofónico a ciegas
6. **Nombres propios anagramados** con +1 letra extra
7. **Pista falsa "Matemagia"** — el diálogo NPC dirige hacia las matemáticas, no al lenguaje

## Licencia

**Licencia MIT** — Usa libremente para cualquier propósito.

Los datos del juego (`books.json`) contienen contenido transcrito por la comunidad de Tibia, propiedad intelectual de CipSoft GmbH. Incluidos con fines de investigación.

Ver [CREATORS.es.md](CREATORS.es.md) para el media kit para creadores de contenido.

## Agradecimientos

- **CipSoft GmbH** por crear y mantener Tibia desde 1997
- **s2ward/469** repositorio con datos de libros transcritos por la comunidad
- **TibiaSecrets** y **Tales of Tibia** por análisis previos

---

*Esta investigación fue conducida de manera independiente. CipSoft GmbH posee toda la propiedad intelectual relacionada con Tibia y su contenido in-game.*

---

## Disclaimer — by kardfon dogon

**No puedo confirmar que el contenido decodificado sea el texto plano real que CipSoft escribio.**

El mapeo pasa todas las pruebas de validacion computacional que le lanzamos: el Indice de Coincidencia confirma aleman + codificacion de 2 digitos (independiente de cualquier mapeo), 164 solapamientos entre libros decodifican con cero inconsistencias, las frecuencias de letras coinciden con el aleman dentro de un 2%, y el mapeo supera las 200 permutaciones aleatorias probadas (p < 0.005). La matematica es solida.

Pero la matematica sola no prueba que CipSoft escribio estas palabras.

### Como llegamos aqui

Los libros de la Biblioteca de Hellgate son 70 secuencias de digitos que totalizan 11,263 digitos. Los tratamos como un **cifrado de sustitucion homofonica**: cada par de dos digitos codifica una de 22 letras alemanas, con multiples codigos por letra (solo la E tiene 20 codigos). El ataque combino:

- **Analisis de frecuencia** para establecer proporciones de codigo-a-letra
- **Cribs de dialogos NPC** (frases conocidas del Wrinkled Bonelord) como anclas para ataques de texto plano conocido
- **Cadenas de solapamiento entre libros** — los libros comparten solapamientos sufijo-prefijo, permitiendonos reconstruir 12 cadenas de los 70 fragmentos
- **Particion de Bolsa de Letras (BoLWP)** — una tecnica novedosa que descompone bloques de letras ilegibles en combinaciones de palabras alemanas validas, tolerando intercambios sistematicos de letras
- **Testing de Digit-Split con Conciencia de Concatenacion** — CipSoft elimino un solo digito de 37/70 libros para romper la alineacion de pares; nosotros buscamos por fuerza bruta la insercion optima para cada uno
- **Resolucion de Anagramas Sensible al Contexto** — los nombres propios estan anagramados con +1 letra extra (LABGZERAS = SALZBERG + A), coincidiendo con el patron conocido de CipSoft (Ferumbras, Vladruc, Dallheim)

### La preocupacion del overfitting

Con 98 codigos mapeados a 22 letras y un corpus de 5,515 caracteres, hay suficientes grados de libertad para que un optimizador determinado *pudiera* forzar texto aleman de apariencia plausible a partir de datos aleatorios. Nuestro 94.6% de cobertura de palabras se mide contra un diccionario aleman — pero el 5.4% restante consiste en clusters de consonantes y nombres propios sin decodificar, no ruido aleatorio. Eso es evidencia de un texto real en aleman arcaico con vocabulario especifico de bonelords... o evidencia de un overfit muy convincente.

### Libros vs NPCs: dos sistemas de cifrado diferentes

Esto es critico y frecuentemente ignorado:

- **Los 70 libros de la biblioteca** usan una **sustitucion homofonica de dos digitos** limpia — pares de digitos se mapean a letras, sin espacios, sin puntuacion. Esto es lo que resolvimos.
- **El dialogo de los NPCs** (el poema de Avar Tar, las frases de los Evil Eyes) usa una **codificacion completamente diferente** — grupos de digitos de longitud variable separados por espacios, con patrones que no coinciden con el cifrado de los libros en absoluto. El poema de Avar Tar tiene grupos como `29639`, `46781`, `9063376290` — estos NO son pares de dos digitos.

Resolvimos los libros. NO hemos resuelto el cifrado de los NPCs. Pueden usar el mismo lenguaje subyacente pero un esquema de codificacion diferente, o pueden ser sistemas completamente separados. **Hasta que alguien descifre la codificacion NPC de forma independiente y encuentre que es consistente con la solucion de los libros, los dos sistemas permanecen desvinculados.**

### Lo que probamos in-game

Volvi a Tibia despues de años y probe palabras clave decodificadas (`SALZBERG`, `RUNE`, `STEIN`, `LEICH`, `GOTTDIENER`, `SCHARDT`) con el Wrinkled Bonelord. **Sin resultados.** Ningun dialogo nuevo, ninguna reaccion, nada. Esto es extraño, pero no necesariamente refuta la solucion — mi teoria es que el lenguaje *escrito* de los bonelords y su lenguaje *hablado* pueden ser sistemas fundamentalmente diferentes. Los bonelords se comunican parpadeando sus ojos en patrones, lo que podria explicar por que el dialogo hablado del NPC usa una codificacion completamente diferente a la de los libros de la biblioteca. Los libros son registros *escritos* — quiza en un registro formal o arcaico que no se mapea a como un bonelord vivo "habla" a traves de parpadeos de ojos.

### En que puede ayudar la comunidad

- **Avar Tar en Edron** — Este NPC recita un poema en 469 y podria ser critico para obtener mas datos. Su poema usa grupos de digitos de longitud variable (no pares de dos digitos como los libros), sugiriendo una capa de codificacion diferente. Descifrar su poema de forma independiente y encontrar consistencia con la narrativa de los libros seria la prueba definitiva.
- **Referencia cruzada con el lore de Tibia** — Aparecen "King Salzberg", "Orangenstrasse", "Weichstein" o "Gottdiener" en algun otro lugar del juego? Alguna referencia en la wiki, algun dialogo NPC, algun libro fuera de Hellgate?
- **Mas textos cifrados** — Hay textos codificados en 469 fuera de Hellgate? Isle of Kings? Ferumbras Citadel? Mientras mas datos, mas fuerte (o mas debil) se vuelve la solucion.
- **Hablantes nativos de aleman** — El texto decodificado parece ser alto aleman medio. Un hablante nativo o un especialista en MHG revisando el texto podria confirmar si se lee como aleman arcaico coherente o como ruido estadistico que casualmente parece palabras.

La evidencia estadistica dice que este mapeo es real. El texto decodificado se lee como aleman arcaico con una narrativa funeraria coherente. Pero he pasado suficientes horas mirando estos digitos para saber que el reconocimiento de patrones es una droga potente, y el cerebro humano es perturbadoramente bueno encontrando significado en el ruido.

Me retire de Tibia hace años y volvi para cumplir mi sueño de llegar a nivel 100. Encontre un juego completamente diferente, uno que ya no me motiva a jugar. Pero este enigma de los bonelords siempre me causo intriga, y seguire a disposicion de la comunidad para seguir explorando.

Solo espero que esta no sea otra puerta como la del nivel 999.
