# experiments/run_pipeline.py
import os
import sys
import time
import pandas as pd
from pathlib import Path
from datetime import datetime

# Configurare path-uri
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, ".."))
src_path = os.path.join(root_path, "src")

if src_path not in sys.path:
    sys.path.insert(0, src_path)
if root_path not in sys.path:
    sys.path.insert(0, root_path)

try:
    from schematic_rag.parsing.pdf_parser import extract_text 
    from schematic_rag.graph.net_inference import infer_connections 
    from schematic_rag.graph.graph_builder import build_graph 
    from schematic_rag.evaluation.metrics import evaluate_components, graph_density
    from schematic_rag.bom_loader import load_bom
    from schematic_rag.graph.netlist_generator import generate_netlist
except ImportError as e:
    print(f"❌ Eroare la importul modulelor: {e}")
    sys.exit(1)

def run_experiment(pdf_path, bom_path):
    print(f"\n🔍 Procesare document: {os.path.basename(pdf_path)}")
    start_time = time.time()

    # --- PASUL 1 & 2: Parsare și Construcție Graf ---
    text = extract_text(pdf_path)
    connections = infer_connections(text)
    G = build_graph(connections)

    gt_components = []
    if os.path.exists(bom_path):
        try:
            df_bom = load_bom(bom_path)
            import re
            
            df_bom.columns = [str(c).strip() for c in df_bom.columns]
            cols = df_bom.columns.tolist()
            
            p_col = next((c for c in cols if c.upper() in ['PREFIX', 'DESIGNATOR PREFIX']), None)
            n_col = next((c for c in cols if c.upper() in ['REFDESNO', 'REFNO', 'DESIGNATOR NUMBER']), None)
            full_col = next((c for c in cols if c.upper() in ['REFDES', 'REFERENCE', 'REFERENCE DESIGNATOR', 'REF.-DESIGNATOR']), None)

            found_refs = []

            # LOGICA 1: PRIORITATE MAXIMĂ - Dacă avem coloane separate (A2C..., bom.xlsx)
            if p_col and n_col:
                print(f"🔗 Format detectat: Unire {p_col} + {n_col}")
                for idx in df_bom.index:
                    p = str(df_bom.at[idx, p_col]).strip().upper()
                    n = str(df_bom.at[idx, n_col]).strip()
                    n = re.sub(r'\.0$', '', n) 
                    if p != 'NAN' and n != 'NAN' and n.replace('-','').isdigit() and len(p) <= 3:
                        found_refs.append(p + n)

            # LOGICA 2: PRIORITATE SECUNDARĂ - Dacă nu avem coloane separate, dar avem una completă (HUD2G, PSA)
            elif full_col:
                print(f"📜 Format detectat: Coloană completă {full_col}")
                for val in df_bom[full_col].dropna().astype(str):
                    # re.findall prinde listele din PSA (C1, C2)
                    matches = re.findall(r'\b([A-Z]{1,3}\d+[A-Z0-9]*)\b', val.upper())
                    found_refs.extend(matches)

            # LOGICA 3: FALLBACK - Doar dacă primele două au eșuat complet
            else:
                print("⚠️ Nicio coloană standard găsită. Scanare globală...")
                for col in cols:
                    if any(x in col.upper() for x in ['PART', 'VALUE', 'MATERIAL', 'SAP']): continue
                    for val in df_bom[col].dropna().astype(str):
                        matches = re.findall(r'\b([A-Z]{1,3}\d+[A-Z0-9]*)\b', val.upper())
                        found_refs.extend(matches)

            # FILTRARE FINALĂ
            gt_components = list(set([r for r in found_refs if 2 <= len(r) <= 12 and r != 'NAN']))
            
            print(f"✅ Identificate {len(gt_components)} piese unice.")
            if gt_components:
                print(f"🔍 Mostră: {sorted(gt_components)[:15]}")
                    
        except Exception as e:
            print(f"⚠️ Eroare la procesare: {e}")
    # --- PASUL 4: Evaluare și Statistici ---
    predicted_nodes = list(G.nodes)
    comp_acc = evaluate_components(predicted_nodes, gt_components)
    density = graph_density(G)
    runtime = time.time() - start_time

    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file": os.path.basename(pdf_path),
        "runtime_sec": round(runtime, 3),
        "nodes": len(G.nodes),
        "edges": len(G.edges),
        "density": round(density, 2),
        "comp_accuracy": round(comp_acc, 2),
        "conn_accuracy": 0.0
    }

    print(f"🎯 Match-uri componente: {int(comp_acc * len(gt_components)) if gt_components else 0} din {len(gt_components)}")
    return result, G

import glob

import glob

if __name__ == "__main__":
    # 1. Identificăm toate PDF-urile din folder (data/sample1, data/sample2, etc)
    pdf_files = glob.glob("data/sample1/*.pdf")
    
    # 2. Găsim cel mai recent fișier Excel sau CSV (BOM-ul universal)
    bom_files = glob.glob("data/sample1/*.xlsx") + glob.glob("data/sample1/*.csv")
    
    if not pdf_files:
        print("⚠️ Nu am găsit niciun PDF în folder")
    elif not bom_files:
        print("⚠️ Nu am găsit niciun fișier BOM (.xlsx sau .csv)")
    else:
        # Sortăm BOM-urile după data modificării și îl luăm pe ultimul (cel mai nou)
        latest_bom = max(bom_files, key=os.path.getmtime)
        print(f"📊 Folosim cel mai recent BOM detectat: {os.path.basename(latest_bom)}")

        for pdf_path in pdf_files:
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            print(f"\n🔄 Procesare: {base_name}.pdf")
            
            try:
                # Rulăm experimentul folosind același BOM pentru toate PDF-urile detectate
                final_data, G = run_experiment(pdf_path, latest_bom)
                
                # Salvare în istoric
                output_path = Path("experiments/results/results_history.csv")
                df_current = pd.DataFrame([final_data])
                df_current.to_csv(output_path, mode='a', header=not output_path.exists(), index=False)
                
                # Salvare Netlist individual
                netlist_file = Path(f"experiments/results/{base_name}.net")
                from schematic_rag.graph.netlist_generator import generate_netlist
                extracted_netlist = generate_netlist(G)
                with open(netlist_file, "w") as f:
                    f.write(f"* Netlist extras automat din: {pdf_path}\n")
                    f.write(f"* Folosind BOM: {latest_bom}\n\n")
                    f.write("\n".join(extracted_netlist))
                
                print(f"✅ Succes: {base_name}")
            except Exception as e:
                print(f"❌ Eroare la {base_name}: {e}")