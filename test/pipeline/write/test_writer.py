import unittest

from dsutil.pipeline.write import PipelineWriter


class PipelineWriterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = PipelineWriter()

    @unittest.skip
    def test_something(self) -> None:
        pass
