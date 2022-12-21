from typing import Callable, Dict

from . import BlackScholesCall, BlackScholesPut


class BlackScholesStraddle:
    """
    Create straddle option structure.

    :param S: Price of underlying asset \n
    :param K: Strike price \n
    :param T: Time till expiration in years (1/12 indicates 1 month) \n
    :param r: Risk-free interest rate (0.05 indicates 5%) \n
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%) \n
    :param q: Annual dividend yield (0.05 indicates 5% yield)
    :param type: 'long' or 'short' \n
    - Long Straddle -> Put + Call
    - Short Straddle -> -Put - Call
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
        self.call = BlackScholesCall(S=S, K=K, T=T, r=r, sigma=sigma, q=q)
        self.put = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma, q=q)

        self.type = type
        assert self.type in [
            "long",
            "short",
        ], f"Type can only be 'long' or 'short'. Got {self.type}"
        # Initialize compound methods
        self.methods = list(self.call.get_all_greeks().keys()) + [
            "price",
            "in_the_money",
        ]
        for str_method in self.methods:
            setattr(self, str_method, self._compound_func(str_method))

    def get_core_greeks(self) -> Dict[str, float]:
        """
        Get the top 5 most well known Greeks for the straddle.
        1. Delta
        2. Gamma
        3. Vega
        4. Theta
        5. Rho
        """
        return self.__compound_dict("get_core_greeks")

    def get_all_greeks(self) -> Dict[str, float]:
        """Retrieve all Greeks for the straddle
        implemented as a dictionary."""
        return self.__compound_dict("get_all_greeks")

    def get_itm_proxies(self) -> Dict[str, float]:
        """Get multiple ways of calculating probability
        of straddle being in the money.
        """
        return self.__compound_dict("get_itm_proxies")

    def _compound_func(self, str_method: str) -> Callable:
        """
        Create compound callable given string method. \n
        :param str_method: String pointing to method. \n
        Method should be available in the call and put. \n
        :return lambda function that executes compound function.
        """
        put_attr = getattr(self.put, str_method)()
        call_attr = getattr(self.call, str_method)()
        # Long Straddle
        if self.type == "long":
            func = lambda: put_attr + call_attr  # noqa
        # Short straddle
        else:
            func = lambda: -put_attr - call_attr  # noqa
        return func

    def __compound_dict(self, str_method: str) -> Dict[str, float]:
        """
        Merge two dictionaries to create compounds for the straddle.

        :param str_method: String pointing to method. \n
        Method should be available in the call and put. \n
        :return: Dictionary compounding values from call and put.
        """
        return {
            func: self._compound_func(func)()
            for func in getattr(self.call, str_method)().keys()
        }
