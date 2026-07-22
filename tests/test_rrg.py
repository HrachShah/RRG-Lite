import unittest

import pandas as pd

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


if __name__ == "__main__":
    unittest.main()
