import os
import unittest

import pandas as pd

from dsutil.pipeline import CSVDatasetWriter


class CSVDatasetWriterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.datasets = [
            pd.DataFrame({'one': [1, 2, 3], 'two': [2, 3, 4]}),
            pd.DataFrame({'a': [1, 2, 3, 4, 5]}),
        ]
        self.filenames = ['tmp/one.csv', 'tmp/two.csv']
        self.writer = CSVDatasetWriter(
            datasets=self.datasets,
            filenames=self.filenames,
        )
        os.system('mkdir -p tmp/')

    def tearDown(self) -> None:
        os.system('rm -rf tmp/')

    def test_write(self) -> None:
        self.writer.write()
        for actual, filename in zip(self.datasets, self.filenames):
            expected = pd.read_csv(filename)
            pd.testing.assert_frame_equal(expected, actual)
