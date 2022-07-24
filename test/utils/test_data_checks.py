from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)
import unittest

import numpy as np
import pandas as pd

from dsutil.utils import DataChecker as dc


@dataclass
class CompleteGroupTestData:
    complete_df: pd.DataFrame
    missing_df: pd.DataFrame
    complete_groups: Dict[str, List[Any]]
    missing_groups: List[Dict[str, Any]]


class DataChecksTest(unittest.TestCase):
    def test_same_shape_check(self) -> None:
        one = pd.DataFrame({'a': [1], 'b': [2]})
        two = pd.DataFrame({'b': [1, 2], 'c': [3, 4]})
        self.assertIsNone(dc.assert_same_shape(one, one))
        with self.assertRaises(AssertionError):
            dc.assert_same_shape(one, two)

    def test_has_same_column_names(self) -> None:
        self.assertIsNone(dc.assert_same_columns(
            left=pd.DataFrame({'a': [1], 'b': [2]}),
            right=pd.DataFrame({'a': [-1, -2], 'b': [-2, -3]})
        ))
        with self.assertRaises(AssertionError):
            dc.assert_same_columns(
                left=pd.DataFrame({'a': [1], 'b': [2]}),
                right=pd.DataFrame({'a': [1], 'c': [2]}),
            )

    def test_has_same_column_types(self) -> None:
        self.assertIsNone(dc.assert_same_columns(
            left=pd.DataFrame({'a': [1], 'b': [2]}),
            right=pd.DataFrame({'a': [0, 1], 'b': [1, 2]}),
        ))
        with self.assertRaises(AssertionError):
            dc.assert_same_columns(
                left=pd.DataFrame({'a': [1], 'b': [2]}),
                right=pd.DataFrame({'a': ['1'], 'b': [2]}),
            )

    def _complete_groups_test_data(self) -> CompleteGroupTestData:
        complete_df = pd.DataFrame({
            'group1': ['a', 'a', 'b', 'b', 'c', 'c'],
            'group2': ['1', '2', '1', '2', '1', '2'],
        })
        complete_groups = {
            'group1': ['a', 'b', 'c'],
            'group2': ['1', '2'],
        }
        missing_df = pd.DataFrame({
            'group1': ['a', 'a', 'b', 'c', 'c'],
            'group2': ['1', '2', '1', '1', '2'],
        })
        missing_groups = [{'group1': 'b', 'group2': '2'}]
        return CompleteGroupTestData(
            complete_df=complete_df,
            complete_groups=complete_groups,
            missing_df=missing_df,
            missing_groups=missing_groups,
        )

    def test_groups_dict_to_list(self) -> None:
        def _group_cmp(item: Dict[str, Any]) -> str:
            return '{grp1}_{grp2}'.format(
                grp1=item['group1'],
                grp2=item['group2'],
            )

        groups_test = self._complete_groups_test_data().complete_groups
        expected = [
            {'group1': 'a', 'group2': '1'},
            {'group1': 'a', 'group2': '2'},
            {'group1': 'b', 'group2': '1'},
            {'group1': 'b', 'group2': '2'},
            {'group1': 'c', 'group2': '1'},
            {'group1': 'c', 'group2': '2'},
        ]
        actual = dc._group_dict_to_list(groups=groups_test)
        self.assertEqual(
            sorted(expected, key=_group_cmp),
            sorted(actual, key=_group_cmp),
        )

    def test_all_groups_exist(self) -> None:
        group_test_data = self._complete_groups_test_data()
        self.assertIsNone(dc.assert_all_groups_exist(
            data=group_test_data.complete_df,
            groups=group_test_data.complete_groups,
        ))
        with self.assertRaises(AssertionError):
            dc.assert_all_groups_exist(
                data=group_test_data.missing_df,
                groups=group_test_data.complete_groups,
            )

    def test_all_combinations_exist(self) -> None:
        group_test_data = self._complete_groups_test_data()
        self.assertIsNone(dc.assert_all_combinations_exist(
            data=group_test_data.complete_df,
            cols=['group1', 'group2'],
        ))
        self.assertIsNone(dc.assert_all_combinations_exist(
            data=group_test_data.complete_df,
            cols=None,
        ))
        with self.assertRaises(AssertionError):
            dc.assert_all_combinations_exist(
                data=group_test_data.missing_df,
                cols=['group1', 'group2'],
            )
            dc.assert_all_combinations_exist(
                data=group_test_data.missing_df,
                cols=None,
            )

    def test_all_times_exist(self) -> None:
        all_times_df = pd.DataFrame({
            'date': pd.to_datetime([
                '2022-01-01', '2022-01-03', '2022-01-05',
                '2022-01-07', '2022-01-09', '2022-01-11',
            ]),
            'val': [1, 2, 3, 4, 5, 6],
        })
        missing_times_df = pd.DataFrame({
            'date': pd.to_datetime([
                '2022-01-01', '2022-01-03', '2022-01-05',
                '2022-01-06', '2022-01-09', '2022-01-11',
            ]),
            'val': [1, 2, 3, 4, 5, 6],
        })
        self.assertIsNone(dc.assert_all_times_exist(
            data=all_times_df,
            time_cols=['date'],
            freq='2d',
        ))
        with self.assertRaises(AssertionError):
            dc.assert_all_times_exist(
                data=missing_times_df,
                time_cols=['date'],
                freq='2d',
            )

    def test_no_missing(self) -> None:
        missing_df = pd.DataFrame({
            'one': [1, 2, None, 4, np.inf, 6, -np.inf, 8, np.nan],
            'two': [2, 3, 4, 5, 6, 7, 8, 9, 10],
            'three': [-np.inf, np.inf, 7, 8, 9, 10, 11, 12, 13],
        })
        no_missing_df = pd.DataFrame({
            'one': [1, 2, 3, 4],
            'two': [2, 3, 4, 5],
            'three': [5, 6, 7, 8],
        })
        self.assertIsNone(dc.assert_no_missing(no_missing_df))
        self.assertIsNone(dc.assert_no_missing(
            data=no_missing_df,
            cols=['one', 'two', 'three'],
        ))
        self.assertIsNone(dc.assert_no_missing(
            data=missing_df,
            cols=['two'],
        ))
        with self.assertRaises(AssertionError):
            dc.assert_no_missing(missing_df)

    @unittest.skip
    def test_percent_values_at_mode(self) -> None:
        pass
