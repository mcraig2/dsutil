import unittest

from dsutil.pipeline import (
    DatasetPipelineConfig,
    DatasetPipeline,
    PipelineReader,
    PipelineProcessor,
    PipelineFitter,
    PipelineMonitor,
    PipelineWriter,
)


class DatasetPipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.config = DatasetPipelineConfig(
            name='',
            reader=PipelineReader(),
            processor=PipelineProcessor(),
            fitter=PipelineFitter(),
            monitor=PipelineMonitor(),
            writer=PipelineWriter(filenames=['output.csv']),
        )
        self.pipeline = DatasetPipeline(config=self.config)

    @unittest.skip
    def test_raw_data(self) -> None:
        pass

    @unittest.skip
    def test_processed_data(self) -> None:
        pass

    @unittest.skip
    def test_models(self) -> None:
        pass

    @unittest.skip
    def test_report_artifacts(self) -> None:
        pass

    @unittest.skip
    def test_output_filenames(self) -> None:
        pass

    @unittest.skip
    def test_run(self) -> None:
        pass
