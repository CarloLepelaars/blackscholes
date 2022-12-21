import numpy as np

from blackscholes import Black76Call, Black76Put, BlackScholesCall, BlackScholesPut

# Test parameters
test_S = 55.0  # Asset price of 55
test_K = 50.0  # Strike price of 50
test_T = 1.0  # 1 year to maturity
test_r = 0.0025  # 0.25% risk-free rate
test_sigma = 0.15  # 15% vol


class TestBlackScholesPut:
    put = BlackScholesPut(S=test_S, K=test_K, T=test_T, r=test_r, sigma=test_sigma)

    def test_price(self):
        put_price = self.put.price()
        np.testing.assert_almost_equal(put_price, 1.214564, decimal=4)

    def test_delta(self):
        put_delta = self.put.delta()
        np.testing.assert_almost_equal(put_delta, -0.233592191490538, decimal=6)

        # Due to put-call parity, Call delta - Put delta should be 1.
        call = BlackScholesCall(
            S=test_S,
            K=test_K,
            T=test_T,
            r=test_r,
            sigma=test_sigma,
        )
        np.testing.assert_almost_equal(call.delta() - put_delta, 1.0, decimal=5)

    def test_dual_delta(self):
        put_delta = self.put.dual_delta()
        assert 0.0 < put_delta < 1.0
        np.testing.assert_almost_equal(put_delta, 0.2812428189591384, decimal=6)

        # Due to put-call parity, Call dual delta + Put dual delta should be 1.
        call = BlackScholesCall(
            S=test_S,
            K=test_K,
            T=test_T,
            r=test_r,
            sigma=test_sigma,
        )
        np.testing.assert_almost_equal(call.dual_delta() + put_delta, 1.0, decimal=2)

    def test_theta(self):
        put_theta = self.put.theta()
        np.testing.assert_almost_equal(put_theta, -1.2282536767758119, decimal=6)

    def test_epsilon(self):
        call_epsilon = self.put.epsilon()
        np.testing.assert_almost_equal(call_epsilon, 12.84757053197959, decimal=6)

    def test_rho(self):
        put_rho = self.put.rho()
        np.testing.assert_almost_equal(put_rho, -14.062140947956918, decimal=6)

    def test_charm(self):
        charm = self.put.charm()
        np.testing.assert_almost_equal(charm, 0.0832677717846717, decimal=6)

    def test_get_core_greeks(self):
        core_greeks = self.put.get_core_greeks()
        expected_result = {
            "delta": -0.233592191490538,
            "gamma": 0.03712496688031454,
            "vega": 16.84545372194272,
            "theta": -1.2282536767758119,
            "rho": -14.062140947956918,
        }
        assert set(core_greeks.keys()) == set(expected_result.keys())
        for key in expected_result.keys():
            np.testing.assert_almost_equal(
                core_greeks[key], expected_result[key], decimal=5
            )

    def test_get_itm_proxies(self):
        itm_proxies = self.put.get_itm_proxies()
        expected_result = {
            "in_the_money": 0.2819468056232066,
            "dual_delta": 0.2812428189591384,
        }
        assert set(itm_proxies.keys()) == set(expected_result.keys())
        for key in expected_result.keys():
            np.testing.assert_almost_equal(
                itm_proxies[key], expected_result[key], decimal=5
            )

    def test_in_the_money(self):
        itm_prob = self.put.in_the_money()
        assert 0.0 < itm_prob < 1.0
        np.testing.assert_almost_equal(itm_prob, 0.2819468056232066, decimal=6)

    def test_all_greeks(self):
        all_greeks = self.put.get_all_greeks()
        expected_result = {
            "delta": -0.233592191490538,
            "gamma": 0.03712496688031454,
            "vega": 16.84545372194272,
            "theta": -1.2282536767758119,
            "epsilon": 12.84757053197959,
            "rho": -14.062140947956918,
            "lambda_greek": -10.57787211261979,
            "vanna": -1.178299396409533,
            "charm": 0.0832677717846717,
            "vomma": 47.11869947977544,
            "veta": 11.752499520643353,
            "phi": 0.04492120992518061,
            "speed": -0.003946801873134375,
            "zomma": -0.14365691533482322,
            "color": -0.011224141490466934,
            "ultima": -827.4229433648609,
            "dual_delta": 0.2812428189591384,
            "dual_gamma": 0.0449212099251806,
        }
        assert set(all_greeks.keys()) == set(expected_result.keys())
        for key in expected_result.keys():
            np.testing.assert_almost_equal(
                all_greeks[key], expected_result[key], decimal=5
            )


class TestBlack76Put:
    put = Black76Put(F=test_S, K=test_K, T=test_T, r=test_r, sigma=test_sigma)

    def test_price(self):
        price = self.put.price()
        np.testing.assert_almost_equal(price, 1.2470010007171901, decimal=6)

    def test_delta(self):
        delta = self.put.delta()
        np.testing.assert_almost_equal(delta, -0.23813161620464113, decimal=5)

        # Due to put-call parity, Call delta - Put delta should be 1.
        call = Black76Call(
            F=test_S,
            K=test_K,
            T=test_T,
            r=test_r,
            sigma=test_sigma,
        )
        np.testing.assert_almost_equal(call.delta() - delta, 1.0, decimal=2)

    def test_theta(self):
        theta = self.put.theta()
        np.testing.assert_almost_equal(theta, -1.272324203924551, decimal=5)

    def test_rho(self):
        rho = self.put.rho()
        np.testing.assert_almost_equal(rho, -1.2470010007171901, decimal=5)

    def test_get_core_greeks(self):
        core_greeks = self.put.get_core_greeks()
        expected_result = {
            "delta": -0.23813161620464113,
            "gamma": 0.03747854417414418,
            "vega": 17.00588941901792,
            "theta": -1.272324203924551,
            "rho": -1.2470010007171901,
        }
        assert set(core_greeks.keys()) == set(expected_result.keys())
        for key in expected_result.keys():
            np.testing.assert_almost_equal(
                core_greeks[key], expected_result[key], decimal=5
            )

    def test_all_greeks(self):
        all_greeks = self.put.get_all_greeks()
        expected_result = {
            "delta": -0.23813161620464113,
            "gamma": 0.03747854417414418,
            "vega": 17.00588941901792,
            "theta": -1.272324203924551,
            "rho": -1.2470010007171901,
            "vanna": -1.1551661594303946,
            "vomma": 45.13472833935059,
        }

        assert set(all_greeks.keys()) == set(expected_result.keys())
        for key in expected_result.keys():
            np.testing.assert_almost_equal(
                all_greeks[key], expected_result[key], decimal=5
            )
