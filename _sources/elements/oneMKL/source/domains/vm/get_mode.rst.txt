.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_vm_get_mode:

get_mode
========


.. container::


   Gets the VM mode.


   .. container:: section


      .. rubric:: Syntax
         :class: sectiontitle

      .. code-block:: cpp


            namespace oneapi::mkl::vm {

                oneapi::mkl::vm::mode get_mode(
                    sycl::queue& exec_queue);

            } // namespace oneapi::mkl::vm




      .. rubric:: Description
         :class: sectiontitle


      The function get_mode function returns the global VM ``mode``
      parameter that controls accuracy for a given queue.

      .. list-table::
         :header-rows: 1

         * - Value of mode
           - Description
         * - Accuracy Control
           -
         * - ``oneapi::mkl::vm::mode::ha``
           - High accuracy versions of VM functions.
         * - ``oneapi::mkl::vm::mode::la``
           - Low accuracy versions of VM functions.
         * - ``oneapi::mkl::vm::mode::ep``
           - Enhanced performance accuracy versions of VM functions.
         * - ``oneapi::mkl::vm::mode::not_defined``
           - VM mode not defined. It means that no special provisions
             for accuracy have been made for this queue.
             See :ref:`onemkl_vm_setmode` for details.


.. container:: section


   .. rubric:: Input Parameters
      :class: sectiontitle


   exec_queue
      The queue where the routine should be executed.


.. container:: section


   .. rubric:: Output Parameters
      :class: sectiontitle


   return value
      The current global VM mode for the queue ``exec_queue``.


.. container:: familylinks


   .. container:: parentlink

      **Parent topic:** :ref:`onemkl_vm_service_functions`
