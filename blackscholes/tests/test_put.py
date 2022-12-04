import numpy as np

from blackscholes import BlackScholesCall, BlackScholesPut


class TestBlackScholesPut:
    test_S = 55.0  # Asset price of 55
    test_K = 50.0  # Strike price of 50
    test_T = 1.0  # 1 year to maturity
    test_r = 0.0025  # 0.25% risk-free rate
    test_sigma = 0.15  # 15% vol
    put = BlackScholesPut(S=test_S, K=test_K, T=test_T, r=test_r, sigma=test_sigma)

    def test_price(self):
        put_price = self.put.price()
        np.testing.assert_almost_equal(put_price, 1.214564, decimal=4)

    def test_delta(self):
        put_delta = self.put.delta()
        np.testing.assert_almost_equal(put_delta, -0.233592191490538, decimal=6)

        # Due to put-call parity, Call delta - Put delta should be 1.
        call = BlackScholesCall(
            S=self.test_S,
            K=self.test_K,
            T=self.test_T,
            r=self.test_r,
            sigma=self.test_sigma,
        )
        assert call.delta() - put_delta == 1.0

    def test_dual_delta(self):
        put_delta = self.put.dual_delta()
        assert 0.0 < put_delta < 1.0
        np.testing.assert_almost_equal(put_delta, 0.2812428189591384, decimal=6)

        # Due to put-call parity, Call dual delta + Put dual delta should be 1.
        call = BlackScholesCall(
            S=self.test_S,
            K=self.test_K,
            T=self.test_T,
            r=self.test_r,
            sigma=self.test_sigma,
        )
        np.testing.assert_almost_equal(call.dual_delta() + put_delta, 1.0, decimal=2)

    def test_theta(self):
        put_theta = self.put.theta()
        np.testing.assert_almost_equal(put_theta, -1.2282536767758119, decimal=6)

    def test_rho(self):
        put_rho = self.put.rho()
        np.testing.assert_almost_equal(put_rho, -14.062140947956918, decimal=6)

    def test_get_core_greeks(self):
        core_greeks = self.put.get_core_greeks()
        expected_result = {
            "delta": -0.233592191490538,
            "gamma": 0.03712496688031454,
            "vega": 16.84545372194272,
            "theta": -1.2282536767758119,
            "rho": -14.062140947956918,
        }
        for key in expected_result.keys():
            np.testing.assert_almost_equal(
                core_greeks[key], expected_result[key], decimal=5
            )

    def test_get_itm_proxies(self):
        itm_proxies = self.put.get_itm_proxies()
        expected_result = {
            "naive_itm": 0.2819468056232066,
            "dual_delta": 0.2812428189591384,
        }
        for key in expected_result.keys():
            np.testing.assert_almost_equal(
                itm_proxies[key], expected_result[key], decimal=5
            )

    def test_in_the_money(self):
        itm_prob = self.put.in_the_money()
        assert 0.0 < itm_prob < 1.0
        np.testing.assert_almost_equal(itm_prob, 0.2819468056232066, decimal=6)
