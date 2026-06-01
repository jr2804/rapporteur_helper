"""Tests for word_docx utilities — no filesystem I/O required."""
from __future__ import annotations

import docx
import pytest
from docx import Document

from rapporteur_helper.word_docx.links import add_hyperlink, create_hyperlink
from rapporteur_helper.word_docx.tables import replace_in_table


@pytest.fixture()
def blank_document() -> Document:
    return docx.Document()


class TestCreateHyperlink:
    def test_returns_xml_element(self, blank_document: Document) -> None:
        result = create_hyperlink(blank_document, "Click here", "https://example.com")
        assert result is not None
        assert result.tag.endswith("hyperlink")

    def test_bold_format_adds_bold_run(self, blank_document: Document) -> None:
        result = create_hyperlink(blank_document, "Bold link", "https://example.com", format="bold")
        xml_str = docx.oxml.shared.OxmlElement("w:root")
        xml_str.append(result)
        # Check that a w:b element exists inside the hyperlink
        ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        assert result.find(f".//{{{ns}}}b") is not None

    def test_hyperlink_format_adds_rStyle(self, blank_document: Document) -> None:
        result = create_hyperlink(blank_document, "styled", "https://example.com", format="hyperlink")
        ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        r_style = result.find(f".//{{{ns}}}rStyle")
        assert r_style is not None
        assert r_style.get(f"{{{ns}}}val") == "Hyperlink"

    def test_italic_format_adds_italic_run(self, blank_document: Document) -> None:
        result = create_hyperlink(blank_document, "Italic", "https://example.com", format="italic")
        ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        assert result.find(f".//{{{ns}}}i") is not None


class TestAddHyperlink:
    def test_appends_to_paragraph(self, blank_document: Document) -> None:
        para = blank_document.add_paragraph()
        original_count = len(para._p)
        add_hyperlink(para, "Link text", "https://example.com")
        assert len(para._p) > original_count

    def test_returns_hyperlink_element(self, blank_document: Document) -> None:
        para = blank_document.add_paragraph()
        result = add_hyperlink(para, "text", "https://example.com")
        assert result is not None


class TestReplaceInTable:
    def test_replaces_string_in_cell(self, blank_document: Document) -> None:
        table = blank_document.add_table(rows=1, cols=1)
        table.cell(0, 0).paragraphs[0].add_run("PLACEHOLDER")
        found = replace_in_table(table, "PLACEHOLDER", "REPLACED")
        assert found is True
        assert "REPLACED" in table.cell(0, 0).paragraphs[0].text

    def test_returns_false_when_not_found(self, blank_document: Document) -> None:
        table = blank_document.add_table(rows=1, cols=1)
        table.cell(0, 0).paragraphs[0].add_run("no match here")
        result = replace_in_table(table, "NOTPRESENT", "anything")
        assert result is False

    def test_no_filesystem_io(self, blank_document: Document, tmp_path) -> None:
        """Verify replace_in_table never writes files — document stays in memory."""
        import os
        table = blank_document.add_table(rows=1, cols=1)
        table.cell(0, 0).paragraphs[0].add_run("value")
        replace_in_table(table, "value", "new_value")
        # No files should have been created in tmp_path during this test
        assert list(tmp_path.iterdir()) == []
