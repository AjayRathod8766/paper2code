"""
app/extractor/info_extractor.py
The brain of Paper2Code.

Extracts:
  - Model architecture name
  - Dataset name
  - Hyperparameters (lr, epochs, batch size)
  - Optimizer
  - Loss function
  - Framework hint (PyTorch / TensorFlow)
  - Task type (classification, detection, NLP, etc.)

Uses regex + keyword matching — no heavy NLP dependency needed.
"""

import re
from app.logger.logger import get_logger
from config import (
    DEFAULT_LR, DEFAULT_EPOCHS, DEFAULT_BATCH_SIZE,
    DEFAULT_OPTIMIZER, DEFAULT_LOSS, DEFAULT_FRAMEWORK
)

log = get_logger(__name__)


class InfoExtractor:
    """
    Extracts structured ML info from cleaned paper text.

    Example:
        extractor = InfoExtractor()
        info = extractor.extract(clean_text)
        print(info)
    """

    # ── Known model architectures ─────────────────────────────
    KNOWN_MODELS = [
        "ResNet", "VGG", "AlexNet", "GoogLeNet", "Inception",
        "EfficientNet", "MobileNet", "DenseNet", "BERT", "GPT",
        "Transformer", "LSTM", "GRU", "RNN", "U-Net", "YOLO",
        "GAN", "VAE", "ViT", "T5", "XGBoost", "Random Forest",
    ]

    # ── Known datasets ────────────────────────────────────────
    KNOWN_DATASETS = [
        "ImageNet", "CIFAR-10", "CIFAR-100", "MNIST", "COCO",
        "Pascal VOC", "WikiText", "Penn Treebank", "SQuAD",
        "GLUE", "IMDb", "Reuters", "SVHN", "STL-10", "CelebA",
    ]

    # ── Known optimizers ─────────────────────────────────────
    KNOWN_OPTIMIZERS = [
        "Adam", "SGD", "AdaGrad", "RMSProp", "AdamW",
        "Adagrad", "Adadelta", "LBFGS", "Rprop",
    ]

    # ── Known loss functions ──────────────────────────────────
    KNOWN_LOSSES = [
        "CrossEntropyLoss", "MSELoss", "BCELoss", "NLLLoss",
        "HuberLoss", "L1Loss", "CTCLoss", "KLDivLoss",
        "cross entropy", "mean squared error", "binary cross entropy",
    ]

    def extract(self, text: str) -> dict:
        """
        Returns a dict with all extracted paper metadata.
        Falls back to safe defaults for anything not found.
        """
        log.info("Starting information extraction...")

        result = {
            "model":       self._extract_model(text),
            "dataset":     self._extract_dataset(text),
            "framework":   self._extract_framework(text),
            "task":        self._extract_task(text),
            "optimizer":   self._extract_optimizer(text),
            "loss":        self._extract_loss(text),
            "epochs":      self._extract_epochs(text),
            "batch_size":  self._extract_batch_size(text),
            "lr":          self._extract_lr(text),
            "num_classes": self._extract_num_classes(text),
        }

        log.info(f"Extraction complete: {result}")
        return result

    # ── Extractors ────────────────────────────────────────────

    def _extract_model(self, text: str) -> str:
        for model in self.KNOWN_MODELS:
            if re.search(rf"\b{re.escape(model)}\b", text, re.IGNORECASE):
                log.debug(f"Model found: {model}")
                return model
        log.warning("Model not found — using 'CustomModel'")
        return "CustomModel"

    def _extract_dataset(self, text: str) -> str:
        for ds in self.KNOWN_DATASETS:
            if re.search(rf"\b{re.escape(ds)}\b", text, re.IGNORECASE):
                log.debug(f"Dataset found: {ds}")
                return ds
        log.warning("Dataset not found — using 'CustomDataset'")
        return "CustomDataset"

    def _extract_framework(self, text: str) -> str:
        text_lower = text.lower()
        if "pytorch" in text_lower or "torch" in text_lower:
            return "pytorch"
        if "tensorflow" in text_lower or "keras" in text_lower:
            return "tensorflow"
        log.warning(f"Framework not detected — defaulting to '{DEFAULT_FRAMEWORK}'")
        return DEFAULT_FRAMEWORK

    def _extract_task(self, text: str) -> str:
        text_lower = text.lower()
        if any(k in text_lower for k in ["object detection", "bounding box"]):
            return "object_detection"
        if any(k in text_lower for k in ["image segmentation", "semantic segmentation"]):
            return "segmentation"
        if any(k in text_lower for k in ["text classification", "sentiment"]):
            return "text_classification"
        if any(k in text_lower for k in ["language model", "text generation"]):
            return "language_modeling"
        if any(k in text_lower for k in ["image classification", "classify"]):
            return "image_classification"
        return "image_classification"

    def _extract_optimizer(self, text: str) -> str:
        for opt in self.KNOWN_OPTIMIZERS:
            if re.search(rf"\b{re.escape(opt)}\b", text, re.IGNORECASE):
                log.debug(f"Optimizer found: {opt}")
                return opt
        return DEFAULT_OPTIMIZER

    def _extract_loss(self, text: str) -> str:
        for loss in self.KNOWN_LOSSES:
            if re.search(rf"\b{re.escape(loss)}\b", text, re.IGNORECASE):
                log.debug(f"Loss found: {loss}")
                # normalize common text variants
                if "cross entropy" in loss.lower():
                    return "CrossEntropyLoss"
                if "mean squared" in loss.lower():
                    return "MSELoss"
                if "binary cross" in loss.lower():
                    return "BCELoss"
                return loss
        return DEFAULT_LOSS

    def _extract_epochs(self, text: str) -> int:
        patterns = [
            r"(?:train(?:ed)?\s+for|epochs?\s*[=:of]+)\s*(\d+)\s*epochs?",
            r"(\d+)\s*training\s*epochs?",
            r"epochs?\s*=\s*(\d+)",
        ]
        for pat in patterns:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                val = int(match.group(1))
                if 1 <= val <= 1000:
                    log.debug(f"Epochs found: {val}")
                    return val
        return DEFAULT_EPOCHS

    def _extract_batch_size(self, text: str) -> int:
        patterns = [
            r"batch\s*size\s*(?:of|=|:)?\s*(\d+)",
            r"mini[- ]batch\s*(?:of|=|:)?\s*(\d+)",
            r"(\d+)[- ]sample\s*(?:mini[- ])?batch",
        ]
        for pat in patterns:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                val = int(match.group(1))
                if 1 <= val <= 4096:
                    log.debug(f"Batch size found: {val}")
                    return val
        return DEFAULT_BATCH_SIZE

    def _extract_lr(self, text: str) -> float:
        patterns = [
            r"learning\s*rate\s*(?:of|=|:)?\s*([\d.e\-]+)",
            r"lr\s*(?:of|=|:)?\s*([\d.e\-]+)",
            r"(?:lr|learning rate)\s*=\s*([\d.e\-]+)",
        ]
        for pat in patterns:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                try:
                    val = float(match.group(1))
                    if 1e-7 <= val <= 1.0:
                        log.debug(f"Learning rate found: {val}")
                        return val
                except ValueError:
                    pass
        return DEFAULT_LR

    def _extract_num_classes(self, text: str) -> int:
        patterns = [
            r"(\d+)\s*(?:output\s*)?classes",
            r"num_classes\s*=\s*(\d+)",
            r"(\d+)[- ]class\s*(?:classification)?",
        ]
        for pat in patterns:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                val = int(match.group(1))
                if 2 <= val <= 100000:
                    log.debug(f"Num classes found: {val}")
                    return val
        # Guess from known datasets
        if "CIFAR-10" in text or "MNIST" in text:
            return 10
        if "CIFAR-100" in text:
            return 100
        if "ImageNet" in text:
            return 1000
        return 10
