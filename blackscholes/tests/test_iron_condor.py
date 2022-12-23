import pytest

from .. import BlackScholesIronCondorLong, BlackScholesIronCondorShort

# Test parameters
test_S = 55.0  # Asset price of 55
test_K1 = 20.0  # Strike price of 20
test_K2 = 25.0  # Strike price of 25
test_K3 = 45.0  # Strike price of 45
test_K4 = 50.0  # Strike price of 50
test_T = 1.0  # 1 year to maturity
test_r = 0.0025  # 0.25% risk-free rate
test_sigma = 0.15  # 15% vol


class TestBlackScholesIronCondorLong:
    def test_init(self):
        # Assert K1 < K2 < K3 < K4
        with pytest.raises(AssertionError):
            BlackScholesIronCondorLong(
                S=test_S,
                K1=60,
                K2=50,
                K3=40,
                K4=30,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
        with pytest.raises(AssertionError):
            BlackScholesIronCondorLong(
                S=test_S,
                K1=41,
                K2=40,
                K3=50,
                K4=60,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
        # Assert K2 - K1 = K3 - K2 (symmetry)
        with pytest.raises(AssertionError):
            BlackScholesIronCondorLong(
                S=test_S,
                K1=20,
                K2=25,
                K3=45,
                K4=61,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
            BlackScholesIronCondorLong(
                S=test_S,
                K1=20,
                K2=26,
                K3=45,
                K4=60,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )

    def test_individual_methods(self):
        iron_condor = BlackScholesIronCondorLong(
            test_S, test_K1, test_K2, test_K3, test_K4, test_T, test_r, test_sigma
        )
        test_methods = list(iron_condor.call1.get_all_greeks().keys()) + [
            "price",
        ]
        # Long iron condor = Put1 - Put2 - Call1 + Call2
        for attr in test_methods:
            assert (
                getattr(iron_condor, attr)()
                == -getattr(iron_condor.put1, attr)()
                + getattr(iron_condor.put2, attr)()
                + getattr(iron_condor.call1, attr)()
                - getattr(iron_condor.call2, attr)()
            )


class TestBlackScholesIronCondorShort:
    def test_init(self):
        # Assert K1 < K2 < K3 < K4
        with pytest.raises(AssertionError):
            BlackScholesIronCondorShort(
                S=test_S,
                K1=60,
                K2=50,
                K3=40,
                K4=30,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
        with pytest.raises(AssertionError):
            BlackScholesIronCondorShort(
                S=test_S,
                K1=41,
                K2=40,
                K3=50,
                K4=60,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
        # Assert K2 - K1 = K3 - K2 (symmetry)
        with pytest.raises(AssertionError):
            BlackScholesIronCondorShort(
                S=test_S,
                K1=20,
                K2=25,
                K3=45,
                K4=61,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )
            BlackScholesIronCondorShort(
                S=test_S,
                K1=20,
                K2=26,
                K3=45,
                K4=60,
                T=test_T,
                r=test_r,
                sigma=test_sigma,
            )

    def test_individual_methods(self):
        iron_condor = BlackScholesIronCondorShort(
            test_S, test_K1, test_K2, test_K3, test_K4, test_T, test_r, test_sigma
        )
        test_methods = list(iron_condor.call1.get_all_greeks().keys()) + [
            "price",
        ]
        # Short iron condor = -Put1 + Put2 + Call1 - Call2
        for attr in test_methods:
            (
                getattr(iron_condor, attr)()
                == getattr(iron_condor.put1, attr)()
                - getattr(iron_condor.put2, attr)()
                - getattr(iron_condor.call1, attr)()
                + getattr(iron_condor.call2, attr)()
            )
