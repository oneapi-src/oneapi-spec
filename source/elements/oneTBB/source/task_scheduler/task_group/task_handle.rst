.. SPDX-FileCopyrightText: 2021 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

=================
task_handle
=================
**[scheduler.task_handle]**

A ``task_handle`` type is an implementation-defined type that represents the handle of an associated
task. An instance of ``task_handle`` type can be default-constructed, move-constructed and
move-assigned, but not copy-constructed, nor copy-assigned from another instance of the
``task_handle`` type.

.. code:: cpp

    namespace tbb {
        struct task_handle {
            task_handle();

            task_handle(const task_handle&) = delete;
            task_handle& operator=(const task_handle&) = delete;

            task_handle(task_handle&&);
            task_handle& operator=(task_handle&&);

            // implementation-defined
        };
    }

Member functions
----------------

.. namespace:: tbb::task_handle

.. cpp:function:: task_handle()

    Constructs an empty ``task_handle``.

.. cpp:function:: task_handle(task_handle&& th);

    Constructs a ``task_handle``, which value is moved from ``th``. The value ``th`` is unspecified
    after the call.

.. cpp:function:: task_handle& operator=(task_handle&& th)

    Assigns the value of ``th`` to ``this``. The value ``th`` is unspecified after the call.
