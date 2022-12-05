<script
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
  type="text/javascript">
</script>


# The Greeks

- [Delta](#delta)
- [Gamma](#gamma)
- [Vega](#vega)
- [Theta](#theta)
- [Rho](#rho)
- [Epsilon](#delta)
- [Lambda](#delta)
- [Vanna](#vanna)
- [Charm](#charm)
- [Vomma](#vomma)
- [Veta](#veta)
- [Phi](#phi)
- [Speed](#speed)
- [Zomma](#zomma)
- [Color](#color)
- [Ultima](#ultima)
- [Dual Delta](#dual-delta)
- [Dual Gamma](#dual-gamma)



## Delta <a name="delta"></a>

### Call

$$ \Phi(d_2)$$

::: blackscholes.call.BlackScholesCall.delta

### Put

$$ -\Phi(-d_2)$$

::: blackscholes.put.BlackScholesPut.delta

## Gamma <a name="gamma"></a>

::: blackscholes.base.BlackScholesBase.gamma

## Vega <a name="vega"></a>

::: blackscholes.base.BlackScholesBase.vega

## Theta <a name="theta"></a>

### Call

::: blackscholes.call.BlackScholesCall.theta

### Put

::: blackscholes.put.BlackScholesPut.theta

## Rho <a name="rho"></a>

### Call

::: blackscholes.call.BlackScholesCall.rho

### Put

::: blackscholes.put.BlackScholesPut.rho

## Epsilon <a name="epsilon"></a>

Will be implemented when dividend support is added. 

Also known as psi. % change in option value
against change in underlying dividend yield.

## Lambda <a name="lamdba"></a>

::: blackscholes.base.BlackScholesBase.lambda_greek

## Vanna <a name="vanna"></a>

::: blackscholes.base.BlackScholesBase.vanna

## Charm <a name="charm"></a>

Charm is the same for calls and puts unless you include
dividend yield. 

::: blackscholes.base.BlackScholesBase.charm

## Vomma <a name="vomma"></a>

::: blackscholes.base.BlackScholesBase.vomma

## Veta <a name="veta"></a>

::: blackscholes.base.BlackScholesBase.veta

## Phi <a name="phi"></a>

$$\phi$$

::: blackscholes.base.BlackScholesBase.phi

## Speed <a name="speed"></a>

::: blackscholes.base.BlackScholesBase.speed

## Zomma <a name="zomma"></a>

::: blackscholes.base.BlackScholesBase.zomma

## Color <a name="color"></a>

::: blackscholes.base.BlackScholesBase.color

## Ultima <a name="ultima"></a>

::: blackscholes.base.BlackScholesBase.ultima

## Dual Delta <a name="dual-delta"></a>

### Call

::: blackscholes.call.BlackScholesCall.dual_delta

### Put

::: blackscholes.put.BlackScholesPut.dual_delta

## Dual Gamma <a name="dual-gamma"></a>

::: blackscholes.base.BlackScholesBase.dual_gamma