import networkx as nx
import matplotlib.pyplot as plt
import os

def visualize_component_subgraph(netlist_path, target_component, output_image="subgraph.png"):
    """
    Încarcă un fișier .net și generează un graf de conexiuni pentru o componentă specifică.
    """
    G = nx.Graph()
    
    if not os.path.exists(netlist_path):
        print(f" Eroare: Fișierul {netlist_path} nu a fost găsit.")
        return

    # 1. Parsarea fișierului Netlist
    with open(netlist_path, 'r') as f:
        for line in f:
            if line.startswith("*") or not line.strip():
                continue
            
            parts = line.strip().split()
            comp = parts[0]
            nets = parts[1:]
            
            # Adăugăm componenta și tipul ei
            G.add_node(comp, type="component", color='skyblue')
            
            for net in nets:
                if net.lower() == 'exists' or net.lower() == 'link':
                    continue
                # Adăugăm net-ul și tipul lui
                G.add_node(net, type="net", color='orange')
                G.add_edge(comp, net)

    # 2. Extragerea Ego-Graph-ului (componenta țintă și vecinii ei)
    if target_component not in G:
        print(f" Componenta {target_component} nu a fost găsită în netlist.")
        print(f"Mostră de componente disponibile: {list(G.nodes)[:10]}")
        return

    ego_graph = nx.ego_graph(G, target_component)
    
    # 3. Vizualizare
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(ego_graph, k=0.5, iterations=50)
    
    # Culori în funcție de tipul nodului
    colors = [ego_graph.nodes[n].get('color', 'grey') for n in ego_graph.nodes]
    
    nx.draw(ego_graph, pos, 
            with_labels=True, 
            node_color=colors, 
            node_size=2000, 
            font_size=10, 
            font_weight='bold',
            edge_color='gray',
            alpha=0.9)
    
    plt.title(f"Network Topology Sub-graph: {target_component}\n(Extracted from {os.path.basename(netlist_path)})")
    plt.savefig(output_image, bbox_inches='tight', dpi=300)
    print(f"✅ Vizualizare salvată în: {output_image}")

visualize_component_subgraph(
    netlist_path="net1.net", 
    target_component="CR8000", 
    output_image="net1.png"
)