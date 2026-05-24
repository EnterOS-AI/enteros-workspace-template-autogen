"""Smoke test: adapter.py imports cleanly under the conftest stubs.

This pins the contract that `from adapter import AutoGenAdapter` works
with only the minimal stub shims in conftest.py — i.e. without any
production runtime dependency (molecule_runtime, a2a-sdk, autogen-*) being
pip-installed. The corresponding production-deps import path is exercised
by the validate-runtime job, which DOES `pip install -r requirements.txt`
before importing adapter.py.

If a future change to adapter.py introduces a new top-level import not
covered by the conftest stubs, this test fails before any other test in
the suite even collects — surfacing the gap immediately.
"""

from __future__ import annotations


def test_adapter_imports() -> None:
    from adapter import AutoGenAdapter

    assert AutoGenAdapter.name() == "autogen"
    assert AutoGenAdapter.display_name() == "AutoGen"


def test_adapter_does_not_import_removed_a2a_utils() -> None:
    from pathlib import Path

    source = Path(__file__).resolve().parent.parent.joinpath("adapter.py").read_text()
    assert "from a2a.utils import new_agent_text_message" not in source
    assert "new_response_message" in source


def test_image_description_context_extracts_marker_section() -> None:
    from adapter import _image_description_context

    text = (
        "Describe this.\n\n"
        "Image attachment descriptions:\n"
        "- probe.png: A red square and a blue circle sit above a black line."
    )

    assert _image_description_context(text) == (
        "Image attachment descriptions:\n"
        "- probe.png: A red square and a blue circle sit above a black line."
    )


def test_tool_execution_summary_detection() -> None:
    from adapter import _looks_like_tool_execution_summary

    assert _looks_like_tool_execution_summary(
        "{'exit_code': 0, 'stdout': 'Size: (320, 220)', "
        "'stderr': '', 'language': 'python', 'backend': 'subprocess'}"
    )
    assert not _looks_like_tool_execution_summary(
        "A red square and a blue circle sit above a black line."
    )
