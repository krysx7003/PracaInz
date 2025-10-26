"""Module (metrics)."""

from cer import calculate_cer
from jiwer import wer


class Metrics:
    """Wraper class to handle scoring operations."""

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

        return f"{cer_res},{wer_res}"
