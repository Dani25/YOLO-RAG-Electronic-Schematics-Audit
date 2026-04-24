# YOLO-RAG-Electronic-Schematics-Audit


# Multimodal Schematic Extraction & Automated Audit Platform

This project implements an advanced solution for the digitization and verification of complex electrical schematics within the automotive industry. The system utilizes a multimodal approach, fusing **Computer Vision (YOLOv8)**, **Retrieval-Augmented Generation (RAG)**, and **Graph Theory** to extract high-fidelity netlists from unstructured PDF documents.

##  System Architecture

The project is divided into two primary modules that collaborate to transform raw PDF data into a structured electrical model.

### 1. Vision Layer (`/schematic-yolo`)
Handles visual processing for high-density industrial documents.
* **Tiling Engine:** Converts PDFs to 300 DPI and partitions them into 1024 xs 1024 tiles to preserve small-scale component details.
* **Symbol Detection:** A YOLOv8s model fine-tuned for electronic symbol recognition according to industrial standards.
* **Performance:** Achieves a **97.8% mAP** (mean Average Precision).

### 2. Reasoning & Extraction Layer (`/schematic_rag`)
Interprets extracted data and reconstructs the circuit logic.
* **Multimodal Fusion:** Cross-references visual detections with OCR-extracted text to eliminate LLM "hallucinations."
* **Graph Reconstruction:** Converts detected entities into a connectivity graph using NetworkX.
* **Automated Audit:** Compares generated netlists against **BOM (Bill of Materials)** files to validate data integrity.

---

## Repository Structure

```text
.
├── schematic-yolo/          # Vision training and processing pipeline
│   ├── tiling_engine.py     # Script for high-res PDF partitioning
│   └── training_yolo.py     # Script for training the YOLOv8 model
├── schematic_rag/           # Logic, Analysis, and Netlist generation pipeline
│   ├── run_pipeline.py      # Main entry point for the system
│   ├── rag/                 # LLM reasoning and Context Retriever logic
│   ├── graph/               # Netlist generators and graph builders
│   └── evaluation/          # Accuracy calculation and metrics scripts
├── lib/                     # External libraries for graph visualization (JS/CSS)
└── requirements.txt         # Project dependencies (OpenCV, Ultralytics, LangChain)
```

---

## Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/user/schematic-audit-platform.git
   cd schematic-audit-platform
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Data Preparation:**
   * Place your schematic PDFs in `schematic_rag/data/`.
   

4. **Run the Pipeline:**
   ```bash
   python schematic_rag/run_pipeline.py
   ```

---

## 📊 Results & Validation

The system was evaluated using real-world datasets from automotive manufacturers, achieving the following benchmarks:
* **Symbol Detection (mAP):** 97.8%
* **Netlist Accuracy (vs. BOM):** 96.2%
* **Processing Time:** < 45 seconds per complex A3 schematic page.

---

## ⚖️ License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

> **Note:** Data directories (`data/`, `raw_pdfs/`) are intentionally left empty to comply with Non-Disclosure Agreements (NDA). Users must provide their own datasets for testing and evaluation.

---

### Pro-Tips for your GitHub:
* **Requirements:** Make sure your `requirements.txt` is updated with the exact versions you used.
* **Weights:** If you include `best.pt`, remember that it goes in the `models/` or `weights/` folder as discussed.
* **Security:** Double-check that no private API keys are hardcoded in `llm_reasoner.py` before uploading!

Do you have everything ready for the upload? If you need a specific follow-up on how to handle the `lib` folder or the JS visualizations, let me know!
