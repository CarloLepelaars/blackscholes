import numpy as np
from scipy.stats import norm

from .base import BlackScholesBase


class BlackScholesCall(BlackScholesBase):
    """
    Class to calculate (European) call option prices
    and Greeks with the Black-Scholes-Merton formula
    (without dividends).

    :param S: Price of underlying asset \n
    :param K: Strike price \n
    :param T: Time till expiration in years (1/12 indicates 1 month) \n
    :param r: Risk-free interest rate (0.05 indicates 5%) \n
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%) \n
    :param q: Annual dividend yield (0.05 indicates 5% yield)
    """

    def __init__(
        self, S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0
    ):
        super().__init__(S=S, K=K, T=T, r=r, sigma=sigma, q=q)

    def price(self):
        """Price of a call option."""
        return (
            self.S * np.exp(-self.q * self.T) * norm.cdf(self._d1)
            - norm.cdf(self._d2) * np.exp(-self.r * self.T) * self.K
        )

    def delta(self) -> float:
        """Rate of change in option price
        with respect to the asset price (1st derivative).
        Proxy for probability of the option expiring in the money.
        """
        return np.exp(-self.q * self.T) * norm.cdf(self._d1)

    def dual_delta(self) -> float:
        """1st derivative in option price
        with respect to strike price.
        """
        return np.exp(-self.r * self.T) * norm.cdf(self._d2)

    def theta(self):
        """Rate of change in option price
        with respect to time (i.e. time decay).
        """
        return (
            (-np.exp(-self.q * self.T) * self.S * norm.pdf(self._d1) * self.sigma)
            / (2 * np.sqrt(self.T))
            - (self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self._d2))
            + self.q * self.S * np.exp(-self.q * self.T) * norm.cdf(self._d1)
        )

    def rho(self) -> float:
        """Rate of change in option price
        with respect to the risk-free rate.
        """
        return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self._d2)

    def in_the_money(self):
        """Naive Probability that call option will be in the money at maturity."""
        return norm.cdf(self._d2)
