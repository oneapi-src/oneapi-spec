.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

================
Deduction guides
================

Where possible, constructors of ``tbb::concurrent_priority_queue`` support class template argument
deduction (since C++17):

.. code:: cpp

    template <typename InputIterator>
    concurrent_priority_queue( InputIterator, InputIterator)
    -> concurrent_priority_queue<iterator_value_t<InputIterator>>>;

    template <typename InputIterator, typename Compare>
    concurrent_priority_queue( InputIterator, InputIterator, const Compare& )
    -> concurrent_priority_queue<iterator_value_t<InputIterator>,
                                 Compare>;

    template <typename InputIterator, typename Allocator>
    concurrent_priority_queue( InputIterator, InputIterator, const Allocator& alloc )
    -> concurrent_priority_queue<iterator_value_t<InputIterator>,
                                 std::less<iterator_value_t<InputIterator>,
                                 Allocator>;

    template <typename InputIterator, typename Compare, typename Allocator>
    concurrent_priority_queue( InputIterator, InputIterator, const Compare&,
                               const Allocator& )
    -> concurrent_priority_queue<iterator_value_t<InputIterator>,
                                 Compare, Allocator>;

    template <typename T>
    concurrent_priority_queue( std::initializer_list<T> )
    -> concurrent_priority_queue<T>;

    template <typename T, typename Compare>
    concurrent_priority_queue( std::initializer_list<T>, const Compare& )
    -> concurrent_priority_queue<T, Compare>;

    template <typename T, typename Allocator>
    concurrent_priority_queue( std::initializer_list<T>, const Allocator& )
    -> concurrent_priority_queue<T, std::less<T>, Allocator>;

    template <typename T, typename Compare, typename Allocator>
    concurrent_priority_queue( std::initializer_list<T>, const Compare&, const Allocator& )
    -> concurrent_priority_queue<T, Compare, Allocator>;

Where the type alias ``iterator_value_t`` is defined as follows:

.. code:: cpp

    template <typename InputIterator>
    using iterator_value_t = typename std::iterator_traits<InputIterator>::value_type;

**Example**

.. code:: cpp

    #include <tbb/concurrent_priority_queue.h>
    #include <vector>
    #include <functional>
    
    int main() {
        std::vector<int> vec;
        
        // Deduces cpq1 as tbb::concurrent_priority_queue<int>
        tbb::concurrent_priority_queue cpq1(vec.begin(), vec.end());
        
        // Deduces cpq2 as tbb::concurrent_priority_queue<int, std::greater>
        tbb::concurrent_priority_queue cpq2(vec.begin(), vec.end(), std::greater{});
    }
