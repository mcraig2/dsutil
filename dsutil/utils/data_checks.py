from datetime import datetime
import itertools as it
from typing import (
    Any,
    Dict,
    List,
    Optional,
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
        cols = cols or data.columns
        groups = {col: data[col].unique() for col in cols}
        DataChecker.assert_all_groups_exist(data=data, groups=groups)

    @staticmethod
    def assert_all_times_exist(
            data: pd.DataFrame,
            time_cols: List[str],
            freq: str,
    ) -> None:
        assertion_msg = list()
        for col in time_cols:
            missing = (
                data[time_cols]
                .set_index(col)
                .resample(freq)
                .size()
            ) == 0
            if missing.sum() > 0:
                missing_str = ', '.join(
                    datetime.strftime(miss, '%Y-%m-%d %H:%M:%S')
                    for miss in missing.index[missing]
                )
                assertion_msg.append(
                    'Times missing for {col}:\n{missing}'.format(
                        col=col,
                        missing=missing_str,
                    )
                )
        if len(assertion_msg) > 0:
            raise AssertionError('\n'.join(assertion_msg))

    @staticmethod
    def assert_no_missing(
            data: pd.DataFrame,
            cols: Optional[List[str]] = None,
    ) -> None:
        assertion_msg = list()
        for col in cols or data.columns:
            pos_inf = data[col] == np.inf
            neg_inf = data[col] == -np.inf
            missing = pd.isnull(data[col])
            total_missing = (
                pos_inf.sum() +
                neg_inf.sum() +
                missing.sum()
            )
            if total_missing > 0:
                assertion_msg.append(
                    '{col} has missing values:\n'
                    '\t# +Inf: {pos_inf}\n'
                    '\t# -Inf: {neg_inf}\n'
                    '\t# Missing: {missing}'.format(
                        col=col,
                        pos_inf=pos_inf,
                        neg_inf=neg_inf,
                        missing=missing,
                    )
                )
        if len(assertion_msg) > 0:
            raise AssertionError('\n'.join(assertion_msg))

    @staticmethod
    def assert_percent_values_at_mode(
            data: pd.DataFrame,
            threshold: float,
            cols: Optional[List[str]] = None,
    ) -> None:
        assertion_msg = list()
        for col in cols or data.columns:
            mode = data[col].mode()[0]
            pct_mode = (
                (data[col] == mode).sum() /
                data.shape[0]
            )
            if pct_mode > threshold:
                assertion_msg.append(
                    '{col} has {pct:.2f}% of values at {mode}'.format(
                        col=col,
                        pct=pct_mode * 100.,
                        mode=mode,
                    )
                )
        if len(assertion_msg) > 0:
            raise AssertionError('\n'.join(assertion_msg))
