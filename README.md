# BanglaPDFCheck

**A small, offline preflight checker for Bengali PDF text layers.**

BanglaPDFCheck extracts the existing text layer from a PDF and reports simple warning signs that can make Bengali documents difficult to search, quote, index, or use in research. It is a diagnostic utility, not an OCR engine or a text-repair tool.

## What it checks

- Pages from which no usable text can be extracted.
- Pages with no Bengali Unicode letters when Bengali text is expected.
- Unicode replacement characters (`U+FFFD`), which can indicate decoding problems.
- Unicode private-use characters, whose meaning depends on a font mapping.
- Unexpected control characters in extracted text.
- Latin Extended characters mixed into Bengali text, reported as a clue to review—not proof of corruption.
- A compact JSON report suitable for research workflows or continuous integration.

## Quick start

Python 3.10 or newer is required. This initial release is not yet published on PyPI, so install it from the downloaded source folder for now.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install .
bangla-pdfcheck path/to/document.pdf
```

For development from the source folder, install the test and lint tools too:

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

After the package is actually published to PyPI, end users will also be able to install it with `python -m pip install bangla-pdfcheck`.

### Example output

The following is illustrative output, not a measurement from a real public document.

```text
[REVIEW] sample-notice.pdf
  Pages: 3 | with text: 2 | without text: 1 | needs review: 1 | warnings: 2
  Page 1: text_found — 842 extracted characters, 615 Bengali letters
  Page 2: review — 109 extracted characters, 0 Bengali letters
    - no_bengali_unicode: No Bengali Unicode letters were detected...
  Page 3: no_text — 0 extracted characters, 0 Bengali letters
    - no_extractable_text: No usable text was extracted...
```

### Write a JSON report

```bash
bangla-pdfcheck notice.pdf --json report.json
```

The JSON report contains page-level counts, warning codes, and limitations. It does **not** store extracted page text. The `file` field contains the path you supplied, so review it before sharing reports publicly.

For a known non-Bengali PDF, disable the language-specific check:

```bash
bangla-pdfcheck english-document.pdf --allow-non-bengali
```

For a CI job that should fail if any page raises a warning:

```bash
bangla-pdfcheck documents/*.pdf --fail-on-issues
```

Exit codes: `0` means the inspection ran (or no issues were found when strict mode is enabled); `1` means an input/report I/O error occurred; `2` means `--fail-on-issues` found one or more reports needing review.

## Important limitations

- The checks are heuristics. A warning is a reason to inspect the document, not proof that text is wrong.
- A page with no extracted text may be scanned, image-only, or encoded in a way the extractor cannot read. The tool cannot determine which explanation is correct.
- Finding Bengali Unicode characters does not prove that the words are correct or match the visible page.
- The current version does not compare extracted text to page images, run OCR, decode legacy font mappings, or repair content.
- Password-protected PDFs that cannot be opened with an empty password are not inspected.
- PDF parsing can be resource-intensive for malformed or unusually large files. Only inspect files you trust.

## Privacy

All processing occurs locally on your computer. BanglaPDFCheck makes no network requests and does not upload PDFs or extracted text. The optional JSON report contains file paths and aggregate diagnostics; check it before sharing.

## Why a separate tool?

PDF libraries such as [pypdf](https://github.com/py-pdf/pypdf) expose text extraction, but callers still need to interpret the results. More advanced projects can compare OCR and PDF text layers, while Bengali decoding projects aim to repair specific legacy encodings. BanglaPDFCheck has a narrower role: run quick, explainable checks before a document enters a workflow.

See [scope and related tools](docs/scope.md) for what this project does—and does not—try to replace.

## Contributing

Issues, reproducible test cases, documentation improvements, and small pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md). Do not upload private, copyrighted, or personal documents in an issue; describe the symptom or create a synthetic example instead.

## License

MIT. See [LICENSE](LICENSE).

## Project status

Early development (`0.1.0`). It has a test suite and continuous integration, but has not yet demonstrated external adoption. The next step is to get feedback from students, librarians, researchers, and people who process Bengali documents, then improve the checks based on real, permission-safe examples.
