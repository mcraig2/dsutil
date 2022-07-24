from dataclasses import dataclass
from functools import cached_property
from typing import List, Optional
import uuid

import pandas as pd

from dsutil.pipeline import (
    PipelineReader,
    PipelineProcessor,
    PipelineFitter,
    PipelineMonitor,
    PipelineWriter,
)


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
    processed_data: List[pd.DataFrame]
    models: List[object]
    report_artifacts: List[str]
    output_filenames: List[str]
