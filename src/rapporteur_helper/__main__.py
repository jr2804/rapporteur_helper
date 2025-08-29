import logging
from pathlib import Path

import click

from rapporteur_helper.generate_reports import main


@click.command()
@click.option("--meeting-date", "-d", default="250909", help="Meeting date in YYMMDD format (default: 250909)")
@click.option(
    "--questions",
    "-q",
    default="1-20",
    help="Question numbers to process. Can be a range (e.g., '1-20'), comma-separated list (e.g., '1,2,7,14'), or single number (default: 1-20)",
)
@click.option("--meeting-place", "-p", default="Geneva", help="Meeting location (default: Geneva)")
@click.option("--meeting-duration-days", "-n", default=9, type=int, help="Duration of the meeting in days (default: 9)")
@click.option("--study-group", "-s", default=12, type=int, help="ITU-T Study Group number (default: 12)")
@click.option("--study-period-id", default=18, type=int, help="Study period ID for API queries (default: 18)")
@click.option("--study-period-start", default=25, type=int, help="Study period start year (2-digit) for API queries (default: 25)")
@click.option("--add-qall/--no-add-qall", default=False, help="Include documents for all questions in each report (default: False)")
@click.option("--output-dir", "-o", type=click.Path(path_type=Path), help="Output directory for generated reports (default: current directory)")
@click.option("--verbose/--no-verbose", "-v", default=False, help="Enable verbose output (default: False)")
def cli(
    meeting_date: str,
    questions: str,
    meeting_place: str,
    meeting_duration_days: int,
    study_group: int,
    study_period_id: int,
    study_period_start: int,
    add_qall: bool,
    output_dir: Path,
    verbose: bool,
):
    """ITU-T Rapporteur's status report generator.

    This tool generates status reports for ITU-T Study Group questions based on
    contributions and temporary documents from the ITU-T website.
    """
    # Configure logging
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Parse questions parameter
    question_list = parse_questions(questions)

    if verbose:
        click.echo(f"Generating reports for questions: {question_list}")
        click.echo(f"Meeting: {meeting_place}, {meeting_date}")
        click.echo(f"Study Group: {study_group}")

    main(
        meetingDate=meeting_date,
        questions=question_list,
        meeting_place=meeting_place,
        meeting_duration_days=meeting_duration_days,
        studyGroup=study_group,
        studyPeriodId=study_period_id,
        studyPeriodStart=study_period_start,
        add_qall=add_qall,
        output_dir=output_dir,
        verbose=verbose,
    )


def parse_questions(questions: str) -> list[int]:
    """Parse questions parameter into a list of integers.

    Args:
        questions: String containing question numbers in various formats:
                  - Range: "1-20"
                  - Comma-separated: "1,2,7,14"
                  - Single number: "5"

    Returns:
        List of question numbers as integers
    """
    if "-" in questions and "," not in questions:
        # Range format: "1-20"
        start, end = questions.split("-")
        return list(range(int(start), int(end) + 1))
    elif "," in questions:
        # Comma-separated format: "1,2,7,14"
        return [int(q.strip()) for q in questions.split(",")]
    else:
        # Single number: "5"
        return [int(questions)]


if __name__ == "__main__":
    cli()
# end of file
