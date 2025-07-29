"""Module (metrics)."""

import os

from bert_score import BERTScorer
from cer import calculate_cer
from jiwer import wer
from torchmetrics.text.bleu import BLEUScore

os.environ["TRANSFORMERS_CACHE"] = "./bert-base-uncased"


class Metrics:
    """Wraper class to handle scoring operations."""

    def __init__(self):
        """Initializes BLEUScore and BERTScorer(By default model_type="bert-base-uncased")."""
        self.metric = BLEUScore()
        self.scorer = BERTScorer(model_type="bert-base-uncased")

    def cer_score(self, candidate_text: str, reference_text: str) -> str:
        """Calculates cer score. The lower the score the better. Result quality good(1‐2%), average(2- 10%), poor(>10%).

        Args:
            candidate_text (str): Text to be compared.
            reference_text (str): Original text.

        Returns:
            str: Csv formatted score
        """
        candidate_text_arr = candidate_text.split()
        reference_text_arr = reference_text.split()

        result = calculate_cer(candidate_text_arr, reference_text_arr)

        return f"{result:.4f}"

    def wer_score(self, candidate_text: str, reference_text: str) -> str:
        """Calculates wer score. The lower the score the better.

        Args:
            candidate_text (str): Text to be compared.
            reference_text (str): Original text.

        Returns:
            str: Csv formatted score
        """
        result = wer(reference_text, candidate_text)
        return f"{result:.4f}"

    def bleu_score(self, candidate_text: str, reference_text: str) -> str:
        """Calculates bleu score.

        Args:
            candidate_text (str): Text to be compared.
            reference_text (str): Original text.

        Returns:
            str: Csv formatted score
        """
        result = self.metric([candidate_text], [reference_text])
        return f"{result:.4f}"

    def bert_score(self, candidate_text: str, reference_text: str) -> str:
        """Calculates bert score.

        Args:
            candidate_text (str): Text to be compared.
            reference_text (str): Original text.

        Returns:
            str: Csv formatted score
        """
        P, R, F1 = self.scorer.score([candidate_text], [reference_text])

        return f"{P.item():.4f},{R.item():.4f},{F1.item():.4f}"

    def calculate_scores(self, candidate_text: str, reference_text: str) -> str:
        """Calculates the cer,wer,bleu and bert scores for input texts.

        Args:
            candidate_text (str): Text to be compared.
            reference_text (str): Original text.

        Returns:
            str: Csv formatted scores in order cer,wer,bleu,bert
        """
        cer_res = self.cer_score(candidate_text, reference_text)
        wer_res = self.wer_score(candidate_text, reference_text)
        bleu_res = self.bleu_score(candidate_text, reference_text)
        bert_res = self.bert_score(candidate_text, reference_text)

        return f"{cer_res},{wer_res},{bleu_res},{bert_res}"
