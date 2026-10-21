"""PDF reading and report assembly."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from bangla_pdfcheck import __version__
from bangla_pdfcheck.analyzer import analyze_text


class InspectionError(Exception):
    """Raised when an input PDF cannot be inspected."""


def inspect_pdf(path: str | Path, expect_bengali: bool = True) -> dict[str, Any]:
    """Inspect a local PDF and return a JSON-serializable report."""
    source = Path(path)
    if not source.exists():
        raise InspectionError(f"File not found: {source}")
    if not source.is_file():
        raise InspectionError(f"Not a file: {source}")
    if source.suffix.lower() != ".pdf":
        raise InspectionError(f"Expected a .pdf file: {source}")

    try:
        reader = PdfReader(str(source), strict=False)
        if reader.is_encrypted and not reader.decrypt(""):
            raise InspectionError("PDF is password-protected; an empty password did not unlock it.")
        page_count = len(reader.pages)
        if page_count == 0:
            raise InspectionError("PDF contains no pages.")
    except InspectionError:
        raise
    except (OSError, PdfReadError, ValueError, TypeError) as exc:
        raise InspectionError(f"Could not read PDF: {exc}") from exc
    except Exception as exc:  # Some malformed PDFs raise library-specific exceptions.
        raise InspectionError(f"Could not read PDF: {exc}") from exc

    pages: list[dict[str, Any]] = []
    for index, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
            result = analyze_text(text, page_number=index, expect_bengali=expect_bengali)
        except Exception as exc:  # Keep reporting other pages if one page fails.
            result = {
                "page": index,
                "status": "error",
                "characters": 0,
                "non_whitespace_characters": 0,
                "letter_characters": 0,
                "bengali_letters": 0,
                "bengali_letter_ratio": 0.0,
                "replacement_characters": 0,
                "private_use_characters": 0,
                "unexpected_control_characters": 0,
                "warnings": [
                    {
                        "code": "extraction_error",
                        "message": f"Text extraction failed on this page: {exc}",
                    }
                ],
            }
        pages.append(result)

    warning_count = sum(len(page["warnings"]) for page in pages)
    error_count = sum(page["status"] == "error" for page in pages)
    no_text_count = sum(page["status"] == "no_text" for page in pages)
    review_count = sum(page["status"] == "review" for page in pages)
    overall_status = "review" if warning_count else "ok"
    if error_count == page_count:
        overall_status = "error"

    return {
        "tool": "bangla-pdfcheck",
        "version": __version__,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "file": str(source),
        "overall_status": overall_status,
        "summary": {
            "pages": page_count,
            "pages_with_text": sum(page["non_whitespace_characters"] > 0 for page in pages),
            "pages_without_text": no_text_count,
            "pages_needing_review": review_count,
            "pages_with_errors": error_count,
            "warnings": warning_count,
        },
        "pages": pages,
        "limitations": [
            "This report uses heuristics and does not verify text against the page image.",
            (
                "A page with no extracted text is not proof that it is scanned; "
                "its encoding may also be unsupported."
            ),
            "The tool does not perform OCR or repair extracted text.",
        ],
    }
