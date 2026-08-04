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


def test_load_config_rejects_malformed_json(tmp_path, monkeypatch):
    config_path = tmp_path / "broken.json"
    config_path.write_text("{invalid", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["init.py", "--config", str(config_path)])

    from src import utils

    with pytest.raises(SystemExit, match="Failed to read config file"):
        utils.load_config()


def test_load_config_rejects_non_object_json(tmp_path, monkeypatch):
    config_path = tmp_path / "array.json"
    config_path.write_text("[]", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["init.py", "--config", str(config_path)])

    from src import utils

    with pytest.raises(SystemExit, match="must contain a JSON object"):
        utils.load_config()
