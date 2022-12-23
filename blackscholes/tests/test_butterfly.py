import pytest

from .. import BlackScholesButterflyLong, BlackScholesButterflyShort

# Test parameters
test_S = 55.0  # Asset price of 55
test_K1 = 40.0  # Strike price of 40
test_K2 = 50.0  # Strike price of 50
test_K3 = 60.0  # Strike price of 60
test_T = 1.0  # 1 year to maturity
test_r = 0.0025  # 0.25% risk-free rate
test_sigma = 0.15  # 15% vol


class TestBlackScholesButterflyLong:
    def test_init(self):
        # Assert K1 < K2 < K3
        with pytest.raises(AssertionError):
            BlackScholesButterflyLong(
                S=test_S, K1=60, K2=50, K3=40, T=test_T, r=test_r, sigma=test_sigma
            )
        with pytest.raises(AssertionError):
            BlackScholesButterflyLong(
                S=test_S, K1=41, K2=40, K3=50, T=test_T, r=test_r, sigma=test_sigma
            )
        # Assert K2 - K1 = K3 - K2 (symmetry)
        with pytest.raises(AssertionError):
            BlackScholesButterflyLong(
                S=test_S, K1=41, K2=50, K3=60, T=test_T, r=test_r, sigma=test_sigma
            )

    def test_individual_methods(self):
        butterfly = BlackScholesButterflyLong(
            test_S, test_K1, test_K2, test_K3, test_T, test_r, test_sigma
        )
        test_methods = list(butterfly.call1.get_all_greeks().keys()) + [
            "price",
        ]
        # Long (call) butterfly = Call1 - 2 * Call2 + Call3
        for attr in test_methods:
            assert (
                getattr(butterfly, attr)()
                == getattr(butterfly.call1, attr)()
                - 2 * getattr(butterfly.call2, attr)()
                + getattr(butterfly.call3, attr)()
            )


class TestBlackScholesButterflyShort:
    def test_init(self):
        # Assert K1 < K2 < K3
        with pytest.raises(AssertionError):
            BlackScholesButterflyShort(
                S=test_S, K1=60, K2=50, K3=40, T=test_T, r=test_r, sigma=test_sigma
            )
        with pytest.raises(AssertionError):
            BlackScholesButterflyShort(
                S=test_S, K1=41, K2=40, K3=50, T=test_T, r=test_r, sigma=test_sigma
            )
        # Assert K2 - K1 = K3 - K2 (symmetry)
        with pytest.raises(AssertionError):
            BlackScholesButterflyShort(
                S=test_S, K1=41, K2=50, K3=60, T=test_T, r=test_r, sigma=test_sigma
            )

    def test_individual_methods(self):
        butterfly = BlackScholesButterflyShort(
            test_S, test_K1, test_K2, test_K3, test_T, test_r, test_sigma
        )
        test_methods = list(butterfly.put1.get_all_greeks().keys()) + [
            "price",
        ]
        # Short (put) butterfly = -Put1 + 2 * Put2 - Put3
        for attr in test_methods:
            assert (
                getattr(butterfly, attr)()
                == -getattr(butterfly.put1, attr)()
                + 2 * getattr(butterfly.put2, attr)()
                - getattr(butterfly.put3, attr)()
            )
