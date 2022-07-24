from typing import List

import pandas as pd

from dsutil.pipeline.fitter import PipelineFitter


class SingleModelFitter(PipelineFitter):
    def __init__(self, model: object) -> None:
        self.model = model

    def get_fitted(self) -> List[object]:
        return [self.model]

    def fit(self, exog: List[pd.DataFrame], endog: List[pd.DataFrame]) -> None:
        self.model.fit(
            pd.concat(exog, axis=0, ignore_index=True),
            pd.concat(endog, axis=0, ignore_index=True),
        )

    def predict(self, exog: List[pd.DataFrame]) -> List[pd.DataFrame]:
        return [self.model.predict(data) for data in exog]
