from __future__ import annotations

from pathlib import Path

from backend.app.models.schemas import Invoice


def parse_csv(path: Path) -> list[Invoice]:
    # TODO: read CSV, return list of Invoice models
    pass


def parse_json(path: Path) -> list[Invoice]:
    # TODO: read JSON, return list of Invoice models
    pass


def parse_file(path: Path) -> list[Invoice]:
    # TODO: dispatch to parse_csv or parse_json based on suffix
    pass
