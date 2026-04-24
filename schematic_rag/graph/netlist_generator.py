

def generate_netlist(G):
    netlist = []
    # Iterăm prin nodurile care arată a componente (ex: R101, C7)
    for node, data in G.nodes(data=True):
        # Verificăm tipul sau dacă numele nodului conține litere+cifre (fallback)
        if data.get("type") == "component" or any(char.isdigit() for char in str(node)):
            neighbors = list(G.neighbors(node))
            # Filtrăm vecinii să nu fie nodul însuși sau zgomot
            nets = [n for n in neighbors if n != node and str(n).lower() != 'link']
            
            if nets:
                # Format standard: Componentă Net1 Net2 ...
                line = f"{node} {' '.join(nets)}"
                netlist.append(line)

    return netlist