from typing import List

import pandas as pd
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression

from dsutil.pipeline import (
    DatasetPipelineConfig,
    DatasetPipeline,
    PipelineReader,
    PassthroughReader,
    PipelineProcessor,
    ApplyMapProcessor,
    PipelineFitter,
    SingleModelFitter,
    PipelineMonitor,
    PipelineWriter,
)


def generate_data() -> List[pd.DataFrame]:
    X, y, coef = make_regression(
        n_samples=10,
        n_features=4,
        n_informative=4,
        n_targets=1,
        noise=1.,
        coef=True,
    )
    data = pd.DataFrame(X)
    data['target'] = y
    return [
        data,
        pd.DataFrame(coef),
    ]


def generate_plan(data: List[pd.DataFrame]) -> DatasetPipeline:
    reader = PassthroughReader(data=data)
    processor = ApplyMapProcessor(
        applymap_fn=lambda x: x * 2.,
        target_cols=['target'],
    )
    fitter = SingleModelFitter(model=LinearRegression())
    monitor = None
    writer = None
    return DatasetPipeline(
        config=DatasetPipelineConfig(
            name='regression_pipeline',
            reader=reader,
            processor=processor,
            fitter=fitter,
            monitor=monitor,
            writer=writer,
        )
    )
