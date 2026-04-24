import re

def infer_connections(text):
    connections = []
    # Curățăm textul: adăugăm spațiu între cifre și litere (ex: RN1740 -> RN 1740)
    cleaned_text = re.sub(r'(\d)([A-Z])', r'\1 \2', text)
    
    lines = cleaned_text.split("\n")
    for line in lines:
        # Regex îmbunătățit:
        # [A-Z]{1,3} -> permite prefixe de 1 până la 3 litere (C, R, IC, XDM, RN, CN)
        # \d+ -> urmează cifre
        pattern = r'\b([A-Z]{1,4}\d+[A-Z0-9]*)\b'
        comps = re.findall(pattern, text.upper())
        
        # Nets: GND, VCC, etc.
        # În net_inference.py
        nets = [n for n in re.findall(r'\b(GND|VCC|3V3|[A-Z_]{3,})\b', line) if n.lower() != 'link']

        if comps:
            for c in comps:
                if nets:
                    for n in nets:
                        if c != n:
                            connections.append((c, n, "link"))
                else:
                    connections.append((c, c, "exists")) 
    return connections