from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from dsutil.pipeline.entities import ProcessedData
from dsutil.pipeline.fitter import PipelineFitter


@dataclass
class ReportArtifact:
    data: object
    filename: Optional[str] = None


class PipelineMonitor(ABC):
    @abstractmethod
    def monitor(
            self,
            data: List[ProcessedData],
            model_fitter: PipelineFitter,
    ) -> List[ReportArtifact]:
        pass  # pragma: no cover
