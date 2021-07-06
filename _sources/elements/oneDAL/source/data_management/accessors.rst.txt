.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. highlight:: cpp
.. default-domain:: cpp

.. _accessors:

=========
Accessors
=========

This section defines :txtref:`requirements <accessor_reqs>` to an
:txtref:`accessor` implementation and introduces several
:txtref:`accessor_types`.

.. _accessor_reqs:

------------
Requirements
------------

Each accessor implementation shall:

1. Define a single :term:`format of the data <Data format>` for the
   access. Every accessor type shall return and use only one data format.

2. Provide read-only access to the data in the :txtref:`table` types.

3. Provide the :code:`pull()` method for obtaining the values from the table.

4. Be lightweight. Its constructors shall not have computationally intensive
   operations such data copy, reading, or conversion. These operations shall be
   performed by method :code:`pull()`. Support of copy- and move- constructors
   by the accessor is not required since it shall be designed for use in a local
   scope - directly in a place when it is created.

5. The :code:`pull()` method shall avoid data copy and conversion when it is
   possible to return the pointer to the memory block in the table. This is
   applicable for cases such as when the :capterm:`data format` and
   :capterm:`data types <data type>` of the data within the table are the same as the
   :capterm:`data format` and :capterm:`data type` for the access.


.. _accessor_types:

--------------
Accessor Types
--------------

|dal_short_name| defines a set of accessor classes. Each class supports one
specific way of obtaining data from the :txtref:`table`.

All accessor classes in |dal_short_name| are listed below:

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - Accessor type
     - Description
     - List of supported types
   * - :txtref:`row_accessor`
     - Provides access to the range of rows as one :term:`contiguous
       <Contiguous data>` :term:`homogeneous <Homogeneous data>` block of memory.
     - :txtref:`homogen_table`
   * - :txtref:`column_accessor`
     - Provides access to the range of values within a single column as one
       :term:`contiguous <Contiguous data>` :term:`homogeneous <Homogeneous
       data>` block of memory.
     - :txtref:`homogen_table`

-------
Details
-------

.. toctree::

   accessor/column.rst
   accessor/row.rst
