# ITU-T Rapporteur's status report generator

This project generates pre-populated status report for Rapporteurs in Study Group 12.

The scripts use `template.docx` as the template generating formatted word documents.
Information fetched from the ITU-T website are:

- Question title
- (co/associate) rapporteur(s) details
- List of contributions
- List of TDs
- Work programme

[![Release](https://img.shields.io/github/v/release/jr2804/rapporteur-helper)](https://img.shields.io/github/v/release/jr2804/rapporteur-helper)
[![Build status](https://img.shields.io/github/actions/workflow/status/jr2804/rapporteur-helper/main.yml?branch=main)](https://github.com/jr2804/rapporteur-helper/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/jr2804/rapporteur-helper/branch/main/graph/badge.svg)](https://codecov.io/gh/jr2804/rapporteur-helper)
[![Commit activity](https://img.shields.io/github/commit-activity/m/jr2804/rapporteur-helper)](https://img.shields.io/github/commit-activity/m/jr2804/rapporteur-helper)
[![License](https://img.shields.io/github/license/jr2804/rapporteur-helper)](https://img.shields.io/github/license/jr2804/rapporteur-helper)

ITU-T Rapporteur's status report generator

- **Github repository**: <https://github.com/jr2804/rapporteur-helper/>
- **Documentation** <https://jr2804.github.io/rapporteur-helper/>

## How to use

1. Use _uv_ tool to setup virtual environment with required packages:

```shell
uv sync
```

2. Update variables with meeting information in `generate_reports.py`:

 * `meetingDetails`: place and date, example: `"Geneva, 18-26 January 2023"`

 * `meetingDate`: first day of the meeting in the format `YYMMDD`. For example, for the meeting starting January 18, 2023: `"230118"`

 * `add_qall`: bool flag to include or exclude Cs/TDs allocated to question "QALL"

3. Execute the script

```
python generate_report.py
```

Word documents for each question are generated automatically in a directory named as the meeting date, for example `./230118`.


## TO DO

- Implement usage of API or (crawling websites?) to retrieve meeting information / need less redundant information
- better replacement of text in template doc; use jinja2 templating, see: [elapouya/python-docx-template](https://github.com/elapouya/python-docx-template)
- Add logging for better traceability instead of print statements
- Write unit tests for critical functions
- Implement a configuration file for easier customization of meeting parameters
- improve template document:
  - use bookmarks to automatically "copy" summary sections to executive summary in Annex.

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
