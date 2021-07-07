.. SPDX-FileCopyrightText: 2021 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

=============
TaskGroupFunc
=============
**[req.task_group_func]**

A type `Func` satisfies `TaskGroupFunc` if it meets `Function Objects` requirements from
[function.objects] ISO C++ Standard section and has at least one of the following methods:

----------------------------------------------------------------------

**TaskGroupFunc Requirements: Pseudo-Signature, Semantics**

.. namespace:: TaskGroupFunc

.. cpp:function:: void Func::operator()() const

    Function call.

.. cpp:function:: tbb::task_handle Func::operator()() const

    Function call that returns ``tbb::task_handle``. See :doc:`task_handle
    <../../task_scheduler/task_group/task_handle>`.


