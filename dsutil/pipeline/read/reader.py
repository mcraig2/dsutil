from abc import ABC, abstractmethod
from typing import List

import pandas as pd


class PipelineReader(ABC):
    @abstractmethod
    def read(self) -> List[pd.DataFrame]:
        pass  # pragma: no cover
