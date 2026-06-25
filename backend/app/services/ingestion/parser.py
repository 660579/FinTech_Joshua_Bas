"""Invoice ingestion: parse CSV or JSON files into structured pydantic models.

CSV format is flat (one row per line item); rows sharing an invoice_id are
grouped into a single Invoice with a list of LineItems.

JSON format mirrors the Invoice model directly: a list of Invoice objects.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from backend.app.models.schemas import Invoice, LineItem

_REQUIRED_CSV_COLUMNS = {
    "invoice_id", "sme_id", "date", "supplier", "description", "quantity", "unit", "amount"
}


def parse_csv(path: Path) -> list[Invoice]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV file is empty or has no header: {path}")

        actual = set(reader.fieldnames)
        missing = _REQUIRED_CSV_COLUMNS - actual
        if missing:
            raise ValueError(
                f"CSV is missing required columns: {sorted(missing)}"
            )

        # Group rows by invoice_id, preserving insertion order.
        groups: dict[str, list[dict]] = {}
        for row in reader:
            iid = row["invoice_id"]
            groups.setdefault(iid, []).append(row)

    invoices: list[Invoice] = []
    for iid, rows in groups.items():
        first = rows[0]
        line_items = [
            LineItem(
                supplier=r["supplier"],
                description=r["description"],
                quantity=float(r["quantity"]),
                unit=r["unit"] or None,
                amount=float(r["amount"]),
            )
            for r in rows
        ]
        invoices.append(
            Invoice(
                invoice_id=iid,
                sme_id=first["sme_id"],
                date=first["date"],
                currency=first.get("currency", "EUR") or "EUR",
                line_items=line_items,
            )
        )
    return invoices


def parse_json(path: Path) -> list[Invoice]:
    with path.open(encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, list):
        raise ValueError(f"JSON file must contain a list of invoice objects: {path}")

    return [Invoice.model_validate(item) for item in raw]


def parse_file(path: Path) -> list[Invoice]:
    """Dispatch to the correct parser based on file suffix."""
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return parse_csv(path)
    if suffix == ".json":
        return parse_json(path)
    raise ValueError(f"Unsupported file format '{suffix}'. Expected .csv or .json.")


def parse_invoices(filepath: str) -> list[Invoice]:
    """Public API: parse an invoice file (CSV or JSON) and return Invoice list."""
    return parse_file(Path(filepath))
