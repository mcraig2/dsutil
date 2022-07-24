from typing import List

import pandas as pd

from dsutil.pipeline.read import PipelineReader


class PassthroughReader(PipelineReader):
    def __init__(self, data: List[pd.DataFrame]):
        self.data = data

    def read(self) -> List[pd.DataFrame]:
        return self.data
