.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_vm_erfinv:

erfinv
======


.. container::


   Computes inverse error function value of vector elements.


   .. container:: section


      .. rubric:: Syntax
         :class: sectiontitle


      Buffer API:


      .. code-block:: cpp


            namespace oneapi::mkl::vm {

            sycl::event erfinv(
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

            sycl::event erfinv(
                    sycl::queue& exec_queue,
                    std::int64_t n,
                    T* a,
                    T* y,
                    sycl::vector_class<sycl::event> const & depends = {},
                    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
                    oneapi::mkl::vm::error_handler<T> errhandler = {});

            } // namespace oneapi::mkl::vm



      ``erfinv`` supports the following precisions.


      .. list-table::
         :header-rows: 1

         * - T
         * - ``float``
         * - ``double``




.. container:: section


   .. rubric:: Description
      :class: sectiontitle


   The erfinv(a) function computes the inverse error function values for
   elements of the input vector ``a`` and writes them to the output
   vector ``y``.


   .. math::
      y_i = \operatorname{erf}^{-1}(a)


   | where :math:`\operatorname{erf}(x)` is the error function defined as given by:


   .. math::
      \operatorname{erf}(x) = \frac{2}{\sqrt{\pi}} \int_0^x e^{-t^2} \operatorname{d \!} t


   Useful relations for these functions:

   .. math::
      \operatorname{erfcinv}(x) = \operatorname{erfinv}(1 - x)


   .. math::
      \operatorname{cdfnorminv}(x) &= \sqrt{2} \operatorname{erfinv}(2x - 1) \\
                                   &= \sqrt{2} \operatorname{erfcinv}(2 - 2x)

   .. math::
      \operatorname{erf}^{-1}(x) = \operatorname{erfc}^{-1}(1 - x)

   where :math:`\operatorname{erfc}` is the complementary error function.


   .. math::
      \Phi(x) = \frac{1}{2} \left( 1 + \operatorname{erf}\left(x / \sqrt{2}\right) \right)


   where

   .. math::
      \Phi(x) = \frac{1}{\sqrt{2\pi}} \int_0^x \exp(-t^2/2) \operatorname{d \!} t

   is the cumulative normal distribution function.


   .. math::
      \Phi^{-1}(x) = \sqrt{2} \operatorname{erf}^{-1}(2x - 1)


   where :math:`\Phi^{-1}(x)` and :math:`\operatorname{erf}^{-1}(x)` are the inverses to
   :math:`\Phi(x)` and :math:`\operatorname{erf}(x)`, respectively.

   The following figure illustrates the relationships among erfinv
   family functions (erfinv, erfcinv, cdfnorminv).


   .. container:: figtop


      erfinv Family Functions Relationship
      |


      .. container:: imagecenter


         |image0|


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
         * - +1
           - +∞
           - ``oneapi::mkl::vm::status::sing``
         * - -1
           - -∞
           - ``oneapi::mkl::vm::status::sing``
         * - \|a\| > 1
           - QNAN
           - ``oneapi::mkl::vm::status::errdom``
         * - +∞
           - QNAN
           - ``oneapi::mkl::vm::status::errdom``
         * - -∞
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



.. |image0| image:: ../equations/GUID-8C1F2803-8F8F-4795-BF16-41856C6442CF-low.jpg
