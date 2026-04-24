import os
import cv2
import numpy as np
import fitz  # PyMuPDF
from pathlib import Path

# --- CONFIGURARE ---
PDF_DIR = Path(r"..schematic-yolo\raw_pdfs")
BASE_DIR = Path(r"..schematic-yolo\dataset_tiled")
IMG_DIR = BASE_DIR / "images"
LBL_DIR = BASE_DIR / "labels"

for d in [IMG_DIR, LBL_DIR]: d.mkdir(parents=True, exist_ok=True)

TILE_SIZE = 1024
OVERLAP = 200
DPI = 300

def process_to_tiles():
   
    for pdf_path in PDF_DIR.glob("*.pdf"):
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            zoom = DPI / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # 1. Convertire buffer în numpy array
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
            
            # 2. PyMuPDF scoate RGB, OpenCV are nevoie de BGR
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            
            h_img, w_img = img.shape[:2]
            print(f"📄 Procesez {pdf_path.name} pg {page_num} - Rezoluție: {w_img}x{h_img}")
            
            # 3. Logica de Tiling
            count = 0
            for y in range(0, h_img - OVERLAP, TILE_SIZE - OVERLAP):
                for x in range(0, w_img - OVERLAP, TILE_SIZE - OVERLAP):
                    y2 = min(y + TILE_SIZE, h_img)
                    x2 = min(x + TILE_SIZE, w_img)
                    
                    tile = img[y:y2, x:x2]
                    
                    if tile.shape[0] < 100 or tile.shape[1] < 100: continue
                    
                    tile_name = f"{pdf_path.stem}_p{page_num}_y{y}_x{x}.jpg"
                    cv2.imwrite(str(IMG_DIR / tile_name), tile)
                    count += 1
            
            print(f"   ✅ Generate {count} tile-uri pentru pagina {page_num}")

if __name__ == "__main__":
    process_to_tiles()