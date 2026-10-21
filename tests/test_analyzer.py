from bangla_pdfcheck.analyzer import analyze_text


def test_clean_bengali_text_is_accepted():
    result = analyze_text("বাংলা ভাষার লেখা।", page_number=1)
    assert result["status"] == "text_found"
    assert result["bengali_letters"] > 0
    assert result["warnings"] == []


def test_empty_text_is_flagged():
    result = analyze_text("  \n\t", page_number=2)
    assert result["status"] == "no_text"
    assert result["warnings"][0]["code"] == "no_extractable_text"


def test_english_text_can_be_allowed_explicitly():
    result = analyze_text("This is a normal English page.", page_number=1, expect_bengali=False)
    assert result["status"] == "text_found"
    assert result["warnings"] == []


def test_missing_bengali_text_is_a_warning_by_default():
    result = analyze_text("This page contains only English.", page_number=1)
    assert "no_bengali_unicode" in {item["code"] for item in result["warnings"]}
    assert result["status"] == "review"


def test_replacement_characters_are_reported():
    result = analyze_text("বাংলা \ufffd লেখা", page_number=1)
    assert result["replacement_characters"] == 1
    assert "replacement_characters" in {item["code"] for item in result["warnings"]}


def test_private_use_characters_are_reported():
    result = analyze_text("বাংলা \ue001 লেখা", page_number=1)
    assert result["private_use_characters"] == 1
    assert "private_use_characters" in {item["code"] for item in result["warnings"]}


def test_unexpected_controls_are_reported():
    result = analyze_text("বাংলা\x01লেখা", page_number=1)
    assert result["unexpected_control_characters"] == 1
    assert "control_characters" in {item["code"] for item in result["warnings"]}


def test_latin_extended_mixed_with_bengali_is_only_a_review_clue():
    result = analyze_text("ভোটাÏর তালিকা", page_number=1)
    assert "mixed_latin_extended" in {item["code"] for item in result["warnings"]}
    assert result["status"] == "review"


def test_bengali_letter_ratio_is_bounded():
    result = analyze_text("বাংলা text", page_number=1)
    assert 0.0 < result["bengali_letter_ratio"] < 1.0
