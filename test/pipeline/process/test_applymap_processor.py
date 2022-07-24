import unittest

import pandas as pd

from dsutil.pipeline import ApplyMapProcessor


class PassthroughReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pd.DataFrame({
            'one': [1., 2., 3.],
            'two': [2., 4., 6.],
        })
        self.processor = ApplyMapProcessor(
            applymap_fn=lambda x: x * 2.,
        )

    def test_process(self) -> None:
        actual = self.processor.process([self.data])[0]
        expected = pd.DataFrame({
            'one': [2., 4., 6.],
            'two': [4., 8., 12.],
        })
        pd.testing.assert_frame_equal(expected, actual)
