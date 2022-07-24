import unittest

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from dsutil.pipeline import SingleModelFitter


class SingleModelFitterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = pd.DataFrame({
            'x': [1., 2., 3.],
            'y': [3., 5., 7.],
            'intercept': [1., 1., 1.],
        })
        self.exog = [self.data[['x', 'intercept']]]
        self.endog = [self.data[['y']]]
        self.fitter = SingleModelFitter(
            model=LinearRegression(fit_intercept=False)
        )

    def test_model_object(self) -> None:
        self.assertIsInstance(self.fitter.model, LinearRegression)
        self.assertIsInstance(self.fitter.get_fitted()[0], LinearRegression)

    def test_fit(self) -> None:
        self.fitter.fit(exog=self.exog, endog=self.endog)
        actual_coefs = self.fitter.model.coef_
        expected_coefs = np.array([[2., 1.]])
        self.assertTrue(np.allclose(actual_coefs, expected_coefs, atol=1e-3))

    def test_predict(self) -> None:
        self.fitter.fit(exog=self.exog, endog=self.endog)
        new_exog = pd.DataFrame({
            'x': [-5., 10., 7.],
            'intercept': [1., 1., 1.],
        })
        actual_preds = self.fitter.predict(exog=[new_exog])[0].flatten()
        expected_preds = np.array([-9., 21., 15.])
        self.assertTrue(np.allclose(actual_preds, expected_preds, atol=1e-3))
