from typing import List, Optional
import os

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


class Predictor:
    """Simple wrapper to load a seq2seq model and run predictions."""

    def __init__(self, model_dir: Optional[str] = None, device: Optional[str] = None):
        self.model_dir = model_dir or os.path.join(
            os.getcwd(), "artifacts", "model_trainer", "pegasus-samsum-model"
        )
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None

    def load(self):
        if self.model is not None and self.tokenizer is not None:
            return
        # allow local directory or HuggingFace name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_dir)
        self.model.to(self.device)

    def predict(self, texts: List[str], max_length: int = 64) -> List[str]:
        if self.model is None or self.tokenizer is None:
            self.load()

        inputs = self.tokenizer(texts, truncation=True, padding=True, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=4,
                early_stopping=True,
            )
        decoded = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return decoded
