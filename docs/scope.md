# Scope and related tools

## Problem this project addresses

A PDF can look readable on screen while yielding empty or suspicious text when copied or extracted. This creates friction for search, text indexing, quotation, accessibility and small research workflows. The issue can be especially confusing when Bengali text uses a font mapping that does not extract as expected Unicode.

BanglaPDFCheck aims to give a user a quick, repeatable first-pass report without sending a document to a web service or requiring OCR software.

## Scope for version 0.1

Included:

- Read a local PDF using `pypdf`.
- Extract each page's existing text layer.
- Count Bengali letters and selected Unicode warning signals.
- Emit a terminal summary and optional JSON diagnostics.
- Keep processing independent of network services.

Not included:

- OCR, image rendering, or a visual comparison between page images and extracted text.
- Automatic text correction, translation, or legacy-font decoding.
- A web application, document store, account system, or background server.
- Claims that a document is legally accessible, accurate, or suitable for every downstream use.

## Related tools and how they differ

- **pypdf** provides PDF parsing and text extraction. BanglaPDFCheck builds a small diagnostic report around extracted text; it does not replace pypdf.
- **Hypothesis `pdf-text-quality`** compares the PDF text layer with OCR output and examines spatial correspondence. That is a deeper and more resource-intensive check. BanglaPDFCheck does not attempt to reproduce it.
- **Bengali PDF decoding/extraction projects** target extraction, OCR, or repair for particular Bengali font encodings. BanglaPDFCheck does not decode or repair text; it can only flag a few clues that merit manual review.

These are related tools, not proof that the current heuristics identify every Bengali PDF problem. The project's value must be validated with users and permission-safe test cases.

## Validation plan

1. Ask Bengali-language students and document-processing users which failures they encounter in practice.
2. Collect synthetic or explicitly permissioned examples of empty text layers and suspicious Unicode output.
3. Check false positives, especially for documents that legitimately mix Bengali and Latin characters.
4. Add each confirmed case as a regression test.
5. Release only after the report wording is clear that it gives clues, not a correctness score.
