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


## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:jr2804/rapporteur-helper.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/codecov/).

## Releasing a new version

TODO

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
