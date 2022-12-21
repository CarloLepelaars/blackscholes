import numpy as np

from blackscholes import Black76Call, Black76Put, BlackScholesCall, BlackScholesPut

# Test parameters
test_S = 55.0  # Asset price of 55
test_K = 50.0  # Strike price of 50
test_T = 1.0  # 1 year to maturity
test_r = 0.0025  # 0.25% risk-free rate
test_sigma = 0.15  # 15% vol


class TestBlackScholesCall:
    call = BlackScholesCall(S=test_S, K=test_K, T=test_T, r=test_r, sigma=test_sigma)

    def test_price(self):
        call_price = self.call.price()
        np.testing.assert_almost_equal(call_price, 6.339408, decimal=4)

    def test_delta(self):
        call_delta = self.call.delta()
        np.testing.assert_almost_equal(call_delta, 0.766407808509462, decimal=6)

        # Due to put-call parity, Call delta - Put delta should be 1.
        put = BlackScholesPut(
            S=test_S,
            K=test_K,
            T=test_T,
            r=test_r,
            sigma=test_sigma,
        )
        np.testing.assert_almost_equal(call_delta - put.delta(), 1.0, decimal=5)

    def test_dual_delta(self):
        call_delta = self.call.dual_delta()
        assert 0.0 < call_delta < 1.0
        np.testing.assert_almost_equal(call_delta, 0.7162603034383217, decimal=6)

        # Due to put-call parity, Put dual delta + call dual delta should be 1.
        put = BlackScholesPut(
            S=test_S,
            K=test_K,
            T=test_T,
            r=test_r,
            sigma=test_sigma,
        )
        np.testing.assert_almost_equal(put.dual_delta() + call_delta, 1.0, decimal=2)

    def test_theta(self):
        call_theta = self.call.theta()
        np.testing.assert_almost_equal(call_theta, -1.3529415670754943, decimal=6)

    def test_epsilon(self):
        call_epsilon = self.call.epsilon()
        np.testing.assert_almost_equal(call_epsilon, -42.15242946802041, decimal=6)

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
        assert set(core_greeks.keys()) == set(expected_result.keys())
        for key in expected_result.keys():
            np.testing.assert_almost_equal(
                core_greeks[key], expected_result[key], decimal=5
            )

    def test_get_itm_proxies(self):
        itm_proxies = self.call.get_itm_proxies()
        expected_result = {
            "in_the_money": 0.7180531943767934,
            "dual_delta": 0.7162603034383217,
        }
        assert set(itm_proxies.keys()) == set(expected_result.keys())
        for key in expected_result.keys():
            np.testing.assert_almost_equal(
                itm_proxies[key], expected_result[key], decimal=5
            )

    def test_in_the_money(self):
        itm_prob_call = self.call.in_the_money()
        assert 0.0 < itm_prob_call < 1.0
        np.testing.assert_almost_equal(itm_prob_call, 0.7180531943767934, decimal=6)

        # Due to put-call parity, Call itm + Put itm should be 1.
        put = BlackScholesPut(
            S=test_S,
            K=test_K,
            T=test_T,
            r=test_r,
            sigma=test_sigma,
        )
        assert itm_prob_call + put.in_the_money() == 1.0

    def test_lambda(self):
        lambda_greek = self.call.lambda_greek()
        np.testing.assert_almost_equal(lambda_greek, 6.6492624553539335, decimal=6)

    def test_charm(self):
        charm = self.call.charm()
        np.testing.assert_almost_equal(charm, 0.0832677717846717, decimal=6)

    def test_all_greeks(self):
        all_greeks = self.call.get_all_greeks()
        expected_result = {
            "delta": 0.766407808509462,
            "gamma": 0.03712496688031454,
            "vega": 16.84545372194272,
            "theta": -1.3529415670754943,
            "epsilon": -42.15242946802041,
            "rho": 35.813015171916085,
            "lambda_greek": 6.6492624553539255,
            "vanna": -1.178299396409533,
            "charm": 0.0832677717846717,
            "vomma": 47.11869947977544,
            "veta": 11.752499520643353,
            "phi": 0.04492120992518061,
            "speed": -0.003946801873134375,
            "zomma": -0.14365691533482322,
            "color": -0.011224141490466934,
            "ultima": -827.4229433648609,
            "dual_delta": 0.7162603034383217,
            "dual_gamma": 0.0449212099251806,
        }
        assert set(all_greeks.keys()) == set(expected_result.keys())
        for key in expected_result.keys():
            np.testing.assert_almost_equal(
                all_greeks[key], expected_result[key], decimal=5
            )


class TestBlack76Call:
    call = Black76Call(F=test_S, K=test_K, T=test_T, r=test_r, sigma=test_sigma)

    def test_price(self):
        price = self.call.price()
        np.testing.assert_almost_equal(price, 6.234516612704489, decimal=6)

    def test_delta(self):
        delta = self.call.delta()
        np.testing.assert_almost_equal(delta, 0.7593715061928189, decimal=5)

        # Due to put-call parity, Call delta - Put delta should be 1.
        put = Black76Put(
            F=test_S,
            K=test_K,
            T=test_T,
            r=test_r,
            sigma=test_sigma,
        )
        np.testing.assert_almost_equal(delta - put.delta(), 1.0, decimal=2)

    def test_theta(self):
        theta = self.call.theta()
        np.testing.assert_almost_equal(theta, -1.2598554148945826, decimal=5)

    def test_rho(self):
        rho = self.call.rho()
        np.testing.assert_almost_equal(rho, -6.234516612704489, decimal=5)

    def test_get_core_greeks(self):
        core_greeks = self.call.get_core_greeks()
        expected_result = {
            "delta": 0.7593715061928189,
            "gamma": 0.03747854417414418,
            "vega": 17.00588941901792,
            "theta": -1.2598554148945826,
            "rho": -6.234516612704489,
        }

        assert set(core_greeks.keys()) == set(expected_result.keys())
        for key in expected_result.keys():
            np.testing.assert_almost_equal(
                core_greeks[key], expected_result[key], decimal=5
            )

    def test_all_greeks(self):
        all_greeks = self.call.get_all_greeks()
        expected_result = {
            "delta": 0.7593715061928189,
            "gamma": 0.03747854417414418,
            "vega": 17.00588941901792,
            "theta": -1.2598554148945826,
            "rho": -6.234516612704489,
            "vanna": -1.1551661594303946,
            "vomma": 45.13472833935059,
        }
        assert set(all_greeks.keys()) == set(expected_result.keys())
        for key in expected_result.keys():
            np.testing.assert_almost_equal(
                all_greeks[key], expected_result[key], decimal=5
            )
