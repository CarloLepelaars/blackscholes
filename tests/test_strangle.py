import pytest

from blackscholes import BlackScholesStrangleLong, BlackScholesStrangleShort

from tests.helpers import MARKET_2K, assert_rejects, assert_structure


@pytest.mark.parametrize("cls", [BlackScholesStrangleLong, BlackScholesStrangleShort])
def test_init_requires_k1_lt_k2(cls):
    assert_rejects(cls, MARKET_2K, dict(K1=50, K2=45))


class TestBlackScholesStrangleLong:
    def test_individual_methods(self):
        strangle = BlackScholesStrangleLong(**MARKET_2K)
        # Long strangle = Put1 + Call1
        assert_structure(strangle, lambda s, a: getattr(s.put1, a)() + getattr(s.call1, a)())


class TestBlackScholesStrangleShort:
    def test_individual_methods(self):
        strangle = BlackScholesStrangleShort(**MARKET_2K)
        # Short strangle = -Put1 - Call1
        assert_structure(strangle, lambda s, a: -getattr(s.put1, a)() - getattr(s.call1, a)())
