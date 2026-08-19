import pytest

from blackscholes import BlackScholesIronButterflyLong, BlackScholesIronButterflyShort

from tests.helpers import MARKET_IB, assert_rejects, assert_structure

_BAD_WINGS = (
    dict(K1=60, K2=50, K3=60),
    dict(K1=40, K2=40, K3=50),
    dict(K1=19, K2=25, K3=35),
    dict(K1=20, K2=25, K3=36),
    dict(K1=19, K2=25, K3=30),
)


@pytest.mark.parametrize("cls", [BlackScholesIronButterflyLong, BlackScholesIronButterflyShort])
def test_init_requires_equidistant_strikes(cls):
    assert_rejects(cls, MARKET_IB, *_BAD_WINGS)


class TestBlackScholesIronButterflyLong:
    def test_individual_methods(self):
        ib = BlackScholesIronButterflyLong(**MARKET_IB)
        # Long iron butterfly = -Put1 + Put2 + Call1 - Call2
        assert_structure(ib, lambda s, a: -getattr(s.put1, a)() + getattr(s.put2, a)() + getattr(s.call1, a)() - getattr(s.call2, a)())


class TestBlackScholesIronButterflyShort:
    def test_individual_methods(self):
        ib = BlackScholesIronButterflyShort(**MARKET_IB)
        # Short iron butterfly = Put1 - Put2 - Call1 + Call2
        assert_structure(ib, lambda s, a: getattr(s.put1, a)() - getattr(s.put2, a)() - getattr(s.call1, a)() + getattr(s.call2, a)())
