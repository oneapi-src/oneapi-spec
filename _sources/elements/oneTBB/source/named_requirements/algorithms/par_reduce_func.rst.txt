.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

==================
ParallelReduceFunc
==================
**[req.parallel_reduce_body]**

A type `Func` satisfies `ParallelReduceFunc` if it meets the following requirements:

-----------------------------------------------------------------------------------------------------

**ParallelReduceFunc Requirements: Pseudo-Signature, Semantics**

.. cpp:function:: Value Func::operator()(const Range& range, const Value& x) const

    Accumulates result for a subrange, starting with initial value ``x``.
    ``Range`` type must meet the :doc:`Range requirements <range>`.
    ``Value`` type must be the same as a corresponding template parameter for the
    :doc:`parallel_reduce algorithm <../../algorithms/functions/parallel_reduce_func>` algorithm.

See also:

* :doc:`parallel_reduce algorithm <../../algorithms/functions/parallel_reduce_func>`
* :doc:`parallel_determinstic_reduce algorithm <../../algorithms/functions/parallel_deterministic_reduce_func>`
