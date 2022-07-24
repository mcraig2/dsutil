from typing import Any, Callable, List

import pandas as pd

from dsutil.pipeline.process import (
    ProcessedData,
    PipelineProcessor,
)


class ApplyMapProcessor(PipelineProcessor):
    def __init__(
            self,
            applymap_fn: Callable[[Any], Any],
            target_cols: List[str],
    ) -> None:
        self.fn = applymap_fn
        self.target_cols = target_cols

    def process(self, data: List[pd.DataFrame]) -> List[ProcessedData]:
        return [
            PipelineProcessor._separate_exog_endog(
                data=frame.applymap(self.fn),
                target_cols=self.target_cols
            )
            for frame in data
        ]
