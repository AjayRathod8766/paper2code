"""
app/parser/text_cleaner.py
Cleans raw PDF text: removes headers/footers, fixes spacing,
normalizes unicode and strips non-content lines.
"""

import re
from app.logger.logger import get_logger

log = get_logger(__name__)


class TextCleaner:
    """
    Cleans raw text extracted from a research paper PDF.

    Example:
        cleaner = TextCleaner()
        clean = cleaner.clean(raw_text)
    """

    # Lines shorter than this are likely headers/footers
    MIN_LINE_LENGTH = 20

    def clean(self, raw_text: str) -> str:
        log.info("Starting text cleaning...")
        text = raw_text

        text = self._fix_encoding(text)
        text = self._remove_urls(text)
        text = self._remove_page_numbers(text)
        text = self._normalize_whitespace(text)
        text = self._remove_short_lines(text)

        log.info(f"Cleaning done. Output length: {len(text)} chars")
        return text

    # ── Private helpers ────────────────────────────────────────

    def _fix_encoding(self, text: str) -> str:
        """Fix common unicode issues in PDFs."""
        replacements = {
            "\ufb01": "fi", "\ufb02": "fl", "\u2013": "-",
            "\u2014": "--", "\u2018": "'", "\u2019": "'",
            "\u201c": '"', "\u201d": '"', "\u00a0": " ",
        }
        for bad, good in replacements.items():
            text = text.replace(bad, good)
        return text

    def _remove_urls(self, text: str) -> str:
        return re.sub(r"http\S+|www\.\S+", "", text)

    def _remove_page_numbers(self, text: str) -> str:
        """Remove standalone page number lines like '- 4 -' or just '4'."""
        return re.sub(r"^\s*[-–]?\s*\d+\s*[-–]?\s*$", "", text, flags=re.MULTILINE)

    def _normalize_whitespace(self, text: str) -> str:
        text = re.sub(r"[ \t]+", " ", text)         # collapse spaces
        text = re.sub(r"\n{3,}", "\n\n", text)       # max 2 blank lines
        return text.strip()

    def _remove_short_lines(self, text: str) -> str:
        """Remove very short lines that are likely noise (headers, footers)."""
        lines = text.split("\n")
        filtered = [
            line for line in lines
            if len(line.strip()) >= self.MIN_LINE_LENGTH or line.strip() == ""
        ]
        return "\n".join(filtered)
