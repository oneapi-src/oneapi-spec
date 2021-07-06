.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_sparse_supported_types:

Supported Types
===============


.. container::


   .. container:: tablenoborder


      .. list-table:: 
         :header-rows: 1

         * -  Data Types <fp> 
           -  Integer Types <intType> 
         * -  ``float`` 
           -  ``std::int32_t`` 
         * -  ``double`` 
           -  ``std::int64_t`` 
         * -  ``std::complex<float>`` 
           -    
         * -  ``std::complex<double>`` 
           -    


General descriptions
--------------------

.. _onemkl_sparse_matrix_handle_t:

.. rubric:: matrix_handle_t
   :name: matrix_handle_t

Type for the ``handle`` that can be used to store information about the initial sparse
matrix (represented in a sparse format) and data created/obtained during the analysis
stage to be used in the execution stage.