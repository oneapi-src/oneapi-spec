.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_sparse_optimize_trsv:

optimize_trsv
=============

Performs internal optimizations for oneapi::mkl::sparse::trsv by analyzing
the matrix structure.

.. rubric:: Description and Assumptions

The oneapi::mkl::sparse::optimize_trsv routine analyzes matrix structure
and performs optimizations. Optimized data is then stored in
the handle.


.. _onemkl_sparse_optimize_trsv_buffer:

optimize_trsv (Buffer version)
------------------------------

.. rubric:: Syntax

.. code-block:: cpp

   namespace oneapi::mkl::sparse {

      void optimize_trsv (sycl::queue                          &queue,
                          oneapi::mkl::uplo                    uplo_val,
                          oneapi::mkl::transpose               transpose_val,
                          oneapi::mkl::diag                    diag_val,
                          oneapi::mkl::sparse::matrix_handle_t handle);
   }

.. container:: section


   .. rubric:: Input Parameters


   queue
        Specifies the SYCL command queue which will be used for SYCL
        kernels execution.


   uplo_val
        Specifies which part is to be processed. The possible options are
        described in :ref:`onemkl_enum_uplo` enum class.


   transpose_val
         Specifies operation ``op()`` on input matrix. The possible options
         are described in :ref:`onemkl_enum_transpose` enum class.


   diag_val
            Specifies if the diagonal is unit or not. The possible options
            are described in :ref:`onemkl_enum_diag` enum class.


   handle
      Handle to object containing sparse matrix and other internal
      data. Created using the
      oneapi::mkl::sparse::set_csr_data routine.


.. container:: section

    .. rubric:: Throws
         :class: sectiontitle

    This routine shall throw the following exceptions if the associated condition is detected.
    An implementation may throw additional implementation-specific exception(s)
    in case of error conditions not covered here.

    | :ref:`oneapi::mkl::computation_error<onemkl_exception_computation_error>`
    | :ref:`oneapi::mkl::device_bad_alloc<onemkl_exception_device_bad_alloc>`
    | :ref:`oneapi::mkl::host_bad_alloc<onemkl_exception_host_bad_alloc>`
    | :ref:`oneapi::mkl::invalid_argument<onemkl_exception_invalid_argument>`
    | :ref:`oneapi::mkl::unimplemented<onemkl_exception_unimplemented>`
    | :ref:`oneapi::mkl::uninitialized<onemkl_exception_uninitialized>`
    | :ref:`oneapi::mkl::unsupported_device<onemkl_exception_unsupported_device>`

.. _onemkl_sparse_optimize_trsv_usm:

optimize_trmv (USM version)
------------------------------

.. rubric:: Syntax


.. code-block:: cpp

   namespace oneapi::mkl::sparse {

      sycl::event optimize_trsv (sycl::queue                          &queue,
                                 oneapi::mkl::uplo                    uplo_val,
                                 oneapi::mkl::transpose               transpose_val,
                                 oneapi::mkl::diag                    diag_val,
                                 oneapi::mkl::sparse::matrix_handle_t handle,
                                 sycl::vector_class<sycl::event>      &dependencies);
   }

.. container:: section


   .. rubric:: Input Parameters


   queue
        Specifies the SYCL command queue which will be used for SYCL
        kernels execution.


   uplo_val
        Specifies which part is to be processed. The possible options are
        described in :ref:`onemkl_enum_uplo` enum class.


   transpose_val
         Specifies operation ``op()`` on input matrix. The possible options
         are described in :ref:`onemkl_enum_transpose` enum class.


   diag_val
            Specifies if the diagonal is unit or not. The possible options
            are described in :ref:`onemkl_enum_diag` enum class.


   handle
      Handle to object containing sparse matrix and other internal
      data. Created using the
      oneapi::mkl::sparse::set_csr_data routine.


   dependencies
       List of events that oneapi::mkl::sparse::optimize_trsv routine depends on.


.. container:: section

    .. rubric:: Throws
         :class: sectiontitle

    This routine shall throw the following exceptions if the associated condition is detected.
    An implementation may throw additional implementation-specific exception(s)
    in case of error conditions not covered here.

    | :ref:`oneapi::mkl::computation_error<onemkl_exception_computation_error>`
    | :ref:`oneapi::mkl::device_bad_alloc<onemkl_exception_device_bad_alloc>`
    | :ref:`oneapi::mkl::host_bad_alloc<onemkl_exception_host_bad_alloc>`
    | :ref:`oneapi::mkl::invalid_argument<onemkl_exception_invalid_argument>`
    | :ref:`oneapi::mkl::unimplemented<onemkl_exception_unimplemented>`
    | :ref:`oneapi::mkl::uninitialized<onemkl_exception_uninitialized>`
    | :ref:`oneapi::mkl::unsupported_device<onemkl_exception_unsupported_device>`

.. container:: section

    .. rubric:: Return Values
       :class: sectiontitle

    Output event that can be waited upon or added as a
    dependency for the completion of optimize_trsv routine.


.. container:: familylinks


   .. container:: parentlink


      **Parent topic:** :ref:`onemkl_spblas`