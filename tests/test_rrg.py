import tempfile
import unittest
from pathlib import Path

import pandas as pd

from loaders.EODFileLoader import EODFileLoader
from RRG import RRG


class TestMomentumBaseDate(unittest.TestCase):
    def test_missing_base_date_reports_configuration_error(self):
        rrg = RRG.__new__(RRG)
        rrg.base_date = "2026-01-01"
        rrg.period = 2
        rrg.window = 2
        ratios = pd.Series(
            [100.0, 101.0],
            index=pd.to_datetime(["2026-01-02", "2026-01-03"]),
        )

        with self.assertRaisesRegex(ValueError, "BASE_DATE not found"):
            rrg._calculate_momentum(ratios)


class TestLoaderConfiguration(unittest.TestCase):
    def test_non_positive_period_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaisesRegex(ValueError, "period must be greater than zero"):
                EODFileLoader({"DATA_PATH": tmpdir}, period=0)


class TestMonthlyLoaderErrors(unittest.TestCase):
    def test_malformed_monthly_csv_returns_no_data(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            symbol_csv = tmpdir / "symbol.csv"
            symbol_csv.write_text("a,b\n1,2\n")
            loader = EODFileLoader({"DATA_PATH": str(tmpdir)}, tf="monthly")
            self.assertIsNone(loader.get("symbol"))


if __name__ == "__main__":
    unittest.main()
