import networkx as nx

def build_graph(connections):
    """
    Construiește graful folosind lista de conexiuni.
    connections: lista de tuple-uri (componenta, net1, net2)
    """
    G = nx.Graph()
    
    if not connections:
        return G

    for item in connections:
        # Verificăm dacă item-ul are formatul corect (trio)
        if len(item) == 3:
            comp, net1, net2 = item
            G.add_node(comp, type="component")
            G.add_node(net1, type="net")
            G.add_node(net2, type="net")
            G.add_edge(comp, net1)
            G.add_edge(comp, net2)
            
    return G