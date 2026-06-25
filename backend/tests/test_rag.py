from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from backend.app.services.classification.rag import build_rationale


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_completion(text: str):
    """Build a minimal object that looks like a Groq chat completion."""
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=text))]
    )


# ---------------------------------------------------------------------------
# Stub fallback (no API key)
# ---------------------------------------------------------------------------

def test_stub_fires_when_no_api_key(monkeypatch):
    """build_rationale must return a non-empty stub without calling Groq."""
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with patch("backend.app.services.classification.rag._get_client") as mock_client:
        result = build_rationale(
            line_item_description="solar panel installation 10kW",
            taxonomy_category="Solar Energy Generation",
            category_definition="Generation of electricity from solar photovoltaic.",
        )
    mock_client.assert_not_called()
    assert "solar panel installation 10kW" in result
    assert "Solar Energy Generation" in result


def test_stub_returns_string(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    result = build_rationale("any description", "any category", "any definition")
    assert isinstance(result, str)
    assert len(result) > 0


# ---------------------------------------------------------------------------
# Prompt construction: the core RAG contract
# ---------------------------------------------------------------------------

def test_prompt_contains_category_definition(monkeypatch):
    """The retrieved category definition must be injected into the prompt (the RAG part)."""
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _make_completion("Rationale text.")

    with patch("backend.app.services.classification.rag._get_client", return_value=mock_client):
        build_rationale(
            line_item_description="solar panel installation",
            taxonomy_category="Solar Energy Generation",
            category_definition="Electricity generation from solar photovoltaic systems.",
        )

    call_kwargs = mock_client.chat.completions.create.call_args[1]
    prompt = call_kwargs["messages"][0]["content"]
    assert "Electricity generation from solar photovoltaic systems." in prompt


def test_prompt_contains_qualifying_activities(monkeypatch):
    """Qualifying activities text must also appear in the prompt when provided."""
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _make_completion("Rationale.")

    with patch("backend.app.services.classification.rag._get_client", return_value=mock_client):
        build_rationale(
            line_item_description="solar panel installation",
            taxonomy_category="Solar Energy Generation",
            category_definition="Definition text.",
            qualifying_activities="Installation of rooftop PV systems.",
        )

    prompt = mock_client.chat.completions.create.call_args[1]["messages"][0]["content"]
    assert "Installation of rooftop PV systems." in prompt


def test_prompt_contains_line_item_description(monkeypatch):
    """The actual invoice line item must appear in the prompt so the model reasons about it."""
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _make_completion("Rationale.")

    with patch("backend.app.services.classification.rag._get_client", return_value=mock_client):
        build_rationale(
            line_item_description="diesel fuel 500L",
            taxonomy_category="Some Category",
            category_definition="Some definition.",
        )

    prompt = mock_client.chat.completions.create.call_args[1]["messages"][0]["content"]
    assert "diesel fuel 500L" in prompt


def test_prompt_omits_qualifying_section_when_empty(monkeypatch):
    """When qualifying_activities is empty the prompt must not contain a spurious empty section."""
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _make_completion("Rationale.")

    with patch("backend.app.services.classification.rag._get_client", return_value=mock_client):
        build_rationale(
            line_item_description="item",
            taxonomy_category="Category",
            category_definition="Definition.",
            qualifying_activities="",
        )

    prompt = mock_client.chat.completions.create.call_args[1]["messages"][0]["content"]
    assert "Qualifying activities:" not in prompt


# ---------------------------------------------------------------------------
# Return value
# ---------------------------------------------------------------------------

def test_returns_llm_response_stripped(monkeypatch):
    """build_rationale must return the LLM text, stripped of surrounding whitespace."""
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _make_completion(
        "  This item qualifies under EU Taxonomy.  \n"
    )

    with patch("backend.app.services.classification.rag._get_client", return_value=mock_client):
        result = build_rationale("item", "Category", "Definition.")

    assert result == "This item qualifies under EU Taxonomy."


def test_uses_correct_model(monkeypatch):
    """Must call llama-3.3-70b-versatile, not a cheaper/different model."""
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _make_completion("Rationale.")

    with patch("backend.app.services.classification.rag._get_client", return_value=mock_client):
        build_rationale("item", "Category", "Definition.")

    call_kwargs = mock_client.chat.completions.create.call_args[1]
    assert call_kwargs["model"] == "llama-3.3-70b-versatile"
