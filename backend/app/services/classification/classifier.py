from __future__ import annotations

from backend.app.models.schemas import LineItem, ClassifiedLineItem


def classify_line_items(line_items: list[LineItem]) -> list[ClassifiedLineItem]:
    # TODO: orchestrate embed → match → RAG for each line item
    pass
