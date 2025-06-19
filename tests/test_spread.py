import pytest

from blackscholes import (BlackScholesBullSpread, BlackScholesBearSpread, 
                BlackScholesCalendarCallSpread, BlackScholesCalendarPutSpread,
                Black76BullSpread, Black76BearSpread, 
                Black76CalendarCallSpread, Black76CalendarPutSpread)

# Test parameters
test_S = 55.0  # Asset price of 55
test_F = 50.0  # Futures price of 50
test_K1 = 40.0  # Strike price of 40
test_K2 = 50.0  # Strike price of 50
test_T = 1.0  # 1 year to maturity
test_T2 = 0.5  # 6 months to maturity
test_r = 0.0025  # 0.25% risk-free rate
test_sigma = 0.15  # 15% vol


class TestBlackScholesBullSpread:
    def test_init(self):
        # Assert K1 < K2
        with pytest.raises(AssertionError):
            BlackScholesBullSpread(
                S=test_S, K1=50, K2=45, T=test_T, r=test_r, sigma=test_sigma
            )

    def test_individual_methods(self):
        spread = BlackScholesBullSpread(
            test_S, test_K1, test_K2, test_T, test_r, test_sigma
        )
        test_methods = list(spread.call1.get_all_greeks().keys()) + [
            "price",
        ]
        # Bull spread = Call1 - Call2
        for attr in test_methods:
            assert (
                getattr(spread, attr)()
                == getattr(spread.call1, attr)() - getattr(spread.call2, attr)()
            )


class TestBlackScholesBearSpread:
    def test_init(self):
        # Assert K1 > K2
        with pytest.raises(AssertionError):
            BlackScholesBearSpread(
                S=test_S, K1=45, K2=50, T=test_T, r=test_r, sigma=test_sigma
            )

    def test_individual_methods(self):
        spread = BlackScholesBearSpread(
            test_S, test_K2, test_K1, test_T, test_r, test_sigma
        )
        test_methods = list(spread.put1.get_all_greeks().keys()) + [
            "price",
        ]
        # Bear spread = Put1 - Put2
        for attr in test_methods:
            assert (
                getattr(spread, attr)()
                == getattr(spread.put1, attr)() - getattr(spread.put2, attr)()
            )

class TestBlackScholesCalendarCallSpread:
    def test_init(self):
        # Assert T1 > T2
        with pytest.raises(AssertionError):
            BlackScholesCalendarCallSpread(
                S=test_S, K1=test_K1, K2=test_K2, T1=1., T2=1.5, r=test_r, sigma=test_sigma
            )

    def test_individual_methods(self):
        spread = BlackScholesCalendarCallSpread(
            test_S, test_K1, test_K2, test_T, test_T2, test_r, test_sigma
        )
        test_methods = list(spread.call1.get_all_greeks().keys()) + [
            "price",
        ]
        # Calendar Call Spread = Call1 - Call2
        for attr in test_methods:
            assert (
                getattr(spread, attr)()
                == getattr(spread.call1, attr)() - getattr(spread.call2, attr)()
            )

class TestBlackScholesCalendarPutSpread:
    def test_init(self):
        # Assert T1 > T2
        with pytest.raises(AssertionError):
            BlackScholesCalendarPutSpread(
                S=test_S, K1=test_K1, K2=test_K2, T1=1., T2=1.5, r=test_r, sigma=test_sigma
            )

    def test_individual_methods(self):
        spread = BlackScholesCalendarPutSpread(
            test_S, test_K1, test_K2, test_T, test_T2, test_r, test_sigma
        )
        test_methods = list(spread.put1.get_all_greeks().keys()) + [
            "price",
        ]
        # Calendar Put Spread = Put1 - Put2
        for attr in test_methods:
            assert (
                getattr(spread, attr)()
                == getattr(spread.put1, attr)() - getattr(spread.put2, attr)()
            )

class TestBlack76BullSpread:
    def test_init(self):
        # Assert K1 < K2
        with pytest.raises(AssertionError):
            Black76BullSpread(
                F=test_F, K1=50, K2=45, T=test_T, r=test_r, sigma=test_sigma
            )

    def test_individual_methods(self):
        spread = Black76BullSpread(
            test_F, test_K1, test_K2, test_T, test_r, test_sigma
        )
        test_methods = list(spread.call1.get_all_greeks().keys()) + [
            "price",
        ]
        # Bull spread = Call1 - Call2
        for attr in test_methods:
            assert (
                getattr(spread, attr)()
                == getattr(spread.call1, attr)() - getattr(spread.call2, attr)()
            )


class TestBlack76BearSpread:
    def test_init(self):
        # Assert K1 > K2
        with pytest.raises(AssertionError):
            Black76BearSpread(
                F=test_F, K1=45, K2=50, T=test_T, r=test_r, sigma=test_sigma
            )

    def test_individual_methods(self):
        spread = Black76BearSpread(
            test_F, test_K2, test_K1, test_T, test_r, test_sigma
        )
        test_methods = list(spread.put1.get_all_greeks().keys()) + [
            "price",
        ]
        # Bear spread = Put1 - Put2
        for attr in test_methods:
            assert (
                getattr(spread, attr)()
                == getattr(spread.put1, attr)() - getattr(spread.put2, attr)()
            )

class TestBlack76CalendarCallSpread:
    def test_init(self):
        # Assert T1 > T2
        with pytest.raises(AssertionError):
            Black76CalendarCallSpread(
                F=test_F, K1=test_K1, K2=test_K2, T1=1., T2=1.5, r=test_r, sigma=test_sigma
            )

    def test_individual_methods(self):
        spread = Black76CalendarCallSpread(
            test_F, test_K1, test_K2, test_T, test_T2, test_r, test_sigma
        )
        test_methods = list(spread.call1.get_all_greeks().keys()) + [
            "price",
        ]
        # Calendar Call Spread = Call1 - Call2
        for attr in test_methods:
            assert (
                getattr(spread, attr)()
                == getattr(spread.call1, attr)() - getattr(spread.call2, attr)()
            )

class TestBlack76CalendarPutSpread:
    def test_init(self):
        # Assert T1 > T2
        with pytest.raises(AssertionError):
            Black76CalendarPutSpread(
                F=test_F, K1=test_K1, K2=test_K2, T1=1., T2=1.5, r=test_r, sigma=test_sigma
            )

    def test_individual_methods(self):
        spread = Black76CalendarPutSpread(
            test_F, test_K1, test_K2, test_T, test_T2, test_r, test_sigma
        )
        test_methods = list(spread.put1.get_all_greeks().keys()) + [
            "price",
        ]
        # Calendar Put Spread = Put1 - Put2
        for attr in test_methods:
            assert (
                getattr(spread, attr)()
                == getattr(spread.put1, attr)() - getattr(spread.put2, attr)()
            )
