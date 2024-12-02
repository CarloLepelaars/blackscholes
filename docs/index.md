# blackscholes

![](https://img.shields.io/pypi/dm/blackscholes)
![Python Version](https://img.shields.io/badge/dynamic/toml?url=https://raw.githubusercontent.com/carlolepelaars/blackscholes/master/pyproject.toml&query=%24.project%5B%22requires-python%22%5D&label=python&color=blue) 
![](https://img.shields.io/codecov/c/github/carlolepelaars/blackscholes)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Documentation structure:

[1. Quickstart](https://carlolepelaars.github.io/blackscholes/1.quickstart)

[2. Price calculation](https://carlolepelaars.github.io/blackscholes/2.price)

[3. The Greeks (Black-Scholes)](https://carlolepelaars.github.io/blackscholes/3.the_greeks_blackscholes)

[4. The Greeks (Black-76)](https://carlolepelaars.github.io/blackscholes/4.the_greeks_black76)

[5. In-the-money proxies](https://carlolepelaars.github.io/blackscholes/5.itm)

[6. Option Structures](https://carlolepelaars.github.io/blackscholes/6.option_structures)

[7. Source Code References](https://carlolepelaars.github.io/blackscholes/7.references)

[8. Disclaimer](https://carlolepelaars.github.io/blackscholes/8.disclaimer)

[Contribution guide](https://carlolepelaars.github.io/blackscholes/contributing)


A Black-Scholes calculator for Python that includes up to the third-order Greeks.

Supports the Black-Scholes-Merton model, 
Black-76 model and option structures.

Currently only supports 
[European options](https://www.investopedia.com/articles/optioninvestor/08/american-european-options.asp).

There is also a graphical interface available at: [https://carlo.ai/tools/blackscholes](https://carlo.ai/tools/blackscholes)

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
call.spot_delta() ## 0.7683
call.charm()  ## 0.083267
```

### Put

```python3
from blackscholes import BlackScholesPut
put = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma, q=q)
put.price()  ## 1.214564
put.delta()  ## -0.23359
put.spot_delta() ## -0.23417
put.charm()  ## 0.083267
```

### Black76

The Black-76 model is often specifically used for options and futures and bonds.
`blackscholes` also supports this model. To see all available greeks
check out section [4. The Greeks (Black-76)](https://carlolepelaars.github.io/blackscholes/4.the_greeks_black76).

**Call**

```python
from blackscholes import Black76Call
call = Black76Call(F=55, K=50, T=1, r=0.0025, sigma=0.15)
call.price()  ## 6.2345
call.delta()  ## 0.7594
call.vomma()  ## 45.1347
```

**Put**

```python
from blackscholes import Black76Put
put = Black76Put(F=55, K=50, T=1, r=0.0025, sigma=0.15)
put.price()  ## 1.2470
put.delta()  ## -0.2381
put.vomma()  ## 45.1347
```


### Structures

Structures are combination of call and put options. Every option structure
has a `Long` and `Short` version. To learn more
check out section [6. Option Structures](https://carlolepelaars.github.io/blackscholes/6.option_structures).

**Long Straddle**
```python3
from blackscholes import BlackScholesStraddleLong

straddle = BlackScholesStraddleLong(S=55, K=50, T=1.0,
                                    r=0.0025, sigma=0.15)
straddle.price()  ## 7.5539
straddle.delta()  ## 0.5328
```

**Long Strangle**
```python
from blackscholes import BlackScholesStrangleLong

strangle = BlackScholesStrangleLong(S=55, K1=40, K2=50, T=1.0,
                                    r=0.0025, sigma=0.15)
strangle.price()  ## 6.3800
strangle.delta()  ## 0.7530
```

**Long (Call) Butterfly**
```python
from blackscholes import BlackScholesButterflyLong

butterfly = BlackScholesButterflyLong(S=55, K1=40, K2=50, K3=60, 
                                      T=1.0, r=0.0025, sigma=0.15)
butterfly.price()  ## 3.9993
butterfly.delta()  ## -0.2336
```

**Long Iron Condor**
```python3
from blackscholes import BlackScholesIronCondorLong

iron_condor = BlackScholesIronCondorLong(S=55, K1=20, K2=25, K3=45, K4=50, 
                                         T=1.0, r=0.0025, sigma=0.15)
iron_condor.price()  ## 4.0742
iron_condor.delta()  ## 0.1572
```

**Bull Spread**

```python3
from blackscholes import BlackScholesBullSpread
bull_spread = BlackScholesBullSpread(S=55, K1=40, K2=50, T=1.0,
                                     r=0.0025, sigma=0.15)
bull_spread.price()  ## 8.8011
bull_spread.delta()  ## 0.2202
```

**Bear Spread**

```python
from blackscholes import BlackScholesBearSpread
bear_spread = BlackScholesBearSpread(S=55, K1=50, K2=40, T=1.0,
                                     r=0.0025, sigma=0.15)
bear_spread.price()  ## 1.1740
bear_spread.delta()  ## -0.2202
```

**Long Iron Butterfly**

```python
from blackscholes import BlackScholesIronButterflyLong
iron_butterfly = BlackScholesIronButterflyLong(S=55, K1=95, K2=100, K3=105, 
                                               T=1.0, r=0.0025, sigma=0.15)
iron_butterfly.price()  ## 4.9873
iron_butterfly.delta()  ## -0.0001
```

**Short Iron Butterfly**

```python
from blackscholes import BlackScholesIronButterflyShort
iron_butterfly = BlackScholesIronButterflyShort(S=55, K1=95, K2=100, K3=105, 
                                                T=1.0, r=0.0025, sigma=0.15)
iron_butterfly.price()  ## -4.9873
iron_butterfly.delta()  ## 0.0001
```

### Binary options

Binary options are also called exotic, digital or bet options. `blackscholes` supports Greeks for binary calls and puts.



