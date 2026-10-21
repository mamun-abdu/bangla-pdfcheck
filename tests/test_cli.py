import json

from reportlab.pdfgen import canvas

from bangla_pdfcheck.cli import main


def test_cli_writes_json_report(tmp_path):
    source = tmp_path / "sample.pdf"
    pdf = canvas.Canvas(str(source))
    pdf.drawString(72, 720, "A searchable PDF")
    pdf.save()
    output = tmp_path / "report.json"

    code = main([str(source), "--allow-non-bengali", "--json", str(output)])

    assert code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["files_checked"] == 1
    assert payload["files"][0]["summary"]["pages"] == 1


def test_fail_on_issues_returns_two_for_english_only_pdf(tmp_path):
    source = tmp_path / "sample.pdf"
    pdf = canvas.Canvas(str(source))
    pdf.drawString(72, 720, "English only")
    pdf.save()

    assert main([str(source), "--fail-on-issues"]) == 2


def test_cli_does_not_overwrite_input_pdf(tmp_path):
    source = tmp_path / "sample.pdf"
    pdf = canvas.Canvas(str(source))
    pdf.drawString(72, 720, "A searchable PDF")
    pdf.save()
    original_size = source.stat().st_size

    assert main([str(source), "--allow-non-bengali", "--json", str(source)]) == 1
    assert source.stat().st_size == original_size
