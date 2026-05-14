"""Time series loaded from Hector's ``core_inputs.csv``.

This module avoids copying long lists into Python source and instead reads
the canonical CSV distributed with Hector.
"""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path


_CORE_INPUTS_REL_PATH = Path("hector") / "inst" / "input" / "tables" / "core_inputs.csv"


def _core_inputs_path() -> Path:
    """Return absolute path to Hector's core input table."""
    repo_root = Path(__file__).resolve().parents[1]
    path = repo_root / _CORE_INPUTS_REL_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"Could not find core inputs table at {path}. "
            "Ensure the Hector submodule is present."
        )
    return path


@lru_cache(maxsize=1)
def _read_core_inputs() -> list[dict[str, str]]:
    """Read ``core_inputs.csv`` into a list of row dictionaries."""
    path = _core_inputs_path()

    # The first line is a semicolon-prefixed comment; strip comment/blank lines.
    with path.open("r", encoding="utf-8") as fh:
        lines = [line for line in fh if line.strip() and not line.lstrip().startswith(";")]

    return list(csv.DictReader(lines))


def _column_as_timeseries(column: str) -> list[tuple[int, float]]:
    """Extract a (year, value) list for one CSV column."""
    rows = _read_core_inputs()
    out: list[tuple[int, float]] = []
    for row in rows:
        out.append((int(row["Date"]), float(row[column])))
    return out


CH4N = _column_as_timeseries("CH4N")
N2O_NATURAL_EMISSIONS = _column_as_timeseries("N2O_natural_emissions")
SV = _column_as_timeseries("SV")
