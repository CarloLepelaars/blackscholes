import numpy as np

from blackscholes import BlackScholesPut, BlackScholesCall


class TestBlackScholesPut:
    test_S = 55.  # Asset price of 55
    test_K = 50.  # Strike price of 50
    test_T = 1.  # 1 year to maturity
    test_r = 0.0025  # 0.25% risk-free rate
    test_sigma = 0.15  # 15% vol
    put = BlackScholesPut(S=test_S, K=test_K, T=test_T, r=test_r, sigma=test_sigma)

    def test_delta(self):
        put_delta = self.put.delta()
        np.testing.assert_almost_equal(put_delta, -0.233592191490538, decimal=6)

        # Due to put-call parity, Call delta - Put delta should be 1.
        call = BlackScholesCall(S=self.test_S, K=self.test_K, T=self.test_T,
                                r=self.test_r, sigma=self.test_sigma)
        assert call.delta() - put_delta == 1.
