from math import exp

import numpy as np
import pytest

from blackscholes import BinaryCall, BinaryPut, Black76Call, Black76Put, BlackScholesCall, BlackScholesPut

from tests.helpers import assert_almost_dict, assert_outputs, cases, discount_q, discount_r, spot_delta_factor


@pytest.mark.parametrize("case", cases("bsm"), ids=lambda c: c["id"])
class TestBlackScholesPut:
    def test_outputs(self, case):
        put = BlackScholesPut(**case["inputs"])
        assert_outputs(put, case["put"]["outputs"])
        assert_almost_dict(put.get_core_greeks(), case["put"]["core_greeks"])
        assert_almost_dict(put.get_itm_proxies(), case["put"]["itm_proxies"])
        assert_almost_dict(put.get_all_greeks(), case["put"]["all_greeks"])

    def test_put_call_parity(self, case):
        inp, call, put = case["inputs"], BlackScholesCall(**case["inputs"]), BlackScholesPut(**case["inputs"])
        np.testing.assert_almost_equal(call.delta() - put.delta(), discount_q(inp), decimal=5)
        np.testing.assert_almost_equal(call.spot_delta() - put.spot_delta(), spot_delta_factor(inp), decimal=5)
        np.testing.assert_almost_equal(call.dual_delta() + put.dual_delta(), discount_r(inp), decimal=5)
        itm = put.in_the_money()
        assert 0.0 < itm < 1.0
        assert 0.0 < put.dual_delta() < 1.0

    def test_theta_with_dividend(self, case):
        # With q>0, put theta density term must use exp(-qT) (not exp(+qT)).
        inp = {**case["inputs"], "q": 0.05}
        call_q, put_q = BlackScholesCall(**inp), BlackScholesPut(**inp)
        q, S, T, r, K = inp["q"], inp["S"], inp["T"], inp["r"], inp["K"]
        np.testing.assert_almost_equal(call_q.theta() - put_q.theta(), q * S * exp(-q * T) - r * K * exp(-r * T), decimal=6)


@pytest.mark.parametrize("case", cases("black76"), ids=lambda c: c["id"])
class TestBlack76Put:
    def test_outputs(self, case):
        put = Black76Put(**case["inputs"])
        assert_outputs(put, case["put"]["outputs"])
        assert_almost_dict(put.get_core_greeks(), case["put"]["core_greeks"])
        assert_almost_dict(put.get_all_greeks(), case["put"]["all_greeks"])

    def test_put_call_parity(self, case):
        call, put = Black76Call(**case["inputs"]), Black76Put(**case["inputs"])
        np.testing.assert_almost_equal(call.delta() - put.delta(), discount_r(case["inputs"]), decimal=5)


@pytest.mark.parametrize("case", cases("binary"), ids=lambda c: c["id"])
class TestBinaryPut:
    def test_outputs(self, case):
        put = BinaryPut(**case["inputs"])
        assert_outputs(put, case["put"]["outputs"])
        assert_almost_dict(put.get_core_greeks(), case["put"]["core_greeks"])

    def test_call_is_opposite_gamma_vega(self, case):
        put, call = BinaryPut(**case["inputs"]), BinaryCall(**case["inputs"])
        np.testing.assert_almost_equal(put.gamma(), -call.gamma(), decimal=12)
        np.testing.assert_almost_equal(put.vega(), -call.vega(), decimal=12)
