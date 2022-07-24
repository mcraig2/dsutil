from abc import ABC, abstractmethod
from typing import List


class PipelineWriter(ABC):
    def __init__(self, filenames: List[str]):
        self.filenames = filenames

    @abstractmethod
    def write(self) -> None:
        pass  # pragma: no cover
