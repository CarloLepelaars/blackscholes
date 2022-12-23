from . import BlackScholesCall, BlackScholesPut
from .base import BlackScholesStructureBase


class BlackScholesStraddleLong(BlackScholesStructureBase):
    """
    Create long straddle option structure. \n
    - Long Straddle -> Put(K) + Call(K)

    :param S: Price of underlying asset \n
    :param K: Strike price \n
    :param T: Time till expiration in years (1/12 indicates 1 month) \n
    :param r: Risk-free interest rate (0.05 indicates 5%) \n
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%) \n
    :param q: Annual dividend yield (0.05 indicates 5% yield) \n
    """

    def __init__(
        self,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        q: float = 0.0,
    ):
        self.call1 = BlackScholesCall(S=S, K=K, T=T, r=r, sigma=sigma, q=q)
        self.put1 = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma, q=q)
        super().__init__()

    def _calc_attr(self, attribute_name: str):
        put_attr = getattr(self.put1, attribute_name)
        call_attr = getattr(self.call1, attribute_name)
        return put_attr() + call_attr()


class BlackScholesStraddleShort(BlackScholesStructureBase):
    """
    Create straddle option structure. \n
    - Short Straddle -> -Put(K) - Call(K)

    :param S: Price of underlying asset \n
    :param K: Strike price \n
    :param T: Time till expiration in years (1/12 indicates 1 month) \n
    :param r: Risk-free interest rate (0.05 indicates 5%) \n
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%) \n
    :param q: Annual dividend yield (0.05 indicates 5% yield)
    """

    def __init__(
        self,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        q: float = 0.0,
    ):
        self.call1 = BlackScholesCall(S=S, K=K, T=T, r=r, sigma=sigma, q=q)
        self.put1 = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma, q=q)
        super().__init__()

    def _calc_attr(self, attribute_name: str):
        put_attr = getattr(self.put1, attribute_name)
        call_attr = getattr(self.call1, attribute_name)
        return -put_attr() - call_attr()
