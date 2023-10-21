from . import BlackScholesCall, BlackScholesPut
from .base import BlackScholesStructureBase


class BlackScholesBullSpread(BlackScholesStructureBase):
    """
    Create bull spread option structure. \n
    - Bull Spread -> Call(K1) - Call(K2)

    :param S: Price of underlying asset \n
    :param K1: Strike price for 1st call \n
    :param K2: Strike price for 2nd call \n
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
        self.call1 = BlackScholesCall(S=S, K=K1, T=T, r=r, sigma=sigma, q=q)
        self.call2 = BlackScholesCall(S=S, K=K2, T=T, r=r, sigma=sigma, q=q)
        super().__init__()

    def _calc_attr(self, attribute_name: str) -> float:
        """
        Combines attributes from two call options into a bull spread. \n
        All greeks and prices are combined in the same way.

        :param attribute_name: String name of option attribute
        pointing to a method that can be called on
        BlackScholesCall and BlackScholesPut.

        :return: Combined value according to bull spread.
        """
        call1_attr = getattr(self.call1, attribute_name)
        call2_attr = getattr(self.call2, attribute_name)
        return call1_attr() - call2_attr()


class BlackScholesBearSpread(BlackScholesStructureBase):
    """
    Create bear spread option structure. \n
    - Bear Spread -> Put(K1) - Put(K2)

    :param S: Price of underlying asset \n
    :param K1: Strike price for 1st put \n
    :param K2: Strike price for 2nd put \n
    It must hold that K1 > K2. \n
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
            K1 > K2
        ), f"""1st strike price should be larger than 2nd.
        Got K1={K1}, which is not larger than K2={K2}.
        """
        self.put1 = BlackScholesPut(S=S, K=K1, T=T, r=r, sigma=sigma, q=q)
        self.put2 = BlackScholesPut(S=S, K=K2, T=T, r=r, sigma=sigma, q=q)
        super().__init__()

    def _calc_attr(self, attribute_name: str) -> float:
        """
        Combines attributes from two put options into a bear spread. \n
        All greeks and prices are combined in the same way.

        :param attribute_name: String name of option attribute
        pointing to a method that can be called on
        BlackScholesCall and BlackScholesPut.

        :return: Combined value according to bear spread.
        """
        put1_attr = getattr(self.put1, attribute_name)
        put2_attr = getattr(self.put2, attribute_name)
        return put1_attr() - put2_attr()


class BlackScholesCalendarCallSpread(BlackScholesStructureBase):
    """
    Create a calendar call spread option structure. \n
    Horizontal Calendar Call Spread -> K1 == K2 \n 
    Diagonal Calendar Call Spread -> K1 != K2 \n

    :param S: Price of underlying asset \n
    :param K1: Strike price for 1st call to buy. \n
    :param K2: Strike price for 2nd call to sell. \n
    :param T1: Time till expiration in years for 1st call. \n
    :param T2: Time till expiration in years for 2nd call. \n
    (1/12 indicates 1 month) \n
    :param r: Risk-free interest rate (0.05 indicates 5%) \n
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%) \n
    :param q: Annual dividend yield (0.05 indicates 5% yield) \n
    """
    def __init__(
        self,
        S: float,
        K1: float,
        K2: float,
        T1: float,
        T2: float,
        r: float,
        sigma: float,
        q: float = 0.0,
    ):
        assert (
            T1 > T2
        ), f"""1st time to maturity should be longer than 2nd.
        Got T1={T1}, which is not longer than T2={T2}.
        """
        self.call1 = BlackScholesCall(S=S, K=K1, T=T1, r=r, sigma=sigma, q=q)
        self.call2 = BlackScholesCall(S=S, K=K2, T=T2, r=r, sigma=sigma, q=q)
        super().__init__()

    def _calc_attr(self, attribute_name: str) -> float:
        """
        Combines attributes from two put options into a calendar spread. \n
        All greeks and prices are combined in the same way.

        :param attribute_name: String name of option attribute
        pointing to a method that can be called on
        BlackScholesCall and BlackScholesPut.

        :return: Combined value according to the calendar spread.
        """
        call1_attr = getattr(self.call1, attribute_name)
        call2_attr = getattr(self.call2, attribute_name)
        return call1_attr() - call2_attr()
    
    
class BlackScholesCalendarPutSpread(BlackScholesStructureBase):
    """
    Create a calendar put spread option structure. \n
    Horizontal Calendar Put Spread -> K1 == K2 \n 
    Diagonal Calendar Put Spread -> K1 != K2 \n

    :param S: Price of underlying asset \n
    :param K1: Strike price for 1st put to buy. \n
    :param K2: Strike price for 2nd put to sell. \n
    :param T1: Time till expiration in years for 1st put. \n
    :param T2: Time till expiration in years for 2nd put. \n
    (1/12 indicates 1 month) \n
    :param r: Risk-free interest rate (0.05 indicates 5%) \n
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%) \n
    :param q: Annual dividend yield (0.05 indicates 5% yield) \n
    """
    def __init__(
        self,
        S: float,
        K1: float,
        K2: float,
        T1: float,
        T2: float,
        r: float,
        sigma: float,
        q: float = 0.0,
    ):
        assert (
            T1 > T2
        ), f"""1st time to maturity should be longer than 2nd.
        Got T1={T1}, which is not longer than T2={T2}.
        """
        self.put1 = BlackScholesPut(S=S, K=K1, T=T1, r=r, sigma=sigma, q=q)
        self.put2 = BlackScholesPut(S=S, K=K2, T=T2, r=r, sigma=sigma, q=q)
        super().__init__()

    def _calc_attr(self, attribute_name: str) -> float:
        """
        Combines attributes from two put options into a calendar spread. \n
        All greeks and prices are combined in the same way.

        :param attribute_name: String name of option attribute
        pointing to a method that can be called on
        BlackScholesCall and BlackScholesPut.

        :return: Combined value according to the calendar spread.
        """
        put1_attr = getattr(self.put1, attribute_name)
        put2_attr = getattr(self.put2, attribute_name)
        return put1_attr() - put2_attr()