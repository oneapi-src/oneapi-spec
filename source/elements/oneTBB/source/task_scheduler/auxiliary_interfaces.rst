.. SPDX-FileCopyrightText: 2021 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

====================
auxiliary_interfaces
====================
**[scheduler.auxiliary_interfaces]**

A set of helpers that allows to query information about state of the task scheduler on the calling
thread.

.. code:: cpp

    namespace tbb {
        namespace task {
            task_group_context* current_context();
        }
    }

Member functions
----------------

.. namespace:: tbb::task

.. cpp:function:: task_group_context* current_context()

    **Returns**: a pointer to the ``task_group_context`` associated with the task currently
     running. If no task is running by the calling thread, ``nullptr`` is returned.
