---
title: "Canonical Probability distributions in Python"
description: "Leveraging scipy.stats to represent probability distributions in Python"
date: "2015-01-07"
draft: false
tags:
    - "python"
    - "statistics"
    - "oop"
---

### Distributions.jl

I often need to use probability distributions in my work and research. Julia has an excellent package, [Distributions.jl](https://github.com/JuliaStats/Distributions.jl), for representing many common probability distributions. The three main features I like from this package are

1. Excellent [documentation](http://distributionsjl.readthedocs.org) where they clearly specify the methods available to each probability distribution as well as the parameterization used to define the pdf
2. Canonical parameterizations for all distributions. By canonical I mean the form of the pdf you would find on the Wikipedia page for a particular distribution or open up a standard reference like *Bayesian Data Analysis* (Gelman, 2013)
3. A consistent interface to all distributions of the same type. This means there are a [set of functions](http://distributionsjl.readthedocs.org/en/latest/univariate.html#common-interface) you can count on being defined and tested for all continuous univariate distributions (or other type of distribution)

These three features combine to expose a very user friendly interface into common probability distributions.

### scipy.stats

The standard resource for working with probability distributions in Python is [`scipy.stats`](http://docs.scipy.org/doc/scipy-0.14.0/reference/stats.html#continuous-distributions). This module contains an impressive amount of high quality work (almost 100 distributions last time I counted), but the scipy developers have taken a slightly different approach compared to Distributions.jl. Instead of choosing to represent each distribution in its common parameterization, they chose to have a consistent parameterization *across* distributions. Specifically, each distribution can be specified by setting one or more of three parameters: `shape`, `scale`, or `loc` (meaning location).

#### Example: Normal (N) and Inverse Gamma (IG)

To see why this is an issue, consider the following example. Suppose we wanted to work with the normal and inverse gamma distributions. From wikipedia, we see that the pdf for the normal distribution with mean $\mu$ and standard deviation $\sigma$ is given by

<div>$$\begin{align*}p(x; \mu, \sigma) = \frac{1}{\sigma \sqrt{2 \pi}} e^{- \frac{(x - \mu)^2}{2 \sigma^2}}\end{align*}.$$</div>

Similarly, the pdf for the inverse gamma distribution with shape $\alpha$ and scale $\beta$ is

<div>$$\begin{align*}p(x; \alpha, \beta) = \frac{\beta^{\alpha}}{\Gamma(\alpha)} x^{- \alpha - 1} \exp \left(- \frac{\beta}{x} \right)\end{align*}.$$</div>

In scipy these distributions are given by `scipy.stats.norm` and `scipy.stats.invgamma`. If we consult the [scipy.stats documentation](http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.norm.html#scipy.stats.norm) for the normal distribution we would see

```
The location (loc) keyword specifies the mean. The scale (scale) keyword specifies the standard deviation.
```

and

```
The probability density function for norm is:
    norm.pdf(x) = exp(-x**2/2)/sqrt(2*pi)
```

Wait, what?! This looks nothing like the pdf above, what's going on? Let's move forward and trust that if we set `loc` equal to the mean and `scale` equal to the standard deviation we will get the correct distribution. To verify that this is true, I copied and pasted the following into an IPython session:



```python
In [1]: %paste
from numpy import sqrt, pi, exp
import scipy.stats as st

mu = 1.0
sigma = 2.0
n = st.norm(loc=mu, scale=sigma)


def diff_pdf(d, f, x):
    "compute d.pdf(x) - f(x)"
    return d.pdf(x) - f(x)

# pdf by hand from Wikipedia form
n_pdf = lambda x: 1/(sigma*sqrt(2*pi)) * exp(-(x-mu)**2/(2*sigma**2))

print("(scipy - by hand) for normal: %.3e" % diff_pdf(n, n_pdf, 2.1))

## -- End pasted text --
(scipy - by hand) for normal: 0.000e+00
```

Phew, it appears that scipy.stats *is* doing the correct thing! I want to point out two problems with the Normal distribution here:

1. Instead of using the common names for the parameters of the normal distribution (mean or mu and std_dev or sigma), they chose to have the `loc` and `scale` parameters *assume* those roles. To me this meant that in order to construct the $N(1, 2)$ distribution I was after I had to go to the documentation to look up what `loc`, `scale`, and `shape` meant for `scipy.stats.norm`
2. The documentation displays an expression for the pdf, but it doesn't match the canonical form of the pdf we found online (or any any introductory probability textbook). Even worse, the pdf they gave didn't even mention the parameters of the distribution.

Now lets see what happens when we look up the inverse gamma distribution. From the documentation for [`scipy.stats.invgamma`](http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.invgamma.html) we read

```
An inverted gamma continuous random variable.
```

and

```
The probability density function for invgamma is:
invgamma.pdf(x, a) = x**(-a-1) / gamma(a) * exp(-1/x)
```

So, this appears to be related to the pdf we have above, but where did $\beta$ go? The docstring also calls this an *inverted* gamma distribution instead of the standard *inverse* gamma, so maybe this isn't actually the inverse gamma distribution? It turns out that it is the inverse gamma distribution where this time the *first positional argument* (I couldn't find it's name after about 20 minutes of searching) takes on the role of $\alpha$ and the `scale` keyword argument represents $\beta$. I verified that this is true in an IPython session also:

```python
In [2]: paste
# Same imports from above
from scipy.special import gamma

alpha = 5.0
beta = 6.0
ig = st.invgamma(alpha, scale=beta)

ig_pdf = lambda x: beta**alpha / gamma(alpha) * x**(-alpha - 1) * exp(- beta / x)
print("(scipy - by hand) for inverse gamma: %.3e" % diff_pdf(ig, ig_pdf, 2.1))

## -- End pasted text --
(scipy - by hand) for inverse gamma: -8.327e-17

```

Like like we did identify the correct distribution! In this example we had the same problems as in the example for the normal distribution, but we had additional problems:

* Even though inverse gamma is a two parameter distribution, the documentation for `scipy.stats.invgamma` never once mentioned a second parameter ($\beta$)
* The docstring called the distribution by a less well-known name "inverted gamma" instead of inverse gamma

These issues, combined with those highlighted in the first example required me to do quite a bit of detective work (ultimately testing the pdf by hand) to make sure that I had the correct distribution.

<div style="border: 1px solid green; padding: 9.5px;">
    NOTE: I do not want this post to sound at all like I am bashing scipy. That is not the intent. scipy.stats contains an incredible number of high quality probability distributions that exposes a consistent and, though sometimes awkward, predictable interface. I showed these examples merely to highlight that the current state of scipy.stats is not appropriate for users looking for the standard representations of probability distributions they are used to.
</div>


### The Solution: `distcan`

I am in the *very* early stages of a project that will hopefully address these issues. I call the project [`distcan`](https://github.com/spencerlyon2/distcan). The purpose of `distcan` is to expose probability **dist**ributions in their **can**onical form to Python users. Some goals for the project are:

* Represent probability distributions in their canonical form, with parameters given their standard names
* Expose an API that is encompasses functionality in Distributions.jl and scipy.stats, with naming conventions that are consistent for users of both packages
* Have documentation that accurately describes the distribution being used

To accomplish these goals I am heavily leveraging the code in `scipy.stats`. To see just how much I am using this mature code base, consider the actual implementation of the InverseGamma distribution from `distcan` (as of 2015-01-20):

```python
class InverseGamma(CanDistFromScipy):                                       # 1

    _metadata = {
        "name": "InverseGamma",
        "pdf_tex": (r"p(x;\alpha,\beta)=\frac{\beta^{\alpha}}{\Gamma(\alpha)}"
                    + r"x^{-\alpha-1}\exp\left(-\frac{\beta}{x}\right)"),

        "cdf_tex": r"\frac{\Gamma(\alpha, \beta / x)}{\Gamma(\alpha)}",

        "param_names": ["alpha", "beta"],

        "param_descrs": ["Shape parameter (must be >0)",
                         "Scale Parameter (must be >0)"],

        "_str": "InverseGamma(alpha=%.5f, beta=%.5f)"}                      # 2

    # set docstring
    __doc__ = _create_class_docstr(**_metadata)                             # 3

    def __init__(self, alpha, beta):                                        # 4
        self.alpha = alpha                                                  # 5
        self.beta = beta

        # set dist before calling super's __init__
        self.dist = st.invgamma(alpha, scale=beta)                          # 6
        super(InverseGamma, self).__init__()                                # 7

    @property                                                               # 8
    def params(self):
        return (self.alpha, self.beta)
```

I have labeled certain lines of the code above. Let's analyze what is happening item by item:

1. Notice that we are subclassing `CanDistFromScipy`. This class is defined in `distcan.scipy_wrap` and does almost all the work for us, including defining methods and setting docstrings for each method.
2. `_metadata` is a dict that is used to set the docstring of the class and  each method as well as the `__str__` and `__repr__` methods. For an explanation of what this dict should contain and how it is used, see the [metadata section](TODO: link) of the docs
3. This line uses the information from the `_metadata` dict to set the docstring for the class
4. The arguments to `__init__` method are the canonical parameters and associated names for the distribution
5. These arguments are stored as attributes of the class
6. Create an internal instance of the distribution, based on the implementation in `scipy.stats`. This is where we map canonical parameter names into the notation from `scipy.stats`
7. Call the `__init__` method of `CanDistFromScipy`. This is where the heavy lifting happens
8. Set an additional property called `params` that returns the parameters of the distribution

To create another distribution based on a distribution found in `scipy.stats`, you simply need to define a class that inherits from `CanDistFromScipy` and implements the 8 points listed above.

#### Functionality

All the functionality of `scipy.stats` and almost all of the functionality in `Distributions.jl` (except for `mgf`, `cf`, `insupport`, and `succprob`/`failprob` where applicable) is exposed by each distribution. This includes the following methods:


* `pdf`: evaluate the probability density function
* `logpdf`: evaluate the log of the pdf
* `cdf`: evaluate the cumulative density function
* `logcdf`: evaluate the log of the cdf
* `rvs`: draw random samples from the distribution
* `moment`: evaluate nth non-central moment
* `stats`: some statistics of the RV (such as mean, variance, skewness, kurtosis)
* `fit` (when available in scipy.stats): return the maximum likelihood estimators of the distribution, given data
* `sf` (also given name `ccdf`): compute the survival function (or complementary cumulative density
function)
* `logsf` (also given name `logccdf`): compute the log of the survival function (or complementary cumulative
density function)
* `isf`: compute the inverse of the survival function (or complementary
cumulative density function)
* `ppf` (also given name `quantile`): compute the percent point function (or quantile), which is the inverse
of the cdf. This is commonly used to compute critical values.
* `loglikelihood` (not in scipy): the loglikelihood of the distribution with respect to all the samples
in x
* `invlogcdf` (not in scipy): evaluate inverse function of the logcdf
* `cquantile` (not in scipy): evaluate the complementary quantile function. Equal to `d.ppf(1-x)` for
x in (0, 1). Could be used to compute the lower critical values of a
distribution
* `invlogccdf` (not in scipy): evaluate inverse function of the logccdf

Additionally, each distribution has the following properties (accessed as `dist_object.property_name` -- i.e. without parenthesis):

* `mean`: the mean of the distribution
* `var`: the var of the distribution
* `std`: the std of the distribution
* `skewness`: the skewness of the distribution
* `kurtosis`: the kurtosis of the distribution
* `median`: the median of the distribution
* `mode`: the mode of the distribution
* `isplaykurtic`: boolean indicating if kurtosis is greater than zero
* `isleptokurtic`: boolean indicating if kurtosis is less than zero
* `ismesokurtic`: boolean indicating if kurtosis is equal to zero
* `entropy`: the entropy of the distribution
* `params` (not in scipy): return a tuple of the distributions parameters


### Future plans

I plan on adding to `distcan` on an as needed basis -- meaning when I need a new distribution or functionality or another user requests something. If you would like to contribute, check out the project on [GitHub](https://github.com/spencerlyon2/distcan).
