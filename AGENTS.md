# AGENTS.md

## Project

CLI tool for tracking Vitamin D deficiency. Pure Python, zero dependencies. Built with `uv`, packaged with `hatchling`.

## Commands

```bash
uv run vitd <command>          # Run any CLI command
uv build                       # Build wheel + sdist to dist/
uv run vitd setup --level X    # First-time setup (writes ~/.vitd/data.json)
```

## Architecture

- `src/vitd/cli.py` — all commands, entry point via `vitd.cli:main` (defined in pyproject.toml `[project.scripts]`)
- `src/vitd/storage.py` — JSON persistence at `~/.vitd/data.json` (not in repo)
- `src/vitd/config.py` — thresholds, ANSI color codes
- `src/vitd/__init__.py` — version (must match `pyproject.toml` version on release)

## Gotchas

- No test suite yet. Verify changes by running `uv run vitd` + subcommands manually.
- No linter/formatter configured. Follow existing style: no comments, single quotes not used, 4-space indent.
- `config.py` uses delayed imports in `storage.py` (`from .config import ...`) — don't restructure to top-level without reason.
- `~/.vitd/` is user data, created at runtime. Never reference it in tests or build.
- Hatchling validates classifiers strictly — only use official PyPI trove classifiers.
- `README.md` must exist (hatchling enforces it per `readme = "README.md"` in pyproject.toml).
- Version is in two places: `pyproject.toml` and `src/vitd/__init__.py`. Bump both on release.
- `.python-version` pins the uv Python version; don't change casually.
