
from pyvis.network import Network
import streamlit.components.v1 as components
import os

def visualize_graph(G):
    # Inițializăm rețeaua FĂRĂ setări de notebook
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
    
    # Adăugăm nodurile și muchiile din graful NetworkX (G)
    net.from_nx(G)

    # Opțional: Personalizare culori noduri direct aici dacă nu ai făcut-o deja
    for node in net.nodes:
        node["color"] = "red" if "IC" in node["id"] else "blue"

    # SALVARE: Aceasta este partea critică pentru a evita eroarea .render()
    # Dezactivăm notebook=False pentru a evita bug-ul PyVis
    path = "graph.html"
    net.save_graph(path)

    # CITIRE ȘI AFIȘARE în Streamlit
    with open(path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        components.html(html_content, height=650)