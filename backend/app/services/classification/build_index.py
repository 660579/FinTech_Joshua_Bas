"""Run once to precompute EU Taxonomy category embeddings.

Usage:
    python -m backend.app.services.classification.build_index
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np

from backend.app.services.classification.embedder import embed_texts


TAXONOMY_DIR = Path("backend/data/taxonomy")
VECTORSTORE_DIR = Path("backend/data/vectorstore")


def _parse_taxonomy_file(path: Path) -> dict:
    """Parse a taxonomy .txt file into a structured dict."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    meta: dict[str, str] = {}
    sections: dict[str, list[str]] = {}
    current_section: str | None = None

    section_headers = {
        "Definition:",
        "Qualifying activities include:",
        "Example invoice descriptions:",
        "Do substantial harm considerations:",
    }

    for line in lines:
        stripped = line.strip()

        # Top-level key: value header lines
        if re.match(r"^(Category|EU Taxonomy Objective|NACE Code Reference):\s+", stripped):
            key, _, value = stripped.partition(": ")
            meta[key] = value.strip()
            current_section = None
            continue

        # Section header lines (e.g. "Definition:")
        if stripped in section_headers:
            current_section = stripped.rstrip(":")
            sections[current_section] = []
            continue

        # Content lines for current section
        if current_section is not None:
            sections[current_section].append(line)

    def join_section(name: str) -> str:
        return "\n".join(sections.get(name, [])).strip()

    definition = join_section("Definition")
    qualifying = join_section("Qualifying activities include")
    examples = join_section("Example invoice descriptions")

    # The text we embed combines all three rich sections so similarity search
    # captures regulatory wording, activity descriptions, and concrete invoice phrases.
    embed_text = "\n\n".join(part for part in [definition, qualifying, examples] if part)

    return {
        "name": meta.get("Category", path.stem),
        "objective": meta.get("EU Taxonomy Objective", ""),
        "nace_code": meta.get("NACE Code Reference", ""),
        "definition": definition,
        "qualifying": qualifying,
        "embed_text": embed_text,
    }


def build_index(
    taxonomy_dir: Path = TAXONOMY_DIR,
    vectorstore_dir: Path = VECTORSTORE_DIR,
) -> None:
    taxonomy_dir = Path(taxonomy_dir)
    vectorstore_dir = Path(vectorstore_dir)

    txt_files = sorted(taxonomy_dir.glob("*.txt"))
    if not txt_files:
        raise FileNotFoundError(f"No .txt files found in {taxonomy_dir}")

    categories = [_parse_taxonomy_file(f) for f in txt_files]

    embed_texts_input = [c["embed_text"] for c in categories]
    index = embed_texts(embed_texts_input)  # (N, D) float32, already normalised

    vectorstore_dir.mkdir(parents=True, exist_ok=True)

    np.save(vectorstore_dir / "taxonomy_index.npy", index)

    # Store only the fields needed at runtime (drop embed_text to keep JSON small)
    runtime_categories = [
        {k: v for k, v in c.items() if k not in {"embed_text"}}
        for c in categories
    ]
    (vectorstore_dir / "categories.json").write_text(
        json.dumps(runtime_categories, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Built index: {len(categories)} categories → {vectorstore_dir}")


if __name__ == "__main__":
    build_index()
