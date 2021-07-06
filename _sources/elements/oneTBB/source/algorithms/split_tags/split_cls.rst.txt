.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

=====
split
=====
**[algorithms.split]**

Type of an argument for a splitting constructor of :doc:`Range <../../named_requirements/algorithms/range>`.
An argument of type ``split`` is used to distinguish a splitting constructor from a copy constructor.

.. code:: cpp

    // Defined in header <tbb/blocked_range.h>
    // Defined in header <tbb/blocked_range2d.h>
    // Defined in header <tbb/blocked_range3d.h>
    // Defined in header <tbb/partitioner.h>
    // Defined in header <tbb/parallel_for.h>
    // Defined in header <tbb/parallel_reduce.h>
    // Defined in header <tbb/parallel_scan.h>

    class split;

See also:

* :doc:`Range requirements <../../named_requirements/algorithms/range>`

