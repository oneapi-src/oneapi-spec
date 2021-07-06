.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_spblas:

Sparse BLAS
---------------

.. container::

   Sparse BLAS Routines provide basic operations on sparse vectors and matrices

.. container:: tablenoborder


      .. list-table::
         :header-rows: 1

         * -     Routines
           -     Description
         * -     :ref:`onemkl_sparse_init_matrix_handle`
           -     Initialize the sparse matrix handle
         * -     :ref:`onemkl_sparse_release_matrix_handle`
           -     Release the sparse matrix handle
         * -     :ref:`onemkl_sparse_set_csr_data`
           -     Fills the internal CSR data structure
         * -     :ref:`onemkl_sparse_optimize_gemv`
           -     Optimize routine for gemv
         * -     :ref:`onemkl_sparse_optimize_trmv`
           -     Optimize routine for trmv
         * -     :ref:`onemkl_sparse_optimize_trsv`
           -     Optimize routine for trsv
         * -     :ref:`onemkl_sparse_gemv`
           -     Sparse matrix-dense vector product using a general sparse matrix
         * -     :ref:`onemkl_sparse_gemvdot`
           -     Sparse matrix-dense vector product followed by dot product
         * -     :ref:`onemkl_sparse_symv`
           -     Sparse matrix-dense vector product using a symmetric sparse matrix
         * -     :ref:`onemkl_sparse_trmv`
           -     Sparse matrix-dense vector product using a triangular sparse matrix
         * -     :ref:`onemkl_sparse_trsv`
           -     Solving a linear system with a triangular sparse matrix
         * -     :ref:`onemkl_sparse_gemm`
           -     Sparse matrix-dense matrix product using a general sparse matrix


.. container::

     - :ref:`onemkl_sparse_format_descriptions`

.. toctree::
    :hidden:

    matrixinit
    releasematrixhandle
    setcsrstructure
    gemm
    gemv
    gemvdot
    gemvoptimize
    symv
    trmv
    trmvoptimize
    trsv
    trsvoptimize
    supported-types
    format-descriptions

**Parent topic:** :ref:`onemkl_sparse_linear_algebra`
