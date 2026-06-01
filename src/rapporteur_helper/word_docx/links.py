"""Word document hyperlink creation utilities."""

from __future__ import annotations

from typing import Literal

import docx
from docx.document import Document
from docx.oxml.shared import OxmlElement, qn
from docx.text.paragraph import Paragraph
from lxml.etree import _Element

HyperlinkFormat = Literal["None", "bold", "italic", "hyperlink", "button"]


def create_hyperlink(document: Document, text: str, url: str, format: HyperlinkFormat = "None") -> _Element:
    """Create a ``w:hyperlink`` XML element with an external relationship.

    Args:
        document: The Word document used to register the hyperlink relationship.
        text: Display text for the hyperlink.
        url: Target URL.
        format: Visual style to apply — ``'None'``, ``'bold'``, ``'italic'``,
            ``'hyperlink'``, or ``'button'``.

    Returns:
        A ``w:hyperlink`` lxml element ready to append to a paragraph.
    """
    # Create the w:hyperlink tag and add needed values
    hyperlink = OxmlElement("w:hyperlink")

    # Access to the document settings (DocumentPart) to create a new relation id value
    documentPart = document.part
    r_id = documentPart.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    # Attach the relation ID to the hyperlink object
    hyperlink.set(
        qn("r:id"),
        r_id,
    )

    # Create a w:r element
    new_run = OxmlElement("w:r")

    # Create a new w:rPr element
    rPr = OxmlElement("w:rPr")

    if format == "italic":
        rStyle = OxmlElement("w:i")
        rPr.append(rStyle)
    if format == "bold":
        rStyle = OxmlElement("w:b")
        rPr.append(rStyle)

    if format == "hyperlink":
        rStyle = OxmlElement("w:rStyle")
        rStyle.set(qn("w:val"), "Hyperlink")
        rPr.append(rStyle)

    # Join all the xml elements together and add the required text to the w:r element
    new_run.append(rPr)
    new_run.text = f"{text}"

    hyperlink.append(new_run)

    if format == "button":
        # Create a link button with the Hyperlink style, prettier than coloring the whole text
        new_run = OxmlElement("w:r")
        new_run.text = "  "
        hyperlink.append(new_run)

        new_run = OxmlElement("w:r")
        # Unicode character for "download"
        # https://www.fileformat.info/info/unicode/char/2913/fontsupport.htm

        rStyle = OxmlElement("w:rStyle")
        rStyle.set(qn("w:val"), "Hyperlink")
        rPr = OxmlElement("w:rPr")
        rPr.append(rStyle)
        new_run.append(rPr)

        new_run.text = "\u2913"

        hyperlink.append(new_run)

    return hyperlink


def add_hyperlink(paragraph: Paragraph, text: str, url: str, format: HyperlinkFormat = "None") -> _Element:
    """Create a hyperlink and append it to *paragraph*.

    Args:
        paragraph: The paragraph to append the hyperlink to.
        text: Display text for the hyperlink.
        url: Target URL.
        format: Visual style — ``'None'``, ``'bold'``, ``'italic'``,
            ``'hyperlink'``, or ``'button'``.

    Returns:
        The appended ``w:hyperlink`` lxml element.
    """
    # Create hyperlink
    hyperlink = create_hyperlink(paragraph, text, url, format)

    # Append hyperlink to paragraph
    paragraph._p.append(hyperlink)

    return hyperlink
