.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _homogen_table:

=================
Homogeneous table
=================

Class ``homogen_table`` is an implementation of a table type
for which the following is true:

- The data within the table are dense and stored as one contiguous memory block.
- All the columns have the same :capterm:`data type <Data type>`.

---------------------
Programming interface
---------------------

All types and functions in this section shall be declared in the
``oneapi::dal`` namespace and be available via inclusion of the
``oneapi/dal/table/homogen.hpp`` header file.

.. onedal_class:: oneapi::dal::homogen_table
