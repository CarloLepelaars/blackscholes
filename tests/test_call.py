import numpy as np
import pytest

from blackscholes import BinaryCall, BinaryPut, Black76Call, BlackScholesCall

from tests.helpers import assert_black76_parity, assert_bsm_parity, assert_option, cases


@pytest.mark.parametrize("case", cases("bsm"), ids=lambda c: c["id"])
class TestBlackScholesCall:
    def test_price_and_greeks(self, case):
        assert_option(BlackScholesCall(**case["inputs"]), case["call"])

    def test_put_call_parity(self, case):
        assert_bsm_parity(case["inputs"])


@pytest.mark.parametrize("case", cases("black76"), ids=lambda c: c["id"])
class TestBlack76Call:
    def test_price_and_greeks(self, case):
        assert_option(Black76Call(**case["inputs"]), case["call"])

    def test_put_call_parity(self, case):
        assert_black76_parity(case["inputs"])


@pytest.mark.parametrize("case", cases("binary"), ids=lambda c: c["id"])
class TestBinaryCall:
    def test_price_and_greeks(self, case):
        assert_option(BinaryCall(**case["inputs"]), case["call"])

    def test_put_is_opposite_gamma_vega(self, case):
        call, put = BinaryCall(**case["inputs"]), BinaryPut(**case["inputs"])
        almost = np.testing.assert_almost_equal
        almost(call.gamma(), -put.gamma(), decimal=12)
        almost(call.vega(), -put.vega(), decimal=12)

    def test_greeks_match_finite_differences(self, case):
        """Binary greeks should match a small numerical bump in price."""
        eps, inp, c = 1e-5, case["inputs"], BinaryCall(**case["inputs"])

        def price(**kw):
            return BinaryCall(**{**inp, **kw}).price()

        np.testing.assert_allclose(c.delta(), (price(S=inp["S"] + eps) - price(S=inp["S"] - eps)) / (2 * eps), rtol=1e-5, atol=1e-7)
        np.testing.assert_allclose(c.vega(), (price(sigma=inp["sigma"] + eps) - price(sigma=inp["sigma"] - eps)) / (2 * eps), rtol=1e-5, atol=1e-7)
        np.testing.assert_allclose(c.rho(), (price(r=inp["r"] + eps) - price(r=inp["r"] - eps)) / (2 * eps), rtol=1e-5, atol=1e-7)
