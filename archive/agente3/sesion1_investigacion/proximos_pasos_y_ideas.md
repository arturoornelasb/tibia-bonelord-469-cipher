# Próximos Pasos e Ideas para la Investigación 469

> Compilado por Agente 3. Fecha: 2026-03-23.
> Basado en: FINDINGS.md, agente2/FINDINGS_SESSION3.md, docs/README-469.md.

---

## PRIORIDAD ALTA

### 1. Investigar los 20 códigos "gap-only"
- Hay ~700 ocurrencias que **nunca** aparecen en palabras alemanas confirmadas.
- Los más sospechosos: `[64]=T (124x)`, `[80]=G (79x)`, `[97]=G (58x)`, `[96]=Z (53x)`.
- **Acción**: Reasignación sistemática CON protección de códigos ancla (URALTE, KOENIG).

### 2. Conectar Cadena 0 y Cadena 2
- Cadena 0 tiene URALTE pero no KOENIG; Cadena 2 tiene KOENIG pero no URALTE.
- **Acción**: Encontrar libros intermedios que conecten ambas para obtener la inscripción COMPLETA.

### 3. Hipótesis [04]=M → E
- Score +72 de mejora. MINHLD → EINHLD (comienza con EIN).
- M quedaría con 0 códigos, pero M ya está sub-representado (1.1%).
- **Acción**: Probar este cambio y evaluar el impacto completo.

### 4. Reasignar [64]=T
- 124 ocurrencias, 100% en gaps. Nunca aparece en palabras confirmadas.
- **Acción**: Si no es T, ¿qué es? Perder 124 del T da 264 (4.7%), bajo pero posible.

---

## PRIORIDAD MEDIA

### 5. Reparación per-book de dígitos corruptos
- s2ward confirma: "un solo número ha sido removido en algunos libros" y "algunos libros han sido partidos por la mitad y volteados".
- **Acción**: Para cada libro sospechoso, insertar un dígito en cada posición y verificar si mejora la decodificación.

### 6. Análisis de bigramas de códigos gap-only
- Para los 20 códigos gap-only, analizar qué bigramas forman con códigos vecinos.
- Si producen bigramas imposibles en alemán de forma consistente, están mal asignados.

### 7. Prueba de intercambio de dos códigos simultáneamente
- En lugar de cambios individuales, probar intercambios de parejas.

### 8. Buscar NICHT vía corrupción
- NICHT es estructuralmente imposible con el mapeo actual.
- Podría existir en la versión no corrupta de algún libro.

---

## PRIORIDAD BAJA / EXPLORATORIA

### 9. Alemán arcaico / Medio Alto Alemán (MHG)
- Patrones como HEARUCHTIG, TAUTRIST, SCHAUNRU podrían ser formas arcaicas.
- HEARUCHTIG podría ser un adjetivo del MHG.

### 10. Vocabulario del lore de Tibia
- Verificar si TAUTRIST, SCHAUNRU, ADTHARSC aparecen en otros contenidos de Tibia (diálogos NPC, textos de quests, otros libros).

### 11. Análisis de anagramas
- CipSoft usa anagramas extensivamente: Vladruc=Dracula, Dallheim=Heimdall.
- ¿Alguno de los nombres propios se rearregla a términos conocidos?
  - LABGZERAS → ¿¿??
  - TAUTR → ¿¿??
  - SCHWITEIONE → ¿¿??
  - TOTNIURG invertido = GRUIN+TOT (ruina+muerte) ← ya descubierto.

### 12. Capa de transposición
- ¿Podría haber una transposición columnar encima de la sustitución?
- El Zodiac Z340 se resolvió encontrando una capa de transposición.

### 13. Códigos P/V
- Ambos al 0%. ¿El texto genuinamente evita estas letras o no hemos encontrado sus códigos?
- Verificar si alguno de los 20 códigos gap-only podría ser P o V.

---

## IDEAS DE LA COMUNIDAD DE YOUTUBE

| Teoría | Fuente | Evaluación vs nuestra investigación |
|--------|--------|-------------------------------------|
| Sustitución alfanumérica simple | Múltiples videos | ✅ Confirmado como sustitución homofónica de parejas de 2 dígitos |
| 4, 6, 9 son puntuación | Reddit/YouTube | ❌ No compatible con nuestro análisis — son parte de códigos de pareja |
| Texto en inglés | TibiaSecrets | ❌ Refutado — IC y bigramas coinciden con alemán, no inglés |
| Uso de IA (ChatGPT) | Videos brasileños | ⚠️ Intentos superficiales; nuestro enfoque usa cripto-análisis estructurado |
| Referencia a Intel 486 | Fessor Lih | 🔍 Sin evidencia concluyente |
| Conexión con Pac-Man (Blinky) | Videos | 🔍 Posible broma interna pero no relevante al cifrado |
| Llave para Serpentine Tower | Múltiples videos | 🔍 Plausible pero no verificable hasta que el texto esté completo |

---

## HERRAMIENTAS Y RECURSOS EXTERNOS

- **Repositorio fuente de datos**: [github.com/s2ward/469](https://github.com/s2ward/469)
- **TibiaSecrets**: Artículo sobre intento de decodificación en inglés (probablemente espurio).
- **TibiaWiki**: HEDEMI y KELSEI son reconocidos como términos de búsqueda (sin páginas propias).
- **Facebook de Tibia**: Imagen espejada con pares numéricos que siguen relación lineal (R = 0.593L + 25.28).
