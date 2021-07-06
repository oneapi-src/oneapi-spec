.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

=======================
Common type definitions
=======================

This section describes common types used in |dal_short_name|.

---------------------
Programming interface
---------------------

All types and functions in this section shall be declared in the
``oneapi::dal`` namespace and be available via inclusion of the
``oneapi/dal/common.hpp`` header file.

.. _scalar_types:

Scalar types
------------

|dal_short_name| relies on the use of integral types defined in ``<cstdint>``.
This file shall be included in ``oneapi/dal/common.hpp`` and all
|dal_short_name| types shall use these data types.

The interfaces of the library shall use ``std::int64_t`` data type to represent
dimensionality (for example, the number of rows and columns in the table).

It is recommended to use standard C++ types for applications as well.

Enum classes
------------

Which base type to use when defining ``enum`` or ``enum class`` representing a
|dal_short_name| concept is up to the implementer unless specification requires
a specific base type.

Data type
---------

The implementation of :capterm:`data type` concept. It shall enumerate all the
data types supported by |dal_short_name| to perform computations. The
``data_type`` class shall contain all the base :txtref:`scalar_types` and can also
extend them. Base scalar types include the types whose names follow the pattern
``std::int_XX_t`` or ``std::uint_XX_t``, where XX is 8, 16, 32, or 64.

.. onedal_enumclass:: oneapi::dal::data_type


Range
-----

A range ``[start_index, end_index)`` in an array or any other container that
supports value indexing.

.. onedal_class:: oneapi::dal::range
