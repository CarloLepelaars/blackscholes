# blackscholes

![](https://img.shields.io/pypi/dm/blackscholes) | 
![](https://img.shields.io/pypi/pyversions/blackscholes)

Black Scholes calculator for Python including all Greeks.

## Installation

`pip install blackscholes`

## Examples

### Input variables
```python3
S = 55.0  # Asset price of 55
K = 50.0  # Strike price of 50
T = 1.0  # 1 Year to maturity
r = 0.0025  # 0.25% Risk-free rate
sigma = 0.15  # 15% Volatility
q = 0.0 # 0% Annual Dividend Yield
```

### Call

```python3
from blackscholes import BlackScholesCall
call = BlackScholesCall(S=S, K=K, T=T, r=r, sigma=sigma, q=q)
call.price()  ## 6.339408
call.delta()  ## 0.766407
call.charm()  ## 0.083267
```

### Put

```python3
from blackscholes import BlackScholesPut
put = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma, q=q)
put.price()  ## 1.214564
put.delta()  ## -0.23359
put.charm()  ## 0.083267
```

## Contributing

We very much welcome new contributions! Check out the [Github Issues](https://github.com/CarloLepelaars/blackscholes/issues)
to see what is currently being worked on.

Also check out [5. Contributing](https://carlolepelaars.github.io/blackscholes/5.contributing/) in the documentation to learn more about 
contributing to [blackscholes](https://github.com/CarloLepelaars/blackscholes).
