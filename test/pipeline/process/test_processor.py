import unittest

import pandas as pd

from dsutil.pipeline.process import PipelineProcessor


class PipelineProcessorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.processor = PipelineProcessor

    def test_separate_exog_endog(self) -> None:
        data = pd.DataFrame({
            'one': [1, 2, 3],
            'two': [2, 3, 4],
            'target': [10, 11, 12],
        })
        actual = self.processor._separate_exog_endog(
            data=data,
            target_cols=['target'],
        )
        expected_exog = data[['one', 'two']]
        expected_endog = data[['target']]
        pd.testing.assert_frame_equal(expected_exog, actual.exog)
        pd.testing.assert_frame_equal(expected_endog, actual.endog)
