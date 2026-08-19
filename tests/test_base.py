import numpy as np
import pytest
from scipy.stats import norm

from blackscholes.base import BinaryBase, Black76Base, BlackScholesBase, StandardNormalMixin

from tests.helpers import assert_outputs, assert_positive_params, cases


class TestStandardNormalMixIn:
    mix = StandardNormalMixin()
    for n in range(-10, 10, 2):
        np.testing.assert_almost_equal(norm.pdf(n), mix._pdf(n), decimal=5)
        np.testing.assert_almost_equal(norm.cdf(n), mix._cdf(n), decimal=5)


class BlackScholesMeta(BlackScholesBase):
    """Dummy class for testing Black Scholes base methods."""

    def __init__(self, S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0):
        super().__init__(S=S, K=K, T=T, r=r, sigma=sigma, q=q)

    def price(self): ...
    def in_the_money(self): ...
    def delta(self): ...
    def spot_delta(self): ...
    def dual_delta(self): ...
    def theta(self): ...
    def epsilon(self): ...
    def rho(self): ...
    def charm(self): ...


@pytest.mark.parametrize("case", cases("bsm"), ids=lambda c: c["id"])
class TestBlackScholesBase:
    def test_arg_assert(self, case):
        assert_positive_params(BlackScholesMeta, case["inputs"], ("S", "K", "T", "sigma"))

    def test_d_and_shared_greeks(self, case):
        meta, expected = BlackScholesMeta(**case["inputs"]), case["base"]
        np.testing.assert_almost_equal(meta._d1, expected["d1"], decimal=6)
        np.testing.assert_almost_equal(meta._d2, expected["d2"], decimal=6)
        assert_outputs(meta, {k: v for k, v in expected.items() if k not in ("d1", "d2")})


class Black76Meta(Black76Base):
    """Dummy class for testing Black76 base methods."""

    def __init__(self, F: float, K: float, T: float, r: float, sigma: float):
        super().__init__(F=F, K=K, T=T, r=r, sigma=sigma)

    def price(self): ...
    def delta(self): ...
    def theta(self): ...
    def rho(self): ...


@pytest.mark.parametrize("case", cases("black76"), ids=lambda c: c["id"])
class TestBlack76Base:
    def test_arg_assert(self, case):
        assert_positive_params(Black76Meta, case["inputs"], ("F", "K", "T", "sigma"))

    def test_d_and_shared_greeks(self, case):
        meta, expected = Black76Meta(**case["inputs"]), case["base"]
        np.testing.assert_almost_equal(meta._d1, expected["d1"], decimal=6)
        np.testing.assert_almost_equal(meta._d2, expected["d2"], decimal=6)
        assert_outputs(meta, {k: v for k, v in expected.items() if k not in ("d1", "d2")}, decimal=5)


class BinaryMeta(BinaryBase):
    """Dummy class for testing Binary base methods."""

    def __init__(self, S: float, K: float, T: float, r: float, sigma: float):
        super().__init__(S=S, K=K, T=T, r=r, sigma=sigma)

    def price(self): ...
    def forward(self): ...
    def delta(self): ...
    def vega(self): ...
    def theta(self): ...
    def rho(self): ...


@pytest.mark.parametrize("case", cases("binary"), ids=lambda c: c["id"])
class TestBinaryBase:
    def test_arg_assert(self, case):
        assert_positive_params(BinaryMeta, case["inputs"], ("S", "K", "T", "sigma"))

    def test_d_and_gamma(self, case):
        meta, expected = BinaryMeta(**case["inputs"]), case["base"]
        np.testing.assert_almost_equal(meta._d1, expected["d1"], decimal=6)
        np.testing.assert_almost_equal(meta._d2, expected["d2"], decimal=6)
        np.testing.assert_almost_equal(meta.gamma(), expected["gamma"], decimal=6)
