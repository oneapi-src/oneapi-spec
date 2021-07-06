.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

======
Lookup
======

All methods in this section can be executed concurrently with each other
and concurrently-safe modifiers.

find
----

    .. code:: cpp

        bool find( const_accessor& result, const key_type& key ) const;

        bool find( accessor& result, const key_type& key );

    If the accessor ``result`` is not empty, releases the ``result``.

    If an element with the key that is equivalent to ``key`` exists, sets the ``result`` to provide access
    to this element.

    **Returns**: ``true`` if an element with the key equivalent to  ``key`` is found; ``false``, otherwise.

count
-----

    .. code:: cpp

        size_type count( const key_type& key ) const;

    **Returns**: ``1`` if an element with the equivalent to ``key`` exists; ``0``, otherwise.
