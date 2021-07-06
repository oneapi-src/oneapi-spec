.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

===============
parallel_reduce
===============
**[algorithms.parallel_reduce]**

Function template that computes reduction over a range.

.. code:: cpp

    // Defined in header <tbb/parallel_reduce.h>

    namespace tbb {

        template<typename Range, typename Value, typename Func, typename Reduction>
        Value parallel_reduce(const Range& range, const Value& identity, const Func& func, const Reduction& reduction, /* see-below */ partitioner, task_group_context& group);
        template<typename Range, typename Value, typename Func, typename Reduction>
        Value parallel_reduce(const Range& range, const Value& identity, const Func& func, const Reduction& reduction, /* see-below */ partitioner);
        template<typename Range, typename Value, typename Func, typename Reduction>
        Value parallel_reduce(const Range& range, const Value& identity, const Func& func, const Reduction& reduction, task_group_context& group);
        template<typename Range, typename Value, typename Func, typename Reduction>
        Value parallel_reduce(const Range& range, const Value& identity, const Func& func, const Reduction& reduction);

        template<typename Range, typename Body>
        void parallel_reduce(const Range& range, Body& body, /* see-below */ partitioner, task_group_context& group);
        template<typename Range, typename Body>
        void parallel_reduce(const Range& range, Body& body, /* see-below */ partitioner);
        template<typename Range, typename Body>
        void parallel_reduce(const Range& range, Body& body, task_group_context& group);
        template<typename Range, typename Body>
        void parallel_reduce(const Range& range, Body& body);

    } // namespace tbb

A ``partitioner`` type may be one of the following entities:

* ``const auto_partitioner&``
* ``const simple_partitioner&``
* ``const static_partitioner&``
* ``affinity_partitioner&``

.. _par_reduce_requirements:

Requirements:

* The ``Range`` type must meet the :doc:`Range requirements <../../named_requirements/algorithms/range>`.
* The ``Body`` type must meet the :doc:`ParallelReduceBody requirements <../../named_requirements/algorithms/par_reduce_body>`.
* The ``Func`` type must meet the :doc:`ParallelReduceFunc requirements <../../named_requirements/algorithms/par_reduce_func>`.
* The ``Reduction`` types must meet ::doc:`ParallelReduceReduction requirements <../../named_requirements/algorithms/par_reduce_func>`.

The function template ``parallel_reduce`` has two forms:
The functional form is designed to be easy to use in conjunction with lambda expressions.
The imperative form is designed to minimize copying of data.

The functional form ``parallel_reduce(range, identity, func, reduction)`` performs a parallel reduction by applying *func* to
subranges in *range* and reducing the results with the binary operator *reduction*.
It returns the result of the reduction. The *identity* parameter specifies the left identity element for *func*'s ``operator()``.
Parameters *func* and *reduction* can be lambda expressions.

The imperative form ``parallel_reduce(range,body)`` performs parallel reduction of *body* over each value in *range*.

A ``parallel_reduce`` recursively splits the range into subranges to the point such that ``is_divisible()`` is false for each subrange.
A ``parallel_reduce`` uses the splitting constructor to make one or more copies of the body for each thread.
It may copy a body while the body’s ``operator()`` or method ``join`` runs concurrently.
You are responsible for ensuring the safety of such concurrency. In typical usage, the safety requires no extra effort.

``parallel_reduce`` may invoke the splitting constructor for the body.
For each such split of the body, it invokes the ``join`` method to merge the results from the bodies.
Define ``join`` to update this to represent the accumulated result for this and rhs.
The reduction operation should be associative, but does not have to be commutative.
For a noncommutative operation *op*, ``left.join(right)`` should update *left* to be the result of *left op right*.

A body is split only if the range is split, but the converse is not necessarily to be so.
The user must neither rely on a particular choice of body splitting nor on the subranges processed by a
given body object being consecutive. ``parallel_reduce`` makes the choice of body splitting nondeterministically.

When executed serially ``parallel_reduce`` run sequentially from left to right in the same sense as for ``parallel_for``.
Sequential execution never invokes the splitting constructor or method join.

All overloads can accept a :doc:`task_group_context <../../task_scheduler/scheduling_controls/task_group_context_cls>` object
so that the algorithm’s tasks are executed in this group. By default, the algorithm is executed in a bound group of its own.

**Complexity**

If the range and body take *O(1)* space, and the range splits into nearly equal pieces,
the space complexity is *O(P×log(N))*, where *N* is the size of the range and *P* is the number of threads.

Example (Imperative Form)
-------------------------

The following code sums the values in an array.

.. code:: cpp

    #include "tbb/parallel_reduce.h"
    #include "tbb/blocked_range.h"

    using namespace tbb;

    struct Sum {
        float value;
        Sum() : value(0) {}
        Sum( Sum& s, split ) {value = 0;}
        void operator()( const blocked_range<float*>& r ) {
            float temp = value;
            for( float* a=r.begin(); a!=r.end(); ++a ) {
                temp += *a;
            }
            value = temp;
        }
        void join( Sum& rhs ) {value += rhs.value;}
    };

    float ParallelSum( float array[], size_t n ) {
        Sum total;
        parallel_reduce( blocked_range<float*>( array, array+n ), total );
        return total.value;
    }

The example generalizes to reduction for any associative operation *op* as follows:

* Replace occurrences of 0 with the identity element for *op*
* Replace occurrences of += with *op*\ = or its logical equivalent.
* Change the name ``Sum`` to something more appropriate for *op*.

The operation may be noncommutative. For example, *op* could be matrix multiplication.

Example with Lambda Expressions
-------------------------------

The following is similar to the previous example, but written using lambda
expressions and the functional form of ``parallel_reduce``.

.. code:: cpp

    #include "tbb/parallel_reduce.h"
    #include "tbb/blocked_range.h"

    using namespace tbb;

    float ParallelSum( float array[], size_t n ) {
        return parallel_reduce(
            blocked_range<float*>( array, array+n ),
            0.f,
            [](const blocked_range<float*>& r, float init)->float {
                for( float* a=r.begin(); a!=r.end(); ++a )
                    init += *a;
                return init;
            },
            []( float x, float y )->float {
                return x+y;
            }
        );
    }

See also:

* :ref:`Partitioners <Partitioners>`

