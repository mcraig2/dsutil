from typing import List

import pandas as pd

from dsutil.pipeline.write import PipelineWriter


class CSVDatasetWriter(PipelineWriter):
    def __init__(
            self,
            datasets: List[pd.DataFrame],
            filenames: List[str],
    ) -> None:
        super().__init__(filenames=filenames)
        self.datasets = datasets

    def write(self) -> None:
        for data, filename in zip(self.datasets, self.filenames):
            data.to_csv(filename, index=False)
