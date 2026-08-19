import pytest

from blackscholes import BlackScholesStrangleLong, BlackScholesStrangleShort

from tests.helpers import MARKET_2K, assert_rejects, assert_structure


@pytest.mark.parametrize("cls", [BlackScholesStrangleLong, BlackScholesStrangleShort])
def test_init_requires_k1_lt_k2(cls):
    assert_rejects(cls, MARKET_2K, dict(K1=50, K2=45))


@pytest.mark.parametrize(
    "cls, combo",
    [
        (BlackScholesStrangleLong, lambda s, a: getattr(s.put1, a)() + getattr(s.call1, a)()),
        (BlackScholesStrangleShort, lambda s, a: -getattr(s.put1, a)() - getattr(s.call1, a)()),
    ],
    ids=["long = put + call", "short = -put - call"],
)
def test_strangle_legs(cls, combo):
    assert_structure(cls(**MARKET_2K), combo)
