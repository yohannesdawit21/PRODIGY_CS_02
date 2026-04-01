#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _find_local_venv_python() -> Path | None:
    """Return the repo-local virtualenv interpreter when available."""
    base_dir = Path(__file__).resolve().parent
    candidates = [
        base_dir / ".venv" / "bin" / "python",
        base_dir / ".venv" / "Scripts" / "python.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _reexec_with_local_venv() -> bool:
    """Re-run the command with the project's virtualenv interpreter."""
    local_python = _find_local_venv_python()
    if local_python is None:
        return False

    local_venv_dir = local_python.parent.parent
    if Path(sys.prefix).resolve() == local_venv_dir.resolve():
        return False

    os.execv(str(local_python), [str(local_python), __file__, *sys.argv[1:]])
    return True


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as error:
        if _reexec_with_local_venv():
            return
        raise ImportError(
            "Couldn't import Django. Activate the project's .venv or install the requirements."
        ) from error

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
