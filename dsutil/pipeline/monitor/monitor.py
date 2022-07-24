from abc import ABC, abstractmethod


class PipelineMonitor(ABC):
    def __init__(self):
        self.report_artifacts = None

    @abstractmethod
    def monitor(self) -> None:
        pass  # pragma: no cover
