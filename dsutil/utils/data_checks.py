import pandas as pd


def is_same_shape(left: pd.DataFrame, right: pd.DataFrame) -> bool:
    return left.shape == right.shape


def has_same_columns(left: pd.DataFrame, right: pd.DataFrame) -> bool:
    return set(left.columns) == set(right.columns)
