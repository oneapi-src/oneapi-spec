.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_rng_distributions:

Distributions
=============


.. container::


   oneMKL RNG routines are used to generate random
   numbers with different types of distribution. Each function group is
   introduced below by the type of underlying distribution and contains
   a short description of its functionality, as well as specifications
   of the call sequence and the explanation of input and output
   parameters. `Table Continuous Distribution Generators`_
   and `Table Discrete Distribution Generators`_ list the
   random number generator routines with data types and output
   distributions, and sets correspondence between data types of the
   generator routines and the basic random number generators.


    _`Table Continuous Distribution Generators`


   .. container:: tablenoborder


      .. list-table::
         :header-rows: 1

         * -     Routine
           -     Description
         * -           \ :ref:`onemkl_rng_uniform_continuous`\
           -     Uniform continuous distribution on the interval       [``a,b``)
         * -           \ :ref:`onemkl_rng_gaussian`\
           -     Normal (Gaussian) distribution
         * -           \ :ref:`onemkl_rng_exponential`\
           -     Exponential distribution
         * -           \ :ref:`onemkl_rng_laplace`\
           -     Laplace distribution (double exponential distribution)
         * -           \ :ref:`onemkl_rng_weibull`\
           -     Weibull distribution
         * -           \ :ref:`onemkl_rng_cauchy`\
           -     Cauchy distribution
         * -           \ :ref:`onemkl_rng_rayleigh`\
           -     Rayleigh distribution
         * -           \ :ref:`onemkl_rng_lognormal`\
           -     Lognormal distribution
         * -           \ :ref:`onemkl_rng_gumbel`\
           -     Gumbel (extreme value) distribution
         * -           \ :ref:`onemkl_rng_gamma`\
           -     Gamma distribution
         * -           \ :ref:`onemkl_rng_beta`\
           -     Beta distribution
         * -           \ :ref:`onemkl_rng_chi_square`\
           -     Chi-Square distribution
         * -           \ :ref:`onemkl_rng_gaussian_mv`\
           -     Normal Multivariate (Gaussian Multivariate) distribution


    _`Table Discrete Distribution Generators`
   .. container:: tablenoborder


      .. list-table::
         :header-rows: 1

         * -     Type of Distribution
           -     Description
         * -           \ :ref:`onemkl_rng_uniform_discrete`\
           -     Uniform discrete distribution on the interval       [``a,b``)
         * -           \ :ref:`onemkl_rng_uniform_bits`\
           -     Uniformly distributed bits in 32/64-bit chunks
         * -           \ :ref:`onemkl_rng_bits`\
           -     Bits of underlying BRNG integer recurrence
         * -           \ :ref:`onemkl_rng_bernoulli`\
           -     Bernoulli distribution
         * -           \ :ref:`onemkl_rng_geometric`\
           -     Geometric distribution
         * -           \ :ref:`onemkl_rng_binomial`\
           -     Binomial distribution
         * -           \ :ref:`onemkl_rng_hypergeometric`\
           -     Hypergeometric distribution
         * -           \ :ref:`onemkl_rng_poisson`\
           -     Poisson distribution
         * -           \ :ref:`onemkl_rng_poisson_v`\
           -     Poisson distribution with varying mean
         * -           \ :ref:`onemkl_rng_negative_binomial`\
           -     Negative binomial distribution, or Pascal distribution
         * -           \ :ref:`onemkl_rng_multinomial`\
           -     Multinomial distribution




   .. container:: section

      .. rubric:: Modes of random number generation

      The library provides two modes of random number generation,
      accurate and fast. Accurate generation mode is intended for
      applications that are highly demanding to accuracy of
      calculations. When used in this mode, the generators produce
      random numbers lying completely within the definitional domain for all
      values of the distribution parameters. For example, random numbers
      obtained from the generator of continuous distribution that is
      uniform on interval [``a``,\ ``b``] belong to this interval
      irrespective of what ``a`` and ``b`` values may be. Fast mode
      provides high performance generation and also guarantees that
      generated random numbers belong to the definitional domain except
      for some specific values of distribution parameters. The
      generation mode is set by specifying the relevant value of the method
      parameter in generator routines. The list of distributions that
      support accurate mode of generation is given in the table below.


    _`Table Distribution Generators with Accurate Method`
   .. container:: tablenoborder


      .. list-table::
         :header-rows: 1

         * -     Distribution
           -     Method
         * -           \ :ref:`onemkl_rng_uniform_continuous`\
           -     `oneapi::mkl::rng::unform_method::accurate`
         * -           \ :ref:`onemkl_rng_exponential`\
           -     `oneapi::mkl::rng::exponential_method::icdf_accurate`
         * -           \ :ref:`onemkl_rng_weibull`\
           -     `oneapi::mkl::rng::weibull_method::icdf_accurate`
         * -           \ :ref:`onemkl_rng_rayleigh`\
           -     `oneapi::mkl::rng::rayleigh_method::icdf_accurate`
         * -           \ :ref:`onemkl_rng_lognormal`\
           -     `oneapi::mkl::rng::lognormal_method::box_muller2_accurate`, `oneapi::mkl::rng::lognormal_method::icdf_accurate`
         * -           \ :ref:`onemkl_rng_gamma`\
           -     `oneapi::mkl::rng::gamma_method::marsaglia_accurate`
         * -           \ :ref:`onemkl_rng_beta`\
           -     `oneapi::mkl::rng::beta_method::cja_accurate`
               
   **Parent topic:** :ref:`onemkl_rng`



.. toctree::
    :hidden:

    distributions-template-parameter-mkl-rng-method-values
    mkl-rng-uniform-continuous
    mkl-rng-gaussian
    mkl-rng-exponential
    mkl-rng-laplace
    mkl-rng-weibull
    mkl-rng-cauchy
    mkl-rng-rayleigh
    mkl-rng-lognormal
    mkl-rng-gumbel
    mkl-rng-gamma
    mkl-rng-beta
    mkl-rng-chi_square
    mkl-rng-gaussian_mv
    mkl-rng-uniform-discrete
    mkl-rng-uniform_bits
    mkl-rng-bits
    mkl-rng-bernoulli
    mkl-rng-geometric
    mkl-rng-binomial
    mkl-rng-hypergeometric
    mkl-rng-poisson
    mkl-rng-poisson_v
    mkl-rng-negbinomial
    mkl-rng-multinomial
