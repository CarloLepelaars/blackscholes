import pytest

from blackscholes import BlackScholesBearSpread, BlackScholesBullSpread, BlackScholesCalendarCallSpread, BlackScholesCalendarPutSpread

from tests.helpers import MARKET_2K, MARKET_CAL, assert_rejects, assert_structure

BEAR = {**MARKET_2K, "K1": 50.0, "K2": 40.0}


@pytest.mark.parametrize(
    "cls, valid, bad",
    [
        (BlackScholesBullSpread, MARKET_2K, dict(K1=50, K2=45)),
        (BlackScholesBearSpread, BEAR, dict(K1=45, K2=50)),
        (BlackScholesCalendarCallSpread, MARKET_CAL, dict(T1=1.0, T2=1.5)),
        (BlackScholesCalendarPutSpread, MARKET_CAL, dict(T1=1.0, T2=1.5)),
    ],
    ids=["bull K1<K2", "bear K1>K2", "calendar call T1>T2", "calendar put T1>T2"],
)
def test_spread_init(cls, valid, bad):
    assert_rejects(cls, valid, bad)


@pytest.mark.parametrize(
    "cls, kwargs, combo",
    [
        (BlackScholesBullSpread, MARKET_2K, lambda s, a: getattr(s.call1, a)() - getattr(s.call2, a)()),
        (BlackScholesBearSpread, BEAR, lambda s, a: getattr(s.put1, a)() - getattr(s.put2, a)()),
        (BlackScholesCalendarCallSpread, MARKET_CAL, lambda s, a: getattr(s.call1, a)() - getattr(s.call2, a)()),
        (BlackScholesCalendarPutSpread, MARKET_CAL, lambda s, a: getattr(s.put1, a)() - getattr(s.put2, a)()),
    ],
    ids=["bull = call1-call2", "bear = put1-put2", "cal call = call1-call2", "cal put = put1-put2"],
)
def test_spread_legs(cls, kwargs, combo):
    assert_structure(cls(**kwargs), combo)
