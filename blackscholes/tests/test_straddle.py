from .. import BlackScholesStraddleLong, BlackScholesStraddleShort

# Test parameters
test_S = 55.0  # Asset price of 55
test_K = 50.0  # Strike price of 50
test_T = 1.0  # 1 year to maturity
test_r = 0.0025  # 0.25% risk-free rate
test_sigma = 0.15  # 15% vol


class TestBlackScholesStraddleLong:
    def test_individual_methods(self):
        straddle = BlackScholesStraddleLong(test_S, test_K, test_T, test_r, test_sigma)
        test_methods = list(straddle.call1.get_all_greeks().keys()) + [
            "price",
        ]
        # Long straddle = Put1 + Call1
        for attr in test_methods:
            assert (
                getattr(straddle, attr)()
                == getattr(straddle.put1, attr)() + getattr(straddle.call1, attr)()
            )


class TestBlackScholesStraddleShort:
    def test_individual_methods(self):
        straddle = BlackScholesStraddleShort(test_S, test_K, test_T, test_r, test_sigma)
        test_methods = list(straddle.call1.get_all_greeks().keys()) + [
            "price",
        ]
        # Short straddle = - Put1 - Call1
        for attr in test_methods:
            assert (
                getattr(straddle, attr)()
                == -getattr(straddle.put1, attr)() - getattr(straddle.call1, attr)()
            )
