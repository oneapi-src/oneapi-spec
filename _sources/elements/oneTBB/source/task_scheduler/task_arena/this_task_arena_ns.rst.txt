.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

===============
this_task_arena
===============
**[scheduler.this_task_arena]**

The namespace for functions applicable to the current ``task_arena``.

The namespace ``this_task_arena`` contains global functions for interaction
with the ``task_arena`` currently used by the calling thread.

.. code:: cpp

    // Defined in header <tbb/task_arena.h>

    namespace tbb {
        namespace this_task_arena {
            int current_thread_index();
            int max_concurrency();
            template<typename F> auto isolate(F&& f) -> decltype(f());
        }
    }

.. cpp:function:: int current_thread_index()

    Returns the thread index in a ``task_arena`` currently used by the calling thread,
    or ``task_arena::not_initialized`` if the thread has not yet initialized the task scheduler.

    A thread index is an integer number between 0 and the ``task_arena`` concurrency level.
    Thread indexes are assigned to both application threads and worker threads on joining an arena and are kept until exiting the arena.
    Indexes of threads that share an arena are unique, that is, no two threads within the arena can have the same
    index at the same time - but not necessarily consecutive.

    .. note::

        Since a thread may exit the arena at any time if it does not execute a task, the
        index of a thread may change between any two tasks, even those belonging to the
        same task group or algorithm.

    .. note::

        Threads that use different arenas may have the same current index value.

    .. note::

        Joining a nested arena in ``execute()`` may change current index
        value while preserving the index in the outer arena which will be restored on return.

.. cpp:function:: int max_concurrency()

    Returns the concurrency level of the ``task_arena`` currently used by the calling thread.
    If the thread has not yet initialized the task scheduler, returns the concurrency level
    determined automatically for the hardware configuration.

.. cpp:function:: template<F> auto isolate(F&& f) -> decltype(f())

    Runs the specified functor in isolation by restricting the calling thread to process only tasks
    scheduled in the scope of the functor (also called the isolation region). The function returns the value returned by the functor.
    The ``F`` type must meet the `Function Objects` requirements from the [function.objects] ISO C++ Standard section.

    .. caution::

        The object returned by the functor cannot be a reference. ``std::reference_wrapper`` can be used instead.

