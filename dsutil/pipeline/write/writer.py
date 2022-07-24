from abc import ABC, abstractmethod
from typing import List

from dsutil.pipeline.monitor import ReportArtifact


class PipelineWriter(ABC):
    @abstractmethod
    def write(self, artifacts: List[ReportArtifact]) -> None:
        pass  # pragma: no cover
