import pytest

from blackscholes import BlackScholesButterflyLong, BlackScholesButterflyShort

from tests.helpers import MARKET_3K, assert_rejects, assert_structure

_BAD = (dict(K1=60, K2=50, K3=40), dict(K1=41, K2=40, K3=50), dict(K1=41, K2=50, K3=60))


@pytest.mark.parametrize("cls", [BlackScholesButterflyLong, BlackScholesButterflyShort])
def test_init_requires_symmetric_strikes(cls):
    assert_rejects(cls, MARKET_3K, *_BAD)


@pytest.mark.parametrize(
    "cls, combo",
    [
        (BlackScholesButterflyLong, lambda s, a: getattr(s.call1, a)() - 2 * getattr(s.call2, a)() + getattr(s.call3, a)()),
        (BlackScholesButterflyShort, lambda s, a: -getattr(s.put1, a)() + 2 * getattr(s.put2, a)() - getattr(s.put3, a)()),
    ],
    ids=["long = C1-2C2+C3", "short = -P1+2P2-P3"],
)
def test_butterfly_legs(cls, combo):
    assert_structure(cls(**MARKET_3K), combo)
