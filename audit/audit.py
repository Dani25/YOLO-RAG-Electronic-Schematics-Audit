import os
import re

def perform_netlist_vision_audit(netlist_path, yolo_detections_dir):
    # 1. Extragem componentele din Netlist (.net)
    if not os.path.exists(netlist_path):
        print(f"Eroare: Nu s-a gasit fisierul .net la {netlist_path}")
        return
        
    with open(netlist_path, 'r') as f:
        lines = f.readlines()
    
    all_components = set()
    for line in lines:
        line = line.strip()
        if not line or line.startswith('*'):
            continue
        
        parts = line.split()
        if parts:
            comp_id = parts[0]
            # Filtrare termeni care nu sunt componente discrete
            if comp_id not in ['exists', 'GND', 'VDD', 'PIN', 'Netlist', 'CAD']:
                all_components.add(comp_id)
    
    # 2. Numaram detecțiile YOLO
    yolo_count = 0
    if os.path.exists(yolo_detections_dir):
        for file in os.listdir(yolo_detections_dir):
            if file.endswith(".txt"):
                with open(os.path.join(yolo_detections_dir, file), 'r') as f:
                    yolo_count += len(f.readlines())

    # 3. Rezultate Audit
    total_rag = len(all_components)
    
    print(f"--- Multimodal Audit Report ---")
    print(f"Total Unique Components in Netlist (RAG): {total_rag}")
    print(f"Symbols detected by YOLO (Vision): {yolo_count}")
    
    # Calculam acuratetea fata de totalul de componente
    diff = abs(total_rag - yolo_count)
    accuracy = (1 - diff / max(total_rag, yolo_count)) * 100
    
    print(f"Discrepancy: {diff} units")
    print(f"Multimodal Consistency Score: {accuracy:.2f}%")
    
    return all_components, yolo_count

if __name__ == "__main__":
    net_path = r'C:\Users\User\schematic-multimodal-rag\experiments\results\net3.net'
    yolo_path = r'C:\Users\User\schematic-yolo\dataset_tiled\specific_labels_for_net3'
    perform_netlist_vision_audit(net_path, yolo_path)