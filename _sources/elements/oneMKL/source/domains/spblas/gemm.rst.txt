.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_sparse_gemm:

gemm
====

Computes a sparse matrix times dense matrix product.

.. rubric:: Description and Assumptions

Refer to :ref:`onemkl_sparse_supported_types` for a list of supported ``<fp>`` and ``<intType>`` types. The oneapi::mkl::sparse::gemm routine computes a sparse matrix-dense
matrix product defined as

.. math::

   C \leftarrow \alpha \text{op}(A) B + \beta C

where :math:`\alpha` and :math:`\beta` are scalars, :math:`B` and :math:`C` are dense matrices and :math:`A` is a sparse matrix. Dense matrix storage is in row-major format. Sparse matrix formats are compressed sparse row (CSR) formats. 


.. _onemkl_sparse_gemm_buffer:

gemm (Buffer version)
---------------------

.. rubric:: Syntax

.. code-block:: cpp

   namespace oneapi::mkl::sparse {

      void gemm (sycl::queue                          &queue, 
                 oneapi::mkl::transpose               transpose_val, 
                 const fp                             alpha, 
                 oneapi::mkl::sparse::matrix_handle_t A_handle, 
                 sycl::buffer<fp, 1>                  &B, 
                 const std::int64_t                   columns, 
                 const std::int64_t                   ldb, 
                 const fp                             beta, 
                 sycl::buffer<fp, 1>                  &C, 
                 const std::int64_t                   ldc);

   }



.. container:: section

    .. rubric:: Input parameters

    queue
         Specifies the SYCL command queue which will be used for SYCL
         kernels execution.


    transpose_val
         Specifies operation ``op()`` on input matrix. The possible options
         are described in :ref:`onemkl_enum_transpose` enum class.


    alpha
         Specifies the scalar :math:`\alpha`.


    A_handle
         Handle to object containing sparse matrix, :math:`A`. Created using the oneapi::mkl::sparse::set_csr_data routine.


    B
         The dense matrix in the sparse-dense matrix product. A one dimensional SYCL memory object containing an array of size at least ``cols*ldb``, where ``cols`` = the number of columns of matrix :math:`op(A)`.

    columns
         Number of columns of matrix, :math:`C`.


    ldb
         Specifies the leading dimension of matrix, :math:`B`. Should be greater than or equal to the number of columns of :math:`B` which is ``columns``.


    beta
         Specifies the scalar ``beta``.


    C
         The dense matrix input/output array.  A one-dimensional SYCL memory object containing an array of size at least ``rows*ldc``, where ``rows`` = the number of rows
         of matrix :math:`op(A)`.

    ldc
         Specifies the leading dimension of matrix :math:`C` . Must be greater than or equal to the number of columns of :math:`C` which is ``columns``.


.. container:: section

    .. rubric:: Output Parameters
         :class: sectiontitle


    C
       Dense matrix output is overwritten by the updated matrix, :math:`C`.

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

.. _onemkl_sparse_gemm_usm:

gemm (USM version)
---------------------

.. rubric:: Syntax

.. code-block:: cpp

   namespace oneapi::mkl::sparse {

      sycl::event gemm (sycl::queue                           &queue, 
                        oneapi::mkl::transpose                transpose_val, 
                        const fp                              alpha, 
                        oneapi::mkl::sparse::matrix_handle_t  A_handle, 
                        const fp                              *B, 
                        const std::int64_t                    columns, 
                        const std::int64_t                    ldb, 
                        const fp                              beta, 
                        const fp                              *C, 
                        const std::int64_t                    ldc,
                        const sycl::vector_class<sycl::event> &dependencies = {});

   }


.. container:: section

    .. rubric:: Input parameters

    queue
         Specifies the SYCL command queue which will be used for SYCL
         kernels execution.


    transpose_val
         Specifies operation ``op()`` on input matrix. The possible options
         are described in :ref:`onemkl_enum_transpose` enum class.

    alpha
         Specifies the scalar :math:`\alpha`.

    A_handle
         Handle to object containing sparse matrix, :math:`A`. Created using the oneapi::mkl::sparse::set_csr_data routine.

    B 
         The dense matrix in the sparse-dense matrix product. A device accessible USM object containing an array of size at least ``cols*ldb``, where ``cols`` = the number of columns of matrix :math:`op(A)`.

    columns
         Number of columns of matrix :math:`C`.

    ldb
         Specifies the leading dimension of matrix :math:`B`. Should be greater than or equal to the number of columns of :math:`B`.

    beta
         Specifies the scalar ``beta``.

    C
         The dense matrix input/output array.  A device accessible USM object containing an array of size at least ``rows*ldc``, where ``rows`` = the number of rows
         of matrix :math:`op(A)`.

    ldc
         Specifies the leading dimension of matrix :math:`C` . Must be greater than or equal to ``columns``.

    dependencies
         List of events that oneapi::mkl::sparse::gemm routine depends on.
         If omitted, defaults to no dependencies.

.. container:: section

    .. rubric:: Output Parameters
         :class: sectiontitle


    C
       Dense matrix output is overwritten by the updated matrix :math:`C`.


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
    dependency for the completion of gemm routine.


.. container:: familylinks


   .. container:: parentlink


      **Parent topic:** :ref:`onemkl_spblas`
