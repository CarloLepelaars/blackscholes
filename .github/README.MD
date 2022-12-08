# blackscholes

Black Scholes calculator for Python including all Greeks.

## Installation

`pip install blackscholes`

## Examples

### Input variables
```python3
S = 55.0  # Asset price of 55
K = 50.0  # Strike price of 50
T = 1.0  # 1 year to maturity
r = 0.0025  # 0.25% risk-free rate
sigma = 0.15  # 15% vol
```

### Call

```python3
from blackscholes import BlackScholesCall
call = BlackScholesCall(S=S, K=K, T=T, r=r, sigma=sigma)
call.price()  # Call Option price
call.delta()  # Call Delta
```

### Put

```python3
from blackscholes import BlackScholesPut
put = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma)
put.price()  # Put option price
put.delta()  # Put Delta
```

## Contributing

We very much welcome new contributions! Check out the [Github Issues](https://github.com/CarloLepelaars/blackscholes/issues)
to see what is currently being worked on.

Also check out `5. Contributing` in the documentation to learn more about 
contributing to `blackscholes`.
