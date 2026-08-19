import pytest

from blackscholes import BlackScholesIronCondorLong, BlackScholesIronCondorShort

from tests.helpers import MARKET_IC, assert_rejects, assert_structure

_BAD = (dict(K1=60, K2=50, K3=40, K4=30), dict(K1=41, K2=40, K3=50, K4=60), dict(K1=20, K2=25, K3=45, K4=61), dict(K1=20, K2=26, K3=45, K4=60))


@pytest.mark.parametrize("cls", [BlackScholesIronCondorLong, BlackScholesIronCondorShort])
def test_init_requires_ordered_symmetric_strikes(cls):
    assert_rejects(cls, MARKET_IC, *_BAD)


@pytest.mark.parametrize(
    "cls, combo",
    [
        (BlackScholesIronCondorLong, lambda s, a: -getattr(s.put1, a)() + getattr(s.put2, a)() + getattr(s.call1, a)() - getattr(s.call2, a)()),
        (BlackScholesIronCondorShort, lambda s, a: getattr(s.put1, a)() - getattr(s.put2, a)() - getattr(s.call1, a)() + getattr(s.call2, a)()),
    ],
    ids=["long = -P1+P2+C1-C2", "short = P1-P2-C1+C2"],
)
def test_iron_condor_legs(cls, combo):
    assert_structure(cls(**MARKET_IC), combo)
