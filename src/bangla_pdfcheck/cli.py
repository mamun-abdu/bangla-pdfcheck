"""Command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from bangla_pdfcheck import __version__
from bangla_pdfcheck.inspector import InspectionError, inspect_pdf


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bangla-pdfcheck",
        description=(
            "Inspect Bengali PDF text layers for missing text and common Unicode warning signs. "
            "Files are processed locally; no OCR or network service is used."
        ),
    )
    parser.add_argument("pdf", nargs="+", help="One or more local PDF files")
    parser.add_argument(
        "--json",
        dest="json_path",
        metavar="REPORT.json",
        help="Write a machine-readable JSON report to this path",
    )
    parser.add_argument(
        "--allow-non-bengali",
        action="store_true",
        help="Do not warn when a page contains no Bengali Unicode letters",
    )
    parser.add_argument(
        "--fail-on-issues",
        action="store_true",
        help="Return exit code 2 when any page needs review (useful in CI)",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def _print_report(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print(f"[{report['overall_status'].upper()}] {report['file']}")
    print(
        f"  Pages: {summary['pages']} | with text: {summary['pages_with_text']} | "
        f"without text: {summary['pages_without_text']} | "
        f"needs review: {summary['pages_needing_review']} | warnings: {summary['warnings']}"
    )
    for page in report["pages"]:
        print(
            f"  Page {page['page']}: {page['status']} — "
            f"{page['characters']} extracted characters, "
            f"{page['bengali_letters']} Bengali letters"
        )
        for warning in page["warnings"]:
            print(f"    - {warning['code']}: {warning['message']}")


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    expect_bengali = not args.allow_non_bengali
    reports: list[dict[str, Any]] = []
    failed = False
    input_errors: list[dict[str, str]] = []

    for filename in args.pdf:
        try:
            report = inspect_pdf(filename, expect_bengali=expect_bengali)
            reports.append(report)
            _print_report(report)
        except InspectionError as exc:
            failed = True
            input_errors.append({"file": filename, "message": str(exc)})
            print(f"[ERROR] {filename}: {exc}", file=sys.stderr)

    if args.json_path:
        payload: dict[str, Any] = {
            "tool": "bangla-pdfcheck",
            "version": __version__,
            "files_checked": len(reports),
            "files": reports,
            "errors": input_errors,
        }
        try:
            output = Path(args.json_path)
            if output.resolve() in {Path(filename).resolve() for filename in args.pdf}:
                print("[ERROR] JSON report path must not overwrite an input PDF.", file=sys.stderr)
                return 1
            output.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        except OSError as exc:
            print(f"[ERROR] Could not write JSON report: {exc}", file=sys.stderr)
            return 1

    if failed:
        return 1
    if args.fail_on_issues and any(report["overall_status"] != "ok" for report in reports):
        return 2
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
