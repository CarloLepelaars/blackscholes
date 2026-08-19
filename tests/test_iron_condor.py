import pytest

from blackscholes import BlackScholesIronCondorLong, BlackScholesIronCondorShort

from tests.helpers import MARKET_IC, assert_rejects, assert_structure

_BAD_WINGS = (
    dict(K1=60, K2=50, K3=40, K4=30),
    dict(K1=41, K2=40, K3=50, K4=60),
    dict(K1=20, K2=25, K3=45, K4=61),
    dict(K1=20, K2=26, K3=45, K4=60),
)


@pytest.mark.parametrize("cls", [BlackScholesIronCondorLong, BlackScholesIronCondorShort])
def test_init_requires_ordered_symmetric_strikes(cls):
    assert_rejects(cls, MARKET_IC, *_BAD_WINGS)


class TestBlackScholesIronCondorLong:
    def test_individual_methods(self):
        ic = BlackScholesIronCondorLong(**MARKET_IC)
        # Long iron condor = -Put1 + Put2 + Call1 - Call2
        assert_structure(ic, lambda s, a: -getattr(s.put1, a)() + getattr(s.put2, a)() + getattr(s.call1, a)() - getattr(s.call2, a)())


class TestBlackScholesIronCondorShort:
    def test_individual_methods(self):
        ic = BlackScholesIronCondorShort(**MARKET_IC)
        # Short iron condor = Put1 - Put2 - Call1 + Call2
        assert_structure(ic, lambda s, a: getattr(s.put1, a)() - getattr(s.put2, a)() - getattr(s.call1, a)() + getattr(s.call2, a)())
