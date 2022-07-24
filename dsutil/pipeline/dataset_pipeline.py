from functools import cached_property
from typing import List, Optional

import pandas as pd

from dsutil.pipeline import (
    DatasetPipelineConfig,
    DatasetPipelineResults,
)


class DatasetPipeline:
    def __init__(self, config: DatasetPipelineConfig):
        self.config = config

    def run(self) -> DatasetPipelineResults:
        return DatasetPipelineResults(
            name=self.config.name,
            raw_data=self.raw_data,
            processed_data=self.processed_data,
            models=self.models,
            report_artifacts=self.report_artifacts,
            output_filenames=self.output_filenames,
        )

    @cached_property
    def raw_data(self) -> List[pd.DataFrame]:
        return self.config.reader.read()

    @cached_property
    def processed_data(self) -> List[pd.DataFrame]:
        if self.config.processor is None:
            return self.raw_data
        return self.config.processor.process()

    @cached_property
    def models(self) -> Optional[List[object]]:
        if self.config.fitter is not None:
            self.config.fitter.fit()
            return self.config.fitter.models

    @cached_property
    def report_artifacts(self) -> Optional[List[str]]:
        if self.config.monitor is not None:
            self.config.monitor.monitor()
            return self.config.monitor.report_artifacts

    @cached_property
    def output_filenames(self) -> List[str]:
        if self.config.writer is not None:
            self.config.writer.write()
            return self.config.writer.filenames
