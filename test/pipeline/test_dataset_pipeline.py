import os
import unittest
from typing import List

import pandas as pd

from dsutil.pipeline import (
    DatasetPipelineConfig,
    DatasetPipeline,
    DatasetPipelineResults,
    PipelineReader,
    PipelineProcessor,
    PipelineFitter,
    PipelineMonitor,
    PipelineWriter,
    ProcessedData,
)
from dsutil.pipeline.monitor import ReportArtifact


class ReaderTestObject(PipelineReader):
    def read(self) -> List[pd.DataFrame]:
        return [
            pd.DataFrame({'one': [1, 2, 3], 'target': [4, 5, 6]}),
        ]


class ProcessorTestObject(PipelineProcessor):
    def process(self, data: List[pd.DataFrame]) -> List[ProcessedData]:
        return [
            ProcessedData(exog=df[['one']] ** 2., endog=df[['target']])
            for df in data
        ]


class FitterTestObject(PipelineFitter):
    def get_fitted(self) -> List[object]:
        return ['model']

    def fit(self, exog: List[pd.DataFrame], endog: List[pd.DataFrame]) -> None:
        pass  # pragma: no cover

    def predict(self, exog: List[pd.DataFrame]) -> List[pd.DataFrame]:
        return [frame + 3. for frame in exog]


class MonitorTestObject(PipelineMonitor):
    def monitor(
            self,
            data: List[ProcessedData],
            model_fitter: PipelineFitter,
    ) -> List[ReportArtifact]:
        exog = data[0].exog['one']
        yhat = model_fitter.predict(exog=[exog])
        return [
            ReportArtifact(data=yhat[0].min(), filename='pred_min'),
            ReportArtifact(data=yhat[0].max(), filename='pred_max'),
        ]


class WriterTestObject(PipelineWriter):
    def write(self, artifacts: List[ReportArtifact]) -> None:
        with open('tmp/output.csv', 'w') as fle:
            fle.write(','.join([
                artifact.filename for artifact in artifacts
            ]))


class DatasetPipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.config = DatasetPipelineConfig(
            name='test_pipeline',
            reader=ReaderTestObject(),
            processor=ProcessorTestObject(),
            fitter=FitterTestObject(),
            monitor=MonitorTestObject(),
            writer=WriterTestObject(),
        )
        self.pipeline = DatasetPipeline(config=self.config)
        os.system('mkdir -p tmp/')

    def tearDown(self) -> None:
        os.system('rm -rf tmp/')

    def test_raw_data(self) -> None:
        expected = pd.DataFrame({'one': [1, 2, 3], 'target': [4, 5, 6]})
        actual = self.pipeline.raw_data[0]
        pd.testing.assert_frame_equal(expected, actual)

    def test_processed_data(self) -> None:
        expected = ProcessedData(
            exog=pd.DataFrame({'one': [1., 4., 9.]}),
            endog=pd.DataFrame({'target': [4, 5, 6]}),
        )
        actual = self.pipeline.processed_data[0]
        pd.testing.assert_frame_equal(expected.exog, actual.exog)
        pd.testing.assert_frame_equal(expected.endog, actual.endog)

    def test_missing_some_configs(self) -> None:
        new_config = DatasetPipelineConfig(
            name='new_pipeline',
            reader=ReaderTestObject(),
            processor=None,
            fitter=None,
            monitor=None,
            writer=None,
        )
        pipeline = DatasetPipeline(config=new_config)
        expected = [
            ProcessedData(
                exog=pd.DataFrame({'one': [1, 2, 3], 'target': [4, 5, 6]}),
                endog=None,
            )
        ]
        actual = pipeline.processed_data
        pd.testing.assert_frame_equal(expected[0].exog, actual[0].exog)
        self.assertIsNone(actual[0].endog)
        self.assertIsNone(pipeline.models)
        self.assertIsNone(pipeline.report_artifacts)

    def test_models(self) -> None:
        expected = ['model']
        actual = self.pipeline.models
        self.assertEqual(expected, actual)

    def test_report_artifacts(self) -> None:
        expected = [
            ReportArtifact(data=4., filename='pred_min'),
            ReportArtifact(data=12., filename='pred_max'),
        ]
        actual = self.pipeline.report_artifacts
        for expected_art, actual_art in zip(expected, actual):
            self.assertEqual(expected_art.data, actual_art.data)
            self.assertEqual(expected_art.filename, actual_art.filename)

    def test_run(self) -> None:
        expected = DatasetPipelineResults(
            name='test_pipeline',
            raw_data=[pd.DataFrame({'one': [1, 2, 3], 'target': [4, 5, 6]})],
            processed_data=[
                ProcessedData(
                    exog=pd.DataFrame({'one': [1., 4., 9.]}),
                    endog=pd.DataFrame({'target': [4, 5, 6]}),
                )
            ],
            models=['model'],
            report_artifacts=[
                ReportArtifact(data=4., filename='pred_min'),
                ReportArtifact(data=12., filename='pred_max'),
            ],
        )
        actual = self.pipeline.run()
        self.assertEqual(expected.name, actual.name)
        pd.testing.assert_frame_equal(expected.raw_data[0], actual.raw_data[0])
        pd.testing.assert_frame_equal(
            expected.processed_data[0].exog,
            actual.processed_data[0].exog,
        )
        pd.testing.assert_frame_equal(
            expected.processed_data[0].endog,
            actual.processed_data[0].endog,
        )
        self.assertEqual(expected.models, actual.models)
        self.assertEqual(
            expected.report_artifacts[0].data,
            actual.report_artifacts[0].data,
        )
        self.assertEqual(
            expected.report_artifacts[0].filename,
            expected.report_artifacts[0].filename,
        )
        self.assertEqual(
            expected.report_artifacts[1].data,
            actual.report_artifacts[1].data,
        )
        self.assertEqual(
            expected.report_artifacts[1].filename,
            expected.report_artifacts[1].filename,
        )
        with open('tmp/output.csv', 'r') as fle:
            contents = fle.read()
            self.assertEqual(contents, 'pred_min,pred_max')
