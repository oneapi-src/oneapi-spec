.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_stats_raw_moment:

raw_moment
==========

Entry point to compute raw moments up to the 4th order.

.. _onemkl_stats_raw_moment_description:

.. rubric:: Description and Assumptions

The oneapi::mkl::stats::raw_moment function is used to compute array of raw moments up to the 4th order (raw moments for each dataset's dimension).

:ref:`onemkl_stats_raw_moment` supports the following precisions for data:

    .. list-table::
        :header-rows: 1

        * - T
        * - ``float``
        * - ``double``


.. _onemkl_stats_raw_moment_buffer:

oneapi::mkl::stats::raw_moment (buffer version)
-----------------------------------------------

.. rubric:: Syntax

.. code-block:: cpp

    namespace oneapi::mkl::stats {
    template<method Method = fast, typename Type, layout ObservationsLayout>
        void raw_moment(sycl::queue& queue,
        const dataset<ObservationsLayout, sycl::buffer<Type, 1>>& data,
        sycl::buffer<Type, 1> mean,
        sycl::buffer<Type, 1> raw_moment_2 = {0},
        sycl::buffer<Type, 1> raw_moment_3 = {0},
        sycl::buffer<Type, 1> raw_moment_4 = {0});
    }

.. container:: section

    .. rubric:: Template Parameters

    Method
        Method which is used for estimate computation. The specific values are as follows:

        *  ``oneapi::mkl::stats::method::fast``
        *  ``oneapi::mkl::stats::method::one_pass``

    Type
        Data precision.

    ObservationsLayout
        Data layout. The specific values are described in :ref:`onemkl_stats_dataset`.

.. container:: section

    .. rubric:: Input Parameters

    queue
        The queue where the routine should be executed.

    data
        Dataset which is used for computation.

.. container:: section

    .. rubric:: Output Parameters

    mean
        sycl::buffer array of mean values.

    raw_moment_2
        Optional parameter. sycl::buffer array of 2nd order raw moment values.

    raw_moment_3
        Optional parameter. sycl::buffer array of 3rd order raw moment values.

    raw_moment_4
        Optional parameter. sycl::buffer array of 4th order raw moment values.

.. container:: section

    .. rubric:: Throws

    oneapi::mkl::invalid_argument
        Exception is thrown when mean.get_count() == 0 & raw_moment_2.get_count() == 0 & raw_moment_3.get_count() == 0 & raw_moment_4.get_count() == 0, or dataset object is invalid

.. _onemkl_stats_raw_moment_usm:

raw_moment (USM version)
------------------------

.. rubric:: Syntax

.. code-block:: cpp

    namespace oneapi::mkl::stats {
    template<method Method = method::fast, typename Type, layout ObservationsLayout>
        sycl::event raw_moment(
        sycl::queue& queue,
        const dataset<ObservationsLayout, Type*>& data,
        Type* mean,
        Type* raw_moment_2 = nullptr,
        Type* raw_moment_3 = nullptr,
        Type* raw_moment_4 = nullptr,
        const sycl::vector_class<sycl::event> &dependencies = {});
    }

.. container:: section

    .. rubric:: Template Parameters

    Method
        Method which is used for estimate computation. The specific values are as follows:

        *  ``oneapi::mkl::stats::method::fast``
        *  ``oneapi::mkl::stats::method::one_pass``

    Type
        Data precision.

    ObservationsLayout
        Data layout. The specific values are described in :ref:`onemkl_stats_dataset`.

.. container:: section

    .. rubric:: Input Parameters

    queue
        The queue where the routine should be executed.

    data
        Dataset which is used for computation.

    dependencies
        Optional parameter. List of events to wait for before starting computation, if any.

.. container:: section

    .. rubric:: Output Parameters

    mean
        Pointer to the array of mean values.

    raw_moment_2
        Optional parameter. Pointer to the array of the 2nd order raw moment values.

    raw_moment_3
        Optional parameter. Pointer to the array of the 3rd order raw moment values.

    raw_moment_4
        Optional parameter. Pointer to the array of the 2nd order raw moment values.

.. container:: section

    .. rubric:: Throws

    oneapi::mkl::invalid_argument
        Exception is thrown when mean == nullptr & raw_moment_2 == nullptr & raw_moment_3 == nullptr & raw_moment_4 == nullptr, or dataset object is invalid

.. container:: section

    .. rubric:: Return Value

    Output event to wait on to ensure computation is complete.


**Parent topic:** :ref:`onemkl_stats_routines`

