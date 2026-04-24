
import re

def extract_components(text):
    pattern = r'\b(IC\d+|R\d+|C\d+|L\d+|X\d+)\b'
    return list(set(re.findall(pattern, text)))
