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
    def delta(self) -> float:
        """Rate of change in option price
        with respect to the asset price (1st derivative)."""
        ...

    @abstractmethod
    def dual_delta(self) -> float:
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

    def theta(self) -> float:
        """
        Rate of change in option price
        with respect to time (i.e. time decay).
        """
        ...

    def rho(self) -> float:
        """Rate of change in option price
        with respect to the risk-free rate.
        """
        ...

    def lamdba(self) -> float:
        """Percentage change in option value per %
        change in asset price. Also called gearing.
        As defined on Wikipedia:
        https://en.wikipedia.org/wiki/Greeks_(finance)#Lambda
        NOTE: Lamdba is the same for call and puts.
        """
        return self.delta() * self.S / self.price()

    def vanna(self) -> float:
        return -norm.pdf(self._d1) * self._d2 / self.sigma

    def charm(self) -> float:
        return (
            -norm.pdf(self._d1)
            * (2 * self.r * self.T - self._d2 * self.sigma * np.sqrt(self.T))
            / (2 * self.T * self.sigma * np.sqrt(self.T))
        )

    def get_core_greeks(self) -> dict:
        """
        Get the top 5 most well known Greeks.
        1. Delta
        2. Gamma
        3. Vega
        4. Theta
        5. Rho
        """
        return {
            "delta": self.delta(),
            "gamma": self.gamma(),
            "vega": self.vega(),
            "theta": self.theta(),
            "rho": self.rho(),
        }

    def get_itm_proxies(self) -> dict:
        """Get multiple ways of calculating probability
        of option being in the money.
        """
        return {"naive_itm": self.in_the_money(), "dual_delta": self.dual_delta()}

    @abstractmethod
    def get_all_greeks(self) -> dict:
        """Retrieve all Greeks implemented as a dictionary."""
        ...

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
