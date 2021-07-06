.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_vm_set_status:

set_status
==========


.. container::


   Sets the global VM status according to new value and returns the
   previous VM status.


   .. container:: section


      .. rubric:: Syntax
         :class: sectiontitle


      .. code-block:: cpp

            namespace oneapi::mkl::vm {

                oneapi::mkl::vm::status set_status(
                    sycl::queue& exec_queue,
                    oneapi::mkl::vm::status new_status);

            } // namespace oneapi::mkl::vm


      .. rubric:: Description
         :class: sectiontitle


      The set_status function sets the global VM status to new value and
      returns the previous VM status code for a given queue.


      The global VM status is a single value and it registers the bitwise-OR of status codes 
      that happened inside VM functions run on the specific queue.
      For performance reasons, it might be done in non-atomic manner.
      The possible status codes are listed in the table below.


      .. list-table::
         :header-rows: 1

         * - Status
           - Description
         * - Successful Execution
           -
         * - ``oneapi::mkl::vm::status::success``
           - VM function execution completed successfully
         * - ``oneapi::mkl::vm::status::not_defined``
           - VM status not defined
         * - Warnings
           -
         * - ``oneapi::mkl::vm::status::accuracy_warning``
           - VM function execution completed successfully in a different accuracy mode
         * - Computational status codes
           -
         * - ``oneapi::mkl::vm::status::errdom``
           - Values are out of a range of definition producing invalid (QNaN) result
         * - ``oneapi::mkl::vm::status::sing``
           - Values cause divide-by-zero (singularity) computational errors and produce and invalid (QNaN or Inf) result
         * - ``oneapi::mkl::vm::status::overflow``
           - An overflow happened during the calculation process
         * - ``oneapi::mkl::vm::status::underflow``
           - An underflow happened during the calculation process




.. container:: section


   .. rubric:: Input Parameters
      :class: sectiontitle


   exec_queue
      The queue where the routine should be executed.


   new_status
      Specifies the VM status to be set.


.. container:: section


   .. rubric:: Output Parameters
      :class: sectiontitle


   return value (old_status)
      Specifies the former VM status.


.. container:: familylinks


   .. container:: parentlink

      **Parent topic:** :ref:`onemkl_vm_service_functions`


