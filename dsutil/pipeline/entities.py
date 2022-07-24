from dataclasses import dataclass
from functools import cached_property
from typing import List, Optional
import uuid

import pandas as pd

from dsutil.pipeline.read import PipelineReader
from dsutil.pipeline.process import (
    ProcessedData,
    PipelineProcessor,
)
from dsutil.pipeline.fitter import PipelineFitter
from dsutil.pipeline.monitor import (
    ReportArtifact,
    PipelineMonitor,
)
from dsutil.pipeline.write import PipelineWriter


@dataclass
class DatasetPipelineConfig:
    name: str
    reader: PipelineReader
    processor: Optional[PipelineProcessor] = None
    fitter: Optional[PipelineFitter] = None
    monitor: Optional[PipelineMonitor] = None
    writer: Optional[PipelineWriter] = None

    @cached_property
    def uuid(self) -> str:
        return str(uuid.uuid4())


@dataclass
class DatasetPipelineResults:
    name: str
    raw_data: List[pd.DataFrame]
    processed_data: List[ProcessedData]
    models: List[object]
    report_artifacts: List[ReportArtifact]
