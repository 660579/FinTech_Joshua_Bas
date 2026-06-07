import pytest

from backend.app.services.scoring.scorer import (
    score_dimensions,
    compute_green_credit_score,
    build_esg_profile,
)


def test_green_credit_score_range() -> None:
    # TODO: assert score is in [0, 100] for a synthetic classified item list
    pass


def test_dimension_scores_keys_match_objectives() -> None:
    # TODO: assert dimension_scores keys match the six EU Taxonomy objectives
    pass
