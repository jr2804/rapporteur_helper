"""Typer CLI application for rapporteur helper."""

import logging
from datetime import date
from pathlib import Path
from typing import Annotated

import typer

from rapporteur_helper.cli.args import CLIParameters
from rapporteur_helper.generate_reports import main
from rapporteur_helper.itut.meeting import MeetingInfo, fetch_meeting_info

app = typer.Typer(
    name="rapporteur-helper",
    help="ITU-T Rapporteur's status report generator.",
    no_args_is_help=True,
)


def _parse_yymmdd(s: str) -> date:
    """Parse a YYMMDD string into a date."""
    return date(2000 + int(s[:2]), int(s[2:4]), int(s[4:6]))


@app.command()
def generate(
    questions: Annotated[
        str,
        typer.Option(
            "--questions",
            "-q",
            help="Question numbers: range (1-20), list (1,2,7), or single (5)",
        ),
    ] = "1-20",
    study_group: Annotated[int, typer.Option("--study-group", "-s", help="ITU-T Study Group number")] = 12,
    study_period_id: Annotated[int, typer.Option("--study-period-id", help="Study period ID for API queries")] = 18,
    study_period_start: Annotated[int, typer.Option("--study-period-start", help="Study period start year (2-digit)")] = 25,
    meeting_date: Annotated[
        str | None,
        typer.Option("--meeting-date", "-d", help="Override meeting start date (YYMMDD). If omitted, fetched from ITU-T website."),
    ] = None,
    meeting_place: Annotated[
        str | None,
        typer.Option("--meeting-place", "-p", help="Override meeting location. If omitted, fetched from ITU-T website."),
    ] = None,
    meeting_end_date: Annotated[
        str | None,
        typer.Option("--meeting-end-date", help="Override meeting end date (YYMMDD). If omitted, fetched from ITU-T website."),
    ] = None,
    add_qall: Annotated[bool, typer.Option("--add-qall/--no-add-qall", help="Include documents for all questions")] = False,
    output_dir: Annotated[
        Path | None,
        typer.Option("--output-dir", "-o", help="Output directory for reports"),
    ] = None,
    verbose: Annotated[bool, typer.Option("--verbose/--no-verbose", "-v", help="Enable verbose output")] = False,
) -> None:
    """Generate status reports for ITU-T Study Group questions.

    Automatically fetches meeting details (place, dates) from the ITU-T Study Group page.
    Use --meeting-date, --meeting-place, --meeting-end-date to override.
    """
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    params = CLIParameters(
        meeting_date=meeting_date or "",
        questions=questions,
        meeting_place=meeting_place or "",
        meeting_duration_days=0,
        study_group=study_group,
        study_period_id=study_period_id,
        study_period_start=study_period_start,
        add_qall=add_qall,
        output_dir=output_dir,
        verbose=verbose,
    )
    question_list = params.parse_questions()

    meeting_info: MeetingInfo | None = None
    if meeting_date and meeting_place and meeting_end_date:
        start = _parse_yymmdd(meeting_date)
        end = _parse_yymmdd(meeting_end_date)
        meeting_info = MeetingInfo(place=meeting_place, start_date=start, end_date=end)
    elif meeting_date or meeting_place or meeting_end_date:
        meeting_info = fetch_meeting_info(study_group)
        if meeting_date:
            meeting_info.start_date = _parse_yymmdd(meeting_date)
        if meeting_end_date:
            meeting_info.end_date = _parse_yymmdd(meeting_end_date)
        if meeting_place:
            meeting_info.place = meeting_place

    if verbose:
        info = meeting_info or fetch_meeting_info(study_group)
        typer.echo(f"Meeting: {info.meeting_details}")
        typer.echo(f"Questions: {question_list}")
        typer.echo(f"Study Group: {study_group}")
        if meeting_info is None:
            meeting_info = info

    main(
        questions=question_list,
        meeting_info=meeting_info,
        studyGroup=study_group,
        studyPeriodId=study_period_id,
        studyPeriodStart=study_period_start,
        add_qall=add_qall,
        output_dir=output_dir,
        verbose=verbose,
    )


if __name__ == "__main__":
    app()
