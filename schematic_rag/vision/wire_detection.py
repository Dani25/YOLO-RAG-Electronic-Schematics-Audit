
import cv2
import numpy as np
from skimage.morphology import skeletonize

def detect_wires(image_path):
    img = cv2.imread(image_path, 0)

    # 1. Binarization
    _, binary = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

    # 2. Edge detection
    edges = cv2.Canny(binary, 50, 150)

    # 3. Skeletonization
    skeleton = skeletonize(edges // 255)

    return skeleton
