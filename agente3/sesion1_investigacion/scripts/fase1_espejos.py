"""
fase1_espejos.py — Prueba 4 transformaciones de espejo sobre el cifrado 469.

Hipótesis: CipSoft incorporó la temática de espejo/reflejo en el cifrado.
Evidencia: Facebook post espejado, Paradox Tower con cuarto espejado,
           TOTNIURG = GRUINTOT invertido, bonelords ven blinks espejados.

Transformaciones probadas:
  1A. Reversal de dígitos dentro de cada par (95 -> 59)
  1B. Swap de pares adyacentes ([A,B,C,D] -> [B,A,D,C])
  1C. Lectura del superstring en reversa
  1D. Fórmula del Facebook: R = round(0.593*L + 25.28)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils_469 import (
    load_books, load_mapping, load_superstring,
    digits_to_pairs, decode_pairs, decode_text,
    reverse_pair_digits, swap_adjacent_pairs, facebook_transform,
    print_metrics
)

def build_concat_text():
    """Construye el texto concatenado de todos los libros."""
    books = load_books()
    return "".join(books)

def test_baseline(all_digits, mapping):
    """Prueba el mapeo original (referencia)."""
    print("\n" + "█"*60)
    print("  BASELINE — Mapeo original v4 (sin transformación)")
    print("█"*60)
    
    for offset in [0, 1]:
        pairs = digits_to_pairs(all_digits, offset)
        text = decode_pairs(pairs, mapping)
        print_metrics(f"Offset {offset}", text, pairs)
    
    return digits_to_pairs(all_digits, 0)

def test_1a_reverse_digits(all_digits, mapping):
    """1A: Invertir dígitos dentro de cada par."""
    print("\n" + "█"*60)
    print("  FASE 1A — Reversal de dígitos (95→59, 61→16, etc.)")
    print("█"*60)
    
    for offset in [0, 1]:
        pairs = digits_to_pairs(all_digits, offset)
        mirrored = reverse_pair_digits(pairs)
        text = decode_pairs(mirrored, mapping)
        print_metrics(f"1A Offset {offset}", text, mirrored)
    
    # También: crear un mapeo invertido
    print("\n  --- 1A Alternativa: Mapeo con códigos invertidos ---")
    inv_mapping = {}
    for code, letter in mapping.items():
        if len(code) == 2:
            inv_code = code[1] + code[0]
            inv_mapping[inv_code] = letter
    
    for offset in [0, 1]:
        pairs = digits_to_pairs(all_digits, offset)
        text = decode_pairs(pairs, inv_mapping)
        print_metrics(f"1A-alt (mapeo invertido) Offset {offset}", text, pairs)

def test_1b_swap_adjacent(all_digits, mapping):
    """1B: Intercambiar pares adyacentes."""
    print("\n" + "█"*60)
    print("  FASE 1B — Swap de pares adyacentes ([A,B]→[B,A])")
    print("█"*60)
    
    for offset in [0, 1]:
        pairs = digits_to_pairs(all_digits, offset)
        swapped = swap_adjacent_pairs(pairs)
        text = decode_pairs(swapped, mapping)
        print_metrics(f"1B Offset {offset}", text, swapped)

def test_1c_full_reverse(all_digits, mapping):
    """1C: Lectura del superstring completo al revés."""
    print("\n" + "█"*60)
    print("  FASE 1C — Superstring al revés")
    print("█"*60)
    
    reversed_digits = all_digits[::-1]
    for offset in [0, 1]:
        pairs = digits_to_pairs(reversed_digits, offset)
        text = decode_pairs(pairs, mapping)
        print_metrics(f"1C Reversed Offset {offset}", text, pairs)

def test_1d_facebook_formula(all_digits, mapping):
    """1D: Aplicar la fórmula del Facebook post."""
    print("\n" + "█"*60)
    print("  FASE 1D — Fórmula Facebook: R = round(0.593*L + 25.28)")
    print("█"*60)
    
    # Mostrar la tabla de transformación
    print("\n  Tabla de transformación (muestra):")
    print("  Original → Transformado")
    for x in [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99]:
        t = round(0.593 * x + 25.28)
        t = max(0, min(99, t))
        print(f"    {x:02d} → {t:02d}")
    
    for offset in [0, 1]:
        pairs = digits_to_pairs(all_digits, offset)
        transformed = facebook_transform(pairs)
        text = decode_pairs(transformed, mapping)
        print_metrics(f"1D Facebook Offset {offset}", text, transformed)
    
    # Inversa: ¿los códigos del mapeo son el resultado de la fórmula?
    # Si el texto original fue escrito con código X, y lo que vemos es R=0.593X+25,
    # entonces X_original = (R - 25.28) / 0.593
    print("\n  --- 1D Inversa: X = (código_visto - 25.28) / 0.593 ---")
    inv_pairs_list = []
    for offset in [0, 1]:
        pairs = digits_to_pairs(all_digits, offset)
        inv_pairs = []
        for p in pairs:
            try:
                val = int(p)
                original = round((val - 25.28) / 0.593)
                original = max(0, min(99, original))
                inv_pairs.append(f"{original:02d}")
            except:
                inv_pairs.append(p)
        text = decode_pairs(inv_pairs, mapping)
        print_metrics(f"1D Inversa Offset {offset}", text, inv_pairs)

def test_combinaciones(all_digits, mapping):
    """Prueba combinaciones de transformaciones."""
    print("\n" + "█"*60)
    print("  COMBINACIONES — Espejo + Reversal")
    print("█"*60)
    
    # Combo: reverse digits + full reverse
    reversed_digits = all_digits[::-1]
    pairs = digits_to_pairs(reversed_digits, 0)
    mirrored = reverse_pair_digits(pairs)
    text = decode_pairs(mirrored, mapping)
    print_metrics("Combo: Full reverse + digit reverse (offset 0)", text, mirrored)
    
    # Combo: swap adjacent + reverse digits
    pairs = digits_to_pairs(all_digits, 0)
    swapped = swap_adjacent_pairs(pairs)
    mirrored = reverse_pair_digits(swapped)
    text = decode_pairs(mirrored, mapping)
    print_metrics("Combo: Swap adjacent + digit reverse (offset 0)", text, mirrored)

def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║    FASE 1: HIPÓTESIS DEL ESPEJO — Cifrado 469          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    # Cargar datos
    mapping = load_mapping(4)
    print(f"\nMapeo cargado: {len(mapping)} códigos → {len(set(mapping.values()))} letras")
    
    books = load_books()
    all_digits = "".join(books)
    print(f"Total dígitos: {len(all_digits)} ({len(books)} libros)")
    
    # Ejecutar todas las pruebas
    test_baseline(all_digits, mapping)
    test_1a_reverse_digits(all_digits, mapping)
    test_1b_swap_adjacent(all_digits, mapping)
    test_1c_full_reverse(all_digits, mapping)
    test_1d_facebook_formula(all_digits, mapping)
    test_combinaciones(all_digits, mapping)
    
    # Resumen comparativo
    print("\n" + "█"*60)
    print("  RESUMEN COMPARATIVO")
    print("█"*60)
    print("\n  Recopilando scores de todas las transformaciones...\n")
    
    tests = {
        "Baseline (offset 0)": digits_to_pairs(all_digits, 0),
        "Baseline (offset 1)": digits_to_pairs(all_digits, 1),
        "1A Reverse digits (o0)": reverse_pair_digits(digits_to_pairs(all_digits, 0)),
        "1A Reverse digits (o1)": reverse_pair_digits(digits_to_pairs(all_digits, 1)),
        "1B Swap adjacent (o0)": swap_adjacent_pairs(digits_to_pairs(all_digits, 0)),
        "1C Full reverse (o0)": digits_to_pairs(all_digits[::-1], 0),
        "1D Facebook (o0)": facebook_transform(digits_to_pairs(all_digits, 0)),
        "1D FB Inverse (o0)": None,  # computed below
    }
    
    # Compute FB inverse
    pairs_fb_inv = []
    for p in digits_to_pairs(all_digits, 0):
        try:
            val = int(p)
            original = round((val - 25.28) / 0.593)
            original = max(0, min(99, original))
            pairs_fb_inv.append(f"{original:02d}")
        except:
            pairs_fb_inv.append(p)
    tests["1D FB Inverse (o0)"] = pairs_fb_inv
    
    from utils_469 import ic_from_text, bigram_score, word_parse_score, ic_from_pairs
    
    print(f"  {'Test':<30} {'IC-char':>8} {'IC-pair':>8} {'Bigram%':>8} {'WordParse%':>10} {'?%':>6}")
    print(f"  {'-'*30} {'-'*8} {'-'*8} {'-'*8} {'-'*10} {'-'*6}")
    
    for name, pairs in tests.items():
        text = decode_pairs(pairs, mapping)
        ic_c = ic_from_text(text)
        ic_p = ic_from_pairs(pairs)
        bs = bigram_score(text)[0]
        wp = word_parse_score(text)
        unk = text.count("?") / len(text) * 100
        print(f"  {name:<30} {ic_c:>8.4f} {ic_p:>8.4f} {bs:>7.1f}% {wp*100:>9.1f}% {unk:>5.1f}%")
    
    print(f"\n  Alemán esperado:              {'~0.0762':>8} {'~0.0172':>8} {'>25%':>8} {'>60%':>10}")
    print(f"\n  *** La MEJOR transformación es la que más se acerca a los valores esperados ***")

if __name__ == "__main__":
    main()
