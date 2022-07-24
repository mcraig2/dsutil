import unittest

import pandas as pd

from dsutil.pipeline import ApplyMapProcessor


class PassthroughReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pd.DataFrame({
            'one': [1., 2., 3.],
            'two': [2., 4., 6.],
            'target': [-1., -2., -3.],
        })
        self.processor = ApplyMapProcessor(
            applymap_fn=lambda x: x * 2.,
            target_cols=['target'],
        )

    def test_process(self) -> None:
        result = self.processor.process([self.data])[0]
        actual_exog = result.exog
        expected_exog = pd.DataFrame({
            'one': [2., 4., 6.],
            'two': [4., 8., 12.],
        })
        pd.testing.assert_frame_equal(expected_exog, actual_exog)
        actual_endog = result.endog
        expected_endog = pd.DataFrame({
            'target': [-2., -4., -6.],
        })
        pd.testing.assert_frame_equal(expected_endog, actual_endog)
