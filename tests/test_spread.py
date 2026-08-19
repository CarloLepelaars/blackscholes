import pytest

from blackscholes import BlackScholesBearSpread, BlackScholesBullSpread, BlackScholesCalendarCallSpread, BlackScholesCalendarPutSpread

from tests.helpers import MARKET_2K, MARKET_CAL, assert_rejects, assert_structure


class TestBlackScholesBullSpread:
    def test_init(self):
        assert_rejects(BlackScholesBullSpread, MARKET_2K, dict(K1=50, K2=45))

    def test_individual_methods(self):
        spread = BlackScholesBullSpread(**MARKET_2K)
        # Bull spread = Call1 - Call2
        assert_structure(spread, lambda s, a: getattr(s.call1, a)() - getattr(s.call2, a)())


class TestBlackScholesBearSpread:
    def test_init(self):
        # Bear spread requires K1 > K2
        assert_rejects(BlackScholesBearSpread, {**MARKET_2K, "K1": 50.0, "K2": 40.0}, dict(K1=45, K2=50))

    def test_individual_methods(self):
        spread = BlackScholesBearSpread(**{**MARKET_2K, "K1": 50.0, "K2": 40.0})
        # Bear spread = Put1 - Put2
        assert_structure(spread, lambda s, a: getattr(s.put1, a)() - getattr(s.put2, a)())


@pytest.mark.parametrize("cls", [BlackScholesCalendarCallSpread, BlackScholesCalendarPutSpread])
def test_calendar_requires_t1_gt_t2(cls):
    assert_rejects(cls, MARKET_CAL, dict(T1=1.0, T2=1.5))


class TestBlackScholesCalendarCallSpread:
    def test_individual_methods(self):
        spread = BlackScholesCalendarCallSpread(**MARKET_CAL)
        # Calendar Call Spread = Call1 - Call2
        assert_structure(spread, lambda s, a: getattr(s.call1, a)() - getattr(s.call2, a)())


class TestBlackScholesCalendarPutSpread:
    def test_individual_methods(self):
        spread = BlackScholesCalendarPutSpread(**MARKET_CAL)
        # Calendar Put Spread = Put1 - Put2
        assert_structure(spread, lambda s, a: getattr(s.put1, a)() - getattr(s.put2, a)())
