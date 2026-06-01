"""Word document table text and element replacement utilities."""

from __future__ import annotations

from docx.table import Table


def replace_in_table(table: Table, find: str, replace: str | object) -> bool:
    """Recursively search *table* and replace the first occurrence of *find*.

    Replaces within run text when *replace* is a string, or splices in an XML
    element when *replace* is any other object.

    Args:
        table: The Word table (or nested table) to search.
        find: Placeholder text to locate.
        replace: Replacement string or lxml/OxmlElement to splice in.

    Returns:
        ``True`` if a replacement was made, ``False`` otherwise.
    """
    for row in table.rows:
        for cell in row.cells:
            for subtable in cell.tables:
                if replace_in_table(subtable, find, replace):
                    return True
            for paragraph in cell.paragraphs:
                foundInRun = False
                for run in paragraph.runs:
                    if find in run.text:
                        if isinstance(replace, str):
                            run.text = run.text.replace(find, replace)
                            run.font.highlight_color = 0
                        else:
                            run.text = ""
                            paragraph._p.append(replace)
                        return True

                if not foundInRun and find in paragraph.text:
                    if isinstance(replace, str):
                        paragraph.text = paragraph.text.replace(find, replace)
                    else:
                        pass
                        paragraph._p.addnext(replace)

                    return True
    return False


if __name__ == "__main__":
    pass
