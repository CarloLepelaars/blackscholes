import pytest

from blackscholes import BlackScholesIronButterflyLong, BlackScholesIronButterflyShort

# Test parameters
test_S = 25.0  # Asset price of 30
test_K1 = 20.0  # Strike price of 20
test_K2 = 25.0  # Strike price of 25
test_K3 = 30.0  # Strike price of 30
test_T = 1.0  # 1 year to maturity
test_r = 0.0025  # 0.25% risk-free rate
test_sigma = 0.15  # 15% vol


class TestBlackScholesIronButterflyLong:
    def test_init(self):
        # Assert K1 < K2 < K3
        with pytest.raises(AssertionError):
            BlackScholesIronButterflyLong(
                S=test_S,
                K1=60,
                K2=50,
                K3=60,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
        with pytest.raises(AssertionError):
            BlackScholesIronButterflyLong(
                S=test_S,
                K1=40,
                K2=40,
                K3=50,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
        # Assert equidistance between strike prices
        with pytest.raises(AssertionError):
            BlackScholesIronButterflyLong(
                S=test_S,
                K1=19,
                K2=25,
                K3=35,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
        with pytest.raises(AssertionError):
            BlackScholesIronButterflyLong(
                S=test_S,
                K1=20,
                K2=25,
                K3=36,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
        with pytest.raises(AssertionError):
            BlackScholesIronButterflyLong(
                S=test_S,
                K1=19,
                K2=25,
                K3=30,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )

    def test_individual_methods(self):
        iron_butterfly = BlackScholesIronButterflyLong(
            test_S, test_K1, test_K2, test_K3, test_T, test_r, test_sigma
        )
        test_methods = list(iron_butterfly.call1.get_all_greeks().keys()) + [
            "price",
        ]
        # Long iron butterfly = -Put1 + Put2 + Call1 - Call2
        for attr in test_methods:
            assert (
                getattr(iron_butterfly, attr)()
                == -getattr(iron_butterfly.put1, attr)()
                + getattr(iron_butterfly.put2, attr)()
                + getattr(iron_butterfly.call1, attr)()
                - getattr(iron_butterfly.call2, attr)()
            )


class TestBlackScholesIronButterflyShort:
    def test_init(self):
        # Assert K1 < K2 < K3
        with pytest.raises(AssertionError):
            BlackScholesIronButterflyShort(
                S=test_S,
                K1=60,
                K2=50,
                K3=60,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
        with pytest.raises(AssertionError):
            BlackScholesIronButterflyShort(
                S=test_S,
                K1=40,
                K2=40,
                K3=50,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
        # Assert equidistance between strike prices
        with pytest.raises(AssertionError):
            BlackScholesIronButterflyShort(
                S=test_S,
                K1=19,
                K2=25,
                K3=35,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
        with pytest.raises(AssertionError):
            BlackScholesIronButterflyShort(
                S=test_S,
                K1=20,
                K2=25,
                K3=36,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
        with pytest.raises(AssertionError):
            BlackScholesIronButterflyShort(
                S=test_S,
                K1=19,
                K2=25,
                K3=30,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )

    def test_individual_methods(self):
        iron_butterfly = BlackScholesIronButterflyShort(
            test_S, test_K1, test_K2, test_K3, test_T, test_r, test_sigma
        )
        test_methods = list(iron_butterfly.call1.get_all_greeks().keys()) + [
            "price",
        ]
        # Short iron butterfly = Put1 - Put2 - Call1 + Call2
        for attr in test_methods:
            assert (
                getattr(iron_butterfly, attr)()
                == getattr(iron_butterfly.put1, attr)()
                - getattr(iron_butterfly.put2, attr)()
                - getattr(iron_butterfly.call1, attr)()
                + getattr(iron_butterfly.call2, attr)()
            )
