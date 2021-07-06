.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_stats_kurtosis:

kurtosis
========

Entry point to compute kurtosis.

.. _onemkl_stats_kurtosis_description:

.. rubric:: Description and Assumptions

The oneapi::mkl::stats::kurtosis function is used to compute a kurtosis array (kurtosis for each dataset's dimension).

:ref:`onemkl_stats_kurtosis` supports the following precisions for data:

    .. list-table::
        :header-rows: 1

        * - T
        * - ``float``
        * - ``double``


.. _onemkl_stats_kurtosis_buffer:

kurtosis (buffer version)
-------------------------

.. rubric:: Syntax

.. code-block:: cpp

    namespace oneapi::mkl::stats {
        template<method Method = method::fast, typename Type, layout ObservationsLayout>
        void kurtosis(sycl::queue& queue,
        const dataset<ObservationsLayout, sycl::buffer<Type, 1>>& data,
        sycl::buffer<Type, 1> kurtosis);
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

    kurtosis
        sycl::buffer array of kurtosis values.

.. container:: section

    .. rubric:: Throws

    oneapi::mkl::invalid_argument
        Exception is thrown when kurtosis.get_count() == 0, or dataset object is invalid

.. _onemkl_stats_kurtosis_usm:

kurtosis (USM version)
----------------------

.. rubric:: Syntax

.. code-block:: cpp

    namespace oneapi::mkl::stats {
    template<method Method = method::fast, typename Type, layout ObservationsLayout>
        sycl::event kurtosis(sycl::queue& queue,
        const dataset<ObservationsLayout, Type*>& data,
        Type* kurtosis,
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

    kurtosis
        Pointer to the array of kurtosis values.

.. container:: section

    .. rubric:: Throws

    oneapi::mkl::invalid_argument
        Exception is thrown when kurtosis == nullptr, or dataset object is invalid

.. container:: section

    .. rubric:: Return Value

    Output event to wait on to ensure computation is complete.


**Parent topic:** :ref:`onemkl_stats_routines`

