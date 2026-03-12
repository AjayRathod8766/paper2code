# 📄 Paper2Code

> Automatically transform AI/ML research papers into executable Python training scripts.

## 🧠 What It Does

Paper2Code reads a research paper (PDF), extracts the model architecture, dataset, hyperparameters, optimizer, and loss function using NLP — then generates a ready-to-run PyTorch or TensorFlow training script with logging and MLflow experiment tracking.

---

## 📁 Project Structure

```
paper2code/
├── main.py                          # Entry point (CLI + Server)
├── config.py                        # All configuration
├── requirements.txt
├── app/
│   ├── parser/
│   │   ├── pdf_parser.py            # Extract text from PDF
│   │   └── text_cleaner.py          # Clean raw extracted text
│   ├── extractor/
│   │   └── info_extractor.py        # Extract model/hyperparams via regex+NLP
│   ├── generator/
│   │   ├── code_generator.py        # Render Jinja2 training templates
│   │   └── templates/
│   │       ├── pytorch_template.py  # PyTorch training script template
│   │       └── tensorflow_template.py
│   ├── logger/
│   │   └── logger.py                # Colored logging + file logging
│   └── api/
│       └── routes.py                # Flask REST API
├── outputs/                         # Generated .py scripts saved here
├── logs/                            # Auto-created log files
└── sample_papers/                   # Put test PDFs here
```

---

## ⚙️ Setup

```bash
# 1. Clone / enter project folder
cd paper2code

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

### Option 1 — CLI (Process a PDF directly)
```bash
python main.py --pdf sample_papers/resnet_paper.pdf
python main.py --pdf sample_papers/resnet_paper.pdf --framework pytorch
```

### Option 2 — Flask API Server
```bash
python main.py --server
```

#### API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/generate` | Upload PDF → get code |
| POST | `/api/generate/text` | Send raw text → get code |
| GET  | `/api/outputs` | List all generated scripts |
| GET  | `/api/outputs/<file>` | Download a script |
| GET  | `/api/health` | Health check |

#### Example API call (Python)
```python
import requests

with open("paper.pdf", "rb") as f:
    res = requests.post(
        "http://localhost:5000/api/generate",
        files={"file": f},
        data={"framework": "pytorch"}
    )
print(res.json()["info"])    # Extracted info
print(res.json()["code"])    # Generated training script
```

#### Example API call (curl)
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "file=@paper.pdf" \
  -F "framework=pytorch"
```

---

## 📊 What Gets Extracted

| Field | Example |
|-------|---------|
| model | ResNet |
| dataset | CIFAR-10 |
| framework | pytorch |
| task | image_classification |
| optimizer | Adam |
| loss | CrossEntropyLoss |
| epochs | 100 |
| batch_size | 64 |
| lr | 0.001 |
| num_classes | 10 |

---

## 🔬 Experiment Tracking (MLflow)

Generated scripts automatically log to MLflow.

```bash
# After running training, view results:
mlflow ui
# Open: http://localhost:5000
```

---

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| PDF Parsing | pdfplumber |
| NLP Extraction | regex + keyword matching |
| Code Generation | Jinja2 templates |
| API | Flask + Flask-CORS |
| Experiment Tracking | MLflow |
| Logging | colorlog |
| Deep Learning | PyTorch / TensorFlow |

---

## 👤 Author
Ajay Rathod — Paper2Code Project  
GitHub: github.com/AjayRathod8766
