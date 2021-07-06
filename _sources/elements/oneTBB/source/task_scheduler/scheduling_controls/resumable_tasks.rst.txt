.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

===============
Resumable tasks
===============
**[scheduler.resumable_tasks]**

Functions to suspend task execution at a specific point and signal to resume it later.

.. code:: cpp

    // Defined in header <tbb/task.h>

    using tbb::task::suspend_point = /* implementation-defined */;
    template < typename Func > void tbb::task::suspend( Func );
    void tbb::task::resume( tbb::task::suspend_point );

Requirements:

* The ``Func`` type must meet the :doc:`SuspendFunc requirements <../../named_requirements/task_scheduler/suspend_func>`.

The ``tbb::task::suspend`` function called within a running task suspends execution of the task and switches the thread to participate in other oneTBB parallel work.
This function accepts a user callable object with the current execution context ``tbb::task::suspend_point`` as an argument.

The ``tbb::task::suspend_point`` context tag must be passed to the ``tbb::task::resume`` function to trigger a program execution at the suspended point.
The ``tbb::task::resume`` function can be called at any point of an application, even on a separate thread.
In this regard, this function acts as a signal for the task scheduler.

.. note::

    There are no guarantees that the same thread that called ``tbb::task::suspend`` continues execution after the suspended point.
    However, these guarantees are provided for the outermost blocking oneTBB calls
    (such as ``tbb::parallel_for`` and ``tbb::flow::graph::wait_for_all``) and ``tbb::task_arena::execute`` calls.

Example
-------

.. code:: cpp

    // Parallel computation region
    tbb::parallel_for(0, N, [&](int) {
        // Suspend the current task execution and capture the context
        tbb::task::suspend([&] (tbb::task::suspend_point tag) {
            // Dedicated user-managed activity that processes async requests.
            async_activity.submit(tag); // could be OpenCL/IO/Database/Network etc.
        }); // execution will be resumed after this function
    });

.. code:: cpp

    // Dedicated user-managed activity:

    // Signal to resume execution of the task referenced by the tbb::task::suspend_point
    // from a dedicated user-managed activity
    tbb::task::resume(tag);

