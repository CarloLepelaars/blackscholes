import pytest

from ..straddle import BlackScholesStraddle

# Test parameters
test_S = 55.0  # Asset price of 55
test_K = 50.0  # Strike price of 50
test_T = 1.0  # 1 year to maturity
test_r = 0.0025  # 0.25% risk-free rate
test_sigma = 0.15  # 15% vol


class TestBlackScholesStraddle:
    def test_init(self):
        # Type should be either 'long' or 'short'.
        with pytest.raises(AssertionError):
            BlackScholesStraddle(
                test_S, test_K, test_T, test_r, test_sigma, type="invalid!"
            )

    def test_individual_methods_long(self):
        straddle = BlackScholesStraddle(
            test_S, test_K, test_T, test_r, test_sigma, type="long"
        )
        test_methods = list(straddle.call.get_all_greeks().keys()) + [
            "price",
            "in_the_money",
        ]
        for attr in test_methods:
            assert (
                getattr(straddle, attr)()
                == getattr(straddle.put, attr)() + getattr(straddle.call, attr)()
            )

    def test_individual_methods_short(self):
        straddle = BlackScholesStraddle(
            test_S, test_K, test_T, test_r, test_sigma, type="short"
        )
        test_methods = list(straddle.call.get_all_greeks().keys()) + [
            "price",
            "in_the_money",
        ]
        for attr in test_methods:
            assert (
                getattr(straddle, attr)()
                == -getattr(straddle.put, attr)() - getattr(straddle.call, attr)()
            )
