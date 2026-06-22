from __future__ import annotations

import anthropic

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def build_rationale(
    line_item_description: str,
    taxonomy_category: str,
    category_definition: str,
    qualifying_activities: str = "",
) -> str:
    """Return a one-sentence rationale grounding the classification in EU Taxonomy text.

    Both the category definition and qualifying activities are passed as context so
    the rationale is derived from regulation rather than the model's parametric memory.
    Uses ANTHROPIC_API_KEY from the environment.
    """
    qualifying_section = (
        f"\nQualifying activities:\n{qualifying_activities}\n" if qualifying_activities else ""
    )

    prompt = (
        f"EU Taxonomy category: {taxonomy_category}\n\n"
        f"Category definition:\n{category_definition}\n"
        f"{qualifying_section}\n"
        f"Invoice line item: \"{line_item_description}\"\n\n"
        "In one sentence, explain why this line item qualifies under the EU Taxonomy "
        "category above, citing specific language from the definition or qualifying activities."
    )

    message = _get_client().messages.create(
        model="claude-opus-4-8",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text.strip()
