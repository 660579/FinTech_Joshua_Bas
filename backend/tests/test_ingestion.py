"""Tests for backend/app/services/ingestion/parser.py.

Uses small inline fixtures rather than the full generated demo file so that
tests stay fast and self-contained.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from backend.app.models.schemas import Invoice
from backend.app.services.ingestion.parser import parse_file, parse_invoices

# ---------------------------------------------------------------------------
# Shared fixture content
# ---------------------------------------------------------------------------

VALID_CSV = """\
invoice_id,sme_id,date,supplier,description,quantity,unit,amount
INV-001,sme-001,2025-01-10,SolarTech BV,Rooftop solar panel installation 4 kWp,1.0,installation,12400.00
INV-001,sme-001,2025-01-10,SolarTech BV,LED high-bay lighting retrofit 40 units,40.0,unit,3200.00
INV-002,sme-001,2025-02-05,Total Energies NL,Diesel fuel B7 500 L for forklift fleet,500.0,L,780.00
"""

VALID_JSON = json.dumps([
    {
        "invoice_id": "INV-A",
        "sme_id": "sme-001",
        "date": "2025-03-01",
        "currency": "EUR",
        "line_items": [
            {
                "supplier": "EcoVolt Europe SA",
                "description": "EV charging station 22 kW installation",
                "quantity": 2.0,
                "unit": "unit",
                "amount": 4800.00,
            }
        ],
    },
    {
        "invoice_id": "INV-B",
        "sme_id": "sme-001",
        "date": "2025-03-15",
        "line_items": [
            {
                "supplier": "DMG Mori Service BV",
                "description": "CNC milling machine preventive maintenance 4 000 h service",
                "quantity": 1.0,
                "unit": "service",
                "amount": 1450.00,
            },
            {
                "supplier": "DMG Mori Service BV",
                "description": "Carbide end-mill cutting tool set 20-piece",
                "quantity": 20.0,
                "unit": "unit",
                "amount": 860.00,
            },
        ],
    },
])


# ---------------------------------------------------------------------------
# CSV tests
# ---------------------------------------------------------------------------

class TestParseCsv:
    def test_returns_correct_invoice_count(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "invoices.csv"
        csv_file.write_text(VALID_CSV, encoding="utf-8")

        invoices = parse_file(csv_file)

        # Two distinct invoice_ids in the fixture.
        assert len(invoices) == 2

    def test_groups_line_items_under_invoice(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "invoices.csv"
        csv_file.write_text(VALID_CSV, encoding="utf-8")

        invoices = parse_file(csv_file)
        inv001 = next(i for i in invoices if i.invoice_id == "INV-001")

        assert len(inv001.line_items) == 2

    def test_fields_map_correctly(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "invoices.csv"
        csv_file.write_text(VALID_CSV, encoding="utf-8")

        invoices = parse_file(csv_file)
        inv002 = next(i for i in invoices if i.invoice_id == "INV-002")

        assert inv002.sme_id == "sme-001"
        assert inv002.date == "2025-02-05"
        assert len(inv002.line_items) == 1

        item = inv002.line_items[0]
        assert item.description == "Diesel fuel B7 500 L for forklift fleet"
        assert item.quantity == 500.0
        assert item.unit == "L"
        assert item.amount == 780.00

    def test_returns_invoice_instances(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "invoices.csv"
        csv_file.write_text(VALID_CSV, encoding="utf-8")

        invoices = parse_file(csv_file)

        assert all(isinstance(inv, Invoice) for inv in invoices)

    def test_missing_column_raises_value_error(self, tmp_path: Path) -> None:
        # 'amount' column intentionally omitted.
        bad_csv = "invoice_id,sme_id,date,supplier,description,quantity,unit\n"
        bad_csv += "INV-001,sme-001,2025-01-10,Supplier A,Some item,1.0,unit\n"
        csv_file = tmp_path / "bad.csv"
        csv_file.write_text(bad_csv, encoding="utf-8")

        with pytest.raises(ValueError, match="missing required columns"):
            parse_file(csv_file)

    def test_empty_file_raises_value_error(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("", encoding="utf-8")

        with pytest.raises(ValueError, match="empty or has no header"):
            parse_file(csv_file)


# ---------------------------------------------------------------------------
# JSON tests
# ---------------------------------------------------------------------------

class TestParseJson:
    def test_returns_correct_invoice_count(self, tmp_path: Path) -> None:
        json_file = tmp_path / "invoices.json"
        json_file.write_text(VALID_JSON, encoding="utf-8")

        invoices = parse_file(json_file)

        assert len(invoices) == 2

    def test_line_items_parsed(self, tmp_path: Path) -> None:
        json_file = tmp_path / "invoices.json"
        json_file.write_text(VALID_JSON, encoding="utf-8")

        invoices = parse_file(json_file)
        inv_b = next(i for i in invoices if i.invoice_id == "INV-B")

        assert len(inv_b.line_items) == 2

    def test_fields_map_correctly(self, tmp_path: Path) -> None:
        json_file = tmp_path / "invoices.json"
        json_file.write_text(VALID_JSON, encoding="utf-8")

        invoices = parse_file(json_file)
        inv_a = next(i for i in invoices if i.invoice_id == "INV-A")

        assert inv_a.currency == "EUR"
        item = inv_a.line_items[0]
        assert item.amount == 4800.00
        assert item.quantity == 2.0

    def test_non_list_json_raises_value_error(self, tmp_path: Path) -> None:
        json_file = tmp_path / "bad.json"
        json_file.write_text('{"invoice_id": "INV-001"}', encoding="utf-8")

        with pytest.raises(ValueError, match="must contain a list"):
            parse_file(json_file)


# ---------------------------------------------------------------------------
# Unsupported format test
# ---------------------------------------------------------------------------

class TestParseFile:
    def test_unsupported_extension_raises_value_error(self, tmp_path: Path) -> None:
        xml_file = tmp_path / "invoices.xml"
        xml_file.write_text("<invoices/>", encoding="utf-8")

        with pytest.raises(ValueError, match="Unsupported file format"):
            parse_file(xml_file)


# ---------------------------------------------------------------------------
# Public API (parse_invoices)
# ---------------------------------------------------------------------------

class TestParseInvoices:
    def test_accepts_string_path(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "invoices.csv"
        csv_file.write_text(VALID_CSV, encoding="utf-8")

        invoices = parse_invoices(str(csv_file))

        assert len(invoices) == 2
