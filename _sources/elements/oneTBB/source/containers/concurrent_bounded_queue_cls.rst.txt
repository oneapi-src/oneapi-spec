.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

========================
concurrent_bounded_queue
========================
**[containers.concurrent_bounded_queue]**

``tbb::concurrent_bounded_queue`` is a class template for a bounded first-in-first-out data structure
that permits multiple threads to concurrently push and pop items.

Class Template Synopsis
-----------------------

.. code:: cpp

    // Defined in header <tbb/concurrent_queue.h>

    namespace tbb {

        template <typename T, typename Allocator = cache_aligned_allocator<T>>
        class concurrent_bounded_queue {
        public:
            using value_type = T;
            using reference = T&;
            using const_reference = const T&;
            using pointer = typename std::allocator_traits<Allocator>::pointer;
            using const_pointer = typename std::allocator_traits<Allocator>::const_pointer;

            using allocator_type = Allocator;

            using size_type = <implementation-defined signed integer type>;
            using difference_type = <implementation-defined signed integer type>;

            using iterator = <implementation-defined ForwardIterator>;
            using const_iterator = <implementation-defined constant ForwardIterator>;

            concurrent_bounded_queue();

            explicit concurrent_bounded_queue( const allocator_type& alloc );

            template <typename InputIterator>
            concurrent_bounded_queue( InputIterator first, InputIterator last,
                                      const allocator_type& alloc = allocator_type() );

            concurrent_bounded_queue( const concurrent_bounded_queue& other );
            concurrent_bounded_queue( const concurrent_bounded_queue& other,
                                      const allocator_type& alloc );

            concurrent_bounded_queue( concurrent_bounded_queue&& other );
            concurrent_bounded_queue( concurrent_bounded_queue&& other,
                                      const allocator_type& alloc );

            ~concurrent_bounded_queue();

            allocator_type get_allocator() const;

            void push( const value_type& value );
            void push( value_type&& value );

            bool try_push( const value_type& value );
            bool try_push( value_type&& value );

            template <typename... Args>
            void emplace( Args&&... args );

            template <typename... Args>
            bool try_emplace( Args&&... args );

            void pop( value_type& result );

            bool try_pop( value_type& result );

            void abort();

            size_type size() const;

            bool empty() const;

            size_type capacity() const;
            void set_capacity( size_type new_capacity );

            void clear();

            iterator unsafe_begin();
            const_iterator unsafe_begin() const;
            const_iterator unsafe_cbegin() const;

            iterator unsafe_end();
            const_iterator unsafe_end() const;
            const_iterator unsafe_cend() const;
        }; // class concurrent_bounded_queue

    } // namespace tbb

Requirements:

* The type ``T`` must meet the ``Erasable`` requirements from the [container.requirements] ISO C++
  Standard section. Member functions can impose stricter requirements depending on the type of the operation.
* The type ``Allocator`` must meet the ``Allocator`` requirements from the [allocator.requirements] ISO C++ Standard section.

Member functions
----------------

.. toctree::
    :maxdepth: 1

    concurrent_bounded_queue_cls/construct_destroy_copy.rst
    concurrent_bounded_queue_cls/safe_member_functions.rst
    concurrent_bounded_queue_cls/unsafe_member_functions.rst
    concurrent_bounded_queue_cls/iterators.rst

Other
-----

.. toctree::
    :maxdepth: 1

    concurrent_bounded_queue_cls/deduction_guides.rst
