from pathlib import Path

import pytest

from backend.app.services.ingestion.parser import parse_file
from backend.app.models.schemas import Invoice


def test_parse_csv_returns_invoices(tmp_path: Path) -> None:
    # TODO: write a minimal CSV fixture, assert parse_file returns Invoice list
    pass


def test_parse_json_returns_invoices(tmp_path: Path) -> None:
    # TODO: write a minimal JSON fixture, assert parse_file returns Invoice list
    pass
