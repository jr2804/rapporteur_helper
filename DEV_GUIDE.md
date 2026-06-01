# Developer Guide

## Running Tests

```powershell
uv run python -m pytest
```

Run with coverage:

```powershell
uv run python -m pytest --cov=rapporteur_helper --cov-report=term-missing
```

Run a specific test file:

```powershell
uv run python -m pytest tests/test_itut_parsing.py
```

## Running tox (multi-version CI)

```powershell
uv run tox
```

## Pre-commit Hooks

Install pre-commit hooks once:

```powershell
uv run pre-commit install
```

Run hooks manually against all files:

```powershell
uv run pre-commit run --all-files
```

### Hooks configured

| Hook | Purpose |
|------|---------|
| `ruff` | Lint and auto-format Python source |
| `ty check` | Static type checking |

## Dependency Management

Add a runtime dependency:

```powershell
uv add <package>
```

Add a development dependency:

```powershell
uv add --dev <package>
```

Sync the environment after editing `pyproject.toml`:

```powershell
uv sync
```
