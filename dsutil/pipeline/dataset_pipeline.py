from functools import cached_property
from typing import List, Optional

import pandas as pd

from dsutil.pipeline.process import ProcessedData
from dsutil.pipeline.monitor import ReportArtifact
from dsutil.pipeline.entities import (
    DatasetPipelineConfig,
    DatasetPipelineResults,
)


class DatasetPipeline:
    def __init__(self, config: DatasetPipelineConfig):
        self.config = config

    def run(
            self,
            write_out_artifacts: Optional[bool] = True,
    ) -> DatasetPipelineResults:
        result = DatasetPipelineResults(
            name=self.config.name,
            raw_data=self.raw_data,
            processed_data=self.processed_data,
            models=self.models,
            report_artifacts=self.report_artifacts,
        )
        if write_out_artifacts:
            self.save_artifacts()
        return result

    def save_artifacts(self) -> None:
        valid = (
            self.config.writer is not None and
            self.report_artifacts is not None
        )
        if valid:
            self.config.writer.write(artifacts=self.report_artifacts)

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
    def report_artifacts(self) -> Optional[List[ReportArtifact]]:
        if self.config.monitor is not None:
            return self.config.monitor.monitor(
                data=self.processed_data,
                model_fitter=self.config.fitter,
            )
