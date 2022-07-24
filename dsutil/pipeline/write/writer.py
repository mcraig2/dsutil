from abc import ABC, abstractmethod
from typing import List


class PipelineWriter(ABC):
    @abstractmethod
    def write(self, datasets: List[object], filenames: List[str]) -> None:
        pass  # pragma: no cover
