import unittest

from dsutil.pipeline.monitor import PipelineMonitor


class PipelineMonitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = PipelineMonitor()

    @unittest.skip
    def test_something(self) -> None:
        pass
