from abc import ABC, abstractmethod
from typing import List

import pandas as pd


class PipelineFitter(ABC):
    @abstractmethod
    def get_fitted(self) -> List[object]:
        pass  # pragma: no cover

    @abstractmethod
    def fit(self, exog: List[pd.DataFrame], endog: List[pd.DataFrame]) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def predict(self, exog: List[pd.DataFrame]) -> List[pd.DataFrame]:
        pass  # pragma: no cover
