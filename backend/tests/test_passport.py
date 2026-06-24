from __future__ import annotations

import json
from pathlib import Path

import pytest

from backend.app.models.schemas import ClassifiedLineItem, ESGProfile, SectorBenchmark
from backend.app.services.passport.assembler import assemble_passport, get_passport
from backend.app.services.report.vsme_export import export_vsme


def _make_esg_profile(
    sme_id: str = "sme-test",
    green_credit_score: float = 60.0,
    pss: float = 45.0,
) -> ESGProfile:
    items = [
        ClassifiedLineItem(
            supplier="Acme Solar",
            description="solar panel installation",
            quantity=1.0,
            amount=500.0,
            taxonomy_category="Solar energy generation",
            taxonomy_objective="Climate Change Mitigation",
            similarity_score=0.90,
        ),
        ClassifiedLineItem(
            supplier="Green Freight",
            description="electric vehicle fleet lease",
            quantity=2.0,
            amount=300.0,
            taxonomy_category="Transport",
            taxonomy_objective="Climate Change Mitigation",
            similarity_score=0.80,
        ),
    ]
    return ESGProfile(
        sme_id=sme_id,
        procurement_sustainability_score=pss,
        green_credit_score=green_credit_score,
        dimension_scores={"Climate Change Mitigation": 0.45},
        classified_line_items=items,
        sector_benchmark=SectorBenchmark(sector="C25", median_green_credit_score=15.0),
    )


def test_assemble_passport_returns_passport_with_correct_ids() -> None:
    profile = _make_esg_profile()
    passport = assemble_passport(profile, sme_id="sme-test")
    assert passport.sme_id == "sme-test"
    assert passport.passport_id  # non-empty UUID
    assert passport.esg_profile is profile


def test_assemble_passport_stores_and_retrieves() -> None:
    profile = _make_esg_profile(sme_id="sme-retrieve")
    passport = assemble_passport(profile, sme_id="sme-retrieve")
    retrieved = get_passport(passport.passport_id)
    assert retrieved is not None
    assert retrieved.passport_id == passport.passport_id


def test_get_passport_returns_none_for_unknown_id() -> None:
    assert get_passport("does-not-exist") is None


def test_assemble_passport_financial_health_keys() -> None:
    profile = _make_esg_profile()
    passport = assemble_passport(profile, sme_id="sme-fh")
    fh = passport.financial_health
    assert "total_spend_eur" in fh
    assert "classified_green_spend_eur" in fh
    assert "green_spend_share" in fh
    assert fh["classified_green_spend_eur"] == pytest.approx(800.0)


def test_export_vsme_returns_required_keys(tmp_path: Path, monkeypatch) -> None:
    from backend.app.services.report import vsme_export
    monkeypatch.setattr(vsme_export, "REPORTS_DIR", tmp_path)

    profile = _make_esg_profile()
    passport = assemble_passport(profile, sme_id="sme-export")
    report = export_vsme(passport)

    for key in ("sme_id", "passport_id", "generated_at", "green_credit_score", "esg_profile", "vsme_indicators"):
        assert key in report, f"missing key: {key}"


def test_export_vsme_indicators_structure(tmp_path: Path, monkeypatch) -> None:
    from backend.app.services.report import vsme_export
    monkeypatch.setattr(vsme_export, "REPORTS_DIR", tmp_path)

    profile = _make_esg_profile()
    passport = assemble_passport(profile, sme_id="sme-indicators")
    report = export_vsme(passport)

    ind = report["vsme_indicators"]
    for key in ("coverage_ratio", "alignment_score", "classified_spend", "total_spend"):
        assert key in ind, f"missing vsme_indicator: {key}"
    assert ind["classified_spend"] == pytest.approx(800.0)
    assert 0.0 <= ind["coverage_ratio"] <= 1.0


def test_export_vsme_writes_json_file(tmp_path: Path, monkeypatch) -> None:
    from backend.app.services.report import vsme_export
    monkeypatch.setattr(vsme_export, "REPORTS_DIR", tmp_path)

    profile = _make_esg_profile()
    passport = assemble_passport(profile, sme_id="sme-file")
    report = export_vsme(passport)

    expected_file = tmp_path / f"{passport.passport_id}.json"
    assert expected_file.exists()
    saved = json.loads(expected_file.read_text())
    assert saved["passport_id"] == passport.passport_id
