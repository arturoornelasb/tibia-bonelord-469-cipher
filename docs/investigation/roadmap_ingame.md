> **Note:** This document is written in Spanish (the primary investigator's working language). Below is a brief English summary.

## English Summary

In-game verification roadmap for the decoded Bonelord 469 cipher (94.6% coverage, 31 sessions). This document lists:

- **Confirmed proper nouns** (SALZBERG, WEICHSTEIN, ORANGENSTRASSE, GOTTDIENER, SCHARDT) with specific NPCs and locations to investigate in-game
- **Unsolved proper nouns** (THENAEUT, LGTNELGZ, WRLGTNELNR, NDCE, HISDIZA) requiring field research
- **Key phrases and locations** to verify against NPC dialogues
- **Priority-ordered investigation routes** through Tibia's game world
- **NPC dialogue tests** with decoded keywords

---

# Roadmap de Investigación In-Game — Cifra 469 Bonelord

**Estado actual:** 94.6% del texto descifrado (5219/5514 caracteres). 100% decodificado a nivel de letra.
**Fecha:** 2026-03-25 | **Sesiones completadas:** 31

---

## 1. Pistas del Texto Descifrado

El texto descifrado revela nombres propios, lugares y conceptos que deben verificarse dentro del juego.

### Nombres Propios Confirmados (anagramas resueltos)

| Cifrado | Descifrado | Significado | Investigar en juego |
|---------|-----------|-------------|---------------------|
| LABGZERAS | **SALZBERG** | "Montana de Sal" (= Salzburg, Austria) | Buscar referencia a Salzburg/montanas de sal en NPCs y libros |
| SCHWITEIONE | **WEICHSTEIN** | "Piedra blanda" — posible nombre de la raza bonelord | Preguntar al Wrinkled Bonelord sobre `weichstein`, `race name` |
| AUNRSONGETRASES | **ORANGENSTRASSE** | "Calle de los Naranjos" — aparece 10x en el texto | Buscar calles con nombre en ciudades de Tibia |
| EDETOTNIURG | **GOTTDIENER** | "Servidor de Dios" — titulo religioso, 6x | Probar con NPCs religiosos: Cipfried, templos |
| ADTHARSC | **SCHARDT** | Nombre de lugar + A | Buscar locaciones similares |
| HEDDEMI | **HEIME** | "Hogar/patria" + DD, 11x "IM MIN HEIME" | El narrador tiene un hogar — buscar locaciones bonelord antiguas |

### Nombres Propios Sin Resolver

| Nombre | Frecuencia | Contexto | Que buscar |
|--------|-----------|----------|------------|
| **THENAEUT** | 7x | "ER THENAEUT ER ALS STANDE NOT" | Posible titulo o rango. Probar como keyword con NPCs |
| **LGTNELGZ** | 7x | Siempre junto a THENAEUT | Podria ser otro anagrama — probar variantes |
| **WRLGTNELNR** | 4x | "STEH WRLGTNELNR HEL" | Nombre propio largo, posiblemente un lugar |
| **NDCE** | 9x | "HEHL DIE NDCE FACH" | Un objeto o lugar oculto ("FACH" = compartimento) |
| **HISDIZA** | 2x | "NUN AM HISDIZA RUNE" | Lugar donde hay runas |
| **IGAA** | 4x | "TUT IGAA ER GIGE" | Posible verbo o nombre MHG |
| **OWI** | 4x | "GODES DA SIE OWI RUNE" | Conectado a Dios y runas |
| **CHN** | 7x | "IN CHN SER ER SCE AUS" | Posible abreviatura o nombre truncado |

### Frases Clave Repetidas (Narrativa Central)

| Frase alemana | Traduccion | Frecuencia | Implicacion para investigacion |
|--------------|-----------|-----------|-------------------------------|
| TUN DIE REIST EN ER | "Hacen los viajeros de el" | 12x | Los bonelords hablan de "viajeros" — aventureros? |
| IM MIN HEIME DIE URALTE STEIN | "En mi hogar las piedras antiguas" | 11x | Piedras antiguas en el hogar bonelord |
| DEN EN DE REDER KOENIG | "De los del Rey orador" | 10x | Rey SALZBERG es un orador/legislador |
| TRAUT IST LEICH AN BERUCHTIG | "El fiel es cadaver, notorio" | 9x | Muerte de un ser confiable |
| ER SO DASS TUN DIE REIST | "El asi que hacen los viajeros" | 9x | Patron narrativo central |
| HEL WI ND UNRUH FINDEN NEIGT | "Luz como viento inquietud encontrar inclina" | 7x | Concepto mistico de busqueda |
| GODES DA SIE OWI RUNE MANIER | "De Dios que ellos OWI runa manera" | 4x | Runas divinas |

---

## 2. Locaciones a Visitar (Prioridad)

### PRIORIDAD CRITICA

#### A. Hellgate Library (bajo Ab'Dendriel)
**Ruta:** Ab'Dendriel depot underground > Shadow Caves (NW) > 2 pisos abajo > sur y este > puerta Hellgate (Key 3012)

**Tareas:**
- [ ] **Verificar transcripciones**: Comparar los 71 libros del archivo `Hellgate_Library.txt` con los libros in-game. CipSoft podria haberlos actualizado en parches recientes
- [ ] **Contar libros exactos**: El archivo tiene #1-#71 pero books.json tiene 70 entradas. Verificar si hay 70 o 71 libros fisicos
- [ ] **Buscar libros nuevos**: Podrian haber agregado libros en actualizaciones recientes
- [ ] **Hablar con A Wrinkled Bonelord** (ver seccion NPCs abajo)
- [ ] **Fotografiar/documentar** la distribucion de los estantes (40 estantes documentados)
- [ ] **Buscar objetos interactivos** en la biblioteca que no sean libros

#### B. Paradox Tower (cerca de Kazordoon)
**Tareas:**
- [ ] **Sala espejo**: Examinar los libros de la sala espejada — pueden contener textos 469 no documentados
- [ ] **The Mad Mage / A Prisoner**: Probar keywords decodificados (`salzberg`, `runen`, `gottdiener`, `weichstein`, `469`, `bonelord`)
- [ ] **Teletransporte a Hellgate**: Verificar que el teleport directo Paradox Tower > Hellgate sigue activo
- [ ] **Numero unico**: El Mago Loco da un numero unico a cada jugador ("el secreto de las matemagicias"). Documentar que numero da y analizar su relacion con la cifra

#### C. Demona
**Tareas:**
- [ ] **Formula de Honeminas**: Releer "The Honeminas Formula" in-game. Contiene `(4,3,1,5,3)*(3,4,7,8,4)` — donde 3478 probablemente = "BONELORD"
- [ ] **5 libros en blanco**: Zhandramon tiene 5 libros blancos titulados "History of the Ancients" — verificar si siguen en blanco o fueron actualizados
- [ ] **Hablar con Zhandramon**: Keywords: `honeminas`, `formula`, `bonelord`, `ancient`, `469`
- [ ] **Hablar con Danae**: Keywords: `bonelord`, `honeminas`, `history`, `ancient`

### PRIORIDAD ALTA

#### D. Isle of Kings
- [ ] **Libro identico**: Confirmar que la biblioteca tiene un libro identico a Hellgate Book 35. Documentar ubicacion exacta
- [ ] **Otros textos 469**: Buscar mas libros numericos en la isla

#### E. Ab'Dendriel (sobre Hellgate)
- [ ] **Eroth** (lider Cenath): Keywords `hellgate`, `bonelord`, `ancient`, `library`, `underground`
- [ ] **Elathriel**: Keywords similares
- [ ] **Buscar referencias a "las criaturas de abajo"** en dialogos elficos

#### F. Ferumbras Citadel / Kharos
- [ ] **Texto 469**: Confirmar existencia de texto 469 con promedio numerico coincidente
- [ ] **Documentar el texto completo** y comparar con los libros de Hellgate

### PRIORIDAD MEDIA

#### G. Thais
- [ ] **Inscripcion antigua bajo Thais**: Ancient Temple > piso -2 > usar Dead Explorer en inscripcion > obtener Blurred Transcript
- [ ] **King Tibianus**: Probar `salzberg`, `ancient king`, `bonelord king`, `labgzeras`
- [ ] **Noodles**: Probar frases decodificadas nuevas (ver seccion NPCs)

#### H. Edron
- [ ] **Wyrdin** (Ivory Towers): Murmura sobre el lenguaje bonelord. Keywords: `469`, `madman`, `cipher`, `formula`
- [ ] **Zoltan**: Keywords sobre magia bonelord

#### I. Kazordoon
- [ ] **Emperor Kruzak**: `bonelord`, `hellgate`, `ancient`
- [ ] **Lokur**: Recitar Poema de Beregar, buscar conexiones con texto descifrado
- [ ] **Kawill** (Geomancers): Conocimiento de estructuras subterraneas

---

## 3. NPCs — Protocolo de Interrogacion

### Protocolo estandar para CADA NPC:
```
1. hi / hello
2. bonelord
3. 469
4. language / ancient language
5. hellgate
6. library
7. ancient / uralte
8. rune / runen
9. stone / steinen
10. salzberg
11. king / koenig
12. schrat / forest demon
13. gottdiener / god servant
14. weichstein
15. orangenstrasse
```

### A Wrinkled Bonelord (MAXIMA PRIORIDAD)

Keywords ya probados y documentados:
`hi, job, librarian, library, books, 469, language, numbers, mathemagic, name, bonelord, old, race, eyes, city, wars, god, 0, death, ab'dendriel, tibia, minotaurs, cyclops, humans, elves, orcs, excalibug, bye`

**Keywords nuevos a probar (de texto descifrado):**

| Keyword | Razon | Expectativa |
|---------|-------|-------------|
| `salzberg` | Rey mencionado 10x en texto | Posible respuesta sobre su historia |
| `weichstein` | Posible nombre de raza bonelord | Podria confirmar/negar |
| `orangenstrasse` | Lugar mencionado 10x | Posible locacion bonelord |
| `schrat` | Demonio forestal en el texto | Criatura conocida por bonelords? |
| `gottdiener` | "Servidor de Dios" 6x | Concepto religioso bonelord |
| `rune` / `runen` | Runas mencionadas 8x | Conexion con magia runica |
| `stone` / `steinen` | "Piedras antiguas" 11x | Las piedras de su hogar |
| `king` / `koenig` | Rey SALZBERG | Monarquia bonelord |
| `heime` | "Hogar" 11x | Su antigua ciudad |
| `leich` | "Cadaver" 9x | El muerto del poema |
| `traut` / `trusted` | "El fiel" 9x | Sujeto principal del texto |
| `thenaeut` | Nombre propio 7x | Personaje desconocido |
| `ancient stones` | Frase clave | Reaccion a frase decodificada |
| `1` (el numero) | "It's 1, not 'Tibia'" | Expandir sobre por que el mundo es "1" |
| `formula` | Mathemagics | Conexion con Honeminas |
| `hisdiza` | Lugar de runas | Nombre propio misterioso |
| Secuencias de digitos de los libros | Hablarle en su idioma | Posible respuesta oculta |

### Avar Tar (NE de Edron)

**Verificar:**
- [ ] `4378` vs `3478` en su poema — es mentira deliberada o pista?
- [ ] Probar: `poem`, `469`, `bonelord`, `number`, `salzberg`, `cipher`
- [ ] Decodificar su poema con nuestro mapping v7 y verificar si tiene sentido

**Decodificacion de su poema:**
```
29639 46781! 9063376290 3222011 677 80322429 67538 14805394
6880326 677 63378129 337011 72683 149630 4378! 453 639 578300
986372 2953639!
```
Nota: Este poema usa espacios (a diferencia de los libros). Decodificar con v7 tratando cada segmento como grupo de pares.

### Noodles (Perro Real, Thais)

Respuestas documentadas:
- BARK: `gottdiener`, `godes`
- SNIFF: `thenaeut`, "ancient stones", "runes of the forest demon"
- WIGGLE: `bone`, `bonelord`, `book`

**Nuevos keywords a probar:**
- [ ] `weichstein`, `salzberg`, `orangenstrasse`
- [ ] `hechelt` (jadear/oracionar), `hehl` (ocultamiento)
- [ ] `windunruh` (desasosiego del viento)
- [ ] `hisdiza`, `lgtnelgz`, `wrlgtnelnr`
- [ ] "the king of Salzberg speaks" / "der koenig salzberg reder"
- [ ] `oil`, `anointing`, `sand`

### Knightmare (NPC de evento)
- [ ] Hablarle la palabra "Excalibug" codificada en 469
- [ ] Probar secuencia `3478` directamente
- [ ] Keywords: `bonelord`, `469`, `cipher`, `language`

---

## 4. Verificaciones Criticas

### A. Transcripciones de Libros
Los libros fueron transcritos manualmente por la comunidad. Errores de transcripcion afectan todo el descifrado.

**Verificar:**
- [ ] Cada libro in-game vs `Hellgate_Library.txt` — un solo digito mal cambia todo
- [ ] Libros 49 (68% cobertura) y 4 (69% cobertura) tienen la peor cobertura — posibles errores de transcripcion
- [ ] Book 49 contiene el unico caracter `?` (codigo no mapeado) — verificar ese digito in-game
- [ ] Verificar si los libros tienen titulos que no se documentaron (los titulos numericos como "5611457278" podrian ser parte del texto)

### B. Libros Fuera de Hellgate
Se sabe que existen textos 469 fuera de Hellgate:

| Locacion | Que buscar |
|----------|-----------|
| Isle of Kings | Libro identico a Book 35 |
| Ferumbras Citadel / Kharos | Texto 469 con mismo promedio numerico |
| Demona | Formula de Honeminas (contiene 3478) |
| Paradox Tower sala espejo | Libros potencialmente en 469 |
| Bonelord spawns | Criatura speech: "653768764!", "659978 54764!" |

### C. NPC Speech en 469
Decodificar con mapping v7:

| NPC | 469 Text | Decodificacion v7 |
|-----|---------|-------------------|
| Evil Eye | `653768764` | Decodificar y verificar |
| Elder Bonelord | `659978 54764` | Decodificar y verificar |
| Knightmare | `3478 67 90871 97664 3466 0 345` | 3478 -> posible "BONELORD" |
| Avar Tar | Poema completo (ver arriba) | Decodificar con v7 |

### D. Patches y Actualizaciones
- [ ] Revisar patch notes de Tibia de los ultimos 2 anos para cambios en Hellgate
- [ ] Verificar si el 25th Anniversary (2022) cambio algo en la biblioteca
- [ ] Buscar si CipSoft ha dado pistas nuevas sobre 469 en comunicados recientes

---

## 5. Hipotesis para Verificar In-Game

### Hipotesis 1: ORANGENSTRASSE es un lugar fisico en Tibia
El texto menciona "GEH EN ORANGENSTRASSE" (ir a Orangenstrasse) 10 veces. Podria ser:
- Una calle literal en alguna ciudad
- Un nombre interno de CipSoft para una zona
- Una referencia a la cultura alemana (CipSoft esta en Regensburg)
**Accion:** Buscar calles con nombre en todas las ciudades de Tibia

### Hipotesis 2: WEICHSTEIN = nombre de raza bonelord
"Piedra blanda" aparece con EID (juramento) y WARD (se convirtio). El Wrinkled Bonelord dice que su nombre de raza "no es fijo sino una formula compleja".
**Accion:** Preguntar al Wrinkled Bonelord `weichstein`

### Hipotesis 3: SCHRAT es una criatura en Tibia
"Demonio forestal" — los Schrat aparecen en folklore germanico.
**Accion:** Buscar en TibiaWiki si existe criatura "Schrat" o "Waldschrat". Verificar en zonas boscosas.

### Hipotesis 4: KOENIG SALZBERG es un rey bonelord historico
El texto habla de un "Rey Salzberg" como orador/legislador. No coincide con ninguno de los ~68 reyes conocidos de Tibia.
**Accion:** Buscar "Salzberg" en TibiaWiki. Preguntar a NPCs historicos.

### Hipotesis 5: Las "URALTE STEINEN" son objetos fisicos in-game
"Piedras antiguas" aparece 11x. Podrian ser:
- Los megaliths/dolmens que se ven en varias zonas
- Las piedras runicas de la Paradox Tower
- Los obeliscos de varias quest areas
**Accion:** Documentar todos los objetos de piedra antigua en zonas bonelord

### Hipotesis 6: HISDIZA es un lugar accesible
"NUN AM HISDIZA RUNE" (ahora en HISDIZA runa). Podria ser un anagrama.
- HISDIZA -> DASHIZI? DIZHIAS?
- Probar anagramas: SHADIZ, DISHAZ, ZAHIDS...
**Accion:** Intentar resolver como anagrama y buscar el resultado en TibiaWiki

### Hipotesis 7: El texto es un poema funerario bonelord
La estructura repetitiva (12x "TUN DIE REIST EN ER", 9x "LEICH AN BERUCHTIG") sugiere un canto ritual o epitafio. LEICH en MHG = "poema/canto" ademas de "cadaver".
**Accion:** Buscar referencias a rituales funerarios bonelord en lore del juego

### Hipotesis 8: Los titulos numericos de los libros son parte del texto
Cada libro tiene un titulo numerico (ej: "5611457278"). Estos podrian ser:
- Los primeros digitos del contenido (ya verificado — si lo son)
- Un indice de ordenacion
- Coordenadas o claves adicionales
**Accion:** Verificar in-game si los titulos son identicos a los primeros digitos

---

## 6. Prioridades de Investigacion (Ordenadas)

### Inmediato (Puede hacerse ahora)
1. Decodificar el poema de Avar Tar con mapping v7
2. Decodificar speech de Evil Eye y Elder Bonelord con v7
3. Buscar "Orangenstrasse", "Salzberg", "Weichstein", "Schrat" en TibiaWiki
4. Intentar resolver anagramas de THENAEUT, LGTNELGZ, WRLGTNELNR, HISDIZA

### Requiere acceso in-game
5. Verificar transcripciones de libros (especialmente books 49, 4, 30)
6. Probar keywords nuevos con A Wrinkled Bonelord
7. Explorar sala espejo de Paradox Tower
8. Verificar libros blancos de Demona
9. Probar Noodles con keywords nuevos
10. Buscar textos 469 fuera de Hellgate

### Investigacion de largo plazo
11. Analizar si las cadenas de libros forman un mapa o patron geografico
12. Cross-reference nombres decodificados con lore de actualizaciones recientes
13. Contactar a la comunidad 469 con hallazgos para verificacion cruzada
14. Documentar el numero unico del Mad Mage y analizarlo

---

## 7. Herramientas Necesarias

- **Cuenta de Tibia activa** con acceso a Hellgate (Key 3012 requerida)
- **Personaje nivel 50+** para sobrevivir en Hellgate
- **Screenshots/video** para documentar libros y dialogos NPC
- **TibiaWiki** para cross-reference
- **Script de decodificacion** (`scripts/core/narrative_v3_clean.py`) para probar nuevos textos encontrados

---

*Generado el 2026-03-24 basado en 94.4% de texto descifrado (30 sesiones de criptoanalisis).*
