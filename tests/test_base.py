import numpy as np
import pytest
from scipy.stats import norm

from blackscholes.base import BinaryBase, Black76Base, BlackScholesBase, StandardNormalMixin

from tests.helpers import assert_methods, assert_positive_params, cases


class TestStandardNormalMixIn:
    mix = StandardNormalMixin()
    for n in range(-10, 10, 2):
        np.testing.assert_almost_equal(norm.pdf(n), mix._pdf(n), decimal=5)
        np.testing.assert_almost_equal(norm.cdf(n), mix._cdf(n), decimal=5)


class BlackScholesMeta(BlackScholesBase):
    def price(self): ...
    def in_the_money(self): ...
    def delta(self): ...
    def spot_delta(self): ...
    def dual_delta(self): ...
    def theta(self): ...
    def epsilon(self): ...
    def rho(self): ...
    def charm(self): ...


class Black76Meta(Black76Base):
    def price(self): ...
    def delta(self): ...
    def theta(self): ...
    def rho(self): ...


class BinaryMeta(BinaryBase):
    def price(self): ...
    def forward(self): ...
    def delta(self): ...
    def vega(self): ...
    def theta(self): ...
    def rho(self): ...


@pytest.mark.parametrize("case", cases("bsm"), ids=lambda c: c["id"])
class TestBlackScholesBase:
    def test_arg_assert(self, case):
        assert_positive_params(BlackScholesMeta, case["inputs"], ("S", "K", "T", "sigma"))

    def test_d_and_shared_greeks(self, case):
        assert_methods(BlackScholesMeta(**case["inputs"]), case["base"])


@pytest.mark.parametrize("case", cases("black76"), ids=lambda c: c["id"])
class TestBlack76Base:
    def test_arg_assert(self, case):
        assert_positive_params(Black76Meta, case["inputs"], ("F", "K", "T", "sigma"))

    def test_d_and_shared_greeks(self, case):
        assert_methods(Black76Meta(**case["inputs"]), case["base"], decimal=5)


@pytest.mark.parametrize("case", cases("binary"), ids=lambda c: c["id"])
class TestBinaryBase:
    def test_arg_assert(self, case):
        assert_positive_params(BinaryMeta, case["inputs"], ("S", "K", "T", "sigma"))

    def test_d_and_gamma(self, case):
        assert_methods(BinaryMeta(**case["inputs"]), case["base"])
