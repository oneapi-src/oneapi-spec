.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_rng_overview:

Random Number Generators (RNG) Overview
=======================================

.. rubric:: Definitions


The pseudo-random number generator is defined by a structure(:math:`S`, :math:`\mu`, :math:`f`, :math:`U`, :math:`g`), where:

   -  :math:`S` is a finite set of states (the state space)
   -  :math:`\mu` is a probability distribution on :math:`S` for the initial state
      (or seed) :math:`s_0`
   -  :math:`f:S \rightarrow S` is the transition function
   -  :math:`U` – a finite set of output symbols
   -  :math:`g:S \rightarrow U` an output function


The generation of random numbers is as follows:

   #. Generate the initial state (called the seed) :math:`s_0` according to :math:`\mu` and compute :math:`u_0 = g(s_0)`.
   #. Iterate for :math:`i = 1 , ... , ` :math:`s_i = f(s_{i-1})` and :math:`u_i = g(s_i)`. Output values :math:`u_i` are the so-called random numbers produced by the PRNG.


In computational statistics, random variate generation is usually made in two steps:

   #. Generating imitations of independent and identically distributed
      (i.i.d.) random variables having the uniform distribution over the
      interval :math:`(0, 1)`
   #. Applying transformations to these i.i.d. :math:`U(0, 1)` random variates
      in order to generate (or imitate) random variates and random
      vectors from arbitrary distributions.

.. rubric:: Structure

RNG domain contains two classes types:

   -  Engines (basic random number generators) classes, which holds
      the state of generator and is a source of i.i.d. random. Refer to
      :ref:`onemkl_rng_engines_basic_random_number_generators`
      for a detailed description.
   -  Distribution classes templates (transformation classes) for different types of statistical
      distributions, for example, uniform, normal (Gaussian), binomial,
      etc. These classes contain all of the distribution’s parameters
      (including generation method). Refer to :ref:`onemkl_rng_distributions` for
      a detailed description of the distributions.

The RNG domain also contains two types of free functions:

   -  Generation routines. The current routines are used to obtain random
      numbers from a given engine with proper statistics defined by a
      given distribution. Refer to the :ref:`onemkl_rng_generate_routine`
      section for a detailed description.
   -  Service routines. The routines are used to modify the engine state. Refer to :ref:`onemkl_rng_service_routines` for a
      description of these routines.


Engine classes work with both generation and service routines. Distribution classes are used in
generation routines only. Refer to the :ref:`onemkl_rng_usage_model`
section for the description of typical RNG scenario.
