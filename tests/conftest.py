"""pytest configuration and shared fixtures."""

from __future__ import annotations

import pathlib

import pytest

DATA_DIR = pathlib.Path(__file__).parent / "data"


@pytest.fixture
def workprog_html() -> str:
    """Return the contents of the sample ITU-T work programme HTML fixture."""
    return (DATA_DIR / "workprog_sample.html").read_text(encoding="utf-8")
