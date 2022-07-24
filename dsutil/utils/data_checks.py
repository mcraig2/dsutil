from collections import namedtuple
import itertools as it
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

import numpy as np
import pandas as pd


class DataChecker:
    @staticmethod
    def assert_same_shape(left: pd.DataFrame, right: pd.DataFrame) -> None:
        is_same = left.shape == right.shape
        if not is_same:
            raise AssertionError(
                'left shape: {l}, right shape: {r}'.format(
                    l=left.shape,
                    r=right.shape,
                )
            )

    @staticmethod
    def _assert_same_column_names(left: set, right: set) -> None:
        if left == right:
            return
        msg = list()
        for col in left.union(right):
            if not (col in left) and (col in right):
                msg.append(
                    '"{col}" in {present} not in {missing}'.format(
                        col=col,
                        present='left' if col in left else 'right',
                        missing='left' if col not in left else 'right',
                    )
                )
        raise AssertionError('\n'.join(msg))

    @staticmethod
    def assert_same_columns(
            left: pd.DataFrame,
            right: pd.DataFrame,
            check_dtypes: Optional[bool] = True,
    ) -> None:
        DataChecker._assert_same_column_names(
            left=set(left.columns),
            right=set(right.columns),
        )
        if check_dtypes:
            type_compare = pd.DataFrame({
                'left': left.dtypes.sort_index(),
                'right': right.dtypes.sort_index(),
            })
            type_diffs = type_compare[
                type_compare['left'] != type_compare['right']
            ]
            if type_diffs.shape[0] > 0:
                raise AssertionError(
                    'Columns have different types:\n{diffs}'.format(
                        diffs=type_diffs,
                    )
                )

    @staticmethod
    def _group_dict_to_list(
            groups: Dict[str, List[Any]],
    ) -> List[Dict[str, Any]]:
        for item in it.product(*groups.values()):
            yield dict(zip(groups.keys(), item))

    @staticmethod
    def assert_all_groups_exist(
            data: pd.DataFrame,
            groups: Dict[str, List[Any]],
    ) -> None:
        missing_groups = list()
        for group in DataChecker._group_dict_to_list(groups=groups):
            matching_rows = np.logical_and.reduce([
                data[col] == val for col, val in group.items()
            ])
            if matching_rows.sum() == 0:
                missing_groups.append(group)
        if len(missing_groups) > 0:
            raise AssertionError(
                'There are missing groups:\n{missing}'.format(
                    missing=missing_groups,
                )
            )

    @staticmethod
    def assert_all_combinations_exist(
            data: pd.DataFrame,
            cols: Optional[List[str]] = None,
    ) -> None:
        pass

    @staticmethod
    def assert_all_times_exist(
            data: pd.DataFrame,
            time_cols: List[str],
            freq: str,
    ) -> None:
        pass

    @staticmethod
    def assert_no_missing(
            data: pd.DataFrame,
            cols: Optional[List[str]] = None,
    ) -> None:
        pass

    @staticmethod
    def assert_percent_values_at_mode(
            data: pd.DataFrame,
            threshold: float,
            cols: Optional[List[str]] = None,
    ) -> None:
        pass
