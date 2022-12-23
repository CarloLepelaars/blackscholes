import pytest

from .. import BlackScholesStrangleLong, BlackScholesStrangleShort

# Test parameters
test_S = 55.0  # Asset price of 55
test_K1 = 40.0  # Strike price of 40
test_K2 = 50.0  # Strike price of 50
test_T = 1.0  # 1 year to maturity
test_r = 0.0025  # 0.25% risk-free rate
test_sigma = 0.15  # 15% vol


class TestBlackScholesStrangleLong:
    def test_init(self):
        # Assert K1 < K2
        with pytest.raises(AssertionError):
            BlackScholesStrangleLong(
                S=test_S, K1=50, K2=45, T=test_T, r=test_r, sigma=test_sigma
            )

    def test_individual_methods(self):
        strangle = BlackScholesStrangleLong(
            test_S, test_K1, test_K2, test_T, test_r, test_sigma
        )
        test_methods = list(strangle.call1.get_all_greeks().keys()) + [
            "price",
        ]
        # Long strangle = Put1 + Call1
        for attr in test_methods:
            assert (
                getattr(strangle, attr)()
                == getattr(strangle.put1, attr)() + getattr(strangle.call1, attr)()
            )


class TestBlackScholesStrangleShort:
    def test_init(self):
        # Assert K1 < K2
        with pytest.raises(AssertionError):
            BlackScholesStrangleShort(
                S=test_S, K1=50, K2=45, T=test_T, r=test_r, sigma=test_sigma
            )

    def test_individual_methods(self):
        strangle = BlackScholesStrangleShort(
            test_S, test_K1, test_K2, test_T, test_r, test_sigma
        )
        test_methods = list(strangle.call1.get_all_greeks().keys()) + [
            "price",
        ]
        # Short strangle = -Put1 - Call1
        for attr in test_methods:
            assert (
                getattr(strangle, attr)()
                == -getattr(strangle.put1, attr)() - getattr(strangle.call1, attr)()
            )
