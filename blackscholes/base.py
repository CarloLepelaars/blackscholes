from abc import ABC, abstractmethod

import numpy as np
from scipy.stats import norm


class BlackScholesBase(ABC):
    """
    Base functionality to calculate (European) prices
    and Greeks with the Black-Scholes-Merton formula
    (without dividends).

    :param S: Price of underlying asset
    :param K: Strike price
    :param T: Time till expiration in years (1/12 indicates 1 month)
    :param r: Risk-free interest rate (0.05 indicates 5%)
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%)
    """

    def __init__(self, S: float, K: float, T: float, r: float, sigma: float):
        # Some parameters must be positive
        for param in [S, K, T, sigma]:
            assert (
                param >= 0.0
            ), f"Some parameters cannot be negative. Got '{param}' as an argument."
        self.S, self.K, self.T, self.r, self.sigma = S, K, T, r, sigma

    @abstractmethod
    def price(self) -> float:
        """Price for option."""
        ...

    @abstractmethod
    def in_the_money(self) -> float:
        """Naive probability that option will be in the money at maturity."""
        ...

    @abstractmethod
    def get_all_greeks(self) -> dict:
        """Retrieve all Greeks implemented as a dictionary."""
        ...

    def gamma(self) -> float:
        """
        Rate of change in delta with respect to the underlying stock price (2nd derivative).
        NOTE: Gamma is the same for calls and puts.
        """
        return norm.pdf(self._d1) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self) -> float:
        """
        Rate of change in option price with respect to the volatility of the asset.

        NOTE: Vega is the same for calls and puts.
        """
        return self.S * norm.pdf(self._d1) * np.sqrt(self.T)

    @property
    def _d1(self) -> float:
        """1st probability factor that acts as a multiplication factor for stock prices."""
        return (1 / (self.sigma * np.sqrt(self.T))) * (
            np.log(self.S / self.K) + (self.r + self.sigma**2 / 2) * self.T
        )

    @property
    def _d2(self) -> float:
        """2nd probability parameter that acts as a multiplication factor for discounting."""
        return self._d1 - self.sigma * np.sqrt(self.T)
