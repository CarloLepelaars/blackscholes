import numpy as np

from blackscholes import BlackScholesCall, BlackScholesPut


class TestBlackScholesCall:
    test_S = 55.0  # Asset price of 55
    test_K = 50.0  # Strike price of 50
    test_T = 1.0  # 1 year to maturity
    test_r = 0.0025  # 0.25% risk-free rate
    test_sigma = 0.15  # 15% vol
    call = BlackScholesCall(S=test_S, K=test_K, T=test_T, r=test_r, sigma=test_sigma)

    def test_price(self):
        call_price = self.call.price()
        np.testing.assert_almost_equal(call_price, 6.339408, decimal=4)

    def test_delta(self):
        call_delta = self.call.delta()
        np.testing.assert_almost_equal(call_delta, 0.766407808509462, decimal=6)

        # Due to put-call parity, Call delta - Put delta should be 1.
        put = BlackScholesPut(
            S=self.test_S,
            K=self.test_K,
            T=self.test_T,
            r=self.test_r,
            sigma=self.test_sigma,
        )
        assert call_delta - put.delta() == 1.0

    def test_dual_delta(self):
        call_delta = self.call.dual_delta()
        assert 0.0 < call_delta < 1.0
        np.testing.assert_almost_equal(call_delta, 0.7162603034383217, decimal=6)

        # Due to put-call parity, Put dual delta + call dual delta should be 1.
        put = BlackScholesPut(
            S=self.test_S,
            K=self.test_K,
            T=self.test_T,
            r=self.test_r,
            sigma=self.test_sigma,
        )
        np.testing.assert_almost_equal(put.dual_delta() + call_delta, 1.0, decimal=2)

    def test_theta(self):
        call_theta = self.call.theta()
        np.testing.assert_almost_equal(call_theta, -1.3529415670754943, decimal=6)

    def test_rho(self):
        call_rho = self.call.rho()
        np.testing.assert_almost_equal(call_rho, 35.813015171916085, decimal=6)

    def test_get_core_greeks(self):
        core_greeks = self.call.get_core_greeks()
        expected_result = {
            "delta": 0.766407808509462,
            "gamma": 0.03712496688031454,
            "vega": 16.84545372194272,
            "theta": -1.3529415670754943,
            "rho": 35.813015171916085,
        }
        assert core_greeks == expected_result

    def test_get_itm_proxies(self):
        itm_proxies = self.call.get_itm_proxies()
        expected_result = {
            "naive_itm": 0.7180531943767934,
            "dual_delta": 0.7162603034383217,
        }
        assert itm_proxies == expected_result

    def test_in_the_money(self):
        itm_prob_call = self.call.in_the_money()
        assert 0.0 < itm_prob_call < 1.0
        np.testing.assert_almost_equal(itm_prob_call, 0.7180531943767934, decimal=6)

        # Due to put-call parity, Call itm + Put itm should be 1.
        put = BlackScholesPut(
            S=self.test_S,
            K=self.test_K,
            T=self.test_T,
            r=self.test_r,
            sigma=self.test_sigma,
        )
        assert itm_prob_call + put.in_the_money() == 1.0

    def test_lambda(self):
        lambda_greek = self.call.lamdba()
        np.testing.assert_almost_equal(lambda_greek, 6.6492624553539335, decimal=6)
