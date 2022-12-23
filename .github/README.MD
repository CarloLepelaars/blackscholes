# blackscholes

![](https://img.shields.io/pypi/dm/blackscholes) | 
![](https://img.shields.io/pypi/pyversions/blackscholes)

Black Scholes calculator for Python including all Greeks.

Supports the Black-Scholes-Merton model, 
Black-76 model and option structures.

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

### Black-76

The Black-76 model is often used specifically for options and futures and bonds.
`blackscholes` also supports this model. To see all available greeks
check out section [4. The Greeks (Black-76)](https://carlolepelaars.github.io/blackscholes/4.the_greeks_black76).

**Call Example**
```python
from blackscholes import Black76Call
F = 55. # Discounted futures price
call = Black76Call(F=F, K=K, T=T, r=r, sigma=sigma)
call.price()  ## 6.2345
call.delta()  ## 0.7594
call.vomma()  ## 45.1347
```

**Put Example**
```python
from blackscholes import Black76Put
F = 55. # Discounted futures price
call = Black76Put(F=F, K=K, T=T, r=r, sigma=sigma)
call.price()  ## 1.2470
call.delta()  ## -0.2381
call.vomma()  ## 45.1347
```

### Structures

`blackscholes` offers the following four option structures:
- Straddle
- Strangle
- Butterfly
- Iron Condor

All structures have a long and short version. To learn more
check out section [6. Option Structures](https://carlolepelaars.github.io/blackscholes/6.option_structures).

**Long Straddle Example**
```python3
from blackscholes import BlackScholesStraddleLong

straddle = BlackScholesStraddleLong(S=55, K=50, T=1.0,
                                    r=0.0025, sigma=0.15)
straddle.price()  ## 7.5539
straddle.delta()  ## 0.5328
```

## Contributing

We very much welcome new contributions! Check out the [Github Issues](https://github.com/CarloLepelaars/blackscholes/issues)
to see what is currently being worked on.

Also check out [Contributing](https://carlolepelaars.github.io/blackscholes/contributing) in the documentation 
to learn more about 
contributing to [blackscholes](https://github.com/CarloLepelaars/blackscholes).
