from pathlib import Path

import pytest
from reportlab.pdfgen import canvas

from bangla_pdfcheck.inspector import InspectionError, inspect_pdf


def create_text_pdf(path: Path, text: str = "A searchable English PDF") -> None:
    pdf = canvas.Canvas(str(path))
    pdf.drawString(72, 720, text)
    pdf.save()


def test_inspects_a_real_pdf(tmp_path):
    source = tmp_path / "sample.pdf"
    create_text_pdf(source)
    report = inspect_pdf(source, expect_bengali=False)
    assert report["tool"] == "bangla-pdfcheck"
    assert report["summary"]["pages"] == 1
    assert report["summary"]["pages_with_text"] == 1
    assert report["pages"][0]["status"] == "text_found"


def test_missing_file_is_reported(tmp_path):
    with pytest.raises(InspectionError, match="File not found"):
        inspect_pdf(tmp_path / "missing.pdf")


def test_non_pdf_is_rejected(tmp_path):
    source = tmp_path / "notes.txt"
    source.write_text("not a PDF", encoding="utf-8")
    with pytest.raises(InspectionError, match="Expected a .pdf"):
        inspect_pdf(source)


def test_corrupt_pdf_is_reported(tmp_path):
    source = tmp_path / "bad.pdf"
    source.write_bytes(b"not really a PDF")
    with pytest.raises(InspectionError, match="Could not read PDF"):
        inspect_pdf(source)


def test_blank_pdf_page_has_no_extractable_text(tmp_path):
    source = tmp_path / "blank.pdf"
    pdf = canvas.Canvas(str(source))
    pdf.showPage()
    pdf.save()
    report = inspect_pdf(source)
    assert report["summary"]["pages_without_text"] == 1
    assert report["pages"][0]["status"] == "no_text"
