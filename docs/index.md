# blackscholes

## Documentation structure:

1. Quickstart

2. Price calculation

3. All Greeks

4. In-the-money proxies

5. Contribution guide

6. Source Code References

7. Disclaimer

Black Scholes calculator for Python including all Greeks.

Currently only supports European options.

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
call.price()  ## 6.339408
call.delta()  ## 0.766407
```

### Put

```python3
from blackscholes import BlackScholesPut
put = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma)
put.price()  ## 1.214564
put.delta()  ## -0.23359
```
