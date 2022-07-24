import unittest

import test.integration.pipeline_plans.regression_plan as rp


class RegressionPipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data, cls.coef = rp.generate_data()
        cls.plan = rp.generate_plan([cls.data])

    def test_run(self) -> None:
        pass
