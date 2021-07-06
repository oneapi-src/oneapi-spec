.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_vm_trunc:

trunc
=====


.. container::


   Computes an integer value rounded towards zero for each vector
   element.


   .. container:: section


      .. rubric:: Syntax
         :class: sectiontitle


      Buffer API:


      .. code-block:: cpp


            namespace oneapi::mkl::vm {

            sycl::event trunc(
                    sycl::queue& exec_queue,
                    std::int64_t n,
                    sycl::buffer<T,1>& a,
                    sycl::buffer<T,1>& y,
                    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

            } // namespace oneapi::mkl::vm



      USM API:


      .. code-block:: cpp


            namespace oneapi::mkl::vm {

            sycl::event trunc(
                    sycl::queue& exec_queue,
                    std::int64_t n,
                    T* a,
                    T* y,
                    sycl::vector_class<sycl::event> const & depends = {},
                    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

            } // namespace oneapi::mkl::vm



      ``trunc`` supports the following precisions.


      .. list-table::
         :header-rows: 1

         * - T
         * - ``float``
         * - ``double``




.. container:: section


   .. rubric:: Description
      :class: sectiontitle


   The trunc(a) function computes an integer value rounded towards zero for
   each vector element.

   .. math::
      y_i =
      \begin{cases}
         \lfloor a_i \rfloor , a_i \geq 0 \\
         \lceil  a_i \rceil  , a_i <    0
      \end{cases}


   .. container:: tablenoborder


      .. list-table::
         :header-rows: 1

         * - Argument
           - Result
           - Status code
         * - +0
           - +0
           -  
         * - -0
           - -0
           -  
         * - +∞
           - +∞
           -  
         * - -∞
           - -∞
           -  
         * - QNAN
           - QNAN
           -  
         * - SNAN
           - QNAN
           -  




   The trunc function does not generate any errors.


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
