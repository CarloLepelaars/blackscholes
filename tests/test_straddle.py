from blackscholes import BlackScholesStraddleLong, BlackScholesStraddleShort

from tests.helpers import MARKET, assert_structure


class TestBlackScholesStraddleLong:
    def test_individual_methods(self):
        straddle = BlackScholesStraddleLong(**MARKET)
        # Long straddle = Put1 + Call1
        assert_structure(straddle, lambda s, a: getattr(s.put1, a)() + getattr(s.call1, a)())


class TestBlackScholesStraddleShort:
    def test_individual_methods(self):
        straddle = BlackScholesStraddleShort(**MARKET)
        # Short straddle = -Put1 - Call1
        assert_structure(straddle, lambda s, a: -getattr(s.put1, a)() - getattr(s.call1, a)())
