from abc import ABC, abstractmethod
from typing import List

import pandas as pd


class PipelineProcessor(ABC):
    @abstractmethod
    def process(self, data: List[pd.DataFrame]) -> List[pd.DataFrame]:
        pass  # pragma: no cover
