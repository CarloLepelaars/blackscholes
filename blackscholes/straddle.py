from typing import Callable

from . import BlackScholesCall, BlackScholesPut
from .base import BlackScholesBaseCompound


class BlackScholesStraddle(BlackScholesBaseCompound):
    """
    Create straddle option structure.

    :param S: Price of underlying asset \n
    :param K: Strike price \n
    :param T: Time till expiration in years (1/12 indicates 1 month) \n
    :param r: Risk-free interest rate (0.05 indicates 5%) \n
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%) \n
    :param q: Annual dividend yield (0.05 indicates 5% yield)
    :param type: 'long' or 'short' \n
    - Long Straddle -> Put(K) + Call(K)
    - Short Straddle -> -Put(K) - Call(K)
    """

    def __init__(
        self,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        q: float = 0.0,
        type: str = "long",
    ):
        self.call1 = BlackScholesCall(S=S, K=K, T=T, r=r, sigma=sigma, q=q)
        self.put1 = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma, q=q)
        super().__init__(option=self.call1, type=type)

    def _compound_func(self, str_method: str) -> Callable:
        """
        Create compound callable given string method. \n
        :param str_method: String pointing to method. \n
        Method should be available in the call and put. \n
        :return lambda function that executes compound function.
        """
        put_attr = getattr(self.put1, str_method)()
        call_attr = getattr(self.call1, str_method)()
        # Long Straddle
        if self.type == "long":
            func = lambda: put_attr + call_attr  # noqa
        # Short straddle
        else:
            func = lambda: -put_attr - call_attr  # noqa
        return func
