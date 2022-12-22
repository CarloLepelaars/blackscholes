from typing import Callable

from blackscholes.base import BlackScholesBaseCompound
from blackscholes import BlackScholesCall, BlackScholesPut


class BlackScholesIronCondor(BlackScholesBaseCompound):
    """
    Create iron condor option structure.

    :param S: Price of underlying asset \n
    :param K1: Strike price for 1st option \n
    :param K2: Strike price for 2nd option \n
    :param K3: Strike price for 3rd option \n
    :param K4: Strike price for 3rd option \n
    It must hold that K1 < K2 < K3 < K4. \n
    Additionally, it must hold that K4 - K3 = K2 - K1 \n
    :param T: Time till expiration in years (1/12 indicates 1 month) \n
    :param r: Risk-free interest rate (0.05 indicates 5%) \n
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%) \n
    :param q: Annual dividend yield (0.05 indicates 5% yield)
    :param type: 'long' or 'short' \n
    - Long iron condor -> Put(K1) - Put(K2) - Call(K3) + Call(K4)
    - Short iron condor -> -Put(K1) + Put(K2) + Call(K3) - Call(K4)
    """

    def __init__(
        self,
        S: float,
        K1: float,
        K2: float,
        K3: float,
        K4: float,
        T: float,
        r: float,
        sigma: float,
        q: float = 0.0,
        type: str = "long",
    ):
        assert (
            K1 < K2 < K3 < K4
        ), f"""It must hold that K1 < K2 < K3 < K4.
        Got {K1}, {K2}, {K3} and {K4}.
        """
        assert (
            K4 - K3 == K2 - K1
        ), f"""Strike price must be symmetric, so K4 - K3 = K2 - K1.
        Got {K2}-{K1} != {K3}-{K2}.
        """
        self.put1 = BlackScholesPut(S=S, K=K1, T=T, r=r, sigma=sigma, q=q)
        self.put2 = BlackScholesPut(S=S, K=K2, T=T, r=r, sigma=sigma, q=q)
        self.call1 = BlackScholesCall(S=S, K=K3, T=T, r=r, sigma=sigma, q=q)
        self.call2 = BlackScholesCall(S=S, K=K4, T=T, r=r, sigma=sigma, q=q)
        super().__init__(option=self.call1, type=type)

    def _compound_func(self, str_method: str) -> Callable:
        """
        Create compound callable given string method. \n
        :param str_method: String pointing to method. \n
        Method should be available in the call and put. \n
        :return lambda function that executes compound function.
        """
        put_attr1 = getattr(self.put1, str_method)()
        put_attr2 = getattr(self.put2, str_method)()
        call_attr1 = getattr(self.call1, str_method)()
        call_attr2 = getattr(self.call2, str_method)()
        # Long iron condor
        if self.type == "long":
            func = lambda: put_attr1 - put_attr2 - call_attr1 + call_attr2  # noqa
        # Short iron condor
        else:
            func = lambda: -put_attr1 + put_attr2 + call_attr1 - call_attr2  # noqa
        return func
