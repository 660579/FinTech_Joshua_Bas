"""Generate synthetic demo invoices.

Produces backend/data/demo_invoices.csv with realistic line item descriptions
specific enough for EU Taxonomy classification (e.g. "solar panel installation",
"diesel fuel 500L") rather than generic labels.

Usage:
    python scripts/generate_synthetic_invoices.py
"""
from __future__ import annotations

from pathlib import Path

OUTPUT_PATH = Path("backend/data/demo_invoices.csv")


def generate() -> None:
    # TODO: build a list of synthetic Invoice/LineItem dicts and write to OUTPUT_PATH
    pass


if __name__ == "__main__":
    generate()
