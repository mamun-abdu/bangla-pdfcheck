"""Small, explainable heuristics for inspecting extracted PDF text."""

from __future__ import annotations

import unicodedata
from collections import Counter
from typing import Any


def _is_bengali_letter(char: str) -> bool:
    """Return whether *char* is a letter in the Bengali Unicode block."""
    return "\u0980" <= char <= "\u09ff" and unicodedata.category(char).startswith("L")


def _is_private_use(char: str) -> bool:
    """Check Unicode private-use areas, often used by custom font mappings."""
    codepoint = ord(char)
    return (
        0xE000 <= codepoint <= 0xF8FF
        or 0xF0000 <= codepoint <= 0xFFFFD
        or 0x100000 <= codepoint <= 0x10FFFD
    )


def analyze_text(text: str | None, page_number: int, expect_bengali: bool = True) -> dict[str, Any]:
    """Summarize basic text-layer signals for one page.

    This deliberately reports clues, not a verdict about whether the PDF's
    text is correct. PDF extraction has inherent limits and these heuristics
    can produce false positives or miss problems.
    """
    extracted = text or ""
    visible = [char for char in extracted if not char.isspace()]
    letters = [char for char in extracted if unicodedata.category(char).startswith("L")]
    bengali_letters = [char for char in letters if _is_bengali_letter(char)]
    private_use = [char for char in extracted if _is_private_use(char)]
    replacement_count = extracted.count("\ufffd")
    suspicious_controls = [
        char
        for char in extracted
        if unicodedata.category(char) == "Cc" and char not in "\t\n\r"
    ]
    # Latin Extended characters inside an otherwise Bengali text layer can be
    # a clue that a PDF's font mapping extracted incorrectly. They are not
    # proof of corruption, so we report a warning and the user reviews it.
    latin_extended = [
        char for char in extracted if 0x00C0 <= ord(char) <= 0x024F
    ]

    warnings: list[dict[str, str]] = []
    if not visible:
        warnings.append(
            {
                "code": "no_extractable_text",
                "message": (
                    "No usable text was extracted. This page may be scanned/image-only, "
                    "or its text encoding may not be supported."
                ),
            }
        )
    elif expect_bengali and not bengali_letters:
        warnings.append(
            {
                "code": "no_bengali_unicode",
                "message": (
                    "No Bengali Unicode letters were detected. The page may be non-Bengali, "
                    "image-only, or using a legacy/custom font encoding."
                ),
            }
        )

    if replacement_count:
        warnings.append(
            {
                "code": "replacement_characters",
                "message": (
                    f"Found {replacement_count} Unicode replacement character(s) (U+FFFD); "
                    "some text may not have decoded correctly."
                ),
            }
        )
    if private_use:
        warnings.append(
            {
                "code": "private_use_characters",
                "message": (
                    f"Found {len(private_use)} Unicode private-use character(s); "
                    "their meaning depends on the document's font mapping."
                ),
            }
        )
    if suspicious_controls:
        warnings.append(
            {
                "code": "control_characters",
                "message": (
                    f"Found {len(suspicious_controls)} unexpected control character(s) "
                    "in extracted text."
                ),
            }
        )
    if expect_bengali and bengali_letters and latin_extended:
        counts = Counter(latin_extended)
        examples = " ".join(f"U+{ord(char):04X}" for char, _ in counts.most_common(4))
        warnings.append(
            {
                "code": "mixed_latin_extended",
                "message": (
                    "Bengali text also contains Latin Extended characters "
                    f"({examples}). This can be legitimate, but may indicate a custom or "
                    "legacy font mapping; review the extracted text."
                ),
            }
        )

    if not visible:
        status = "no_text"
    elif warnings:
        status = "review"
    else:
        status = "text_found"

    return {
        "page": page_number,
        "status": status,
        "characters": len(extracted),
        "non_whitespace_characters": len(visible),
        "letter_characters": len(letters),
        "bengali_letters": len(bengali_letters),
        "bengali_letter_ratio": round(len(bengali_letters) / len(letters), 4) if letters else 0.0,
        "replacement_characters": replacement_count,
        "private_use_characters": len(private_use),
        "unexpected_control_characters": len(suspicious_controls),
        "warnings": warnings,
    }
