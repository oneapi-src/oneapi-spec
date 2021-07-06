.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

================
Deduction guides
================

Where possible, constructors of ``concurrent_unordered_set`` support
class template argument deduction (since C++17):

.. code:: cpp

    template <typename InputIterator,
              typename Hash = std::hash<iterator_value_t<InputIterator>>,
              typename KeyEqual = std::equal_to<iterator_value_t<InputIterator>>,
              typename Allocator = tbb_allocator<iterator_value_t<InputIterator>>>
    concurrent_unordered_set( InputIterator, InputIterator,
                              map_size_type = /*implementation_defined*/,
                              Hash = Hash(), KeyEqual = KeyEqual(),
                              Allocator = Allocator() )
    -> concurrent_unordered_set<iterator_value_t<InputIterator>,
                                Hash, KeyEqual, Allocator>;

    template <typename InputIterator,
              typename Allocator>
    concurrent_unordered_set( InputIterator, InputIterator,
                              map_size_type,
                              Allocator )
    -> concurrent_unordered_set<iterator_value_t<InputIterator>,
                                std::hash<iterator_value_t<InputIterator>>,
                                std::equal_to<iterator_value_t<InputIterator>>,
                                Allocator>;

    template <typename InputIterator,
              typename Allocator>
    concurrent_unordered_set( InputIterator, InputIterator, Allocator )
    -> concurrent_unordered_set<iterator_value_t<InputIterator>,
                                std::hash<iterator_value_t<InputIterator>>,
                                std::equal_to<iterator_key_t<InputIterator>>,
                                Allocator>;

    template <typename InputIterator,
              typename Hash,
              typename Allocator>
    concurrent_unordered_set( InputIterator, InputIterator,
                              Hash, Allocator )
    -> concurrent_unordered_set<iterator_value_t<InputIterator>,
                                Hash,
                                std::equal_to<iterator_value_t<InputIterator>>,
                                Allocator>;

    template <typename T,
              typename Hash = std::hash<Key>,
              typename KeyEqual = std::equal_to<Key>,
              typename Allocator = tbb_allocator<std::pair<Key, T>>>
    concurrent_unordered_set( std::initializer_list<value_type>,
                              map_size_type = /*implementation-defined*/,
                              Hash = Hash(),
                              KeyEqual = KeyEqual(),
                              Allocator = Allocator() )
    -> concurrent_unordered_set<T,
                                Hash,
                                KeyEqual,
                                Allocator>;

    template <typename T,
              typename Allocator>
    concurrent_unordered_set( std::initializer_list<value_type>,
                              map_size_type, Allocator )
    -> concurrent_unordered_set<T,
                                std::hash<Key>,
                                std::equal_to<Key>,
                                Allocator>;

    template <typename T,
              typename Hash,
              typename Allocator>
    concurrent_unordered_set( std::initializer_list<value_type>,
                              map_size_type, Hash, Allocator )
    -> concurrent_unordered_set<T,
                                Hash,
                                std::equal_to<Key>,
                                Allocator>;

Where the type ``map_size_type`` refers to the ``size_type`` member type of the deduced ``concurrent_unordered_set``
and the type alias ``iterator_value_t`` is defined as follows:

.. code:: cpp

    template <typename InputIterator>
    using iterator_value_t = typename std::iterator_traits<InputIterator>::value_type;

**Example**

.. code:: cpp

    #include <tbb/concurrent_unordered_set.h>
    #include <vector>
    #include <functional>

    struct CustomHasher {...};

    int main() {
        std::vector<int> v;

        // Deduces s1 as concurrent_unordered_set<int>
        tbb::concurrent_unordered_set s1(v.begin(), v.end());

        // Deduces s2 as concurrent_unordered_set<int, CustomHasher>;
        tbb::concurrent_unordered_set s2(v.begin(), v.end(), CustomHasher{});
    }
