from math import exp, sqrt

from .base import Black76Base, BlackScholesBase


class BlackScholesPut(BlackScholesBase):
    """
    Class to calculate (European) call option prices
    and Greeks with the Black-Scholes-Merton formula.

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

    def price(self) -> float:
        """Fair value of a Black-Scholes put option."""
        return self._cdf(-self._d2) * self.K * exp(-self.r * self.T) - self.S * exp(
            -self.q * self.T
        ) * self._cdf(-self._d1)

    def delta(self) -> float:
        """
        Rate of change in option price
        with respect to the asset price (1st derivative).
        """
        return -exp(-self.q * self.T) * self._cdf(-self._d1)

    def dual_delta(self) -> float:
        """1st derivative in option price
        with respect to strike price.
        """
        return exp(-self.r * self.T) * self._cdf(-self._d2)

    def theta(self) -> float:
        """Rate of change in option price
        with respect to time (i.e. time decay).
        """
        return (
            (-exp(self.q * self.T) * self.S * self._pdf(self._d1) * self.sigma)
            / (2.0 * sqrt(self.T))
        ) + (
            self.r * self.K * exp(-self.r * self.T) * self._cdf(-self._d2)
            - self.q * self.S * exp(-self.q * self.T) * self._cdf(-self._d1)
        )

    def rho(self) -> float:
        """Rate of change in option price
        with respect to the risk-free rate.
        """
        return -self.K * self.T * exp(-self.r * self.T) * self._cdf(-self._d2)

    def epsilon(self) -> float:
        """Change in option price with respect to underlying dividend yield. \n
        Also known as psi."""
        return self.S * self.T * exp(-self.q * self.T) * self._cdf(-self._d1)

    def charm(self) -> float:
        """Rate of change of delta over time (also known as delta decay)."""
        return -self.q * exp(-self.q * self.T) * self._cdf(-self._d1) - exp(
            -self.q * self.T
        ) * self._pdf(self._d1) * (
            2.0 * (self.r - self.q) * self.T - self._d2 * self.sigma * sqrt(self.T)
        ) / (
            2.0 * self.T * self.sigma * sqrt(self.T)
        )

    def in_the_money(self) -> float:
        """Naive Probability that put option will be in the money at maturity."""
        return 1.0 - self._cdf(self._d2)


class Black76Put(Black76Base):
    def __init__(self, F: float, K: float, T: float, r: float, sigma: float):
        super().__init__(F=F, K=K, T=T, r=r, sigma=sigma)

    def price(self) -> float:
        """Fair value of a Black-76 put option."""
        return exp(-self.r * self.T) * (
            self.K * self._cdf(-self._d2) - self.F * self._cdf(-self._d1)
        )

    def delta(self) -> float:
        """Rate of change in option price
        with respect to the underlying futures price (1st derivative).
        Proxy for probability of the option expiring in the money.
        """
        return -exp(-self.r * self.T) * self._cdf(-self._d1)

    def theta(self) -> float:
        """Rate of change in option price
        with respect to time (i.e. time decay).
        """
        return (
            -self.F
            * exp(-self.r * self.T)
            * self._pdf(self._d1)
            * self.sigma
            / (2 * sqrt(self.T))
            + self.r * self.K * exp(-self.r * self.T) * self._cdf(-self._d2)
            - self.r * self.F * exp(-self.r * self.T) * self._cdf(-self._d1)
        )

    def rho(self) -> float:
        """Rate of change in option price
        with respect to the risk-free rate.
        """
        return (
            -self.T
            * exp(-self.r * self.T)
            * (self.K * self._cdf(-self._d2) - self.F * self._cdf(-self._d1))
        )
