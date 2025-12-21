from app.utils.helpers import extract_json_from_text
import pytest


def test_extracts_plain_json_object():
    payload = {"foo": "bar"}
    assert extract_json_from_text('{"foo": "bar"}') == payload


def test_extracts_from_fenced_block():
    raw = """```json\n{\n  \"foo\": 1\n}\n```"""
    assert extract_json_from_text(raw) == {"foo": 1}


def test_extracts_first_braced_object_when_mixed_with_text():
    raw = "Intro text {\"nested\": {\"value\": 42}} trailing instructions"
    assert extract_json_from_text(raw) == {"nested": {"value": 42}}


def test_raises_for_invalid_payload():
    with pytest.raises(ValueError, match="valid JSON"):
        extract_json_from_text("no json here")
