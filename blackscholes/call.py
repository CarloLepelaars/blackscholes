import numpy as np
from scipy.stats import norm

from .base import BlackScholesBase


class BlackScholesCall(BlackScholesBase):
    """
    Class to calculate (European) call option prices
    and Greeks with the Black-Scholes-Merton formula
    (without dividends).

    :param S: Price of underlying asset
    :param K: Strike price
    :param T: Time till expiration in years (1/12 indicates 1 month)
    :param r: Risk-free interest rate (0.05 indicates 5%)
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%)
    """

    def __init__(self, S: float, K: float, T: float, r: float, sigma: float):
        super().__init__(S=S, K=K, T=T, r=r, sigma=sigma)

    def price(self):
        """Price of a call option."""
        return norm.cdf(self._d1) * self.S - norm.cdf(self._d2) * self.K * np.exp(
            -self.r * self.T
        )

    def delta(self) -> float:
        """Rate of change in option price
        with respect to the asset price (1st derivative)."""
        return norm.cdf(self._d1)

    def rho(self) -> float:
        """Rate of change in option price
        with respect to the risk-free rate.
        """
        return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self._d2)

    def get_all_greeks(self) -> dict:
        # TODO Implement after implementing all individual Greeks
        return {}

    def in_the_money(self):
        """Naive Probability that call option will be in the money at maturity."""
        return norm.cdf(self._d2)
