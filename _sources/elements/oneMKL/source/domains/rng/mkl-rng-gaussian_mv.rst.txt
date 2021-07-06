.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_rng_gaussian_mv:

gaussian_mv
===========

Class is used for generation of multivariate normally distributed real types random numbers.

.. _onemkl_rng_gaussian_mv_description:

.. rubric:: Description

The class object is used in the :ref:`oneapi::mkl::rng::generate()<onemkl_rng_generate>` function to provide n random numbers :math:`d`-variate normally distributed, with mean :math:`a` and variance-covariance matrix :math:`C`, where :math:`a \in R^d;` :math:`C` is dxd symmetric positive matrix.

The probability density function is given by:

.. math::

    f_{a, C}(x) = \frac{1}{\sqrt{det(2\pi C)}}exp(-1 / 2(x - a)^T C^{-1}(x-a)).

.. _onemkl_rng_gaussian_mv_syntax:

class gaussian_mv
-----------------

.. rubric:: Syntax

.. code-block:: cpp

    namespace oneapi::mkl::rng {
    template<typename RealType = std::int32_t, layout Layout = layout::packed, typename Method = gaussian_mv_method::by_default>
    class gaussian_mv {
    public:
        using method_type = Method;
        using result_type = RealType;
        explicit gaussian_mv(std::uint32_t dimen, std::vector<RealType> mean, std::vector<RealType> matrix);
        std::int32_t dimen() const;
        std::vector<RealType> mean() const;
        std::vector<RealType> matrix() const;
    };
    }

.. container:: section

    .. rubric:: Template parameters

    .. container:: section

        typename RealType
            Type of the produced values. Supported types:
                * ``float``
                * ``double``

    .. rubric:: Template parameters

    .. container:: section

        oneapi::mkl::rng::layout Layout
            Matrix layout:
                * ``oneapi::mkl::rng::layout::full``
                * ``oneapi::mkl::rng::layout::packed``
                * ``oneapi::mkl::rng::layout::diagonal``

    .. container:: section

        typename Method = oneapi::mkl::rng::gaussian_mv_method::by_default
            Transformation method, which will be used for generation. Supported types:

                * ``oneapi::mkl::rng::gaussian_mv_method::by_default``
                * ``oneapi::mkl::rng::gaussian_mv_method::box_muller``
                * ``oneapi::mkl::rng::gaussian_mv_method::box_muller2``
                * ``oneapi::mkl::rng::gaussian_mv_method::icdf``

            See description of the methods in :ref:`Distributions methods template parameter<onemkl_rng_distributions_template_parameter_mkl_rng_method_values>`.

.. container:: section

    .. rubric:: Class Members

    .. list-table::
        :header-rows: 1

        * - Routine
          - Description
        * - `explicit gaussian_mv(std::uint32_t dimen, std::vector<RealType> mean, std::vector<RealType> matrix)`_
          - Constructor with parameters
        * - `std::int32_t dimen() const`_
          - Method to obtain number of dimensions in output random vectors
        * - `std::vector<double> mean() const`_
          - Method to obtain mean vector `a` of dimension d.
        * - `std::vector<double> matrix() const`_
          - Method to obtain variance-covariance matrix `C`

.. container:: section

    .. rubric:: Member types

    .. container:: section

        .. code-block:: cpp

            gaussian_mv::method_type = Method

        .. container:: section

            .. rubric:: Description

            The type which defines transformation method for generation.

    .. container:: section

        .. code-block:: cpp

            gaussian_mv::result_type = RealType

        .. container:: section

            .. rubric:: Description

            The type which defines type of generated random numbers.

.. container:: section

    .. rubric:: Constructors

    .. container:: section

        .. _`explicit gaussian_mv(std::uint32_t dimen, std::vector<RealType> mean, std::vector<RealType> matrix)`:

        .. code-block:: cpp

            explicit gaussian_mv::gaussian_mv(std::uint32_t dimen, std::vector<RealType> mean, std::vector<RealType> matrix)

        .. container:: section

            .. rubric:: Description

            Constructor with parameters. `dimen` is the number of dimensions, `mean` is a mean vector, `matrix` is a variance-covariance matrix.

        .. container:: section

            .. rubric:: Throws

            oneapi::mkl::invalid_argument
                Exception is thrown when :math:`mean.size() \leq 0`, or :math:`matrix.size() \leq 0`

.. container:: section

    .. rubric:: Characteristics

    .. container:: section

        .. _`std::int32_t dimen() const`:

        .. code-block:: cpp

            std::int32_t gaussian_mv::dimen() const

        .. container:: section

            .. rubric:: Return Value

            Returns the distribution parameter `dimen`.

    .. container:: section

        .. _`std::vector<double> mean() const`:

        .. code-block:: cpp

            std::vector<double> gaussian_mv::mean() const

        .. container:: section

            .. rubric:: Return Value

            Returns the mean vector.

    .. container:: section

        .. _`std::vector<double> matrix() const`:

        .. code-block:: cpp

            std::vector<double> gaussian_mv::matrix() const

        .. container:: section

            .. rubric:: Return Value

            Returns the variance-covariance matrix.

**Parent topic:** :ref:`onemkl_rng_distributions`
