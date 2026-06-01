"""ITU-T question details retrieval and parsing utilities."""

import contextlib
import logging
import re

from lxml.html import HtmlElement

from ..html import get_html_tree

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuestionDetailsParseException(Exception):
    def __init__(self, url: str) -> None:
        super().__init__(f"get_questions_details - Could not parse question details from {url}")


def find_span_in_row(row: HtmlElement, span_id: str) -> str | None:
    """Return the text of the first span whose ``id`` contains *span_id*, or ``None``.

    Args:
        row: The HTML row element to search within.
        span_id: Substring to match against the span ``id`` attribute.

    Returns:
        The text content of the matched span, or ``None`` if not found.
    """
    matched_item = row.xpath(f".//span[contains(@id,'{span_id}')]/text()")
    return matched_item[0] if matched_item else None


def get_questions_details(studyGroup: int, studyPeriodId: int) -> dict:
    """Fetch and parse rapporteur contact details for all questions in a study period.

    Args:
        studyGroup: ITU-T Study Group number.
        studyPeriodId: Numeric study period identifier.

    Returns:
        A dict keyed by question number, each value containing ``'wp'``,
        ``'title'``, and ``'rapporteurs'`` entries.

    Raises:
        QuestionDetailsParseException: If no question data could be parsed.
    """
    info = {}
    qNum = -1
    url = f"https://www.itu.int/net4/ITU-T/lists/loqr.aspx?Group={studyGroup}&Period={studyPeriodId}"

    tree = get_html_tree(url)

    # Find and parse all rows (<tr>) in the document
    rows = tree.xpath("//tr")

    # Extract WP number and Question title
    for row in rows:
        # Question number and WP
        if len(tmp := row.xpath(".//span[contains(@id,'lblQWP')]/text()")) > 0:
            tmp = tmp[0]
            try:
                res = re.search(rf"Q(\d+)/{studyGroup}.*WP(\d+)/{studyGroup}", tmp)
                if res is None:
                    raise AttributeError("Pattern did not match")
                qNum = int(res.group(1))
                wpNum = int(res.group(2))
            except (AttributeError, ValueError, IndexError) as e:
                # If it fails, check that it is because there is no WP number
                res = re.search(rf"Q(\d+)/{studyGroup}.*", tmp)
                if res is None:
                    raise AttributeError("Could not parse question number") from e
                qNum = int(res.group(1))
                wpNum = -1
                logger.warning("Could not parse WP number for question %s: %s -> Plenary Question?", qNum, e, exc_info=True)

            # try:
            # Question title
            qTitle = row.xpath(".//span[contains(@id,'lblQuestion')]/text()")[0]

            if qNum not in info:
                info[qNum] = {"rapporteurs": []}

            info[qNum].update({"wp": wpNum, "title": qTitle})

            # except Exception as exc:
            #    # This is not a row with a question
            # logger.exception("Exception occurred while parsing question row")

        # Extract Rapporteurs contact details, if question number was parsed out successfully
        if qNum > 0:
            # if lastname cannot be parsed, it's an invalid entry
            lastName = find_span_in_row(row, "dtlRappQues_lblLName")
            if lastName is not None:
                tmp = {}
                tmp["lastName"] = lastName.upper()
                tmp["firstName"] = find_span_in_row(row, "dtlRappQues_lblFName")
                tmp["role"] = find_span_in_row(row, "dtlRappQues_lblRole")
                tmp["company"] = find_span_in_row(row, "dtlRappQues_lblCompany")
                tmp["address"] = " ".join(row.xpath(".//span[contains(@id,'dtlRappQues_lblAddress')]/text()"))
                tmp["country"] = row.xpath(".//span[contains(@id,'dtlRappQues_lblAddress')]/text()")[-1]

                with contextlib.suppress(IndexError):
                    # Some Rapporteurs do not have a telephone number available
                    tmp["tel"] = row.xpath(".//span[contains(@id,'dtlRappQues_telLabel')]/text()")[0]
                tmp["email"] = row.xpath(".//a[contains(@id,'dtlRappQues_linkemail')]/text()")[0].replace("[at]", "@")

                info[qNum]["rapporteurs"].append(tmp)

    if len(info) < 1:
        raise QuestionDetailsParseException(url)

    return info


if __name__ == "__main__":
    pass
