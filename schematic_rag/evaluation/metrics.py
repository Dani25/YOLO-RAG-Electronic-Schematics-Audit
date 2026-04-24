
import re
import re

def evaluate_components(pred, gt):
    # 1. Curățăm orice text de caractere speciale și spații
    def total_clean(s):
        return re.sub(r'[^A-Z0-9]', '', str(s).upper())

    # Curățăm setul prezis și setul din BOM
    pred_cleaned = {total_clean(p) for p in pred if p}
    gt_cleaned = {total_clean(g) for g in gt if g}
    
    if not gt_cleaned:
        return 0.0
    
    hits = 0
    # 2. Verificăm fiecare piesă din BOM în "marea" de date găsită de AI
    for target in gt_cleaned:
        # Verificăm dacă identificatorul (ex: C101) există ca atare sau 
        # dacă este "îngropat" într-un nod mai lung (ex: C101HUD)
        if target in pred_cleaned or any(target in p for p in pred_cleaned):
            hits += 1
            
    # Afișăm în consolă pentru confirmare
    if hits > 0:
        print(f"🎯 Match-uri reale găsite: {hits} din {len(gt_cleaned)}")
        
    return hits / len(gt_cleaned)

def evaluate_connections(pred_edges, gt_edges):
    """
    Calculează acuratețea netlist-ului.
    """
    pred_set = set(tuple(sorted(map(str, e))) for e in pred_edges)
    gt_set = set(tuple(sorted(map(str, e))) for e in gt_edges)

    if not gt_set: return 0
    
    correct = len(pred_set & gt_set)
    return correct / len(gt_set)

def graph_density(G):
    """
    Măsoară complexitatea grafului.
    """
    n = len(G.nodes)
    if n < 2: return 0
    return len(G.edges) / n