import pytest
from gradebook_lite.core import validates_scores, mean, min_max, letter_grade


@pytest.fixture
def sample_scores():
    return [78.0, 90.0, 66.0, 82.0]


def test_validate_scores_ok(sample_scores):
    assert validates_scores(sample_scores) == sample_scores


def test_validate_scores_rejects_out_of_range():
    with pytest.raises(ValueError):
        validates_scores([101, 50])


def test_stats(sample_scores):
    assert mean(sample_scores) == pytest.approx(79.0)
    assert min_max(sample_scores) == (66.0, 90.0)


def test_letter_grade_boundaries():
    assert letter_grade(86) == "HD"
    assert letter_grade(75) == "D"
    assert letter_grade(65) == "C"
    assert letter_grade(50) == "P"
    assert letter_grade(49.9) == "F"
