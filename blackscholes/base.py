from abc import ABC, abstractmethod
from math import erf, exp, log, pi, sqrt
from typing import Dict


class BlackScholesBase(ABC):
    """
    Base functionality to calculate (European) prices
    and Greeks with the Black-Scholes-Merton formula
    (without dividends).

    :param S: Price of underlying asset \n
    :param K: Strike price \n
    :param T: Time till expiration in years (1/12 indicates 1 month) \n
    :param r: Risk-free interest rate (0.05 indicates 5%) \n
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%) \n
    :param q: Annual dividend yield (0.05 indicates 5% yield)
    """

    def __init__(self, S: float, K: float, T: float, r: float, sigma: float, q: float):
        # Some parameters must be positive
        for param in [S, K, T, sigma, q]:
            assert (
                param >= 0.0
            ), f"Some parameters cannot be negative. Got '{param}' as an argument."
        self.S, self.K, self.T, self.r, self.sigma, self.q = S, K, T, r, sigma, q

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
        return (
            exp(-self.q * self.T)
            * self._pdf(self._d1)
            / (self.S * self.sigma * sqrt(self.T))
        )

    def dual_gamma(self) -> float:
        return (
            exp(-self.r * self.T)
            * self._pdf(self._d2)
            / (self.K * self.sigma * sqrt(self.T))
        )

    def vega(self) -> float:
        """
        Rate of change in option price with respect to the volatility of the asset.

        NOTE: Vega is the same for calls and puts.
        """
        return self.S * self._pdf(self._d1) * sqrt(self.T)

    @abstractmethod
    def theta(self) -> float:
        """
        Rate of change in option price
        with respect to time (i.e. time decay).
        """
        ...

    @abstractmethod
    def epsilon(self) -> float:
        """Change in option price with respect to underlying dividend yield. \n
        Also known as psi."""
        ...

    @abstractmethod
    def rho(self) -> float:
        """Rate of change in option price
        with respect to the risk-free rate.
        """
        ...

    def lambda_greek(self) -> float:
        """Percentage change in option value per %
        change in asset price. Also called gearing.
        """
        return self.delta() * self.S / self.price()

    def vanna(self) -> float:
        """Sensitivity of delta with respect to change in vol."""
        return -self._pdf(self._d1) * self._d2 / self.sigma

    @abstractmethod
    def charm(self) -> float:
        """Rate of change of delta over time (also known as delta decay)."""
        ...

    def vomma(self) -> float:
        """2nd order sensitivity to vol."""
        return self.vega() * self._d1 * self._d2 / self.sigma

    def veta(self) -> float:
        """Rate of change in `vega` with respect to time."""
        return (
            -self.S
            * exp(-self.q * self.T)
            * self._pdf(self._d1)
            * sqrt(self.T)
            * (
                self.q
                + (self.r - self.q) * self._d1 / (self.sigma * sqrt(self.T))
                - (1 + self._d1 * self._d2) / (2 * self.T)
            )
        )

    def phi(self) -> float:
        sigma2 = self.sigma**2
        exp_factor = (
            -1
            / (2 * sigma2 * self.T)
            * (log(self.K / self.S) - ((self.r - self.q) - 0.5 * sigma2) * self.T) ** 2
        )
        return (
            exp(-self.r * self.T)
            * (1 / self.K)
            * (1 / sqrt(2 * pi * sigma2 * self.T))
            * exp(exp_factor)
        )

    def speed(self) -> float:
        return -self.gamma() / self.S * (self._d1 / (self.sigma * sqrt(self.T)) + 1)

    def zomma(self) -> float:
        """Rate of change of gamma with respect to changes in vol."""
        return self.gamma() * ((self._d1 * self._d2 - 1) / self.sigma)

    def color(self) -> float:
        """Rate of change of gamma over time."""
        return (
            -exp(-self.q * self.T)
            * self._pdf(self._d1)
            / (2 * self.S * self.T * self.sigma * sqrt(self.T))
            * (
                2 * self.q * self.T
                + 1
                + (
                    2 * (self.r - self.q) * self.T
                    - self._d2 * self.sigma * sqrt(self.T)
                )
                / (self.sigma * sqrt(self.T))
                * self._d1
            )
        )

    def ultima(self) -> float:
        """Sensitivity of vomma with respect to change in vol.
        3rd order derivative of option value to vol.
        """
        d1d2 = self._d1 * self._d2
        return (
            -self.vega()
            / self.sigma**2
            * (d1d2 * (1 - d1d2) + self._d1**2 + self._d2**2)
        )

    def get_core_greeks(self) -> Dict[str, float]:
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

    def get_itm_proxies(self) -> Dict[str, float]:
        """Get multiple ways of calculating probability
        of option being in the money.
        """
        return {"naive_itm": self.in_the_money(), "dual_delta": self.dual_delta()}

    def get_all_greeks(self) -> Dict[str, float]:
        """Retrieve all Greeks implemented as a dictionary."""
        return {
            "delta": self.delta(),
            "gamma": self.gamma(),
            "vega": self.vega(),
            "theta": self.theta(),
            "epsilon": self.epsilon(),
            "rho": self.rho(),
            "lambda": self.lambda_greek(),
            "vanna": self.vanna(),
            "charm": self.charm(),
            "vomma": self.vomma(),
            "veta": self.veta(),
            "phi": self.phi(),
            "speed": self.speed(),
            "zomma": self.zomma(),
            "color": self.color(),
            "ultima": self.ultima(),
            "dual_delta": self.dual_delta(),
            "dual_gamma": self.dual_gamma(),
        }

    @property
    def _d1(self) -> float:
        """1st probability factor that acts as a multiplication factor for stock prices."""
        return (1 / (self.sigma * sqrt(self.T))) * (
            log(self.S / self.K) + (self.r + self.sigma**2 / 2) * self.T
        )

    @property
    def _d2(self) -> float:
        """2nd probability parameter that acts as a multiplication factor for discounting."""
        return self._d1 - self.sigma * sqrt(self.T)

    @staticmethod
    def _pdf(x: float) -> float:
        """PDF of standard normal distribution."""
        return exp(-(x**2) / 2) / sqrt(2 * pi)

    @staticmethod
    def _cdf(x):
        """CDF of standard normal distribution."""
        return (1.0 + erf(x / sqrt(2.0))) / 2.0
