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
            struct traits {
                bool ignore_outer_cancellation{false};
            };

            task_group();
            task_group(traits t);
            ~task_group();

            template<typename Func>
            void run( Func&& f );

            template<typename Func>
            task_group_status run_and_wait( const Func& f );

            template<typename Func>
            task_handle make_task( Func&& f );

            void run( task_handle&& th );
            task_group_status run_and_wait( task_handle&& th );

            task_group_status wait();
            void cancel();
        };

        bool is_current_task_group_canceling();

    } // namespace tbb


Member types and constants
--------------------------

.. cpp:struct:: traits

    Represents properties of the ``task_group``.

    .. cpp:bool:: ignore_outer_cancellation

       If equals to ``true``, the created ``task_group`` object ignores cancellation requests from
       outer context.

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

    Adds a task to compute ``f()`` and returns immediately. The ``Func`` type must meet the
    :doc:`TaskGroupFunc requirements <../../named_requirements/task_scheduler/task_group_func>`.

.. cpp:function:: template<typename Func> task_group_status run_and_wait( const Func& f )

    Equivalent to ``{run(f); return wait();}``, but guarantees that ``f()`` runs on the current
    thread. The ``Func`` type must meet the :doc:`TaskGroupFunc requirements
    <../../named_requirements/task_scheduler/task_group_func>`.

    **Returns**: The status of ``task_group``. See :doc:`task_group_status <task_group_status_enum>`.

.. cpp:function:: template<typename Func> task_handle make_task( Func&& f )

    Creates a task that is associated with ``task_handle`` to compute ``f()``, but does not make it
    available for execution. See the :doc:`task_handle <task_handle>`. The ``Func`` type must meet
    the :doc:`TaskGroupFunc requirements <../../named_requirements/task_scheduler/task_group_func>`.

    **Returns**: ``task_handle`` that must be passed to either method ``run`` or ``run_and_wait``.

.. cpp:function:: void run( task_handle&& th )

    Makes the task associated with ``th`` available for execution and returns immediately.

.. cpp:function:: task_group_status run_and_wait( task_handle&& th )

    Equivalent to ``{run(th); return wait();}``, but guarantees that the task associated with ``th``
    runs on the current thread.

    **Returns**: The status of ``task_group``. See :doc:`task_group_status <task_group_status_enum>`.

.. cpp:function:: task_group_status wait()

    Waits for all tasks in the group to complete or be cancelled.

    **Returns**: The status of ``task_group``. See :doc:`task_group_status <task_group_status_enum>`.

.. cpp:function:: void cancel()

    Cancels all tasks in this ``task_group``.

Non-member functions
--------------------

.. cpp:function:: bool is_current_task_group_canceling()

    **Returns**: true if an innermost ``task_group`` executing on this thread is cancelling its tasks.

See also:

* :doc:`task_group_context <../scheduling_controls/task_group_context_cls>`
* :doc:`task_handle <task_handle>`
