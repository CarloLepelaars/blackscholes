import pytest
import numpy as np

from blackscholes.base import BlackScholesBase


class BlackScholesMeta(BlackScholesBase):
    """ Dummy class for testing base methods. """
    def __init__(self, S: float, K: float, T: float, r: float, sigma: float):
        super().__init__(S=S, K=K, T=T, r=r, sigma=sigma)

    def price(self):
        ...

    def in_the_money(self):
        ...

    def get_all_greeks(self):
        ...


class TestBlackScholesBase:
    test_S = 55.  # Asset price of 55
    test_K = 50.  # Strike price of 50
    test_T = 1.  # 1 year to maturity
    test_r = 0.0025  # 0.25% risk-free rate
    test_sigma = 0.15  # 15% vol
    meta = BlackScholesMeta(S=test_S, K=test_K, T=test_T, r=test_r, sigma=test_sigma)

    def test_arg_assert(self):
        # Should not be able to initialize if S, K, T, or sigma is negative.
        with pytest.raises(AssertionError):
            BlackScholesMeta(S=-self.test_S, K=self.test_K, T=self.test_T, r=self.test_r, sigma=self.test_sigma)
            BlackScholesMeta(S=self.test_S, K=-self.test_K, T=self.test_T, r=self.test_r, sigma=self.test_sigma)
            BlackScholesMeta(S=-self.test_S, K=self.test_K, T=-self.test_T, r=self.test_r, sigma=self.test_sigma)
            BlackScholesMeta(S=self.test_S, K=self.test_K, T=self.test_T, r=self.test_r, sigma=-self.test_sigma)

        # Initializing with negative r (interest rate) is possible.
        BlackScholesMeta(S=self.test_S, K=self.test_K, T=self.test_T, r=-self.test_r, sigma=self.test_sigma)

    def test_d(self):
        # d1 and d2 should be accurate up to at least 6 decimals
        np.testing.assert_almost_equal(self.meta._d1, 0.7270678653621663, decimal=6)
        np.testing.assert_almost_equal(self.meta._d2, 0.5770678653621663, decimal=6)

    def test_gamma(self):
        gamma = self.meta.gamma()
        np.testing.assert_almost_equal(gamma, 0.03712496688031454, decimal=6)

    def test_vega(self):
        ...