import unittest

import pandas as pd

from dsutil.pipeline import PassthroughReader


class PassthroughReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = [
            pd.DataFrame({'one': [1, 2, 3], 'two': [2, 3, 4]}),
            pd.DataFrame({'a': [-1, -2], 'b': [-3, -4]}),
        ]
        self.reader = PassthroughReader(data=self.data)

    def test_read(self) -> None:
        actual = self.reader.read()
        expected = self.data
        for actual_frame, expected_frame in zip(actual, expected):
            pd.testing.assert_frame_equal(expected_frame, actual_frame)
