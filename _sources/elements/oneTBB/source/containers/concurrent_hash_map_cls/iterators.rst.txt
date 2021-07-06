.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

=========
Iterators
=========

The types ``concurrent_hash_map::iterator`` and ``concurrent_hash_map::const_iterator``
meet the requirements of ``ForwardIterator`` from the [forward.iterators] ISO C++ Standard section.

All member functions in this section can only be performed serially.
The behavior is undefined in case of concurrent execution of these member functions
with other (either concurrently safe) methods.

begin and cbegin
----------------

    .. code:: cpp

        iterator begin();

        const_iterator begin() const;

        const_iterator cbegin() const;

    **Returns**: an iterator to the first element in the container.

end and cend
------------

    .. code:: cpp

        iterator end();

        const_iterator end() const;

        const_iterator cend() const;

    **Returns**: an iterator to the element that follows the last element in the container.

equal_range
-----------

    .. code:: cpp

        std::pair<iterator, iterator> equal_range( const key_type& key );

        std::pair<const_iterator, const_iterator> equal_range( const key_type& key ) const;

    If an element with the key that is equivalent to ``key`` exists in the container,
    a pair of iterators ``{f, l}``, where ``f`` is an iterator to this element,
    ``l`` is ``std::next(f)``.
    Otherwise, ``{end(), end()}``.
