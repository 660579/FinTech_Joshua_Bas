from __future__ import annotations

import groq

_client: groq.Groq | None = None


def _get_client() -> groq.Groq:
    global _client
    if _client is None:
        _client = groq.Groq()
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
    Uses GROQ_API_KEY from the environment. Returns a stub when key is absent.
    """
    import os
    if not os.environ.get("GROQ_API_KEY"):
        return f'"{line_item_description}" aligns with {taxonomy_category} per EU Taxonomy criteria.'

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

    completion = _get_client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}],
    )

    return completion.choices[0].message.content.strip()
