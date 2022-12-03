# blackscholes
Black Scholes calculator for Python including all Greeks.

Currently only supports European options.

DISCLAIMER: Software is provided AS IS under an MIT licence. 
We can never guarantee that all computations will be correct. The software 
is tested to the best of our ability, but we cannot guarantee correct results.
Always verify results before using 3rd-party libraries like this in high stakes situations.

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

Install dev-requirements:

`pip install -r dev-requirements.txt`

Install the pre-commit hooks with:

`pre-commit install`

## Local Documentation

You can view the docs locally if you have dev-requirements installed:

`mkdocs serve`