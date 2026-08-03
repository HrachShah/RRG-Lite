import pytest

from src.RRG import RRG


def config(**overrides):
    values = {"DATA_PATH": ".", "BENCHMARK": "index"}
    values.update(overrides)
    return values


@pytest.mark.parametrize("name", ["WINDOW", "PERIOD"])
@pytest.mark.parametrize("value", [True, False, 2.5, "14"])
def test_calculation_sizes_must_be_integers(name, value):
    with pytest.raises(TypeError, match=f"{name} must be an integer"):
        RRG(config(**{name: value}), watchlist=[])
