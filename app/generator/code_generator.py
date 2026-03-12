"""
app/generator/code_generator.py
Renders the correct Jinja2 training script template based on:
  - framework (pytorch / tensorflow)
  - task type (image_classification / language_modeling / text_classification / etc.)
"""

import os
from datetime import datetime
from jinja2 import Environment, BaseLoader

from app.logger.logger import get_logger
from app.generator.templates.pytorch_template     import PYTORCH_TEMPLATE
from app.generator.templates.pytorch_nlp_template import PYTORCH_NLP_TEMPLATE
from app.generator.templates.tensorflow_template  import TENSORFLOW_TEMPLATE
from config import OUTPUT_DIR

log = get_logger(__name__)

# NLP / text-based tasks → use NLP template
NLP_TASKS = {
    "language_modeling",
    "text_classification",
    "text_generation",
    "question_answering",
    "summarization",
    "translation",
}

# Models that are always NLP regardless of task
NLP_MODELS = {
    "GPT", "BERT", "T5", "LSTM", "GRU", "RNN",
    "Transformer", "XLNet", "RoBERTa", "DistilBERT",
}


class CodeGenerator:
    """
    Selects and renders the right training script template.

    Logic:
      - If task is NLP-type OR model is an NLP model → use NLP template
      - If framework is tensorflow → use TF template
      - Otherwise → use standard PyTorch image template

    Example:
        gen  = CodeGenerator()
        out  = gen.generate(info, framework="pytorch")
        print(out["code"])
    """

    def generate(self, info: dict, framework: str = None) -> dict:
        fw   = (framework or info.get("framework", "pytorch")).lower()
        task = info.get("task", "image_classification")
        model_name = info.get("model", "CustomModel")

        # Decide which template to use
        is_nlp = (task in NLP_TASKS) or (model_name in NLP_MODELS)

        if fw == "tensorflow":
            template_str  = TENSORFLOW_TEMPLATE
            template_name = "tensorflow"
        elif is_nlp:
            template_str  = PYTORCH_NLP_TEMPLATE
            template_name = "pytorch_nlp"
            log.info(f"NLP task detected ({task} / {model_name}) → using NLP template")
        else:
            template_str  = PYTORCH_TEMPLATE
            template_name = "pytorch"

        log.info(f"Generating [{template_name}] script for model={model_name}, task={task}")

        env      = Environment(loader=BaseLoader())
        template = env.from_string(template_str)
        ts       = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        code     = template.render(**info, timestamp=ts)

        filename = self._make_filename(info, fw)
        out_path = os.path.join(OUTPUT_DIR, filename)

        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(code)
            log.info(f"Script saved: {out_path}")
        except Exception as e:
            log.error(f"Failed to save script: {e}")
            raise

        return {
            "code":     code,
            "path":     out_path,
            "filename": filename,
            "info":     info,
        }

    def _make_filename(self, info: dict, framework: str) -> str:
        model   = info.get("model",   "model").lower().replace(" ", "_")
        dataset = info.get("dataset", "data").lower().replace(" ", "_").replace("-", "")
        ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{model}_{dataset}_{framework}_{ts}.py"
