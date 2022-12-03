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

    def test_rho(self):
        put_rho = self.put.rho()
        np.testing.assert_almost_equal(put_rho, -14.062140947956918, decimal=6)

    def test_in_the_money(self):
        itm_prob = self.put.in_the_money()
        np.testing.assert_almost_equal(itm_prob, 0.2819468056232066, decimal=6)
