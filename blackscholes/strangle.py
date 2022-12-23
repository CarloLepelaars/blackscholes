from . import BlackScholesCall, BlackScholesPut
from .base import BlackScholesStructureBase


class BlackScholesStrangleLong(BlackScholesStructureBase):
    """
    Create long strangle option structure. \n
    - Long strangle -> Put(K1) + Call(K2)

    :param S: Price of underlying asset \n
    :param K1: Strike price for put \n
    :param K2: Strike price for call \n
    It must hold that K1 < K2. \n
    :param T: Time till expiration in years (1/12 indicates 1 month) \n
    :param r: Risk-free interest rate (0.05 indicates 5%) \n
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%) \n
    :param q: Annual dividend yield (0.05 indicates 5% yield) \n
    """

    def __init__(
        self,
        S: float,
        K1: float,
        K2: float,
        T: float,
        r: float,
        sigma: float,
        q: float = 0.0,
    ):
        assert (
            K1 < K2
        ), f"""1st strike price should be smaller than 2nd.
        Got K1={K1}, which is not smaller than K2={K2}.
        """
        self.put1 = BlackScholesPut(S=S, K=K1, T=T, r=r, sigma=sigma, q=q)
        self.call1 = BlackScholesCall(S=S, K=K2, T=T, r=r, sigma=sigma, q=q)
        super().__init__()

    def _calc_attr(self, attribute_name: str):
        put_attr = getattr(self.put1, attribute_name)
        call_attr = getattr(self.call1, attribute_name)
        return put_attr() + call_attr()


class BlackScholesStrangleShort(BlackScholesStructureBase):
    """
    Create short strangle option structure. \n
    - Short strangle -> -Put(K1) - Call(K2)

    :param S: Price of underlying asset \n
    :param K1: Strike price for put \n
    :param K2: Strike price for call \n
    It must hold that K1 < K2. \n
    :param T: Time till expiration in years (1/12 indicates 1 month) \n
    :param r: Risk-free interest rate (0.05 indicates 5%) \n
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%) \n
    :param q: Annual dividend yield (0.05 indicates 5% yield)
    """

    def __init__(
        self,
        S: float,
        K1: float,
        K2: float,
        T: float,
        r: float,
        sigma: float,
        q: float = 0.0,
    ):
        assert (
            K1 < K2
        ), f"""1st strike price should be smaller than 2nd.
        Got K1={K1}, which is not smaller than K2={K2}.
        """
        self.put1 = BlackScholesPut(S=S, K=K1, T=T, r=r, sigma=sigma, q=q)
        self.call1 = BlackScholesCall(S=S, K=K2, T=T, r=r, sigma=sigma, q=q)
        super().__init__()

    def _calc_attr(self, attribute_name: str):
        put_attr = getattr(self.put1, attribute_name)
        call_attr = getattr(self.call1, attribute_name)
        return -put_attr() - call_attr()
