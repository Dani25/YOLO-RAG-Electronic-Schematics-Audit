import pytesseract
import cv2

def ocr_image(image_path):
    """
    Extract text from an image using Tesseract OCR
    """

    img = cv2.imread(image_path)

    # Preprocessing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(thresh)

    return text


def ocr_pdf_images(images):
    """
    OCR multiple images extracted from PDF
    """
    texts = []

    for img in images:
        texts.append(ocr_image(img))

    return "\n".join(texts)
