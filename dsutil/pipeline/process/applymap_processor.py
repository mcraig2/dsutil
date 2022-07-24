from typing import Any, Callable, List

import pandas as pd

from dsutil.pipeline.process import PipelineProcessor


class ApplyMapProcessor(PipelineProcessor):
    def __init__(self, applymap_fn: Callable[[Any], Any]) -> None:
        self.fn = applymap_fn

    def process(self, data: List[pd.DataFrame]) -> List[pd.DataFrame]:
        return [
            frame.applymap(self.fn) for frame in data
        ]
