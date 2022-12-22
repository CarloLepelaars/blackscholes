import numpy as np
import pytest
from scipy.stats import norm

from blackscholes.base import Black76Base, BlackScholesBase, StandardNormalMixin

# Test parameters
test_S = 55.0  # Asset price of 55
test_K = 50.0  # Strike price of 50
test_T = 1.0  # 1 year to maturity
test_r = 0.0025  # 0.25% risk-free rate
test_sigma = 0.15  # 15% vol


class TestStandardNormalMixIn:
    mix = StandardNormalMixin()
    # PDF and CDF in mixin should be similar to SciPy's standard normal distribution
    for n in range(-10, 10, 2):
        np.testing.assert_almost_equal(norm.pdf(n), mix._pdf(n), decimal=5)
        np.testing.assert_almost_equal(norm.cdf(n), mix._cdf(n), decimal=5)


class BlackScholesMeta(BlackScholesBase):
    """Dummy class for testing Black Scholes base methods."""

    def __init__(
        self, S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0
    ):
        super().__init__(S=S, K=K, T=T, r=r, sigma=sigma, q=q)

    def price(self):
        ...

    def in_the_money(self):
        ...

    def delta(self):
        ...

    def dual_delta(self):
        ...

    def theta(self):
        ...

    def epsilon(self):
        ...

    def rho(self):
        ...

    def charm(self):
        ...


class TestBlackScholesBase:
    meta = BlackScholesMeta(S=test_S, K=test_K, T=test_T, r=test_r, sigma=test_sigma)

    def test_arg_assert(self):
        # Should not be able to initialize with invalid values for S, K, T, or sigma.
        with pytest.raises(AssertionError):
            BlackScholesMeta(
                S=0.0,
                K=test_K,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
            BlackScholesMeta(
                S=test_S,
                K=0.0,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
            BlackScholesMeta(
                S=test_S,
                K=test_K,
                T=0.0,
                r=test_r,
                sigma=test_sigma,
            )
            BlackScholesMeta(
                S=test_S,
                K=test_K,
                T=test_T,
                r=test_r,
                sigma=0.0,
            )

        # Initializing with negative r (interest rate) is possible.
        BlackScholesMeta(
            S=test_S,
            K=test_K,
            T=test_T,
            r=-test_r,
            sigma=test_sigma,
        )

    def test_d(self):
        # d1 and d2 should be accurate up to at least 6 decimals
        np.testing.assert_almost_equal(self.meta._d1, 0.7270678653621663, decimal=6)
        np.testing.assert_almost_equal(self.meta._d2, 0.5770678653621663, decimal=6)

    def test_gamma(self):
        gamma = self.meta.gamma()
        np.testing.assert_almost_equal(gamma, 0.03712496688031454, decimal=6)

    def test_dual_gamma(self):
        dual_gamma = self.meta.dual_gamma()
        np.testing.assert_almost_equal(dual_gamma, 0.0449212099251806, decimal=6)

    def test_vega(self):
        vega = self.meta.vega()
        np.testing.assert_almost_equal(vega, 16.84545372194272, decimal=6)

    def test_vanna(self):
        vanna = self.meta.vanna()
        np.testing.assert_almost_equal(vanna, -1.178299396409533, decimal=6)

    def test_vomma(self):
        vomma = self.meta.vomma()
        np.testing.assert_almost_equal(vomma, 47.11869947977544, decimal=6)

    def test_veta(self):
        veta = self.meta.veta()
        np.testing.assert_almost_equal(veta, 11.752499520643353, decimal=6)

    def test_phi(self):
        phi = self.meta.phi()
        np.testing.assert_almost_equal(phi, 0.04492120992518061, decimal=6)

    def test_zomma(self):
        zomma = self.meta.zomma()
        np.testing.assert_almost_equal(zomma, -0.14365691533482322, decimal=6)

    def test_speed(self):
        speed = self.meta.speed()
        np.testing.assert_almost_equal(speed, -0.003946801873134375, decimal=6)

    def test_color(self):
        color = self.meta.color()
        np.testing.assert_almost_equal(color, -0.011224141490466934, decimal=6)

    def test_ultima(self):
        ultima = self.meta.ultima()
        np.testing.assert_almost_equal(ultima, -827.4229433648609, decimal=6)


class Black76Meta(Black76Base):
    """Dummy class for testing Black76 base methods."""

    def __init__(self, F: float, K: float, T: float, r: float, sigma: float):
        super().__init__(F=F, K=K, T=T, r=r, sigma=sigma)

    def price(self):
        ...

    def delta(self):
        ...

    def theta(self):
        ...

    def rho(self):
        ...


class TestBlack76Base:
    meta = Black76Meta(F=test_S, K=test_K, T=test_T, r=test_r, sigma=test_sigma)

    def test_arg_assert(self):
        # Should not be able to initialize if F, K, T, or sigma is negative.
        with pytest.raises(AssertionError):
            Black76Meta(
                F=-test_S,
                K=test_K,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
            Black76Meta(
                F=test_S,
                K=-test_K,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
            Black76Meta(
                F=-test_S,
                K=test_K,
                T=-test_T,
                r=test_r,
                sigma=test_sigma,
            )
            Black76Meta(
                F=test_S,
                K=test_K,
                T=test_T,
                r=test_r,
                sigma=-test_sigma,
            )

        # Initializing with negative r (interest rate) is possible.
        Black76Meta(
            F=test_S,
            K=test_K,
            T=test_T,
            r=-test_r,
            sigma=test_sigma,
        )

    def test_d(self):
        # d1 and d2 should be accurate up to at least 6 decimals
        np.testing.assert_almost_equal(self.meta._d1, 0.7104011986954996, decimal=6)
        np.testing.assert_almost_equal(self.meta._d2, 0.5604011986954995, decimal=6)

    def test_gamma(self):
        gamma = self.meta.gamma()
        np.testing.assert_almost_equal(gamma, 0.03747854417414418, decimal=5)

    def test_vega(self):
        vega = self.meta.vega()
        np.testing.assert_almost_equal(vega, 17.00588941901792, decimal=5)

    def test_vanna(self):
        vanna = self.meta.vanna()
        np.testing.assert_almost_equal(vanna, -1.1551661594303946, decimal=5)

    def test_vomma(self):
        vomma = self.meta.vomma()
        np.testing.assert_almost_equal(vomma, 45.13472833935059, decimal=5)
