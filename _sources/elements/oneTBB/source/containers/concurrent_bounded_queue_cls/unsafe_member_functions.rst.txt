.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

====================================
Concurrently unsafe member functions
====================================

All member functions in this section can only be performed serially. The behavior is undefined in
case of concurrent execution of these methods with other (either concurrently safe) methods.

The number of elements
----------------------

    .. code:: cpp

        size_type size() const;

    **Returns**: the number of elements in the container.

----------------------------

    .. code:: cpp

        bool empty() const;

    **Returns**: ``true`` if the container is empty; ``false``, otherwise.

clear
-----

    .. code:: cpp

        void clear();

    Removes all elements from the container.
