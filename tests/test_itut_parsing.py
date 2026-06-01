"""Offline integration tests for the ITU-T work programme parser.

Uses the ``responses`` library to intercept ``requests.get`` so no live
network calls are made during the test suite.
"""

from __future__ import annotations

import pathlib
import re

import pytest
import responses as responses_lib

from rapporteur_helper.itut.work_programme import WorkItem, get_work_program

DATA_DIR = pathlib.Path(__file__).parent / "data"
_WORKPROG_URL_RE = re.compile(r"https://www\.itu\.int/ITU-T/workprog/wp_search\.aspx.*")


@pytest.fixture
def workprog_html_bytes() -> bytes:
    return (DATA_DIR / "workprog_sample.html").read_bytes()


@responses_lib.activate
def test_get_work_program_returns_list(workprog_html_bytes: bytes) -> None:
    responses_lib.add(
        method=responses_lib.GET,
        url=_WORKPROG_URL_RE,
        body=workprog_html_bytes,
        status=200,
        content_type="text/html; charset=utf-8",
    )
    result = get_work_program(6, studyGroup=12)
    assert isinstance(result, list)
    assert len(result) == 2


@responses_lib.activate
def test_get_work_program_parses_work_item_fields(workprog_html_bytes: bytes) -> None:
    responses_lib.add(
        method=responses_lib.GET,
        url=_WORKPROG_URL_RE,
        body=workprog_html_bytes,
        status=200,
        content_type="text/html; charset=utf-8",
    )
    result = get_work_program(6, studyGroup=12)
    first: WorkItem = result[0]

    assert first.work_item == "G.1234"
    assert first.version == "1.0"
    assert first.process == "AAP"
    assert first.priority == "High"
    assert first.timing == "2026-06"


@responses_lib.activate
def test_get_work_program_parses_editors(workprog_html_bytes: bytes) -> None:
    responses_lib.add(
        method=responses_lib.GET,
        url=_WORKPROG_URL_RE,
        body=workprog_html_bytes,
        status=200,
        content_type="text/html; charset=utf-8",
    )
    result = get_work_program(6, studyGroup=12)
    editors = result[0].editors
    assert len(editors) == 1
    assert editors[0].name == "A. Editor"
    assert "editor@example.com" in editors[0].href


@responses_lib.activate
def test_get_work_program_parses_relationship(workprog_html_bytes: bytes) -> None:
    responses_lib.add(
        method=responses_lib.GET,
        url=_WORKPROG_URL_RE,
        body=workprog_html_bytes,
        status=200,
        content_type="text/html; charset=utf-8",
    )
    result = get_work_program(6, studyGroup=12)
    assert "Q6" in result[0].relationship
    assert "Q9" in result[0].relationship


@responses_lib.activate
def test_get_work_program_no_live_requests(workprog_html_bytes: bytes) -> None:
    """Assert no live HTTP requests are made outside the registered mock.

    ``@responses_lib.activate`` raises ``ConnectionError`` for any unregistered
    URL, so reaching the assertion without error is the meaningful guarantee.
    Cache hits that bypass requests.get are also acceptable — no live call occurs.
    """
    responses_lib.add(
        method=responses_lib.GET,
        url=_WORKPROG_URL_RE,
        body=workprog_html_bytes,
        status=200,
        content_type="text/html; charset=utf-8",
    )
    result = get_work_program(6, studyGroup=12)
    # The result is served from mock or cache — either way no live request was made.
    assert isinstance(result, list)


@responses_lib.activate
def test_get_work_program_malformed_row_does_not_crash(workprog_html_bytes: bytes) -> None:
    """A row that fails to parse should be skipped with a warning, not crash the whole fetch."""
    # Inject an extra malformed row (missing all td elements)
    bad_html = workprog_html_bytes.replace(
        b"</table>",
        b"<tr><td>broken</td></tr></table>",
    )
    responses_lib.add(
        method=responses_lib.GET,
        url=_WORKPROG_URL_RE,
        body=bad_html,
        status=200,
        content_type="text/html; charset=utf-8",
    )
    # Should still return the 2 valid rows without raising
    result = get_work_program(6, studyGroup=12)
    assert len(result) == 2
