"""In-memory stores shared across route handlers.

These are module-level dicts that act as the runtime database for the demo.
A real deployment would replace these with a persistent store (e.g. SQLite or Redis).
"""
from backend.app.models.schemas import LenderDecision, Passport

passport_store: dict[str, Passport] = {}
decision_store: dict[str, LenderDecision] = {}
