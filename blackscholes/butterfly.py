from blackscholes.base import BlackScholesCompoundBase


class BlackScholesButterfly(BlackScholesCompoundBase):
    """
    Create butterfly option structure.

    :param S: Price of underlying asset \n
    :param K1: Strike price for 1st option \n
    :param K2: Strike price for 2nd option \n
    :param K3: Strike price for 3rd option \n
    It must hold that K1 < K2 < K3. \n
    Additionally, it must hold that K2 - K1 = K3 - K2 \n
    :param T: Time till expiration in years (1/12 indicates 1 month) \n
    :param r: Risk-free interest rate (0.05 indicates 5%) \n
    :param sigma: Volatility (standard deviation) of stock (0.15 indicates 15%) \n
    :param q: Annual dividend yield (0.05 indicates 5% yield)
    :param type: 'long' or 'short' \n
    - Long butterfly -> Call(K1) - 2 * Call(K2) + Call(K3)
    - Short butterfly -> -Put(K1) + 2 * Put(K2) - Put(K3)
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
        Got {K1}, {K2} and {K3}.
        """
        assert (
            K2 - K1 == K3 - K2
        ), f"""Strike price must be symmetric, so K2 - K1 = K3 - K2.
        Got {K2}-{K1} != {K3}-{K2}.
        """
        super().__init__()
