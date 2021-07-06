.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_stats_skewness_user_mean:

skewness with provided mean
===========================

Entry point to compute skewness with the provided mean values.

.. _onemkl_stats_skewness_user_mean_description:

.. rubric:: Description and Assumptions

The oneapi::mkl::stats::skewness function is used to compute an array of skewness (skewness for each dataset's dimension) with the provided mean values.

:ref:`onemkl_stats_skewness_user_mean` supports the following precisions for data:

    .. list-table::
        :header-rows: 1

        * - T
        * - ``float``
        * - ``double``


.. _onemkl_stats_skewness_user_mean_buffer:

skewness with provided mean (buffer version)
--------------------------------------------

.. rubric:: Syntax

.. code-block:: cpp

    namespace oneapi::mkl::stats {
    template<method Method = method::fast, typename Type, layout ObservationsLayout>
        void skewness(sycl::queue& queue,
        sycl::buffer<Type, 1> mean,
        const dataset<ObservationsLayout, sycl::buffer<Type, 1>>& data,
        sycl::buffer<Type, 1> skewness);
    }

.. container:: section

    .. rubric:: Template Parameters

    Method
        Method which is used for estimate computation. The specific values are as follows:

        *  ``oneapi::mkl::stats::method::fast``

    Type
        Data precision.

    ObservationsLayout
        Data layout. The specific values are described in :ref:`onemkl_stats_dataset`.

.. container:: section

    .. rubric:: Input Parameters

    queue
        The queue where the routine should be executed.

    mean
        sycl::buffer to the array of provided mean values.

    data
        Dataset which is used for computation.

.. container:: section

    .. rubric:: Output Parameters

    skewness
        sycl::buffer array of skewness values.

.. container:: section

    .. rubric:: Throws

    oneapi::mkl::invalid_argument
        Exception is thrown when skewness.get_count() == 0, or mean.get_count() == 0, or dataset object is invalid

.. _onemkl_stats_skewness_user_mean_usm:

skewness with provided mean (USM version)
-----------------------------------------

.. rubric:: Syntax

.. code-block:: cpp

    namespace oneapi::mkl::stats {
    template<method Method = method::fast, typename Type, layout ObservationsLayout>
        sycl::event skewness(sycl::queue& queue,
        Type* mean,
        const dataset<ObservationsLayout, Type*>& data,
        Type* skewness,
        const sycl::vector_class<sycl::event> &dependencies = {});
    }

.. container:: section

    .. rubric:: Template Parameters

    Method
        Method which is used for estimate computation. The specific values are as follows:

        *  ``oneapi::mkl::stats::method::fast``

    Type
        Data precision.

    ObservationsLayout
        Data layout. The specific values are described in :ref:`onemkl_stats_dataset`.

.. container:: section

    .. rubric:: Input Parameters

    queue
        The queue where the routine should be executed.

    mean
        Pointer to the array of provided mean values.

    data
        Dataset which is used for computation.

    dependencies
        Optional parameter. List of events to wait for before starting computation, if any.

.. container:: section

    .. rubric:: Output Parameters

    skewness
        Pointer to the array of the skewness values.

.. container:: section

    .. rubric:: Throws

    oneapi::mkl::invalid_argument
        Exception is thrown when skewness == nullptr, or mean == nullptr, or dataset object is invalid

.. container:: section

    .. rubric:: Return Value

    Output event to wait on to ensure computation is complete.


**Parent topic:** :ref:`onemkl_stats_routines`

