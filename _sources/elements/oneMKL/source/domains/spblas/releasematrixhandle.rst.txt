.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_sparse_release_matrix_handle:

release_matrix_handle
=====================


Releases internal data and sets matrix_handle_t object to NULL.


.. rubric:: Description and Assumptions

The oneapi::mkl::sparse::release_matrix_handle releases any internal data that the
``matrix_handle_t`` object holds and sets it with defaults values, otherwise it
throws an exception. The routine also waits for the dependencies to be finished
before releasing any data in case of USM.


.. rubric:: Syntax


.. code-block:: cpp

   namespace oneapi::mkl::sparse {

      void release_matrix_handle (oneapi::mkl::sparse::matrix_handle_t  handle,
                                  const sycl::vector_class<sycl::event> &dependencies = {});

   }

.. container:: section


    .. rubric:: Input parameter


    handle
       Handle to object containing sparse matrix and other internal
       data. Created using one of the
       oneapi::mkl::sparse::set_<sparse_matrix_type>_structure routines.

    dependencies
       List of events that ``handle`` depends on.
       The call waits on the events(if any) before resetting the ``handle`` to default values.


.. container:: section

    .. rubric:: Throws
         :class: sectiontitle

    This routine shall throw the following exceptions if the associated condition is detected.
    An implementation may throw additional implementation-specific exception(s)
    in case of error conditions not covered here.

    | :ref:`oneapi::mkl::device_bad_alloc<onemkl_exception_device_bad_alloc>`
    | :ref:`oneapi::mkl::host_bad_alloc<onemkl_exception_host_bad_alloc>`
    | :ref:`oneapi::mkl::invalid_argument<onemkl_exception_invalid_argument>`
    | :ref:`oneapi::mkl::unimplemented<onemkl_exception_unimplemented>`
    | :ref:`oneapi::mkl::uninitialized<onemkl_exception_uninitialized>`
    | :ref:`oneapi::mkl::unsupported_device<onemkl_exception_unsupported_device>`

.. container:: familylinks


   .. container:: parentlink


      **Parent topic:** :ref:`onemkl_spblas`