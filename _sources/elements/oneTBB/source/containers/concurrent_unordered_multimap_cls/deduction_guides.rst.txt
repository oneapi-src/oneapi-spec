.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

================
Deduction guides
================

Where possible, constructors of ``concurrent_unordered_multimap`` support
class template argument deduction (since C++17):

.. code:: cpp

    template <typename InputIterator,
              typename Hash = std::hash<iterator_key_t<InputIterator>>,
              typename KeyEqual = std::equal_to<iterator_key_t<InputIterator>>,
              typename Allocator = tbb_allocator<iterator_alloc_value_t<InputIterator>>>
    concurrent_unordered_multimap( InputIterator, InputIterator,
                                   map_size_type = /*implementation_defined*/,
                                   Hash = Hash(), KeyEqual = KeyEqual(),
                                   Allocator = Allocator() )
    -> concurrent_unordered_multimap<iterator_key_t<InputIterator>,
                                     iterator_mapped_t<InputIterator>,
                                     Hash, KeyEqual, Allocator>;

    template <typename InputIterator,
              typename Allocator>
    concurrent_unordered_multimap( InputIterator, InputIterator,
                              map_size_type,
                              Allocator )
    -> concurrent_unordered_multimap<iterator_key_t<InputIterator>,
                                     iterator_mapped_t<InputIterator>,
                                     std::hash<iterator_key_t<InputIterator>>,
                                     std::equal_to<iterator_key_t<InputIterator>>,
                                     Allocator>;

    template <typename InputIterator,
              typename Allocator>
    concurrent_unordered_multimap( InputIterator, InputIterator, Allocator )
    -> concurrent_unordered_multimap<iterator_key_t<InputIterator>,
                                     iterator_mapped_t<InputIterator>,
                                     std::hash<iterator_key_t<InputIterator>>,
                                     std::equal_to<iterator_key_t<InputIterator>>,
                                     Allocator>;

    template <typename InputIterator,
              typename Hash,
              typename Allocator>
    concurrent_unordered_multimap( InputIterator, InputIterator,
                              Hash, Allocator )
    -> concurrent_unordered_multimap<iterator_key_t<InputIterator>,
                                     iterator_mapped_t<InputIterator>,
                                     Hash,
                                     std::equal_to<iterator_key_t<InputIterator>>,
                                     Allocator>;

    template <typename Key,
              typename T,
              typename Hash = std::hash<Key>,
              typename KeyEqual = std::equal_to<Key>,
              typename Allocator = tbb_allocator<std::pair<Key, T>>>
    concurrent_unordered_multimap( std::initializer_list<value_type>,
                                   map_size_type = /*implementation-defined*/,
                                   Hash = Hash(),
                                   KeyEqual = KeyEqual(),
                                   Allocator = Allocator() )
    -> concurrent_unordered_multimap<Key, T,
                                     Hash,
                                     KeyEqual,
                                     Allocator>;

    template <typename Key,
              typename T,
              typename Allocator>
    concurrent_unordered_multimap( std::initializer_list<value_type>,
                                   map_size_type, Allocator )
    -> concurrent_unordered_multimap<Key, T,
                                     std::hash<Key>,
                                     std::equal_to<Key>,
                                     Allocator>;

    template <typename Key,
              typename T,
              typename Hash,
              typename Allocator>
    concurrent_unordered_multimap( std::initializer_list<value_type>,
                                   map_size_type, Hash, Allocator )
    -> concurrent_unordered_multimap<Key, T,
                                     Hash,
                                     std::equal_to<Key>,
                                     Allocator>;

Where the type ``map_size_type`` refers to the ``size_type`` member type of the deduced ``concurrent_multimap``
and the type aliases ``iterator_key_t``, ``iterator_mapped_t`` and ``iterator_alloc_value_t``
are defined as follows:

.. code:: cpp

    template <typename InputIterator>
    using iterator_key_t = std::remove_const_t<typename std::iterator_traits<InputIterator>::value_type::first_type>;

    template <typename InputIterator>
    using iterator_mapped_t = typename std::iterator_traits<InputIterator>::value_type::second_type;

    template <typename InputIterator>
    using iterator_alloc_value_t = std::pair<std::add_const_t<iterator_key_t<InputIterator>,
                            iterator_mapped_t<InputIterator>>>;

**Example**

.. code:: cpp

    #include <tbb/concurrent_unordered_map.h>
    #include <vector>
    #include <functional>

    struct CustomHasher {...};

    int main() {
        std::vector<std::pair<int, float>> v;

        // Deduces m1 as concurrent_unordered_multimap<int, float>
        tbb::concurrent_unordered_multimap m1(v.begin(), v.end());

        // Deduces m2 as concurrent_unordered_multimap<int, float, CustomHasher>;
        tbb::concurrent_unordered_multimap m2(v.begin(), v.end(), CustomHasher{});
    }
