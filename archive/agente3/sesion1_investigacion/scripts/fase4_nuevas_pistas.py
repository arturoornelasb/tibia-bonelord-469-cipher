"""
fase4_nuevas_pistas.py — Tests de cifrados alternativos y pistas no exploradas.

Pruebas:
  4A. Cifra de Vigenere con clave "469"
  4B. Cifra Nihilista con clave "469"
  4C. Analisis de la formula Facebook como funcion de mapeo
  4D. Test: usar la ecuacion tiveana (1+1=?) como modificador
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils_469 import (
    load_books, load_mapping, digits_to_pairs, decode_pairs,
    print_metrics, ic_from_text, bigram_score, word_parse_score
)

def vigenere_decrypt(pairs, key="469"):
    """
    Descifra usando Vigenere: pair_original = (pair_cifrado - key_digit) mod 100.
    Si los pares son el cifrado, restamos la clave para obtener el texto plano.
    """
    key_vals = [int(k) for k in key]
    result = []
    for i, pair in enumerate(pairs):
        try:
            val = int(pair)
            k = key_vals[i % len(key_vals)]
            decrypted = (val - k) % 100
            result.append(f"{decrypted:02d}")
        except:
            result.append(pair)
    return result

def vigenere_decrypt_full_key(pairs, key="469"):
    """
    Vigenere con la clave como numero de 3 digitos aplicado a pares.
    Variante: key se aplica como [4, 69], [46, 9], [4, 6, 9].
    """
    results = {}
    
    # Variante 1: key como dígitos individuales [4, 6, 9]
    results['key_digits'] = vigenere_decrypt(pairs, "469")
    
    # Variante 2: key como pares [46, 9] -> [46, 09]
    key_pairs = [46, 9]
    result2 = []
    for i, pair in enumerate(pairs):
        try:
            val = int(pair)
            k = key_pairs[i % len(key_pairs)]
            decrypted = (val - k) % 100
            result2.append(f"{decrypted:02d}")
        except:
            result2.append(pair)
    results['key_46_09'] = result2
    
    # Variante 3: Suma en vez de resta
    result3 = []
    key_vals = [4, 6, 9]
    for i, pair in enumerate(pairs):
        try:
            val = int(pair)
            k = key_vals[i % len(key_vals)]
            decrypted = (val + k) % 100
            result3.append(f"{decrypted:02d}")
        except:
            result3.append(pair)
    results['key_add'] = result3
    
    return results

def nihilist_decrypt(pairs, key="469"):
    """
    Cifra Nihilista: cada par es la suma de la posicion en la cuadricula Polybius
    + valor de la clave. Descifrar = restar clave.
    
    Cuadricula Polybius 10x10 (digitos 0-9):
    0: (11)  1: (12)  2: (13)  ...
    """
    key_vals = [int(k) for k in key]
    result = []
    for i, pair in enumerate(pairs):
        try:
            val = int(pair)
            k = key_vals[i % len(key_vals)]
            # Nihilista: par = fila*10 + col del texto + fila*10 + col de la clave
            # Simplificado: par - key_position_value
            decrypted = (val - k * 11) % 100  # key position = k*11 (diagonal)
            result.append(f"{decrypted:02d}")
        except:
            result.append(pair)
    return result

def test_tiveana(pairs, mapping):
    """
    Test: Aplicar las ecuaciones tiveanas como XOR o como offset.
    Ecuaciones conocidas: 1+1=1, 1+1=13, 1+1=49, 1+1=94
    Esto sugiere que el "resultado" modifica cómo se interpreta la secuencia.
    """
    tiveana_values = [1, 13, 49, 94]
    results = {}
    
    for tv in tiveana_values:
        result = []
        for pair in pairs:
            try:
                val = int(pair)
                modified = (val + tv) % 100
                result.append(f"{modified:02d}")
            except:
                result.append(pair)
        results[f"tiveana_add_{tv}"] = result
        
        result2 = []
        for pair in pairs:
            try:
                val = int(pair)
                modified = (val ^ tv) % 100
                result2.append(f"{modified:02d}")
            except:
                result2.append(pair)
        results[f"tiveana_xor_{tv}"] = result2
    
    return results

def main():
    print("=" * 60)
    print("  FASE 4: PISTAS NO EXPLORADAS")
    print("=" * 60)
    
    mapping = load_mapping(4)
    books = load_books()
    all_digits = "".join(books)
    pairs = digits_to_pairs(all_digits, 0)
    
    # Baseline
    text_base = decode_pairs(pairs, mapping)
    baseline_wp = word_parse_score(text_base)
    baseline_bs = bigram_score(text_base)[0]
    print(f"\nBaseline: WP={baseline_wp:.3f} | Bigram={baseline_bs:.3f}")
    
    # 4A: Vigenere
    print(f"\n{'='*60}")
    print(f"  4A: CIFRA DE VIGENERE con clave '469'")
    print(f"{'='*60}")
    
    vig_results = vigenere_decrypt_full_key(pairs, "469")
    
    for name, vig_pairs in vig_results.items():
        text = decode_pairs(vig_pairs, mapping)
        wp = word_parse_score(text)
        bs = bigram_score(text)[0]
        ic = ic_from_text(text)
        unk = text.count("?") / len(text) * 100
        delta = wp - baseline_wp
        print(f"  {name:<20}: WP={wp:.3f} ({delta:+.3f}) | Bigram={bs:.3f} | IC={ic:.4f} | ?={unk:.1f}%")
        if wp > baseline_wp:
            print(f"    *** MEJORA DETECTADA! ***")
            print(f"    Primeros 200 chars: {text[:200]}")
    
    # 4B: Nihilista
    print(f"\n{'='*60}")
    print(f"  4B: CIFRA NIHILISTA con clave '469'")
    print(f"{'='*60}")
    
    nih_pairs = nihilist_decrypt(pairs, "469")
    text = decode_pairs(nih_pairs, mapping)
    wp = word_parse_score(text)
    bs = bigram_score(text)[0]
    ic = ic_from_text(text)
    delta = wp - baseline_wp
    print(f"  Nihilista: WP={wp:.3f} ({delta:+.3f}) | Bigram={bs:.3f} | IC={ic:.4f}")
    if wp > baseline_wp:
        print(f"    *** MEJORA! ***\n    {text[:200]}")
    
    # 4C: Ecuaciones Tiveanas
    print(f"\n{'='*60}")
    print(f"  4C: ECUACIONES TIVEANAS (offsets)")
    print(f"{'='*60}")
    
    tiv_results = test_tiveana(pairs, mapping)
    for name, tiv_pairs in tiv_results.items():
        text = decode_pairs(tiv_pairs, mapping)
        wp = word_parse_score(text)
        bs = bigram_score(text)[0]
        delta = wp - baseline_wp
        marker = " ***" if wp > baseline_wp else ""
        print(f"  {name:<20}: WP={wp:.3f} ({delta:+.3f}) | Bigram={bs:.3f}{marker}")
    
    # 4D: Analisis matematico de la formula Facebook
    print(f"\n{'='*60}")
    print(f"  4D: ANALISIS DE FORMULA FACEBOOK R = 0.593*L + 25.28")
    print(f"{'='*60}")
    
    # Los 26 pares del FB post
    fb_pairs = [
        (11, 32), (12, 32), (13, 33), (15, 34), (18, 36), (19, 36),
        (21, 38), (22, 38), (24, 39), (25, 40), (31, 44), (33, 45),
        (35, 46), (36, 46), (38, 48), (41, 49), (42, 50), (43, 51),
        (44, 51), (45, 52), (46, 53), (48, 54), (51, 55), (52, 56),
        (53, 56), (54, 57)
    ]
    
    print(f"\n  Pares del Facebook post (L->R):")
    print(f"  {'L':>3} {'R':>3} {'Predicted':>9} {'Error':>6} {'L_letter':>8} {'R_letter':>8}")
    for l, r in fb_pairs:
        predicted = round(0.593 * l + 25.28)
        error = r - predicted
        l_str = f"{l:02d}"
        r_str = f"{r:02d}"
        l_letter = mapping.get(l_str, "?")
        r_letter = mapping.get(r_str, "?")
        print(f"  {l:>3} {r:>3} {predicted:>9} {error:>+6} {l_letter:>8} {r_letter:>8}")
    
    # Probar si los pares FB son sustituciones directas (L->R)
    print(f"\n  Test: FB pares como tabla de sustitucion L->R")
    fb_map = {f"{l:02d}": f"{r:02d}" for l, r in fb_pairs}
    fb_substituted = []
    substituted_count = 0
    for p in pairs:
        if p in fb_map:
            fb_substituted.append(fb_map[p])
            substituted_count += 1
        else:
            fb_substituted.append(p)
    
    text = decode_pairs(fb_substituted, mapping)
    wp = word_parse_score(text)
    print(f"  Sustituidos: {substituted_count}/{len(pairs)} pares ({substituted_count/len(pairs)*100:.1f}%)")
    print(f"  WP: {wp:.3f} ({wp-baseline_wp:+.3f} vs baseline)")
    
    # Resumen
    print(f"\n{'='*60}")
    print(f"  RESUMEN FASE 4")
    print(f"{'='*60}")
    
    all_tests = {}
    all_tests["Baseline"] = baseline_wp
    for name, vp in vig_results.items():
        all_tests[f"Vigenere {name}"] = word_parse_score(decode_pairs(vp, mapping))
    all_tests["Nihilista"] = word_parse_score(decode_pairs(nihilist_decrypt(pairs, "469"), mapping))
    for name, tp in tiv_results.items():
        all_tests[name] = word_parse_score(decode_pairs(tp, mapping))
    all_tests["FB substitution"] = wp
    
    print(f"\n  {'Test':<25} {'WordParse':>10} {'vs Baseline':>12}")
    for name in sorted(all_tests.keys(), key=lambda x: -all_tests[x]):
        v = all_tests[name]
        d = v - baseline_wp
        marker = " <<<" if v > baseline_wp and name != "Baseline" else ""
        print(f"  {name:<25} {v:>9.3f} {d:>+11.3f}{marker}")

if __name__ == "__main__":
    main()
