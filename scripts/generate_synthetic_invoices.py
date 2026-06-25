"""Generate synthetic demo invoices for GreenLedger.

Produces backend/data/synthetic/demo_invoices.csv with realistic, specific
line item descriptions suited for EU Taxonomy classification via embedding
similarity. The SME is a NACE C25 (fabricated metal products) manufacturer
with 30-50 employees.

Usage:
    python scripts/generate_synthetic_invoices.py
"""
from __future__ import annotations

import csv
import random
from pathlib import Path

# Seed for reproducibility. Never change without team agreement.
RANDOM_SEED = 42

OUTPUT_PATH = Path("backend/data/synthetic/demo_invoices.csv")

SME_ID = "sme-nace-c25-demo"

# Supplier name pools: randomised, not the line item descriptions.
ENERGY_SUPPLIERS = ["SolarTech NL BV", "GreenPower Installations GmbH", "EcoVolt Europe SA"]
FUEL_SUPPLIERS = ["Total Energies NL", "Shell Business Fuels BV", "Energie Depot Rotterdam"]
STEEL_SUPPLIERS = ["ArcelorMittal Recycled Materials", "European Steel Scrap BV", "MetalloRec GmbH"]
MACHINE_SUPPLIERS = ["DMG Mori Service BV", "Haas CNC Solutions NL", "Trumpf Benelux BV"]
LOGISTICS_SUPPLIERS = ["DB Schenker NL", "DHL Freight Europe", "Kuehne+Nagel BV"]
OFFICE_SUPPLIERS = ["Staples Business NL", "Office Depot Europe BV"]
FURNACE_SUPPLIERS = ["Thermcraft Industrial NL", "SECO Warmtebehandeling BV"]
WATER_SUPPLIERS = ["Veolia Water Technologies", "Pentair Industrial Solutions BV"]
EV_SUPPLIERS = ["EVBox Charging Solutions", "Allego Business BV"]

# Fixed invoice content: (supplier_pool, description, quantity, unit, amount)
# Descriptions are specific and intentional (not randomised) so embeddings
# can reliably distinguish green / non-green / ambiguous items.
INVOICE_LINE_ITEMS: list[tuple[list[str], str, float, str, float]] = [
    # INV-2025-001: energy upgrade (clearly green CapEx)
    (ENERGY_SUPPLIERS, "Rooftop solar panel installation 4 kWp with inverter", 1.0, "installation", 12400.00),
    (ENERGY_SUPPLIERS, "LED high-bay lighting retrofit for production hall (40 units)", 40.0, "unit", 3200.00),
    # INV-2025-002: EV charging (clearly green CapEx)
    (EV_SUPPLIERS, "EV charging station installation 22 kW Type 2 AC (2 points)", 2.0, "unit", 4800.00),
    (EV_SUPPLIERS, "Electrical grid connection upgrade for EV charging infrastructure", 1.0, "installation", 1850.00),
    # INV-2025-003: recycled raw material (clearly green OpEx)
    (STEEL_SUPPLIERS, "Recycled steel sheet S235 2 mm thickness 500 kg", 500.0, "kg", 620.00),
    (STEEL_SUPPLIERS, "Recycled aluminium extrusion alloy 6063 200 kg", 200.0, "kg", 490.00),
    # INV-2025-004: diesel and fossil fuels (clearly non-green OpEx)
    (FUEL_SUPPLIERS, "Diesel fuel B7 500 L for forklift fleet", 500.0, "L", 780.00),
    (FUEL_SUPPLIERS, "LPG propane 250 kg for overhead crane heating system", 250.0, "kg", 310.00),
    # INV-2025-005: coal-fired furnace (clearly non-green)
    (FURNACE_SUPPLIERS, "Coal-fired heat treatment furnace annual service and calibration", 1.0, "service", 2200.00),
    (FURNACE_SUPPLIERS, "Furnace refractory lining replacement (coal-fired batch annealing)", 1.0, "service", 5600.00),
    # INV-2025-006: CNC machine servicing (ambiguous / neutral CapEx maintenance)
    (MACHINE_SUPPLIERS, "CNC milling machine scheduled preventive maintenance (4 000 h service)", 1.0, "service", 1450.00),
    (MACHINE_SUPPLIERS, "Carbide end-mill cutting tool set replacement 20-piece", 20.0, "unit", 860.00),
    # INV-2025-007: office consumables (ambiguous / neutral OpEx)
    (OFFICE_SUPPLIERS, "Office paper A4 80 g/m² 5 reams", 5.0, "ream", 45.00),
    (OFFICE_SUPPLIERS, "General office supplies (pens, folders, toner cartridges)", 1.0, "lot", 210.00),
    # INV-2025-008: logistics and freight (ambiguous)
    (LOGISTICS_SUPPLIERS, "Road freight transport services, outbound finished goods 3 pallets", 3.0, "pallet", 390.00),
    (LOGISTICS_SUPPLIERS, "Inbound raw material transport, steel coil delivery 2 t", 2.0, "tonne", 280.00),
    # INV-2025-009: water treatment (potentially green, circular economy / pollution prevention)
    (WATER_SUPPLIERS, "Industrial wastewater treatment system filter media replacement", 1.0, "service", 1100.00),
    (WATER_SUPPLIERS, "Cooling water treatment chemical dosing pump installation", 1.0, "installation", 2300.00),
    # INV-2025-010: mixed green + neutral CapEx
    (ENERGY_SUPPLIERS, "Building insulation upgrade, mineral wool 150 mm production hall roof", 320.0, "m2", 9600.00),
    (MACHINE_SUPPLIERS, "Variable-frequency drive (VFD) retrofit for main compressor motor 15 kW", 1.0, "unit", 3400.00),
    # INV-2025-011: packaging and consumables (neutral OpEx)
    (LOGISTICS_SUPPLIERS, "Stretch film pallet wrapping consumables 6 rolls", 6.0, "roll", 180.00),
    (OFFICE_SUPPLIERS, "Safety PPE kit: hard hats, gloves, safety glasses (10 sets)", 10.0, "set", 520.00),
    # INV-2025-012: mixed green / non-green maintenance
    (FURNACE_SUPPLIERS, "Natural gas connection inspection and burner efficiency tuning", 1.0, "service", 750.00),
    (WATER_SUPPLIERS, "Rainwater harvesting tank installation 5 000 L with pump", 1.0, "installation", 4100.00),
]

# Map each line-item index to an invoice, grouped intentionally so that
# each invoice contains 2-4 thematically related or mixed items.
INVOICE_GROUPS: list[tuple[str, str, list[int]]] = [
    # (invoice_id, date, [line_item_indices])
    ("INV-2025-001", "2025-01-15", [0, 1]),         # energy upgrades
    ("INV-2025-002", "2025-02-03", [2, 3]),          # EV charging
    ("INV-2025-003", "2025-02-20", [4, 5]),          # recycled materials
    ("INV-2025-004", "2025-03-05", [6, 7]),          # fossil fuels
    ("INV-2025-005", "2025-03-18", [8, 9]),          # coal furnace
    ("INV-2025-006", "2025-04-02", [10, 11]),        # CNC maintenance
    ("INV-2025-007", "2025-04-14", [12, 13]),        # office supplies
    ("INV-2025-008", "2025-05-07", [14, 15]),        # logistics
    ("INV-2025-009", "2025-05-22", [16, 17]),        # water treatment
    ("INV-2025-010", "2025-06-10", [18, 19]),        # insulation + VFD
    ("INV-2025-011", "2025-06-25", [20, 21]),        # consumables + PPE
    ("INV-2025-012", "2025-07-08", [22, 23]),        # gas + rainwater
]

COLUMNS = ["invoice_id", "sme_id", "date", "supplier", "description", "quantity", "unit", "amount"]


def generate() -> None:
    rng = random.Random(RANDOM_SEED)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for invoice_id, date, item_indices in INVOICE_GROUPS:
        for idx in item_indices:
            supplier_pool, description, quantity, unit, amount = INVOICE_LINE_ITEMS[idx]
            rows.append({
                "invoice_id": invoice_id,
                "sme_id": SME_ID,
                "date": date,
                "supplier": rng.choice(supplier_pool),
                "description": description,
                "quantity": quantity,
                "unit": unit,
                "amount": amount,
            })

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    n_invoices = len(INVOICE_GROUPS)
    n_items = len(rows)
    print(f"Written {n_invoices} invoices ({n_items} line items) → {OUTPUT_PATH}")


if __name__ == "__main__":
    generate()
