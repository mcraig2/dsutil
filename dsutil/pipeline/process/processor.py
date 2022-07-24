from abc import ABC, abstractmethod
from typing import List

import pandas as pd


class PipelineProcessor(ABC):
    @abstractmethod
    def process(self) -> List[pd.DataFrame]:
        pass  # pragma: no cover
