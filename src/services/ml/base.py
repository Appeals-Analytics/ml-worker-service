from abc import ABC, abstractmethod
from typing import Any
import os

from .config import ml_settings

os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = str(ml_settings.num_threads)
os.environ["MKL_NUM_THREADS"] = str(ml_settings.num_threads)

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import logging as hf_logging

hf_logging.set_verbosity_info()

torch.set_num_threads(ml_settings.num_threads)
torch.set_num_interop_threads(ml_settings.num_interop_threads)


class BaseDetector(ABC):
  def __init__(self):
    # Instance variables, not class variables
    self._model: AutoModelForSequenceClassification | None = None
    self._tokenizer: AutoTokenizer | None = None

  @property
  @abstractmethod
  def model_name(self) -> str:
    """HuggingFace model name."""
    pass

  @property
  def tokenizer(self) -> AutoTokenizer:
    if self._tokenizer is None:
      print(f"Loading tokenizer: {self.model_name}")
      self._tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=False)
    return self._tokenizer

  @property
  def model(self) -> AutoModelForSequenceClassification:
    if self._model is None:
      print(f"Loading model: {self.model_name}")
      self._model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
      self._model.eval()
      print(f"Model loaded on CPU ({torch.get_num_threads()} threads)")
    return self._model

  def _predict(self, text: str) -> tuple[str, float]:
    inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

    with torch.inference_mode():
      outputs = self.model(**inputs)
      probs = torch.softmax(outputs.logits, dim=-1)

      idx = probs.argmax().item()
      score = probs[0][idx].item()
      label = self.model.config.id2label[idx]

    return label, score

  @abstractmethod
  def detect(self, text: str) -> dict[str, Any]:
    """Process single text."""
    pass

  def warmup(self) -> None:
    _ = self.model
    _ = self.tokenizer
    print(f"{self.__class__.__name__} ready: {self.model_name}")

  def cleanup(self) -> None:
    if self._model is not None:
      del self._model
      self._model = None
    if self._tokenizer is not None:
      del self._tokenizer
      self._tokenizer = None
    torch.cuda.empty_cache() if torch.cuda.is_available() else None
    import gc

    gc.collect()
