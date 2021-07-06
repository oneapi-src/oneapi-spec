.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_sparse_format_descriptions:

Sparse storage formats
======================

.. container:: section

    .. _onemkl_sparse_csr:

    .. rubric:: CSR

    There are a variety of matrix storage formats available for
    representing the sparse matrix. One of the most popular is
    compressed sparse row (CSR) format, that is represented by
    three arrays: *row_ptr*, *col_ind* and *val*, and *index*
    parameter.

    .. container:: tablenoborder

         .. list-table::

            * - num_rows
              - Number of rows in the sparse matrix.
            * - num_cols
              - Number of columns in the sparse matrix.
            * - index
              - Parameter that is used to specify whether the matrix has zero or one-based indexing.
            * - val
              - An array that contains the non-zero elements of the sparse matrix stored row by row.
            * - col_ind
              - An integer array of column indices for non-zero elements stored in the *val* array,
                such that *col_ind[i]* is the column number (using zero- or one-based indexing) of the
                element of the sparse matrix stored in *val[i]*.
            * - row_ptr
              - An integer array of size equal to ``num_rows + 1``.  Element j of this integer array
                gives the position of the element in the *val* array that is first non-zero element in a
                row j of A. Note that this position is equal to *row_ptr[j] - index*. Last element of
                the *row_ptr* array (*row_ptr[num_rows]*) stores the sum of,
                number of nonzero elements and *index*(number of nonzero elements + *index*).


A sparse matrix can be represented in a CSR format in a following way (assuming zero-based indexing):

.. math::
   A = \left(\begin{matrix}
             1 &  0 & 2\\
             0 & -1 & 4\\
             3 &  0 & 0\\
             \end{matrix}\right)


+------------+------------------------------------------------------------+
| num_rows   | 3                                                          |
+------------+------------------------------------------------------------+
| num_cols   | 3                                                          |
+------------+------------------------------------------------------------+
| index      | 0                                                          |
+------------+------------+-----------+-----------+-----------+-----------+
| val        | 1          | 2         | -1        | 4         | 3         |
+------------+------------+-----------+-----------+-----------+-----------+
| col_ind    | 0          | 2         | 1         | 2         | 0         |
+------------+------------+-----------+-----------+-----------+-----------+
| row_ptr    | 0          | 2         | 4         | 5         |           |
+------------+------------+-----------+-----------+-----------+-----------+


.. container:: familylinks


   .. container:: parentlink


      **Parent topic:** :ref:`onemkl_spblas`