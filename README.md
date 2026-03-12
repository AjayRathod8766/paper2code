# ⚡ Paper2Code
### Automated Transformation of AI/ML Research Papers into Executable Training Scripts

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-Ready-red?style=flat-square&logo=pytorch)](https://pytorch.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-Ready-orange?style=flat-square&logo=tensorflow)](https://tensorflow.org)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-blue?style=flat-square)](https://mlflow.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## 📌 What is Paper2Code?

**Paper2Code** is an end-to-end NLP automation system that reads AI/ML research papers (PDF) and automatically generates ready-to-run Python training scripts — eliminating the manual effort of reproducing experiments from academic papers.

> Upload a research paper → Get a working training script in seconds.

---

## 🎯 Key Features

- 📄 **PDF Parsing** — Extracts text page-by-page from any research paper
- 🧠 **Smart Extraction** — Identifies model architecture, dataset, optimizer, loss function, learning rate, epochs, batch size using NLP + regex
- ⚡ **Code Generation** — Renders production-quality training scripts using Jinja2 templates
- 🔀 **3 Smart Templates** — Auto-selects correct template based on task type:
  - PyTorch (Image Classification — ResNet, VGG, EfficientNet)
  - PyTorch NLP (Language Modeling — GPT, BERT, Transformer, LSTM)
  - TensorFlow / Keras
- 📊 **MLflow Integration** — Every generated script includes experiment tracking
- 🔧 **Error Handling** — Logging, debugging modules on every training step
- 🌐 **REST API** — Full Flask API with 5 endpoints
- 💻 **React Frontend** — Drag & drop UI with animated pipeline visualization

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| PDF Parsing | `pdfplumber` |
| NLP Extraction | `regex` + keyword matching |
| Code Generation | `Jinja2` templates |
| Backend API | `Flask` + `Flask-CORS` |
| Experiment Tracking | `MLflow` |
| Logging | `colorlog` |
| Frontend | `React.js` |
| Deep Learning Output | `PyTorch` / `TensorFlow` |

---

## 📁 Project Structure

```
paper2code/
├── main.py                              # Entry point (CLI + Server)
├── config.py                            # Central configuration
├── requirements.txt
├── app/
│   ├── parser/
│   │   ├── pdf_parser.py                # Extract text from PDF
│   │   └── text_cleaner.py              # Clean raw extracted text
│   ├── extractor/
│   │   └── info_extractor.py            # Extract model/hyperparams via NLP
│   ├── generator/
│   │   ├── code_generator.py            # Smart template selector + renderer
│   │   └── templates/
│   │       ├── pytorch_template.py      # PyTorch CNN training script
│   │       ├── pytorch_nlp_template.py  # PyTorch NLP/Transformer script
│   │       └── tensorflow_template.py   # TensorFlow/Keras script
│   ├── logger/
│   │   └── logger.py                    # Colored logging + file logging
│   └── api/
│       └── routes.py                    # Flask REST API (5 endpoints)
└── outputs/                             # Generated .py scripts saved here
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/AjayRathod8766/paper2code.git
cd paper2code
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install pdfplumber flask flask-cors jinja2 colorlog python-dotenv mlflow
```

### 4. Start the server
```bash
python main.py --server
```

### 5. Or use CLI directly
```bash
python main.py --pdf your_paper.pdf --framework pytorch
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/generate` | Upload PDF → get training script |
| `POST` | `/api/generate/text` | Send raw text → get training script |
| `GET` | `/api/outputs` | List all generated scripts |
| `GET` | `/api/outputs/<file>` | Download a generated script |
| `GET` | `/api/health` | Health check |

### Example API Call
```python
import requests

with open("resnet_paper.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:5000/api/generate",
        files={"file": f},
        data={"framework": "pytorch"}
    )

result = response.json()
print(result["info"])   # Extracted: model, dataset, lr, epochs...
print(result["code"])   # Full training script
```

---

## 📊 What Gets Extracted

| Field | Example (ResNet paper) | Example (GPT paper) |
|-------|----------------------|-------------------|
| Model | `ResNet` | `GPT` |
| Dataset | `ImageNet` | `CustomDataset` |
| Framework | `pytorch` | `pytorch` |
| Task | `image_classification` | `language_modeling` |
| Optimizer | `SGD` | `Adam` |
| Loss | `CrossEntropyLoss` | `CrossEntropyLoss` |
| Epochs | `90` | `10` |
| Batch Size | `256` | `32` |
| Learning Rate | `0.1` | `0.001` |

---

## 🧪 Test Results

| Metric | Result |
|--------|--------|
| Papers Tested | 10 |
| Successful Code Generation | 8 (80%) |
| Frameworks Supported | PyTorch, TensorFlow |
| Template Types | 3 (CNN, NLP, TF) |
| Average Setup Time Reduction | ~65% |

---

## 💡 Generated Script Features

Every auto-generated training script includes:

- ✅ Full training loop with epoch logging
- ✅ Validation loop with accuracy / perplexity tracking
- ✅ Optimizer + learning rate scheduler
- ✅ Model checkpointing (saves best model)
- ✅ MLflow experiment tracking
- ✅ Error handling on every batch
- ✅ CUDA / CPU auto-detection
- ✅ Gradient clipping (NLP models)
- ✅ Causal attention mask (Transformer models)

---

## 🖥️ Frontend UI

The React frontend provides:
- Drag & drop PDF upload
- PyTorch / TensorFlow framework selector
- Animated 5-step pipeline visualization
- Extracted info dashboard (10 fields)
- Syntax-highlighted code viewer
- One-click `.py` file download

---

## 👤 Author

**Ajay Rathod**
- 📧 ajaysr2022@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/ajay-rathod-1507aa36b)
- 🐙 [GitHub](https://github.com/AjayRathod8766)

---

## 📄 License

This project is licensed under the MIT License.

---

⭐ **If this project helped you, please give it a star!**
