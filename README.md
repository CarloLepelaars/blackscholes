# blackscholes
Black Scholes calculator for Python including all Greeks.

For European options.

## Installation

`pip install blackscholes`

## 1. Calls

```python3
from blackscholes import BlackScholesCall
S = 55.0  # Asset price of 55
K = 50.0  # Strike price of 50
T = 1.0  # 1 year to maturity
r = 0.0025  # 0.25% risk-free rate
sigma = 0.15  # 15% vol
call = BlackScholesCall(S=S, K=K, T=T, r=r, sigma=sigma)
# Option price
call.price()
# Delta
call.delta()
```

## 1. Put

```python3
from blackscholes import BlackScholesPut
S = 55.0  # Asset price of 55
K = 50.0  # Strike price of 50
T = 1.0  # 1 year to maturity
r = 0.0025  # 0.25% risk-free rate
sigma = 0.15  # 15% vol
put = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma)
# Option price
put.price()
# Delta
put.delta()
```
