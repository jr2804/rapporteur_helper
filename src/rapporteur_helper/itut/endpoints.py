"""ITU-T meeting document endpoint construction utilities."""

from typing import Any

from ..data.constants import hostname
from . import VALID_DOCTYPES, DocType


def get_endpoint(studyGroup: int, question: int | str | None, studyPeriodStart: Any, meetingDate: Any, endpoint_type: DocType) -> dict[str, str]:
    """Build an ITU-T meeting document endpoint descriptor.

    Args:
        studyGroup: ITU-T Study Group number.
        question: Question number, question string, or ``None`` for all questions.
        studyPeriodStart: Two-digit study period start year (e.g. ``25``).
        meetingDate: Meeting date string in ``YYMMDD`` format.
        endpoint_type: Document type selector.

    Returns:
        A dict with ``'url'``, ``'prefix'``, and ``'title'`` keys.
    """
    question = "ALL" if question is None else question
    prefix = f"SG{studyGroup}-{endpoint_type}"
    url = f"{hostname}/md/meetingdoc.asp?lang=en&parent=T{studyPeriodStart}-SG{studyGroup}-{meetingDate}-{endpoint_type}&question=Q{question}/{studyGroup}"

    return {"url": url, "prefix": prefix, "title": VALID_DOCTYPES[endpoint_type]}


if __name__ == "__main__":
    pass
