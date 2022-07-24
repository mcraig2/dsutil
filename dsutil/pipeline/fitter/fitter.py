from abc import ABC, abstractmethod


class PipelineFitter(ABC):
    def __init__(self):
        self.models = None

    @abstractmethod
    def fit(self) -> None:
        pass  # pragma: no cover
