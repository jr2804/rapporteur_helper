"""ITU-T work programme retrieval, parsing, and Word document insertion utilities."""

from __future__ import annotations

import copy
import logging
import string
from dataclasses import dataclass, field

import docx
from docx.document import Document

from ..html import get_html_tree
from ..word_docx.links import create_hyperlink
from ..word_docx.tables import replace_in_table

logger = logging.getLogger(__name__)


@dataclass
class EditorInfo:
    href: str
    name: str


@dataclass
class BaseTextItem:
    href: str
    name: str


@dataclass
class WorkItem:
    href: str
    work_item: str
    version: str
    title: str
    process: str
    priority: str
    timing: str
    editors: list[EditorInfo] = field(default_factory=list)
    basetext: list[BaseTextItem] = field(default_factory=list)
    relationship: list[str] = field(default_factory=list)


def get_work_program(Q: int, verbose: bool = False, studyGroup: int = 12, isn_sp: int | None = None) -> list[WorkItem]:
    """Fetch and parse the ITU-T work programme for a given question.

    Args:
        Q: Question number.
        verbose: Log the request URL when ``True``.
        studyGroup: ITU-T Study Group number.
        isn_sp: Study period ISN; when set, the ISN-based URL form is used.

    Returns:
        A list of :class:`WorkItem` dataclasses, one per row found.

    Raises:
        ValueError: If no rows are returned from the work programme page.
    """
    isn_sp = False
    # isn_sp = 9677

    if isn_sp:
        # Preparing for the day the ITU-T API is being updated to only allow ISNs
        sgIndex = {12: 9683}
        qIndex = {
            1: 10694,
            2: 10695,
            4: 10696,
            5: 10697,
            6: 10698,
            7: 10699,
            9: 10700,
            10: 10701,
            12: 10702,
            13: 10703,
            14: 10704,
            15: 10705,
            17: 10706,
            19: 10707,
            20: 10708,
        }

        url = f"https://www.itu.int/ITU-T/workprog/wp_search.aspx?isn_sg={sgIndex[studyGroup]}&qIndex={qIndex[Q]}&isn_sp={isn_sp}&isn_status=-1,1,3,7&details=1&view=tab&field=ahjgoflki"
    else:
        url = f"https://www.itu.int/ITU-T/workprog/wp_search.aspx?sg={studyGroup}&q={Q}&isn_sp={isn_sp}&isn_status=-1,1,3,7&details=1&view=tab&field=ahjgoflki"

    info = []

    if verbose:
        logger.info(f"Fetching work program from: {url}")
    tree = get_html_tree(url)

    # Find and parse all rows (<tr>) in the document
    rows = tree.xpath("//table[contains(@id, 'tab_tabular_view_gd_wp_tabular')]/tr")

    if not len(rows) >= 1:
        raise ValueError("Error fetching work program - no rows found - Please check query response")

    for row in rows:
        try:
            tds = row.xpath(".//td")

            # 1st column - Work item
            href = tds[0].xpath(".//a/@href")[0].strip()
            work_item_id = tds[0].xpath(".//a/text()")[0]

            # 2nd column - Version
            version = tds[1].xpath(".//div/text()")[0]

            # 3rd column - Title
            title = tds[2].xpath(".//text()")[0]

            # 4th column - Approval process
            process = tds[3].xpath(".//div/text()")[0]

            # 5th column - Priority
            priority = tds[4].xpath(".//div/text()")[0]

            # 6th column - Timing
            timing = tds[5].xpath(".//div/nobr/text()")[0]

            # 7th column - Editors
            editors: list[EditorInfo] = []
            try:
                for editor in tds[6].xpath(".//a"):
                    editors.append(
                        EditorInfo(
                            href=editor.xpath(".//@href")[0].strip().replace("(AT)", "@"),
                            name=editor.xpath("./text()")[0],
                        )
                    )
            except (IndexError, AttributeError):
                logger.warning("Cannot retrieve editors", exc_info=True)

            # 8th column - Base documents
            basetext: list[BaseTextItem] = []
            for text in tds[7].xpath(".//a"):
                basetext.append(
                    BaseTextItem(
                        href=text.xpath(".//@href")[0].strip(),
                        name=text.xpath(".//text()")[0],
                    )
                )

            # 9th column - Liaisons
            relationship = [x.strip() for x in tds[8].xpath(".//text()")[0].split(",")]

            info.append(
                WorkItem(
                    href=href,
                    work_item=work_item_id,
                    version=version,
                    title=title,
                    process=process,
                    priority=priority,
                    timing=timing,
                    editors=editors,
                    basetext=basetext,
                    relationship=relationship,
                )
            )

        except (IndexError, AttributeError, ValueError) as e:
            logger.warning("Skipping malformed work programme row: %s", e, exc_info=True)

    return info


def insert_work_program(document: Document, info: list[WorkItem]) -> None:
    """Populate the work programme table in *document* with parsed work items.

    Args:
        document: The Word document containing the work programme template table.
        info: Parsed work items as returned by :func:`get_work_program`.
    """
    # Find the work program table
    targetTable = None

    for table in document.tables:
        for idx, row in enumerate(table.rows):
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    s = paragraph.text.translate({ord(c): None for c in string.whitespace})
                    if s.lower() == "approvalprocess":
                        targetTable = table
                        break
    if targetTable is None:
        logger.error("Cannot find work program table in document!")
        return

    for idx, work_item in enumerate(info):
        # Duplicate row
        if idx != len(info) - 1:
            targetTable.rows[-1]._tr.addnext(copy.deepcopy(targetTable.rows[-1]._tr))

        new_h = create_hyperlink(targetTable, work_item.work_item, work_item.href, format="hyperlink")
        replace_in_table(targetTable, "WP_WorkItem", new_h)
        replace_in_table(targetTable, "WP_Version", work_item.version)
        replace_in_table(targetTable, "WP_Process", work_item.process)
        replace_in_table(targetTable, "WP_Priority", work_item.priority)
        replace_in_table(targetTable, "WP_Timing", work_item.timing)
        replace_in_table(targetTable, "WP_Relationship", ",\n".join(work_item.relationship))
        replace_in_table(targetTable, "WP_Title", work_item.title)
        replace_in_table(targetTable, "WP_Editors", ",\n".join(x.name for x in work_item.editors))

        # Generate base texts with links
        newRun = docx.oxml.shared.OxmlElement("w:r")
        for idx, x in enumerate(work_item.basetext):
            if idx > 0:
                tmp = docx.oxml.shared.OxmlElement("w:r")
                tmp.text = ", "
                newRun.append(tmp)
            newRun.append(create_hyperlink(document, x.name, x.href, format="hyperlink"))

        replace_in_table(targetTable, "WP_BaseTexts", newRun)

    pass


if __name__ == "__main__":
    pass
