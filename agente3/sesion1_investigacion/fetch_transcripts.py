"""
Descarga transcripciones de los videos de YouTube sobre Bonelord 469.
Usa youtube-transcript-api v1.2.4 (requiere instanciación).
"""
from youtube_transcript_api import YouTubeTranscriptApi
import json

VIDEOS = [
    {"id": "lYMHnFJptiI", "title": "El secreto del lenguaje de los bonelords 469 [ENG SUB] — Expedientes Tibianos X"},
    {"id": "BXwaltlTzcg", "title": "Linguagem 469 foi solucionada por Inteligência Artificial...?"},
    {"id": "YkwMVZkEx_g", "title": "En Vivo | Avance #1 Lenguaje 469 Bonelord | Conversando"},
    {"id": "hpLrzfkBntY", "title": "A Linguagem Bonelord (469) — Live de Mysteriando (1/2)"},
    {"id": "pHpQEsZ66YY", "title": "O Mistério do 469 CONTINUA no Tibia — Fessor Lih"},
]

ytt = YouTubeTranscriptApi()
results = []

for v in VIDEOS:
    vid = v["id"]
    title = v["title"]
    print(f"\n{'='*60}")
    print(f"Descargando: {title} ({vid})")
    
    try:
        t = ytt.fetch(vid, languages=["es", "es-419", "es-ES", "en", "pt", "pt-BR"])
        text = " ".join([s.text for s in t.snippets]).replace("\n", " ")
        lang = t.language
        results.append({
            "title": title,
            "id": vid,
            "language": lang,
            "text": text,
            "length": len(text)
        })
        print(f"  OK — idioma: {lang}, {len(text)} chars")
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append({
            "title": title,
            "id": vid,
            "language": "N/A",
            "text": f"[Error: {e}]",
            "length": 0
        })

# Guardar resultados completos en JSON
with open("c:/tibia-research/agente3/transcripciones_raw.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Guardar en markdown formateado
with open("c:/tibia-research/agente3/transcripciones_videos.md", "w", encoding="utf-8") as f:
    f.write("# Transcripciones de Videos de YouTube sobre Bonelord 469\n\n")
    f.write("> Extraídas automáticamente con youtube-transcript-api. Fecha: 2026-03-23.\n\n")
    for r in results:
        f.write(f"---\n\n## {r['title']}\n\n")
        f.write(f"- **Video ID**: `{r['id']}`\n")
        f.write(f"- **URL**: https://www.youtube.com/watch?v={r['id']}\n")
        f.write(f"- **Idioma subtítulos**: {r['language']}\n")
        f.write(f"- **Longitud**: {r['length']} caracteres\n\n")
        f.write(f"### Transcripción\n\n{r['text']}\n\n")

print(f"\nHecho! {len([r for r in results if r['length'] > 0])}/{len(VIDEOS)} transcripciones descargadas.")
print("Archivos: transcripciones_raw.json, transcripciones_videos.md")
