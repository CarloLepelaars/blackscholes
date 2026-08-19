import numpy as np
import pytest

from blackscholes import BinaryCall, BinaryPut, Black76Call, Black76Put, BlackScholesCall, BlackScholesPut

from tests.helpers import assert_almost_dict, assert_outputs, cases, discount_q, discount_r, spot_delta_factor


@pytest.mark.parametrize("case", cases("bsm"), ids=lambda c: c["id"])
class TestBlackScholesCall:
    def test_outputs(self, case):
        call = BlackScholesCall(**case["inputs"])
        assert_outputs(call, case["call"]["outputs"])
        assert_almost_dict(call.get_core_greeks(), case["call"]["core_greeks"])
        assert_almost_dict(call.get_itm_proxies(), case["call"]["itm_proxies"])
        assert_almost_dict(call.get_all_greeks(), case["call"]["all_greeks"])

    def test_put_call_parity(self, case):
        inp, call, put = case["inputs"], BlackScholesCall(**case["inputs"]), BlackScholesPut(**case["inputs"])
        np.testing.assert_almost_equal(call.delta() - put.delta(), discount_q(inp), decimal=5)
        np.testing.assert_almost_equal(call.spot_delta() - put.spot_delta(), spot_delta_factor(inp), decimal=5)
        np.testing.assert_almost_equal(put.dual_delta() + call.dual_delta(), discount_r(inp), decimal=5)
        itm = call.in_the_money()
        assert 0.0 < itm < 1.0
        assert 0.0 < call.dual_delta() < 1.0
        assert itm + put.in_the_money() == 1.0


@pytest.mark.parametrize("case", cases("black76"), ids=lambda c: c["id"])
class TestBlack76Call:
    def test_outputs(self, case):
        call = Black76Call(**case["inputs"])
        assert_outputs(call, case["call"]["outputs"])
        assert_almost_dict(call.get_core_greeks(), case["call"]["core_greeks"])
        assert_almost_dict(call.get_all_greeks(), case["call"]["all_greeks"])

    def test_put_call_parity(self, case):
        call, put = Black76Call(**case["inputs"]), Black76Put(**case["inputs"])
        np.testing.assert_almost_equal(call.delta() - put.delta(), discount_r(case["inputs"]), decimal=5)


@pytest.mark.parametrize("case", cases("binary"), ids=lambda c: c["id"])
class TestBinaryCall:
    def test_outputs(self, case):
        call = BinaryCall(**case["inputs"])
        assert_outputs(call, case["call"]["outputs"])
        assert_almost_dict(call.get_core_greeks(), case["call"]["core_greeks"])

    def test_put_is_opposite_gamma_vega(self, case):
        call, put = BinaryCall(**case["inputs"]), BinaryPut(**case["inputs"])
        np.testing.assert_almost_equal(call.gamma(), -put.gamma(), decimal=12)
        np.testing.assert_almost_equal(call.vega(), -put.vega(), decimal=12)

    def test_greeks_match_finite_differences(self, case):
        """Cash-or-nothing greeks should match central finite differences on price."""
        eps, inp, c = 1e-5, case["inputs"], BinaryCall(**case["inputs"])

        def price(**kw):
            return BinaryCall(**{**inp, **kw}).price()

        np.testing.assert_allclose(c.delta(), (price(S=inp["S"] + eps) - price(S=inp["S"] - eps)) / (2 * eps), rtol=1e-5, atol=1e-7)
        np.testing.assert_allclose(c.vega(), (price(sigma=inp["sigma"] + eps) - price(sigma=inp["sigma"] - eps)) / (2 * eps), rtol=1e-5, atol=1e-7)
        np.testing.assert_allclose(c.rho(), (price(r=inp["r"] + eps) - price(r=inp["r"] - eps)) / (2 * eps), rtol=1e-5, atol=1e-7)
