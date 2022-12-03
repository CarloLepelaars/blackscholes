import numpy as np
from abc import ABC, abstractmethod


class BlackScholesBase(ABC):
    """
    Class to calculate (European) call and put option prices through the Black-Scholes formula
    without dividends

    :param S: Price of underlying stock
    :param K: Strike price
    :param T: Time till expiration (in years)
    :param r: Risk-free interest rate (0.05 indicates 5%)
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%)
    """
    @staticmethod
    def _d1(S, K, T, r, sigma):
        return (1 / (sigma * np.sqrt(T))) * (np.log(S / K) + (r + sigma ** 2 / 2) * T)

    def _d2(self, S, K, T, r, sigma):
        return self._d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

    @abstractmethod
    def price(self, S, K, T, r, sigma):
        """ Price for option. """
        ...

    @abstractmethod
    def in_the_money(self, S, K, T, r, sigma):
        """
        Calculate probability that option will be in the money at maturity.
        """
        ...
