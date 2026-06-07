from __future__ import annotations

import os

import anthropic


def build_rationale(
    line_item_description: str,
    taxonomy_category: str,
    category_definition: str,
) -> str:
    # TODO: call Anthropic API with the category definition as context,
    #       ask for a one-sentence rationale grounded in the EU Taxonomy text.
    #       Uses ANTHROPIC_API_KEY from environment.
    pass
