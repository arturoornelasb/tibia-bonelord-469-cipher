> **Idioma / Language:** Español | [English](README.md)

# Cifra Bonelord 469 de Tibia — RESUELTA (94.4%)

Criptoanálisis computacional del **Lenguaje Bonelord** del MMORPG [Tibia](https://www.tibia.com). **Primera solución conocida** de una cifra de 25 años de antigüedad.

## El Misterio

La Biblioteca de Hellgate en Tibia contiene **70 libros escritos enteramente en secuencias de dígitos** — 11,263 dígitos en total. La comunidad llama a esto la "cifra 469" por el diálogo del Wrinkled Bonelord: *"Our books are written in 469."*

Ninguna solución pública ha existido en más de 25 años de esfuerzo comunitario.

## Solución

| Resultado | Valor |
|-----------|-------|
| **Tipo de cifra** | Sustitución homofónica (98 códigos de 2 dígitos → 22 letras alemanas) |
| **Idioma del texto plano** | Alemán (con vocabulario del alto alemán medio) |
| **Cobertura a nivel de palabras** | **94.4%** (5204/5515 caracteres) |
| **Cobertura a nivel de letras** | **100%** (todos los códigos mapeados) |
| **Códigos mapeados** | 98/100 (los códigos 07 y 32 nunca aparecen en ningún libro) |
| **Sesiones** | 30 sesiones de criptoanálisis sistemático |
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

Esta investigación produjo tres técnicas criptoanalíticas novedosas, descritas en un [artículo técnico aparte](docs/paper_bag_of_letters.es.md):

1. **Partición de Bolsa de Letras (BoLWP)** — Descomposición combinatoria multipalabra de bloques ilegibles con tolerancia sistemática a intercambio de letras. Mayor ganancia en una sesión: +10.1% de cobertura.

2. **Resolución de Anagramas Sensible al Contexto (CAAR)** — Reemplazo de cadenas sensible a límites de frase que evita romper palabras compuestas válidas durante la sustitución de anagramas.

3. **Testing de Digit-Split con Conciencia de Concatenación (CADST)** — Validación global de modificaciones por fragmento en texto cifrado fragmentado, detectando regresiones entre límites invisibles al testing local.

## Estructura del Repositorio

```
.
├── README.md / README.es.md           # Vista general bilingüe
├── LICENSE                            # BUSL-1.1 (libre para individuos/academia/sin fines de lucro)
├── COMMERCIAL.md / .es.md             # Participación comercial
├── CREATORS.md / .es.md               # Guía para creadores de contenido
├── TERMS.md / .es.md                  # Términos de uso
├── FINDINGS.md                        # Registro de investigación de 30 sesiones (7000+ líneas)
├── data/
│   ├── mapping_v7.json                # EL mapeo (98 códigos → 22 letras)
│   ├── books.json                     # 70 libros como cadenas de dígitos
│   ├── bookcase_mapping.json          # Mapeo libro → estantería
│   └── archive/                       # Versiones históricas del mapeo (v1-v6)
├── scripts/
│   ├── README.md                      # Guía de organización de scripts
│   ├── core/                          # Pipeline de descifrado + ataques
│   ├── analysis/                      # Análisis por sesión
│   └── experimental/                  # Hipótesis tempranas
├── docs/
│   ├── INDEX.md                       # Índice maestro de documentación
│   ├── paper_469_cipher.md / .es.md   # Artículo de investigación (EN/ES)
│   ├── paper_bag_of_letters.md / .es.md # Artículo técnico BoLWP (EN/ES)
│   ├── narrative_translation.md       # Los 70 libros (DE/EN/ES)
│   ├── hellgate_library_guide.md      # Guía de biblioteca para wiki
│   ├── roadmap_ingame.md              # Hoja de ruta de verificación in-game
│   ├── npc-research.md                # Investigación de diálogos NPC
│   └── archive/                       # Datos comunitarios legacy
└── agente3/                           # Fases de investigación en español
```

## Inicio Rápido

```bash
# Decodificar los 70 libros con 94.4% de cobertura
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

**Business Source License 1.1 (BUSL-1.1)**

- **Gratis para:** individuos, académicos, investigadores, organizaciones sin fines de lucro
- **Uso comercial:** requiere acuerdo de participación (ver [COMMERCIAL.es.md](COMMERCIAL.es.md))
- **Obligación de contribución:** las mejoras deben compartirse (ver [TERMS.es.md](TERMS.es.md))
- **Fecha de cambio:** 2030-03-24 (se convierte automáticamente a AGPL-3.0)
- **Datos del juego:** propiedad intelectual de CipSoft GmbH, incluidos bajo uso justo para investigación

Ver [LICENSE](LICENSE) para los términos completos.

**Creadores de contenido:** Puedes monetizar libremente — no se necesita licencia. Ver [CREATORS.es.md](CREATORS.es.md) para guías de atribución y media kit.

## Agradecimientos

- **CipSoft GmbH** por crear y mantener Tibia desde 1997
- **s2ward/469** repositorio con datos de libros transcritos por la comunidad
- **TibiaSecrets** y **Tales of Tibia** por análisis previos

---

*Esta investigación fue conducida de manera independiente. CipSoft GmbH posee toda la propiedad intelectual relacionada con Tibia y su contenido in-game.*
