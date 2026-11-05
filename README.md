# BanglaPDFCheck

Offline preflight checker for Bengali PDF text layers. It reads the text already stored in a local PDF and reports warning signs that can make the file hard to search, copy, or quote. It is a local diagnostic: it does not OCR the page, decode legacy font mappings, or repair text.

## Problem

A Bengali PDF can look fine on screen and still copy or extract as empty, non-Bengali, or suspicious Unicode. That blocks search, quotation, indexing, and small research jobs. BanglaPDFCheck is a first pass on your machine: a short terminal summary and an optional JSON report before the file goes any further.

## How to run

Python 3.10 or newer. Install `0.1.0` from this source tree; it is not on PyPI.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
bangla-pdfcheck path/to/document.pdf
```

On Windows, create the environment with `python -m venv .venv` and activate it with `.venv\Scripts\Activate.ps1`.

Write a JSON report (the path you passed, page counts, and warning codes; extracted page text is left out):

```bash
bangla-pdfcheck notice.pdf --json report.json
```

`--allow-non-bengali` skips the warning for pages with no Bengali letters. `--fail-on-issues` exits `2` when any report needs review. A clean run exits `0`. An input or report I/O error exits `1`.

## Example

Terminal layout from a synthetic three-page PDF: Bengali text, an English-only page, then a blank page. Counts are from that file. The CLI prints the path you passed.

```text
[REVIEW] sample-notice.pdf
  Pages: 3 | with text: 2 | without text: 1 | needs review: 1 | warnings: 2
  Page 1: text_found — 30 extracted characters, 14 Bengali letters
  Page 2: review — 27 extracted characters, 0 Bengali letters
    - no_bengali_unicode: No Bengali Unicode letters were detected. The page may be non-Bengali, image-only, or using a legacy/custom font encoding.
  Page 3: no_text — 0 extracted characters, 0 Bengali letters
    - no_extractable_text: No usable text was extracted. This page may be scanned/image-only, or its text encoding may not be supported.
```

## Limitations

- A warning is a reason to inspect the file. It is not proof the text is wrong.
- A page with no extracted text may be scanned, image-only, or encoded in a way this extractor cannot read.
- Bengali Unicode on a page does not mean the words match what you see.
- There is no image comparison, OCR, legacy-font decoding, or repair.
- Password-protected PDFs that an empty password cannot open are left uninspected.
- Large or malformed PDFs can be expensive to parse. Inspect files you trust.

Privacy: processing stays on your computer (no network calls and no uploads). Review a JSON report before sharing it; it stores the path you passed and aggregate diagnostics.

## More

- Scope and related tools: [docs/scope.md](docs/scope.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- License: [MIT](LICENSE)
- Status: early `0.1.0`. Tests and CI are in place. This is not a validated Bengali PDF quality score, and it has no demonstrated external adoption.
