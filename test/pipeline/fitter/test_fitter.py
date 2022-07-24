import unittest

from dsutil.pipeline.fitter import PipelineFitter


class PipelineFitterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.fitter = PipelineFitter()

    @unittest.skip
    def test_something(self) -> None:
        pass
