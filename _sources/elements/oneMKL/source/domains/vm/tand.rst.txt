.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_vm_tand:

tand
====


.. container::


   Computes the tangent of vector elements multiplied by ``π``/180.


   .. container:: section


      .. rubric:: Syntax
         :class: sectiontitle


      Buffer API:


      .. code-block:: cpp


            namespace oneapi::mkl::vm {

            sycl::event tand(
                    sycl::queue& exec_queue,
                    std::int64_t n,
                    sycl::buffer<T,1>& a,
                    sycl::buffer<T,1>& y,
                    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
                    oneapi::mkl::vm::error_handler<T> errhandler = {});

            } // namespace oneapi::mkl::vm



      USM API:


      .. code-block:: cpp


            namespace oneapi::mkl::vm {

            sycl::event tand(
                    sycl::queue& exec_queue,
                    std::int64_t n,
                    T* a,
                    T* y,
                    sycl::vector_class<sycl::event> const & depends = {},
                    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
                    oneapi::mkl::vm::error_handler<T> errhandler = {});

            } // namespace oneapi::mkl::vm



      ``tand`` supports the following precisions.


      .. list-table::
         :header-rows: 1

         * - T
         * - ``float``
         * - ``double``




.. container:: section


   .. rubric:: Description
      :class: sectiontitle


   The tand(a) function computes the tangent of vector elements
   multiplied by ``π``/180. For an argument ``x``, the function computes
   tan(``π``\ \*\ ``x``/180).


   Note that arguments abs(``a``\ :sub:`i`) ≤ 2\ :sup:`38` for single
   precision or abs(``a``\ :sub:`i` ) ≤ 2\ :sup:`67` for double
   precision, they belong to the *fast computational path*:
   trigonometric function arguments for which VM provides the best
   possible performance. Avoid arguments with do not belong to the fast
   computational path in VM High Accuracy (HA) or Low Accuracy (LA)
   functions. For arguments which do not belong to the fast
   computational path you can use VM Enhanced Performance (EP)
   functions, which are fast on the entire function domain. However,
   these functions provide lower accuracy.


   .. container:: tablenoborder


      .. list-table::
         :header-rows: 1

         * - Argument
           - Result
           - Status code
         * - +0
           - +1
           -  
         * - -0
           - +1
           -  
         * - ±∞
           - QNAN
           - ``oneapi::mkl::vm::status::errdom``
         * - ±∞
           - QNAN
           - ``oneapi::mkl::vm::status::errdom``
         * - QNAN
           - QNAN
           -  
         * - SNAN
           - QNAN
           -  




.. container:: section


   .. rubric:: Input Parameters
      :class: sectiontitle


   Buffer API:


   exec_queue
      The queue where the routine should be executed.


   n
      Specifies the number of elements to be calculated.


   a
      The buffer ``a`` containing input vector of size ``n``.


   mode
      Overrides the global VM mode setting for this function call. See
      :ref:`onemkl_vm_setmode`
      function for possible values and their description. This is an
      optional parameter. The default value is ``oneapi::mkl::vm::mode::not_defined``.


   errhandler
      Sets local error handling mode for this function call. See the
      :ref:`onemkl_vm_create_error_handler`
      function for arguments and their descriptions. This is an optional
      parameter. The local error handler is disabled by default.


   USM API:


   exec_queue
      The queue where the routine should be executed.


   n
      Specifies the number of elements to be calculated.


   a
      Pointer ``a`` to the input vector of size ``n``.


   depends
      Vector of dependent events (to wait for input data to be ready).


   mode
      Overrides the global VM mode setting for this function call. See
      the :ref:`onemkl_vm_setmode`
      function for possible values and their description. This is an
      optional parameter. The default value is ``oneapi::mkl::vm::mode::not_defined``.


   errhandler
      Sets local error handling mode for this function call. See the
      :ref:`onemkl_vm_create_error_handler`
      function for arguments and their descriptions. This is an optional
      parameter. The local error handler is disabled by default.


.. container:: section


   .. rubric:: Output Parameters
      :class: sectiontitle


   Buffer API:


   y
      The buffer ``y`` containing the output vector of size ``n``.


   USM API:


   y
      Pointer ``y`` to the output vector of size ``n``.


   return value (event)
      Event, signifying availability of computed output and status code(s).

.. container:: section


    .. rubric:: Exceptions
        :class: sectiontitle

    For list of generated exceptions please refer to  :ref:`onemkl_vm_exceptions`


.. container:: familylinks


   .. container:: parentlink

      **Parent topic:** :ref:`onemkl_vm_mathematical_functions`


