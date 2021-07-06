.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

======================
ContainerBasedSequence
======================
**[req.container_based_sequence]**

A type `C` satisfies `ContainerBasedSequence` if it meets the following requirements:

----------------------------------------------------------------

**ContainerBasedSequence Requirements: Pseudo-Signature, Semantics**

    .. note::

         In this page ``c`` is an object of type (possibly ``const``) ``C``.

         Templates that use the named requirement can impose stricter requirements on the iterator concept.

.. cpp:function:: std::begin(c)

    Returns an input iterator to the beginning of the sequence represented by ``c``.

.. cpp:function:: std::end(c)

    Returns an input iterator one past the end of the sequence represented by ``c``.

See also:

* :doc:`parallel_for_each algorithm <../../algorithms/functions/parallel_for_each_func>`
* :doc:`parallel_sort algorithm <../../algorithms/functions/parallel_sort_func>`
