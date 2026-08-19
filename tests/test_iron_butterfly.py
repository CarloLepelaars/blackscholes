import pytest

from blackscholes import BlackScholesIronButterflyLong, BlackScholesIronButterflyShort

from tests.helpers import MARKET_IB, assert_rejects, assert_structure

_BAD = (dict(K1=60, K2=50, K3=60), dict(K1=40, K2=40, K3=50), dict(K1=19, K2=25, K3=35), dict(K1=20, K2=25, K3=36), dict(K1=19, K2=25, K3=30))


@pytest.mark.parametrize("cls", [BlackScholesIronButterflyLong, BlackScholesIronButterflyShort])
def test_init_requires_equidistant_strikes(cls):
    assert_rejects(cls, MARKET_IB, *_BAD)


@pytest.mark.parametrize(
    "cls, combo",
    [
        (BlackScholesIronButterflyLong, lambda s, a: -getattr(s.put1, a)() + getattr(s.put2, a)() + getattr(s.call1, a)() - getattr(s.call2, a)()),
        (BlackScholesIronButterflyShort, lambda s, a: getattr(s.put1, a)() - getattr(s.put2, a)() - getattr(s.call1, a)() + getattr(s.call2, a)()),
    ],
    ids=["long = -P1+P2+C1-C2", "short = P1-P2-C1+C2"],
)
def test_iron_butterfly_legs(cls, combo):
    assert_structure(cls(**MARKET_IB), combo)
