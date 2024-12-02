from blackscholes.base import BlackScholesStructureBase
from blackscholes import BlackScholesCall, BlackScholesPut


class BlackScholesIronButterflyLong(BlackScholesStructureBase):
    """
    Create long iron butterfly option structure. \n
    - Long iron butterfly -> - Put(K1) + Put(K2) + Call(K3) - Call(K4)

    :param S: Price of underlying asset \n
    :param K1: Strike price for 1st option \n
    :param K2: Strike price for 2nd and 3rd option \n
    :param K3: Strike price for 4th option \n
    It must hold that K1 < K2 < K3. \n
    Additionally, it must hold that K3 - K2 = K2 - K1 (equidistant strike prices) \n
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
        K3: float,
        T: float,
        r: float,
        sigma: float,
        q: float = 0.0,
    ):
        assert (
            K1 < K2 < K3
        ), f"""It must hold that K1 < K2 < K3.
        Got {K1}, {K2}, {K3}.
        """
        assert (
            K3 - K2 == K2 - K1
        ), f"""All strike prices must be equidistant, so K4 - K3 = K3 - K2 = K2 - K1.
        Got {K3}-{K2} != {K2}-{K1}.
        """
        super().__init__()
        self.put1 = BlackScholesPut(S=S, K=K1, T=T, r=r, sigma=sigma, q=q)
        self.put2 = BlackScholesPut(S=S, K=K2, T=T, r=r, sigma=sigma, q=q)
        self.call1 = BlackScholesCall(S=S, K=K2, T=T, r=r, sigma=sigma, q=q)
        self.call2 = BlackScholesCall(S=S, K=K3, T=T, r=r, sigma=sigma, q=q)

    def _calc_attr(self, attribute_name: str) -> float:
        """
        Combines attributes from two put and two call options into a long iron butterfly. \n
        All greeks and price are combined in the same way.

        :param attribute_name: String name of option attribute
        pointing to a method that can be called on
        BlackScholesCall and BlackScholesPut.

        :return: Combined value according to long iron butterfly.
        """
        put_attr1 = getattr(self.put1, attribute_name)
        put_attr2 = getattr(self.put2, attribute_name)
        call_attr1 = getattr(self.call1, attribute_name)
        call_attr2 = getattr(self.call2, attribute_name)
        return -put_attr1() + put_attr2() + call_attr1() - call_attr2()


class BlackScholesIronButterflyShort(BlackScholesStructureBase):
    """
    Create short iron butterfly option structure. \n
    - Short iron butterfly -> Put(K1) - Put(K2) - Call(K3) + Call(K4)

    :param S: Price of underlying asset \n
    :param K1: Strike price for 1st option \n
    :param K2: Strike price for 2nd and 3rd option \n
    :param K3: Strike price for 4th option \n
    It must hold that K1 < K2 < K3. \n
    Additionally, it must hold that K3 - K2 = K2 - K1 (equidistant strike prices) \n
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
        K3: float,
        T: float,
        r: float,
        sigma: float,
        q: float = 0.0,
    ):
        assert (
            K1 < K2 < K3
        ), f"""It must hold that K1 < K2 < K3.
        Got {K1}, {K2}, {K3}.
        """
        assert (
            K3 - K2 == K2 - K1
        ), f"""All strike prices must be equidistant, so K4 - K3 = K3 - K2 = K2 - K1.
        Got {K3}-{K2} != {K2}-{K1}.
        """
        super().__init__()
        self.put1 = BlackScholesPut(S=S, K=K1, T=T, r=r, sigma=sigma, q=q)
        self.put2 = BlackScholesPut(S=S, K=K2, T=T, r=r, sigma=sigma, q=q)
        self.call1 = BlackScholesCall(S=S, K=K2, T=T, r=r, sigma=sigma, q=q)
        self.call2 = BlackScholesCall(S=S, K=K3, T=T, r=r, sigma=sigma, q=q)

    def _calc_attr(self, attribute_name: str) -> float:
        """
        Combines attributes from two put and two call options into a short iron butterfly. \n
        All greeks and price are combined in the same way.

        :param attribute_name: String name of option attribute
        pointing to a method that can be called on
        BlackScholesCall and BlackScholesPut.

        :return: Combined value according to short iron butterfly.
        """
        put_attr1 = getattr(self.put1, attribute_name)
        put_attr2 = getattr(self.put2, attribute_name)
        call_attr1 = getattr(self.call1, attribute_name)
        call_attr2 = getattr(self.call2, attribute_name)
        return put_attr1() - put_attr2() - call_attr1() + call_attr2()
