from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

import pandas as pd


@dataclass
class ProcessedData:
    exog: pd.DataFrame
    endog: Optional[pd.DataFrame] = None


class PipelineProcessor(ABC):
    @staticmethod
    def _separate_exog_endog(
            data: pd.DataFrame,
            target_cols: List[str],
    ) -> ProcessedData:
        return ProcessedData(
            exog=data.drop(target_cols, axis=1),
            endog=data[target_cols],
        )

    @abstractmethod
    def process(self, data: List[pd.DataFrame]) -> List[ProcessedData]:
        pass  # pragma: no cover
