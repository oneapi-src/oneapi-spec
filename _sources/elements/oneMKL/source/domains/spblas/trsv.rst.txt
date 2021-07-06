.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_sparse_trsv:

trsv
====

Solves a system of linear equations for a triangular sparse matrix.

.. rubric:: Description and Assumptions

Refer to :ref:`onemkl_sparse_supported_types` for a
list of supported ``<fp>`` and ``<intType>``.
The oneapi::mkl::sparse::trsv routine solves a system of linear equations
for a square matrix:


.. math::

      \text{op}(A) y \leftarrow x

where: ``A`` is a triangular sparse matrix of size ``m`` rows by
``m`` columns, op is a matrix modifier for matrix ``A``, ``x`` and ``y`` are dense vectors of length at least
``m``.

.. _onemkl_sparse_trsv_buffer:

trsv (Buffer version)
---------------------

.. rubric:: Syntax

.. code-block:: cpp

   namespace oneapi::mkl::sparse {

      void trsv (sycl::queue                          &queue,
                 oneapi::mkl::uplo                    uplo_val
                 oneapi::mkl::transpose               transpose_val,
                 oneapi::mkl::diag                    diag_val
                 oneapi::mkl::sparse::matrix_handle_t A_handle,
                 sycl::buffer<fp, 1>                  &x,
                 sycl::buffer<fp, 1>                  &y);

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


   A_handle
      Handle to object containing sparse matrix :math:`A`. Created using the
      oneapi::mkl::sparse::set_csr_data routine.


   x
        SYCL memory object containing an array of size at least
        equal to the number of columns of  matrix :math:`\text{op}(A)`.


   y
        SYCL memory object containing an array of size at least
        equal to the number of rows of matrix :math:`\text{op}(A)`.


.. container:: section


    .. rubric:: Output Parameters
         :class: sectiontitle

    y
       SYCL memory object containing an array of size at least ``nRows`` filled with the solution to the system of linear equations.

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

.. _onemkl_sparse_trsv_usm:

trsv (USM version)
------------------

.. rubric:: Syntax

.. code-block:: cpp

   namespace oneapi::mkl::sparse {

      sycl::event trsv (sycl::queue                           &queue,
                        oneapi::mkl::uplo                     uplo_val
                        oneapi::mkl::transpose                transpose_val,
                        oneapi::mkl::diag                     diag_val
                        oneapi::mkl::sparse::matrix_handle_t  A_handle,
                        fp                                    *x,
                        fp                                    *y
                        const sycl::vector_class<sycl::event> &dependencies = {});

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


   A_handle
        Handle to object containing sparse matrix :math:`A`. Created using the
        oneapi::mkl::sparse::set_csr_data routine.


   x
        Device-accessible USM object containing an array of size at least
        equal to the number of columns of matrix :math:`\text{op}(A)`.


   y
        Device-accessible USM object containing an array of size at least
        equal to the number of rows of matrix :math:`\text{op}(A)`.


   dependencies
         List of events that oneapi::mkl::sparse::trmv routine depends on.
         If omitted, defaults to no dependencies.



.. container:: section


    .. rubric:: Output Parameters
         :class: sectiontitle

    y
       Device-accessible USM object containing an array of size at least ``nRows`` filled with the solution to the system of linear equations.

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
    dependency for the completion of trmv routine.

.. container:: familylinks


   .. container:: parentlink


      **Parent topic:** :ref:`onemkl_spblas`