> **Idioma / Language:** English | Español (abajo)

# Primary-Source Verification — Tibia 7.7 Server Data

Source: **[Issue #1](https://github.com/arturoornelasb/tibia-bonelord-469-cipher/issues/1)** by **@kwiiby** — an independent validation of this repository against archival Tibia 7.7 server-side data (`map/*.sec`, `origmap/*.sec`, `npc/*.npc`, `mon/*.mon`). The issue reports **derived findings only** (counts, coordinates, short identifiers, conclusions); no proprietary CipSoft files are reproduced. Tibia and all game content remain © CipSoft GmbH.

Every computationally checkable claim was **independently re-verified** against `data/books.json` and `data/mapping_v7.json` (see `sandbox` verification, summarized below). All checks passed.

## 1. Corpus is exact
- Hellgate Library sector: `map/1024-0990-13.sec` — **71** digit-only books physically shelved.
- All **70 unique** books in `data/books.json` match the server data **digit-for-digit**. One text is duplicated across two bookcases → 70 unique is correct.

## 2. Single-digit removal is original CipSoft authoring
- 38 of the 71 books are odd-length in the server data.
- The pre-edit reference map `origmap/` is **identical** to `map/` → the odd-length structure was authored by CipSoft, not a transcription error or later corruption.
- Consistent with the **CADST** technique premise (37/70 in community data vs 38/71 here; the extra one is the duplicate).

## 3. 2-digit structure confirmed independently of any mapping
- 33 even-length books → 2,886 two-digit pairs at natural alignment.
- Codes **07, 32, 33 never occur** (97/100 present). Under uniform-random digits, P(a specific code absent) ≈ (99/100)^2886 ≈ 3×10⁻¹³.
- **Our re-verification:** confirmed exactly — even-length books = 33, pairs = 2886, absent = {07, 32, 33}.
- Note: in the full digit-inserted/aligned corpus, code 33 occurs once (→ W) and 32 once (insertion artifacts); these rare codes are weakly constrained (see §8).

## 4. Mapping v7 validation
- Dictionary coverage (DP segmentation, 50k modern-German lexicon): **95.5%** over all 71 books.
- Frequency-preserving random permutations of the same mapping: only **80–85%**.
- Decoded letter frequencies match German (E ≈ 17.5% decoded vs ≈17.4% expected).
- Anchor strings reproduce at expected positions: `URALTE STEIN`, `ESCHWITEION` (→ WEICHSTEIN), `EDETOTNIURG` (→ GOTTDIENER), `HISDIZA`, `RUNE`.

## 5. 469 book outside Hellgate — Isle of Kings (confirmed from primary source)
- Location: `map/1005-0998-06.sec`, game coords **(32173, 31936, z=6)** — White Raven Monastery library, Isle of Kings.
- Item TypeID **2821** ("a book", FontSize=1) — a different book object than the Hellgate books.
- Text (137 digits) is an **exact substring** (digits 38–174) of a 177-digit Hellgate book, covering `...TRAUT IST LEICH AN BERUCHTIG ... EDETOTNIURG (GOTTDIENER)`.
- **Our re-verification:** the text equals `data/books.json` index **22** exactly, **and** is a substring of index **2** (177 digits) at offset **38** → matches the claim precisely. This is the same "Isle of Kings" book independently reported in Discussion #2.
- Note: **Kharos / Ferumbras Citadel** 469 text is *not* present in 7.7 (it is 7.8 content) — which is why kwiiby found only the Isle book, and confirms the Kharos text is a later derivative rearrangement.

## 6. Proper-noun resolutions (verified)
- **THENAEUT = ENTHAUTE** ("flayed / skinned") — **exact anagram** ({A, E×2, H, N, T×2, U}). Re-verified: exact. Fits the LEICH (corpse) narrative. Missed earlier because lexicons only carry the infinitive ENTHAUTEN.
- **LGTNELGZ ≈ GEGLANZT** ("gleamed") — anagram + **1 substitution** (L↔A). Re-verified: differs by exactly one letter. Always paired with THENAEUT → two past-tense verbs in the same register. (Weaker than THENAEUT; semantic fit is plausible not certain.)
- **HISDIZA** directly precedes `RUNE` (`NUN AM HISDIZA RUNE`) → likely a *fictional rune name*, intentionally untranslatable.

## 7. Primary-source "spoken 469" specimens (NPC/monster data)
- `npc/beholder.npc` — "A Wrinkled Beholder", Home `[32788, 31690, 13]`. Canonical lines confirmed ("Our books are written in 469", "It's 1, not 'Tibia'", NPC name = **486486**).
- `mon/elderbeholder.mon` and `mon/evileye.mon` both shout **`653768764!`** — a server-side spoken-469 specimen. Under the book mapping it yields no convincing reading (`IERE` / `OEWT` at the two natural alignments), supporting the **two-systems hypothesis** (books ≠ NPC encoding).
- `npc/avar.npc` (Avar Tar, Edron `[33250, 31764, 7]`) has **no 469 poem in 7.7** — the poem is later content, explaining its different (variable-length) encoding.

## 8. Residual uncertainty
Under natural alignment, 12 codes occur ≤5 times in the whole corpus (`69`×1, `66`×1, `10`×2, `38`×2, `39`×2, `79`×3, `02`×3, `41`×4, `37`×4, `93`×5, `87`×5, `98`×5). Their letter assignments are weakly constrained by the data; this, plus the 38 removed digits, bounds any solution's confidence regardless of method.

---

# Verificación por Fuente Primaria — Datos del Servidor de Tibia 7.7

Fuente: **[Issue #1](https://github.com/arturoornelasb/tibia-bonelord-469-cipher/issues/1)** de **@kwiiby** — validación independiente de este repositorio contra datos de archivo server-side de Tibia 7.7 (`map/*.sec`, `origmap/*.sec`, `npc/*.npc`, `mon/*.mon`). El issue reporta **solo hallazgos derivados** (conteos, coordenadas, identificadores cortos, conclusiones); no reproduce archivos propietarios de CipSoft. Tibia y todo su contenido son © CipSoft GmbH.

Cada afirmación computacionalmente checable fue **re-verificada de forma independiente** contra `data/books.json` y `data/mapping_v7.json`. Todas pasaron.

1. **Corpus exacto** — Sector `map/1024-0990-13.sec`: 71 libros físicos; los 70 únicos de `books.json` coinciden dígito por dígito (un texto duplicado en dos estanterías).
2. **Remoción de dígito = autoría original de CipSoft** — `origmap/` (pre-edición) idéntico a `map/`; valida la premisa de CADST.
3. **Estructura de 2 dígitos confirmada sin mapeo** — 33 libros pares, 2886 pares, ausentes {07, 32, 33}, p ≈ 3×10⁻¹³. Re-verificado exacto.
4. **v7 validado** — 95.5% de cobertura (léxico alemán 50k); permutaciones aleatorias 80–85%; frecuencias de letras alemanas (E ≈ 17.5%).
5. **Libro fuera de Hellgate (Isle of Kings)** — coords (32173, 31936, z=6); texto de 137 dígitos = `books.json` índice 22 y substring del índice 2 (offset 38). Kharos NO está en 7.7 (es 7.8) → confirma que Kharos es un derivado posterior.
6. **Nombres propios** — THENAEUT = ENTHAUTE (anagrama exacto, "desollado", encaja con LEICH); LGTNELGZ ≈ GEGLANZT ("resplandeció", + 1 sustitución L↔A); HISDIZA = probable nombre de runa ficticio.
7. **Especímenes de "469 hablado"** — Wrinkled Beholder (nombre 486486); Elder Beholder / Evil Eye gritan `653768764` (no decodifica bajo el cifrado de libros → dos sistemas); Avar Tar **sin poema en 7.7** (contenido posterior).
8. **Incertidumbre residual** — 12 códigos aparecen ≤5 veces; débilmente restringidos.
