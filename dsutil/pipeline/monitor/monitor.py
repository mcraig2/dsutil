from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from dsutil.pipeline.entities import ProcessedData


@dataclass
class ReportArtifact:
    data: object
    filename: Optional[str] = None


class PipelineMonitor(ABC):
    @abstractmethod
    def monitor(
            self,
            data: List[ProcessedData],
            models: List[object],
    ) -> List[ReportArtifact]:
        pass  # pragma: no cover
