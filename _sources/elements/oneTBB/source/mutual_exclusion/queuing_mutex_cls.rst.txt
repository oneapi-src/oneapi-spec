.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

=============
queuing_mutex
=============
**[mutex.queuing_mutex]**

A ``queuing_mutex`` is a class that models the :doc:`Mutex requirement <../named_requirements/mutexes/mutex>`. The ``queuing_mutex`` is not recursive.
The ``queuing_mutex`` is fair, threads acquire a lock on a mutex in the order that they request it.

.. code:: cpp

    // Defined in header <tbb/queuing_mutex.h>

    namespace tbb {
        class queuing_mutex {
        public:
            queuing_mutex() noexcept;
            ~queuing_mutex();

            queuing_mutex(const queuing_mutex&) = delete;
            queuing_mutex& operator=(const queuing_mutex&) = delete;

            class scoped_lock;

            static constexpr bool is_rw_mutex = false;
            static constexpr bool is_recursive_mutex = false;
            static constexpr bool is_fair_mutex = true;
        };
    }

Member classes
--------------

.. namespace:: tbb::queueing_mutex
	       
.. cpp:class:: scoped_lock

    Corresponding ``scoped_lock`` class. See the :doc:`Mutex requirement <../named_requirements/mutexes/mutex>`.

Member functions
----------------

.. cpp:function:: queuing_mutex()

    Constructs unlocked ``queuing_mutex``.

.. cpp:function:: ~queuing_mutex()

    Destroys unlocked ``queuing_mutex``.

