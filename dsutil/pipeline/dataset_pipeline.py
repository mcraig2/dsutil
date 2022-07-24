from functools import cached_property
from typing import List, Optional

import pandas as pd

from dsutil.pipeline import (
    ProcessedData,
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
    def processed_data(self) -> List[ProcessedData]:
        if self.config.processor is None:
            return [
                ProcessedData(exog=data, endog=None)
                for data in self.raw_data
            ]
        return self.config.processor.process(data=self.raw_data)

    @cached_property
    def models(self) -> Optional[List[object]]:
        if self.config.fitter is not None:
            self.config.fitter.fit(
                exog=[processed.exog for processed in self.processed_data],
                endog=[processed.endog for processed in self.processed_data],
            )
            return self.config.fitter.get_fitted()

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
