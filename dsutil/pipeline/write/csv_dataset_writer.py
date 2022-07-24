from typing import List

import pandas as pd

from dsutil.pipeline.write import PipelineWriter


class CSVDatasetWriter(PipelineWriter):
    def write(
            self,
            datasets: List[pd.DataFrame],
            filenames: List[str],
    ) -> None:
        for data, filename in zip(datasets, filenames):
            data.to_csv(filename, index=False)
