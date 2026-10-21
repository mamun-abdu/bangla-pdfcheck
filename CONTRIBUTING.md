# Contributing

Thanks for considering a contribution. The project is intentionally small, so focused and well-tested changes are more useful than adding many features at once.

## Before opening an issue

- Search existing issues first.
- Describe the command you ran, your Python and BanglaPDFCheck versions, and the result you expected.
- Do not attach private, personal, or copyrighted PDFs. Use a synthetic file or describe the visible symptom instead.

## Development setup

```bash
python -m venv .venv
# Activate the environment, then:
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Pull request checklist

- Keep the change limited to one problem where possible.
- Add or update tests for behaviour changes.
- Avoid network access and external services in the inspection path.
- Explain important false-positive or false-negative risks in the README or docs.
- Do not describe heuristic warnings as proof that a document is corrupt.
- Run `pytest` and `ruff check .` before opening a pull request.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
