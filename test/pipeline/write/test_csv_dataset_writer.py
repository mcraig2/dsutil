import os
import unittest

import pandas as pd

from dsutil.pipeline import (
    CSVDatasetWriter,
    ReportArtifact,
)


class CSVDatasetWriterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.datasets = [
            pd.DataFrame({'one': [1, 2, 3], 'two': [2, 3, 4]}),
            pd.DataFrame({'a': [1, 2, 3, 4, 5]}),
        ]
        self.filenames = ['tmp/one.csv', 'tmp/two.csv']
        self.writer = CSVDatasetWriter()
        os.system('mkdir -p tmp/')

    def tearDown(self) -> None:
        os.system('rm -rf tmp/')

    def test_write(self) -> None:
        artifacts = [
            ReportArtifact(data=data, filename=filename)
            for data, filename in zip(self.datasets, self.filenames)
        ]
        self.writer.write(artifacts=artifacts)
        for actual, filename in zip(self.datasets, self.filenames):
            expected = pd.read_csv(filename)
            pd.testing.assert_frame_equal(expected, actual)
