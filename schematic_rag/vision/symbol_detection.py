import cv2
import numpy as np

def detect_symbols(image_path):
    """
    Basic symbol detection using contours.
    (Replace later with YOLO for research-grade)
    """

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    symbols = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Filter small noise
        if w > 20 and h > 20:
            symbols.append({
                "bbox": (x, y, w, h),
                "area": w * h
            })

    return symbols
