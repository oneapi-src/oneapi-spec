.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_sparse_trmv:

trmv
====

Computes a sparse matrix-dense vector product over upper or lower triangular matrix parts.

.. rubric:: Description and Assumptions

Refer to :ref:`onemkl_sparse_supported_types` for a
list of supported ``<fp>`` and ``<intType>``.
The oneapi::mkl::sparse::trmv routine computes a sparse matrix-dense vector
product over a triangular part defined as

.. math::

      y \leftarrow \alpha \text{op}(A) x + \beta y


where: :math:`alpha` and :math:`beta` are scalars, :math:`x` and :math:`y` are dense vectors, ``A`` is a sparse matrix.


.. _onemkl_sparse_trmv_buffer:

trmv (Buffer version)
---------------------

.. rubric:: Syntax

.. code-block:: cpp

   namespace oneapi::mkl::sparse {

      void trmv (sycl::queue                          &queue,
                 oneapi::mkl::uplo                    uplo_val
                 oneapi::mkl::transpose               transpose_val,
                 oneapi::mkl::diag                    diag_val
                 fp                                   alpha,
                 oneapi::mkl::sparse::matrix_handle_t A_handle,
                 sycl::buffer<fp, 1>                  &x,
                 fp                                   beta,
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


   alpha
        Specifies the scalar :math:`\alpha`.


   A_handle
      Handle to object containing sparse matrix :math:`A`. Created using the
      oneapi::mkl::sparse::set_csr_data routine.


   x
        SYCL memory object containing an array of size at least
        equal to the number of columns of matrix :math:`\text{op}(A)`.


   beta
        Specifies the scalar :math:`\beta`.


   y
        SYCL memory object containing an array of size at least
        equal to the number of rows of matrix :math:`\text{op}(A)`.


.. container:: section


    .. rubric:: Output Parameters
         :class: sectiontitle


    y
       Overwritten by the updated vector ``y``.

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

.. _onemkl_sparse_trmv_usm:

trmv (USM version)
------------------

.. rubric:: Syntax

.. code-block:: cpp

   namespace oneapi::mkl::sparse {

      sycl::event trmv (sycl::queue                           &queue,
                        oneapi::mkl::uplo                     uplo_val
                        oneapi::mkl::transpose                transpose_val,
                        oneapi::mkl::diag                     diag_val
                        fp                                    alpha,
                        oneapi::mkl::sparse::matrix_handle_t  A_handle,
                        fp                                    *x,
                        fp                                    beta,
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


   alpha
        Specifies the scalar :math:`\alpha`.


   A_handle
        Handle to object containing sparse matrix :math:`A`. Created using the
        oneapi::mkl::sparse::set_csr_data routine.


   x
        Device-accessible USM object containing an array of size at least
        equal to the number of columns of matrix :math:`\text{op}(A)`.



   beta
        Specifies the scalar :math:`\beta`.


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
       Overwritten by the updated vector ``y``.

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