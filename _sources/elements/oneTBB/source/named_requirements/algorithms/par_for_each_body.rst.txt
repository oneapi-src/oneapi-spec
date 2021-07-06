.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

===================
ParallelForEachBody
===================
**[req.parallel_for_each_body]**

A type `Body` satisfies `ParallelForBody` if it meets the `Function Objects`
requirements from the [function.objects] ISO C++ Standard section.
It should also meet one of the following requirements:

----------------------------------------------------------------

**ParallelForEachBody Requirements: Pseudo-Signature, Semantics**

.. cpp:function:: Body::operator()( ItemType item ) const

    Process the received item.

.. cpp:function:: Body::operator()( ItemType item, tbb::feeder<ItemType>& feeder ) const

    Process the received item. May invoke the ``feeder.add(T)`` function to spawn additional items.

-----------------------------------------------------------------

.. note::

    ``ItemType`` may be optionally passed to ``Body::operator()`` by reference.
    ``const`` and ``volatile`` type qualifiers are also applicable.

ItemType
--------

The argument type ``ItemType`` should either satisfy the *CopyConstructibe*, *MoveConstructibe* or
both requirements from the ISO C++ [utility.arg.requirements] section.
If the type is not *CopyConstructibe*, there are additional usage restrictions:

* If ``Body::operator()`` accepts an argument by value, or if the ``InputIterator`` type
  from :doc:`parallel_for_each algorithm <../../algorithms/functions/parallel_for_each_func>` does
  not satisfy the `Forward Iterator` requirements from the [forward.iterators] ISO C++ Standard section,
  dereferencing an ``InputIterator`` must produce an rvalue reference.
* Additional work items should be passed to the feeder as rvalues, for example, via the ``std::move`` function.

See also:

* :doc:`parallel_for_each algorithm <../../algorithms/functions/parallel_for_each_func>`
* :doc:`feeder class<../../algorithms/functions/feeder>`
