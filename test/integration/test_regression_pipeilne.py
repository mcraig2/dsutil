import unittest

import numpy as np
import pandas as pd

import test.integration.pipeline_plans.regression_plan as rp


class RegressionPipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data, cls.coef = rp.generate_data()
        cls.plan = rp.generate_plan([cls.data])
        cls.results = cls.plan.run()

    def test_postrun_raw_data(self) -> None:
        actual = self.results.raw_data[0]
        expected = self.data
        pd.testing.assert_frame_equal(expected, actual)

    def test_postrun_processed_data(self) -> None:
        actual = self.results.processed_data[0]
        expected = self.data * 2.
        pd.testing.assert_frame_equal(
            expected.drop('target', axis=1),
            actual.exog,
        )
        pd.testing.assert_frame_equal(
            expected[['target']],
            actual.endog,
        )

    def test_postrun_models(self) -> None:
        model = self.results.models[0]
        expected_coef = self.coef.values.flatten()
        actual_coef = model.coef_.flatten()
        self.assertTrue(np.allclose(expected_coef, actual_coef, atol=1.))

    def test_postrun_report_artifacts(self) -> None:
        pass

    def test_postrun_output(self) -> None:
        pass
