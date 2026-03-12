"""
app/parser/pdf_parser.py
Extracts raw text content from a research paper PDF page by page.
Uses pdfplumber — handles multi-column academic PDFs well.
"""

import os
import pdfplumber

from app.logger.logger import get_logger

log = get_logger(__name__)


class PDFParser:
    """
    Parses a PDF file and returns clean page-by-page text.

    Example:
        parser = PDFParser("resnet_paper.pdf")
        result = parser.parse()
        print(result["full_text"])
    """

    def __init__(self, pdf_path: str):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        self.pdf_path = pdf_path
        log.info(f"PDFParser initialized → {os.path.basename(pdf_path)}")

    def parse(self) -> dict:
        """
        Returns:
            {
                "filename":   str,
                "num_pages":  int,
                "pages":      [str, str, ...],   # text per page
                "full_text":  str                # all pages joined
            }
        """
        pages_text = []
        log.info(f"Starting PDF parse: {self.pdf_path}")

        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                total = len(pdf.pages)
                log.info(f"Total pages detected: {total}")

                for i, page in enumerate(pdf.pages):
                    try:
                        text = page.extract_text() or ""
                        pages_text.append(text)
                        log.debug(f"Page {i+1}/{total} extracted ({len(text)} chars)")
                    except Exception as e:
                        log.warning(f"Page {i+1} extraction failed: {e}")
                        pages_text.append("")

        except Exception as e:
            log.error(f"Failed to open PDF: {e}")
            raise

        full_text = "\n\n".join(pages_text)
        log.info(f"Parse complete. Total chars: {len(full_text)}")

        return {
            "filename":  os.path.basename(self.pdf_path),
            "num_pages": len(pages_text),
            "pages":     pages_text,
            "full_text": full_text,
        }
