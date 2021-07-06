.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

==========
task_group
==========
**[scheduler.task_group]**

A ``task_group`` represents concurrent execution of a group of tasks.
Tasks can be dynamically added to the group while it is executing.

.. code:: cpp

    // Defined in header <tbb/task_group.h>

    namespace tbb {

        class task_group {
        public:
            task_group();
            ~task_group();

            template<typename Func>
            void run( Func&& f );

            template<typename Func>
            task_group_status run_and_wait( const Func& f );

            task_group_status wait();
            void cancel();
        };

        bool is_current_task_group_canceling();

    } // namespace tbb

Member functions
----------------

.. namespace:: tbb::task_group

.. cpp:function:: task_group()

    Constructs an empty ``task_group``.

.. cpp:function:: ~task_group()

    Destroys the ``task_group``.

    **Requires**: Method ``wait`` must be called before destroying a ``task_group``,
    otherwise, the destructor throws an exception.

.. cpp:function:: template<typename Func> void run( Func&& f )

    Adds a task to compute ``f()`` and returns immediately.
    The ``Func`` type must meet the `Function Objects` requirements from [function.objects] ISO C++ Standard section.

.. cpp:function:: template<typename Func> task_group_status run_and_wait( const Func& f )

    Equivalent to ``{run(f); return wait();}``, but guarantees that ``f()`` runs on the current thread.
    The ``Func`` type must meet the `Function Objects` requirements from the [function.objects] ISO C++ Standard section.

    **Returns**: The status of ``task_group``. See :doc:`task_group_status <task_group_status_enum>`.

.. cpp:function:: task_group_status wait()

    Waits for all tasks in the group to complete or be cancelled.

    **Returns**: The status of ``task_group``. See :doc:`task_group_status <task_group_status_enum>`.

.. cpp:function:: void cancel()

    Cancels all tasks in this ``task_group``.

Non-member functions
--------------------

.. cpp:function:: bool is_current_task_group_canceling()

    Returns true if an innermost ``task_group`` executing on this thread is cancelling its tasks.

