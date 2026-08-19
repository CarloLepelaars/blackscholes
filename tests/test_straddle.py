import pytest

from blackscholes import BlackScholesStraddleLong, BlackScholesStraddleShort

from tests.helpers import MARKET, assert_structure


@pytest.mark.parametrize(
    "cls, combo",
    [
        (BlackScholesStraddleLong, lambda s, a: getattr(s.put1, a)() + getattr(s.call1, a)()),
        (BlackScholesStraddleShort, lambda s, a: -getattr(s.put1, a)() - getattr(s.call1, a)()),
    ],
    ids=["long = put + call", "short = -put - call"],
)
def test_straddle_legs(cls, combo):
    assert_structure(cls(**MARKET), combo)
