from __future__ import annotations

import anthropic


def build_rationale(
    line_item_description: str,
    taxonomy_category: str,
    category_definition: str,
) -> str:
    """Return a one-sentence rationale grounding the classification in EU Taxonomy text.

    The category definition is passed as context so the rationale is derived from
    regulation rather than the model's parametric memory.
    Uses ANTHROPIC_API_KEY from the environment.
    """
    client = anthropic.Anthropic()

    prompt = (
        f"EU Taxonomy category: {taxonomy_category}\n\n"
        f"Category definition:\n{category_definition}\n\n"
        f"Invoice line item: \"{line_item_description}\"\n\n"
        "In one sentence, explain why this line item qualifies under the EU Taxonomy "
        "category above, citing specific language from the definition."
    )

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text.strip()
