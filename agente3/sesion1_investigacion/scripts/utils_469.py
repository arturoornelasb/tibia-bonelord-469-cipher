"""
utils_469.py — Funciones compartidas para el análisis del cifrado 469.
Carga datos, calcula IC, parsea contra diccionario alemán, etc.
"""
import json
import os
import math
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

def load_books():
    """Carga los 70 libros como lista de strings de dígitos."""
    path = os.path.join(DATA_DIR, "books.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_mapping(version=4):
    """Carga el mapeo código→letra. Retorna dict {str_code: letter}."""
    fname = f"final_mapping_v{version}.json"
    path = os.path.join(DATA_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    # Check format: could be {code: letter} or {letter: [codes]}
    mapping = {}
    for key, val in raw.items():
        if isinstance(val, list):
            # Format: {"E": ["95","56",...]}
            for code in val:
                mapping[code] = key
        else:
            # Format: {"00": "H", "01": "E", ...}
            mapping[key] = val
    return mapping

def load_superstring():
    """Carga el master_text (superstring de 5902 dígitos)."""
    path = os.path.join(DATA_DIR, "master_text.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    # Si no existe, concatenar todos los libros
    books = load_books()
    return "".join(books)

def digits_to_pairs(digits, offset=0):
    """Convierte un string de dígitos en pares de 2 dígitos."""
    s = digits[offset:]
    return [s[i:i+2] for i in range(0, len(s)-1, 2)]

def decode_pairs(pairs, mapping):
    """Decodifica una lista de pares usando el mapeo."""
    result = []
    for p in pairs:
        if p in mapping:
            result.append(mapping[p])
        else:
            result.append("?")
    return "".join(result)

def decode_text(digits, mapping, offset=0):
    """Decodifica un string de dígitos completo."""
    pairs = digits_to_pairs(digits, offset)
    return decode_pairs(pairs, mapping)

def ic_from_pairs(pairs):
    """Calcula el Índice de Coincidencia a nivel de pares."""
    counts = Counter(pairs)
    n = len(pairs)
    if n <= 1:
        return 0
    total = sum(c * (c - 1) for c in counts.values())
    return total / (n * (n - 1))

def ic_from_text(text):
    """Calcula el IC a nivel de caracteres (letras)."""
    text = text.replace("?", "")
    counts = Counter(text)
    n = len(text)
    if n <= 1:
        return 0
    total = sum(c * (c - 1) for c in counts.values())
    return total / (n * (n - 1))

# Bigramas más frecuentes en alemán (top 25)
GERMAN_TOP_BIGRAMS = [
    "EN", "ER", "CH", "DE", "EI", "ND", "TE", "IN", "IE", "GE",
    "ES", "NE", "UN", "ST", "RE", "HE", "AN", "BE", "SE", "DI",
    "DA", "LE", "AU", "NG", "IC"
]

def bigram_score(text):
    """
    Calcula el % de bigramas del texto que están en el top-25 alemán.
    Retorna (score, total_bigrams, matching_bigrams).
    """
    text = text.replace("?", "")
    if len(text) < 2:
        return 0, 0, 0
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    total = len(bigrams)
    matching = sum(1 for b in bigrams if b in GERMAN_TOP_BIGRAMS)
    return matching / total if total > 0 else 0, total, matching

# Diccionario alemán básico para word parse
_GERMAN_WORDS = None

def load_german_dict():
    """Carga un set de palabras alemanas comunes."""
    global _GERMAN_WORDS
    if _GERMAN_WORDS is not None:
        return _GERMAN_WORDS
    # Palabras alemanas más comunes + palabras encontradas en el texto
    _GERMAN_WORDS = {
        "DIE", "DER", "DAS", "UND", "IST", "EIN", "EINE", "EINEN",
        "IN", "DEN", "VON", "ER", "ES", "AN", "AUF", "MIT", "WIR",
        "ICH", "SIE", "SIND", "NICHT", "AUCH", "SO", "WAS", "WIE",
        "NUR", "ALS", "ABER", "HAT", "NOCH", "NACH", "DANN", "WIRD",
        "SEIN", "SEINE", "SEINER", "DIESEM", "DIESER", "DIESE",
        "HIER", "ORT", "UNTER", "RUNE", "RUNEN", "STEIN", "STEINE",
        "STEINEN", "URALTE", "KOENIG", "ENDE", "REDE", "NEU",
        "SCHWERT", "WIE", "TUN", "SEI", "DEM", "DENEN", "DASS",
        "TAUTR", "LABGZERAS", "HEDEMI", "ADTHARSC",  # proper nouns
        "AM", "DES", "IM"
    }
    return _GERMAN_WORDS

def word_parse_score(text, min_word_len=2):
    """
    Score de parseo de palabras alemanas usando programación dinámica.
    Retorna (chars_matched / total_chars).
    """
    text = text.replace("?", "")
    if not text:
        return 0.0
    words = load_german_dict()
    n = len(text)
    # dp[i] = max chars matched up to position i
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]  # skip this char
        for wlen in range(min_word_len, min(i, 15) + 1):
            word = text[i-wlen:i]
            if word in words:
                dp[i] = max(dp[i], dp[i-wlen] + wlen)
    return dp[n] / n if n > 0 else 0.0

def reverse_pair_digits(pairs):
    """Invierte los dígitos dentro de cada par: '95' -> '59'."""
    return [p[1]+p[0] if len(p)==2 else p for p in pairs]

def swap_adjacent_pairs(pairs):
    """Intercambia pares adyacentes: [A,B,C,D] -> [B,A,D,C]."""
    result = []
    for i in range(0, len(pairs)-1, 2):
        result.append(pairs[i+1])
        result.append(pairs[i])
    if len(pairs) % 2 == 1:
        result.append(pairs[-1])
    return result

def facebook_transform(pairs):
    """Aplica la transformación del Facebook post: R = round(0.593*L + 25.28)."""
    result = []
    for p in pairs:
        try:
            val = int(p)
            transformed = round(0.593 * val + 25.28)
            transformed = max(0, min(99, transformed))
            result.append(f"{transformed:02d}")
        except:
            result.append(p)
    return result

def print_metrics(label, text, pairs=None):
    """Imprime las métricas de calidad de una decodificación."""
    ic = ic_from_text(text)
    bs, total_bg, match_bg = bigram_score(text)
    wp = word_parse_score(text)
    unknowns = text.count("?")
    total = len(text)
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Longitud texto:     {total} chars ({unknowns} desconocidos, {unknowns/total*100:.1f}%)")
    print(f"  IC (caracteres):    {ic:.4f}  (alemán esperado: ~0.0762)")
    print(f"  Bigram score:       {bs:.3f}  ({match_bg}/{total_bg} bigramas top-25 alemán)")
    print(f"  Word parse score:   {wp:.3f}  ({wp*100:.1f}% del texto es alemán)")
    print(f"  Primeros 200 chars: {text[:200]}")
    if pairs:
        ic_p = ic_from_pairs(pairs)
        print(f"  IC (pares):         {ic_p:.4f}  (alemán esperado: ~0.0172)")
