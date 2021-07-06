.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

================
Deduction guides
================

Where possible, constructors of ``concurrent_multimap`` support class template argument
deduction (since C++17):

.. code:: cpp

    template <typename InputIterator,
              typename Compare = std::less<iterator_key_t<InputIterator>>,
              typename Allocator = tbb_allocator<iterator_alloc_value_t<InputIterator>>>
    concurrent_multimap( InputIterator, InputIterator, Compare = Compare(), Allocator = Allocator() )
    -> concurrent_multimap<iterator_key_t<InputIterator>,
                           iterator_mapped_t<InputIterator>,
                           Compare,
                           Allocator>;

    template <typename InputIterator,
              typename Allocator>
    concurrent_multimap( InputIterator, InputIterator, Allocator )
    -> concurrent_multimap<iterator_key_t<InputIterator>,
                           iterator_mapped_t<InputIterator>,
                           std::less<iterator_key_t<InputIterator>>,
                           Allocator>;

    template <typename Key,
              typename T,
              typename Compare = std::less<Key>,
              typename Allocator = tbb_allocator<std::pair<const Key, T>>>
    concurrent_multimap( std::initializer_list<std::pair<Key, T>>, Compare = Compare(), Allocator = Allocator() )
    -> concurrent_multimap<Key, T, Compare, Allocator>;

    template <typename Key,
              typename T,
              typename Allocator>
    concurrent_multimap( std::initializer_list<std::pair<Key, T>>, Allocator )
    -> concurrent_multimap<Key, T, std::less<Key>, Allocator>;

where the type aliases ``iterator_key_t``, ``iterator_mapped_t``, ``iterator_alloc_value_t`` are defined as follows:

.. code:: cpp

    template <typename InputIterator>
    using iterator_key_t = std::remove_const_t<typename std::iterator_traits<InputIterator>::value_type::first_type>;

    template <typename InputIterator>
    using iterator_mapped_t = typename std::iterator_traits<InputIterator>::value_type::second_type;

    template <typename InputIterator>
    using iterator_alloc_value_t = std::pair<std::add_const_t<iterator_key_t<InputIterator>>,
                                             iterator_mapped_t<InputIterator>>;

**Example**

.. code:: cpp

  #include <tbb/concurrent_map.h>
  #include <vector>

  int main() {
      std::vector<std::pair<int, float>> v;

      // Deduces cm1 as concurrent_multimap<int, float>
      tbb::concurrent_multimap cm1(v.begin(), v.end());

      // Deduces cm2 as concurrent_multimap<int, float>
      tbb::concurrent_multimap cm2({std::pair(1, 2f), std::pair(2, 3f)});
  }
