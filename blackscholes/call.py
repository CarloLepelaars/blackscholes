import numpy as np
from scipy.stats import norm

from base import BlackScholesBase


class BlackScholesCall(BlackScholesBase):
    def price(self, S, K, T, r, sigma):
        """ Price of a call option """
        d1 = self._d1(S, K, T, r, sigma)
        d2 = self._d2(S, K, T, r, sigma)
        return norm.cdf(d1) * S - norm.cdf(d2) * K * np.exp(-r * T)

    def in_the_money(self, S, K, T, r, sigma):
        """
        Calculate probability that option will be in the money at
        maturity.
        """
        d2 = self._d2(S, K, T, r, sigma)
        return norm.cdf(d2)