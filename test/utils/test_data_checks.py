import unittest

import pandas as pd

from dsutil import utils as du


class DataChecksTest(unittest.TestCase):
    def test_is_same_shape(self) -> None:
        one = pd.DataFrame({'a': [1], 'b': [2]})
        two = pd.DataFrame({'b': [1, 2], 'c': [3, 4]})
        self.assertTrue(du.is_same_shape(one, one))
        self.assertFalse(du.is_same_shape(one, two))

    def test_has_same_columns(self) -> None:
        self.assertTrue(du.has_same_columns(
            left=pd.DataFrame({'a': [1], 'b': [2]}),
            right=pd.DataFrame({'a': [-1, -2], 'b': [-2, -3]}),
        ))
        self.assertFalse(du.has_same_columns(
            left=pd.DataFrame({'a': [1], 'b': [2]}),
            right=pd.DataFrame({'a': [1], 'c': [2]}),
        ))
