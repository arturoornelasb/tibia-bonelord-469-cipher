"""
fase2_gap_analysis.py — Analiza y reasigna los 20 códigos "gap-only"
que nunca aparecen en palabras alemanas confirmadas.

Estos ~700 ocurrencias son los candidatos más probables a estar mal asignados.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils_469 import (
    load_books, load_mapping, digits_to_pairs, decode_pairs,
    print_metrics, word_parse_score, bigram_score, load_german_dict,
    GERMAN_TOP_BIGRAMS
)
from collections import Counter

def find_gap_only_codes(all_digits, mapping):
    """
    Encuentra códigos que NUNCA aparecen en contextos que producen
    bigramas alemanes válidos (top-25).
    """
    pairs = digits_to_pairs(all_digits, 0)
    
    # Para cada código, contar cuántas veces participa en bigramas alemanes top-25
    code_in_german_bigrams = Counter()
    code_total = Counter()
    
    for i, p in enumerate(pairs):
        if p not in mapping:
            continue
        letter = mapping[p]
        code_total[p] += 1
        
        # Check bigrama izquierdo
        if i > 0 and pairs[i-1] in mapping:
            bigram = mapping[pairs[i-1]] + letter
            if bigram in GERMAN_TOP_BIGRAMS:
                code_in_german_bigrams[p] += 1
        
        # Check bigrama derecho
        if i < len(pairs)-1 and pairs[i+1] in mapping:
            bigram = letter + mapping[pairs[i+1]]
            if bigram in GERMAN_TOP_BIGRAMS:
                code_in_german_bigrams[p] += 1
    
    # Gap-only = códigos con 0 participaciones en bigramas alemanes
    gap_only = []
    partial_gap = []
    for code in sorted(mapping.keys()):
        total = code_total.get(code, 0)
        german = code_in_german_bigrams.get(code, 0)
        ratio = german / total if total > 0 else 0
        if total >= 10 and ratio < 0.05:  # <5% en bigramas alemanes
            gap_only.append((code, mapping[code], total, german, ratio))
        elif total >= 10 and ratio < 0.15:
            partial_gap.append((code, mapping[code], total, german, ratio))
    
    return gap_only, partial_gap, code_total, code_in_german_bigrams

def test_reassignment(all_digits, mapping, code, new_letter, baseline_wp):
    """Prueba reasignar un código a una nueva letra y mide el cambio."""
    test_mapping = dict(mapping)
    test_mapping[code] = new_letter
    pairs = digits_to_pairs(all_digits, 0)
    text = decode_pairs(pairs, test_mapping)
    wp = word_parse_score(text)
    bs = bigram_score(text)[0]
    delta = wp - baseline_wp
    return wp, bs, delta

def main():
    print("=" * 60)
    print("  FASE 2: ANALISIS DE CODIGOS GAP-ONLY")
    print("=" * 60)
    
    mapping = load_mapping(4)
    books = load_books()
    all_digits = "".join(books)
    
    # Baseline
    pairs_base = digits_to_pairs(all_digits, 0)
    text_base = decode_pairs(pairs_base, mapping)
    baseline_wp = word_parse_score(text_base)
    baseline_bs = bigram_score(text_base)[0]
    print(f"\nBaseline — Word parse: {baseline_wp:.3f} | Bigram: {baseline_bs:.3f}")
    
    # Encontrar gap-only codes
    gap_only, partial_gap, code_total, code_german = find_gap_only_codes(all_digits, mapping)
    
    print(f"\nCodigos GAP-ONLY (nunca en bigramas alemanes):")
    print(f"{'Codigo':<8} {'Letra':<6} {'Total':<8} {'EnAleman':<10} {'Ratio':<8}")
    print(f"{'-'*40}")
    for code, letter, total, german, ratio in sorted(gap_only, key=lambda x: -x[2]):
        print(f"  [{code}]   {letter:<6} {total:<8} {german:<10} {ratio:.3f}")
    
    print(f"\nTotal gap-only: {len(gap_only)} codigos, {sum(x[2] for x in gap_only)} ocurrencias")
    
    if partial_gap:
        print(f"\nCodigos PARCIALMENTE gap (<15% en bigrams alemanes):")
        for code, letter, total, german, ratio in sorted(partial_gap, key=lambda x: x[4]):
            print(f"  [{code}]   {letter:<6} {total:<8} {german:<10} {ratio:.3f}")
    
    # Frecuencias esperadas en alemán
    german_freq = {
        'E': 16.93, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'T': 6.15, 'R': 7.0,
        'A': 6.51, 'D': 5.08, 'H': 4.76, 'U': 4.35, 'L': 3.44, 'O': 2.51,
        'G': 3.01, 'C': 3.06, 'M': 2.53, 'K': 1.21, 'W': 1.89, 'B': 1.89,
        'F': 1.66, 'Z': 1.13, 'P': 0.79, 'V': 0.85
    }
    
    # Contar frecuencias actuales
    letter_counts = Counter()
    for p in pairs_base:
        if p in mapping:
            letter_counts[mapping[p]] += 1
    total_letters = sum(letter_counts.values())
    
    print(f"\nComparacion de frecuencias (actual vs esperado aleman):")
    print(f"{'Letra':<6} {'Actual%':<10} {'Esperado%':<10} {'Delta':<10} {'#Codigos':<10}")
    print(f"{'-'*46}")
    
    letter_to_codes = {}
    for code, letter in mapping.items():
        letter_to_codes.setdefault(letter, []).append(code)
    
    for letter in sorted(german_freq.keys(), key=lambda x: -german_freq[x]):
        actual_pct = letter_counts.get(letter, 0) / total_letters * 100
        expected_pct = german_freq.get(letter, 0)
        delta = actual_pct - expected_pct
        n_codes = len(letter_to_codes.get(letter, []))
        flag = " <<<" if abs(delta) > 1.5 else ""
        print(f"  {letter:<4}   {actual_pct:>7.2f}%   {expected_pct:>7.2f}%   {delta:>+7.2f}%   {n_codes:<10}{flag}")
    
    # Letras faltantes
    missing = [l for l in ['P', 'V', 'J', 'X', 'Y', 'Q'] if l not in letter_counts or letter_counts[l] == 0]
    if missing:
        print(f"\nLetras con 0 ocurrencias: {', '.join(missing)}")
    
    # Probar reasignaciones para los códigos gap-only más frecuentes
    print(f"\n{'='*60}")
    print(f"  PRUEBAS DE REASIGNACION")
    print(f"{'='*60}")
    
    # Letras sub-representadas (candidatas a recibir más códigos)
    under_rep = []
    for letter in german_freq:
        actual_pct = letter_counts.get(letter, 0) / total_letters * 100
        if german_freq[letter] - actual_pct > 0.5:
            under_rep.append((letter, german_freq[letter] - actual_pct))
    under_rep.sort(key=lambda x: -x[1])
    
    print(f"\nLetras sub-representadas (candidatas):")
    for letter, deficit in under_rep[:10]:
        print(f"  {letter}: deficit de {deficit:+.2f}%")
    
    # Para cada gap-only code, probar las letras sub-representadas
    best_improvements = []
    
    for code, current_letter, total, german, ratio in gap_only[:15]:  # top 15
        if total < 20:
            continue
        best_delta = 0
        best_letter = current_letter
        
        for target_letter, deficit in under_rep[:8]:
            wp, bs, delta = test_reassignment(all_digits, mapping, code, target_letter, baseline_wp)
            if delta > best_delta:
                best_delta = delta
                best_letter = target_letter
                best_wp = wp
                best_bs = bs
        
        if best_delta > 0:
            best_improvements.append((code, current_letter, best_letter, total, best_delta, best_wp))
    
    best_improvements.sort(key=lambda x: -x[4])
    
    print(f"\nMejores reasignaciones individuales:")
    print(f"{'Codigo':<8} {'De':<4} {'A':<4} {'Ocurr':<8} {'Delta WP':<10} {'Nuevo WP':<10}")
    print(f"{'-'*44}")
    for code, from_l, to_l, total, delta, wp in best_improvements:
        print(f"  [{code}]   {from_l:<4} {to_l:<4} {total:<8} {delta:>+.4f}    {wp:.4f}")
    
    # Aplicar las mejores N reasignaciones y medir impacto acumulativo
    print(f"\n{'='*60}")
    print(f"  REASIGNACION ACUMULATIVA (mejores cambios)")
    print(f"{'='*60}")
    
    cumulative_mapping = dict(mapping)
    cumulative_wp = baseline_wp
    
    applied = []
    for code, from_l, to_l, total, delta, wp in best_improvements:
        # Re-test with cumulative mapping
        test_map = dict(cumulative_mapping)
        test_map[code] = to_l
        pairs = digits_to_pairs(all_digits, 0)
        text = decode_pairs(pairs, test_map)
        new_wp = word_parse_score(text)
        if new_wp > cumulative_wp:
            cumulative_mapping[code] = to_l
            improvement = new_wp - cumulative_wp
            cumulative_wp = new_wp
            applied.append((code, from_l, to_l, total, improvement))
            print(f"  [{code}]: {from_l} -> {to_l} (x{total}) | WP: {cumulative_wp:.4f} (+{improvement:.4f})")
    
    print(f"\nTotal cambios aplicados: {len(applied)}")
    print(f"Word parse: {baseline_wp:.4f} -> {cumulative_wp:.4f} ({(cumulative_wp-baseline_wp)*100:+.1f}%)")
    
    # Mostrar texto decodificado con el mapeo mejorado
    pairs = digits_to_pairs(all_digits, 0)
    text = decode_pairs(pairs, cumulative_mapping)
    print_metrics("RESULTADO FASE 2 (mapeo mejorado)", text, pairs)
    
    # Guardar mapeo mejorado
    import json
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mapping_v5_agente3.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cumulative_mapping, f, ensure_ascii=False, indent=2)
    print(f"\nMapeo mejorado guardado en: {output_path}")

if __name__ == "__main__":
    main()
