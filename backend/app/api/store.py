from backend.app.models.schemas import LenderDecision, Passport

passport_store: dict[str, Passport] = {}
decision_store: dict[str, LenderDecision] = {}
