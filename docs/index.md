# blackscholes

## Documentation structure:

[1. Quickstart](https://carlolepelaars.github.io/blackscholes/1.quickstart)

[2. Price calculation](https://carlolepelaars.github.io/blackscholes/2.price)

[3. The Greeks (Black-Scholes)](https://carlolepelaars.github.io/blackscholes/3.the_greeks_blackscholes)

[4. The Greeks (Black-76)](https://carlolepelaars.github.io/blackscholes/4.the_greeks_black76)

[5. In-the-money proxies](https://carlolepelaars.github.io/blackscholes/5.itm)

[6. Contribution guide](https://carlolepelaars.github.io/blackscholes/6.contributing)

[7. Option Structures](https://carlolepelaars.github.io/blackscholes/7.option_structures)

[8. Source Code References](https://carlolepelaars.github.io/blackscholes/8.references)

[9. Disclaimer](https://carlolepelaars.github.io/blackscholes/9.disclaimer)

Black Scholes calculator for Python including all Greeks.

Currently only supports European options.

## Installation

`pip install blackscholes`

## Examples

### Input variables
```python3
S = 55.0  # Asset price of 55
K = 50.0  # Strike price of 50
T = 1.0  # 1 Year to maturity
r = 0.0025  # 0.25% Risk-free rate
sigma = 0.15  # 15% Volatiltiy
q = 0.  # 0% Annual Dividend Yield
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
