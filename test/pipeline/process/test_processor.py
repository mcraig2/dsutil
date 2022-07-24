import unittest

from dsutil.pipeline.process import PipelineProcessor


class PipelineProcessorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = PipelineProcessor()

    @unittest.skip
    def test_something(self) -> None:
        pass
