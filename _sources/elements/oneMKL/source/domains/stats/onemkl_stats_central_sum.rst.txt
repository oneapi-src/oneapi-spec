.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_stats_central_sum:

central_sum
===========

Entry point to compute central sums up to the 4th order.

.. _onemkl_stats_central_sum_description:

.. rubric:: Description and Assumptions

The oneapi::mkl::stats::central_sum function is used to compute an array of central sums up to the 4th order (central sums for each dataset's dimension).

:ref:`onemkl_stats_central_sum` supports the following precisions for data:

    .. list-table::
        :header-rows: 1

        * - T
        * - ``float``
        * - ``double``


.. _onemkl_stats_central_sum_buffer:

central_sum (Buffer version)
----------------------------

.. rubric:: Syntax

.. code-block:: cpp

    namespace oneapi::mkl::stats {
    template<method Method = method::fast, typename Type, layout ObservationsLayout>
        void central_sum(sycl::queue& queue,
        const dataset<ObservationsLayout, sycl::buffer<Type, 1>>& data,
        sycl::buffer<Type, 1> central_sum_2,
        sycl::buffer<Type, 1> central_sum_3 = {0},
        sycl::buffer<Type, 1> central_sum_4 = {0});
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

    central_sum_2
        sycl::buffer array of 2nd order central sum values.

    central_sum_3
        Optional parameter. sycl::buffer array of 3rd order central sum values.

    central_sum_4
        Optional parameter. sycl::buffer array of 4th order central sum values.

.. container:: section

    .. rubric:: Throws

    oneapi::mkl::invalid_argument
        Exception is thrown when central_sum_2.get_count() == 0 & central_sum_3.get_count() == 0 & central_sum_4.get_count() == 0, or dataset object is invalid

.. _onemkl_stats_central_sum_usm:

central_sum (USM version)
-------------------------

.. rubric:: Syntax

.. code-block:: cpp

    namespace oneapi::mkl::stats {
    template<method Method = method::fast, typename Type, layout ObservationsLayout>
        sycl::event central_sum(
        sycl::queue& queue,
        const dataset<ObservationsLayout, Type*>& data,
        Type* central_sum_2,
        Type* central_sum_3 = nullptr,
        Type* central_sum_4 = nullptr,
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

    central_sum_2
        Pointer to the array of the 2nd order central sum values.

    central_sum_3
        Optional parameter. Pointer to the array of the 3rd order central sum values.

    central_sum_4
        Optional parameter. Pointer to the array of the 2nd order central sum values.

.. container:: section

    .. rubric:: Throws

    oneapi::mkl::invalid_argument
        Exception is thrown when central_sum_2 == nullptr & central_sum_3 == nullptr & central_sum_4 == nullptr, or dataset object is invalid

.. container:: section

    .. rubric:: Return Value

    Output event to wait on to ensure computation is complete.


**Parent topic:** :ref:`onemkl_stats_routines`

