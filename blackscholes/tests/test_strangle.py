import pytest

from ..strangle import BlackScholesStrangle

# Test parameters
test_S = 55.0  # Asset price of 55
test_K1 = 40.0  # Strike price of 40
test_K2 = 50.0  # Strike price of 50
test_T = 1.0  # 1 year to maturity
test_r = 0.0025  # 0.25% risk-free rate
test_sigma = 0.15  # 15% vol


class TestBlackScholesStrangle:
    def test_init(self):
        # Type should be either 'long' or 'short'.
        with pytest.raises(AssertionError):
            BlackScholesStrangle(
                test_S, test_K1, test_K2, test_T, test_r, test_sigma, type="invalid!"
            )

    def test_individual_methods_long(self):
        straddle = BlackScholesStrangle(
            test_S, test_K1, test_K2, test_T, test_r, test_sigma, type="long"
        )
        test_methods = list(straddle.call1.get_all_greeks().keys()) + [
            "price",
        ]
        for attr in test_methods:
            assert (
                getattr(straddle, attr)()
                == getattr(straddle.put1, attr)() + getattr(straddle.call1, attr)()
            )

    def test_individual_methods_short(self):
        straddle = BlackScholesStrangle(
            test_S, test_K1, test_K2, test_T, test_r, test_sigma, type="short"
        )
        test_methods = list(straddle.call1.get_all_greeks().keys()) + [
            "price",
        ]
        for attr in test_methods:
            assert (
                getattr(straddle, attr)()
                == -getattr(straddle.put1, attr)() - getattr(straddle.call1, attr)()
            )