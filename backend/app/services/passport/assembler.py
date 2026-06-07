from __future__ import annotations

import uuid

from backend.app.models.schemas import ESGProfile, Passport

# In-memory passport store: passport_id → Passport
_passport_store: dict[str, Passport] = {}


def assemble_passport(esg_profile: ESGProfile) -> Passport:
    # TODO: derive basic financial summary from ESGProfile data,
    #       create Passport with a new UUID, store in _passport_store
    pass


def get_passport(passport_id: str) -> Passport | None:
    return _passport_store.get(passport_id)
