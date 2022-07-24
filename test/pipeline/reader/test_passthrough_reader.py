import unittest

from dsutil.pipeline import PassthroughReader


class PassthroughReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = PassthroughReader(data=0)

    @unittest.skip
    def test_something(self) -> None:
        pass
