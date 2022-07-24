from abc import ABC, abstractmethod
from typing import List


class PipelineFitter(ABC):
    def __init__(self, models: List[object]):
        self.models = models

    @abstractmethod
    def fit(self) -> None:
        pass  # pragma: no cover
