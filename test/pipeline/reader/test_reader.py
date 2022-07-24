import unittest

from dsutil.pipeline.read import PipelineReader


class PipelineReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = PipelineReader()

    @unittest.skip
    def test_something(self) -> None:
        pass
