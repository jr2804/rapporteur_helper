"""CLI parameter definitions and parsing for rapporteur helper."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class CLIParameters:
    """Structured CLI parameters with validation."""

    meeting_date: str
    questions: str
    meeting_place: str
    meeting_duration_days: int
    study_group: int
    study_period_id: int
    study_period_start: int
    add_qall: bool
    output_dir: Path | None
    verbose: bool

    def parse_questions(self) -> list[int]:
        """Parse questions parameter into a list of integers.

        Supports:
            - Range: "1-20"
            - Comma-separated: "1,2,7,14"
            - Single number: "5"

        Returns:
            List of question numbers as integers.
        """
        if "-" in self.questions and "," not in self.questions:
            start, end = self.questions.split("-")
            return list(range(int(start), int(end) + 1))
        elif "," in self.questions:
            return [int(q.strip()) for q in self.questions.split(",")]
        else:
            return [int(self.questions)]
