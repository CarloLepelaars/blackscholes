from math import exp

import numpy as np
import pytest

from blackscholes import BinaryPut, Black76Put, BlackScholesCall, BlackScholesPut

from tests.helpers import assert_option, cases


@pytest.mark.parametrize("case", cases("bsm"), ids=lambda c: c["id"])
class TestBlackScholesPut:
    def test_price_and_greeks(self, case):
        assert_option(BlackScholesPut(**case["inputs"]), case["put"])


@pytest.mark.parametrize("case", cases("black76"), ids=lambda c: c["id"])
class TestBlack76Put:
    def test_price_and_greeks(self, case):
        assert_option(Black76Put(**case["inputs"]), case["put"])


@pytest.mark.parametrize("case", cases("binary"), ids=lambda c: c["id"])
class TestBinaryPut:
    def test_price_and_greeks(self, case):
        assert_option(BinaryPut(**case["inputs"]), case["put"])


def test_put_theta_with_dividend():
    """Put theta with a dividend must use exp(-qT), not exp(+qT)."""
    inp = {**cases("bsm")[0]["inputs"], "q": 0.05}
    q, S, T, r, K = inp["q"], inp["S"], inp["T"], inp["r"], inp["K"]
    lhs = BlackScholesCall(**inp).theta() - BlackScholesPut(**inp).theta()
    np.testing.assert_almost_equal(lhs, q * S * exp(-q * T) - r * K * exp(-r * T), decimal=6)
