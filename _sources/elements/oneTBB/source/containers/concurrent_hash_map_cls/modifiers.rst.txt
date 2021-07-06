.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

===========================
Concurrently safe modifiers
===========================

All methods in this section can be executed concurrently with each other
and lookup methods.

Inserting values
----------------

    .. code:: cpp

        bool insert( const_accessor& result, const key_type& key );

        bool insert( accessor& result, const key_type& key );

    If the accessor ``result`` is not empty, releases the ``result`` and
    attempts to insert the value constructed from ``key, mapped_type()`` into the container.

    Sets the ``result`` to provide access to the inserted element or to the element with equal key
    that was already presented in the container.

    **Requirements**:

    * the type ``value_type`` must meet the ``EmplaceConstructible`` requirements the from [container.requirements] ISO C++ Standard section.
    * the type ``mapped_type`` must meet the ``DefaultConstructible`` requirements from the [defaultconstructible] ISO C++ Standard section.

    **Returns**: ``true`` if an element was inserted; ``false``, otherwise.

--------------------------

    .. code:: cpp

        bool insert( const_accessor& result, const value_type& value );

        bool insert( accessor& result, const value_type& value );

    If the accessor ``result`` is not empty, releases the ``result`` and
    attempts to insert the value ``value`` into the container.

    Sets the ``result`` to provide access to the inserted element or to the element with equal key
    that was already presented in the container.

    **Requirements**: the type ``value_type`` must meet the ``CopyInsertable`` requirements from the
    [container.requirements] ISO C++ Standard section.

    **Returns**: ``true`` if an element was inserted; ``false``, otherwise.

--------------------------

    .. code:: cpp

        bool insert( const value_type& value );

    Attempts to insert the value ``value`` into the container.

    **Requirements**: the type ``value_type`` must meet the ``CopyInsertable`` requirements from the
    [container.requirements] ISO C++ Standard section.

    **Returns**: ``true`` if an element was inserted; ``false``, otherwise.

--------------------------

    .. code:: cpp

        bool insert( const_accessor& result, value_type&& value );

        bool insert( accessor& result, value_type&& value );

    If the accessor ``result`` is not empty, releases the ``result`` and
    attempts to insert the value ``value`` into the container using move semantics.

    Sets the ``result`` to provide access to the inserted element or to the element with equal key
    that was already presented in the container.

    ``value`` is left in a valid, but unspecified state.

    **Requirements**: the type ``value_type`` must meet the ``MoveInsertable`` requirements from the
    [container.requirements] ISO C++ Standard section.

    **Returns**: ``true`` if an element was inserted; ``false``, otherwise.

--------------------------

    .. code:: cpp

        bool insert( value_type&& value );

    Attempts to insert the value ``value`` into the container using move semantics.

    **Requirements**: the type ``value_type`` must meet the ``MoveInsertable`` requirements from the
    [container.requirements] ISO C++ Standard section.

    **Returns**: ``true`` if an element was inserted; ``false``, otherwise.

Inserting sequences of elements
-------------------------------

    .. code:: cpp

        template <typename InputIterator>
        void insert( InputIterator first, InputIterator last );

    Attempts to insert all items from the half-open interval ``[first, last)``
    into the container.

    If the interval ``[first, last)`` contains multiple elements with equal keys,
    it is unspecified which element should be inserted.

    **Requirements**: the type ``InputIterator`` must meet the requirements of `InputIterator`
    from the ``[input.iterators]`` ISO C++ Standard section.

--------------------------

    .. code:: cpp

        void insert( std::initializer_list<value_type> init );

    Equivalent to ``insert(init.begin(), init.end())``.

Emplacing elements
------------------

    .. code:: cpp

        template <typename... Args>
        bool emplace( const_accessor& result, Args&&... args );

        template <typename... Args>
        bool emplace( accessor& result, Args&&... args );

    If the accessor ``result`` is not empty, releases the ``result`` and
    attempts to insert an element constructed in-place from ``args`` into the container.

    Sets the ``result`` to provide access to the inserted element or to the element with equal key
    that was already presented in the container.

    **Requirements**: the type ``value_type`` must meet the ``EmplaceConstructible`` requirements from the
    [container.requirements] ISO C++ Standard section.

    **Returns**: ``true`` if an element was inserted; ``false``, otherwise

--------------------------

    .. code:: cpp

        template <typename... Args>
        bool emplace( Args&&... args );

    Attempts to insert an element constructed in-place from ``args`` into the container.

    **Requirements**: the type ``value_type`` must meet the ``EmplaceConstructible`` requirements from the
    [container.requirements] ISO C++ Standard section.

    **Returns**: ``true`` if an element was inserted; ``false``, otherwise

Erasing elements
----------------

    .. code:: cpp

        bool erase( const key_type& key );

    If an element with the key equivalent to  ``key`` exists, removes it from the container.

    **Returns**: ``true`` if an element was removed; ``false``, otherwise.

--------------------------

    .. code:: cpp

        bool erase( const_accessor& item_accessor );
        bool erase( accessor& item_accessor );

    Removes an element owned by ``item_accessor`` from the container.

    **Requirements**: ``item_accessor`` should not be empty.

    **Returns**: ``true`` if an element was removed by the current thread; ``false``
    if it was removed by another thread.
