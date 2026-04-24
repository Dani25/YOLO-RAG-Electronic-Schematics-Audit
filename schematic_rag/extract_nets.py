
import re

def extract_nets(text):
    bus = re.findall(r'[A-Z_]+\[\d+\]', text)
    signals = re.findall(r'\b[A-Z_]{3,}\b', text)
    return list(set(bus + signals))
