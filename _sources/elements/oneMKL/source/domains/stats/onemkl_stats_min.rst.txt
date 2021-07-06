.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_stats_min:

min
===

Entry point to compute min values.

.. _onemkl_stats_min_description:

.. rubric:: Description and Assumptions

The oneapi::mkl::stats::min function is used to compute min arrays (min value for each dataset's dimension).

:ref:`onemkl_stats_min` supports the following precisions for data:

    .. list-table::
        :header-rows: 1

        * - T
        * - ``float``
        * - ``double``


.. _onemkl_stats_min_buffer:

min (buffer version)
--------------------

.. rubric:: Syntax

.. code-block:: cpp

    namespace oneapi::mkl::stats {
    template<method Method = fast, typename Type, layout ObservationsLayout>
        void min(sycl::queue& queue,
        const dataset<ObservationsLayout, sycl::buffer<Type, 1>>& data,
        sycl::buffer<Type, 1> min);
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

    data
        Dataset which is used for computation.

.. container:: section

    .. rubric:: Output Parameters

    min
        sycl::buffer array of min values.

.. container:: section

    .. rubric:: Throws

    oneapi::mkl::invalid_argument
        Exception is thrown when min.get_count() == 0, or dataset object is invalid

.. _onemkl_stats_min_usm:

min (USM version)
-----------------

.. rubric:: Syntax

.. code-block:: cpp

    namespace oneapi::mkl::stats {
    template<method Method = fast, typename Type, layout ObservationsLayout>
        sycl::event min(sycl::queue& queue,
        const dataset<ObservationsLayout, Type*>& data,
        Type* min,
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

    data
        Dataset which is used for computation.

    dependencies
        Optional parameter. List of events to wait for before starting computation, if any.

.. container:: section

    .. rubric:: Output Parameters

    min
        Pointer to the array of min values.

.. container:: section

    .. rubric:: Throws

    oneapi::mkl::invalid_argument
        Exception is thrown when min == nullptr, or dataset object is invalid

.. container:: section

    .. rubric:: Return Value

    Output event to wait on to ensure computation is complete.


**Parent topic:** :ref:`onemkl_stats_routines`

