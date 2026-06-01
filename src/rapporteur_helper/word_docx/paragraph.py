"""Word document paragraph insertion and text replacement utilities."""

import docx
from docx.document import Document
from docx.text.paragraph import Paragraph


def insert_paragraph_after(paragraph: Paragraph, text: str | None = None, style: str | None = None):
    """Insert a new paragraph after the given paragraph."""
    new_p = docx.oxml.shared.OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = docx.text.paragraph(new_p, paragraph)
    if text:
        new_para.add_run(text)
    if style is not None:
        new_para.style = style
    return new_para


def find_element(document: Document, text: str) -> Paragraph | None:
    """Return the first paragraph in *document* containing *text*, or ``None``.

    Args:
        document: The Word document to search.
        text: The substring to find.

    Returns:
        The matching :class:`Paragraph`, or ``None`` if not found.
    """
    for paragraph in document.paragraphs:
        if text in paragraph.text:
            return paragraph


def replace(document: Document, find: str, replace: str) -> None:
    """Replace all occurrences of *find* with *replace* in every paragraph and table cell.

    Args:
        document: The Word document to modify in-place.
        find: The text string to search for.
        replace: The replacement text string.
    """
    for paragraph in document.paragraphs:
        foundInRun = False
        for run in paragraph.runs:
            if find in run.text:
                run.text = run.text.replace(find, replace)
                # print(f'run: {find}')
                foundInRun = True
        if not foundInRun and find in paragraph.text:
            paragraph.text = paragraph.text.replace(find, replace)
            # print(f'paragraph: {find}')

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    foundInRun = False
                    for run in paragraph.runs:
                        if find in run.text:
                            run.text = run.text.replace(find, replace)
                            # print(f'run: {find}')
                            foundInRun = True
                    if not foundInRun and find in paragraph.text:
                        paragraph.text = paragraph.text.replace(find, replace)
                        # print(f'paragraph: {find}')


if __name__ == "__main__":
    pass
