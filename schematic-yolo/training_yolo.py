from ultralytics import YOLO

def train_model():
    # Încarcă modelul (YOLOv8s este recomandarea noastră pentru precizie)
    model = YOLO('yolov8s.pt')

    # Pornește antrenarea
    results = model.train(
        data='dataset.yaml',      # Asigură-te că path-urile din yaml sunt corecte
        epochs=300,
        imgsz=1024,
        batch=8,                  # Ajustează dacă primești Out of Memory pe GPU
        device=0,                 # Folosește GPU-ul RTX A1000
        workers=4,                # Numărul de nuclee procesor folosite pentru încărcarea datelor
        name='tiled_yolov8s_v2'
    )

# ACEASTA ESTE LINIA CRITICĂ PENTRU WINDOWS:
if __name__ == '__main__':
    train_model()