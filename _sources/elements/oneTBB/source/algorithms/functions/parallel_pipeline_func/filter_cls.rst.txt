.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

======
filter
======
**[algorithms.parallel_pipeline.filter]**

A ``filter`` class template represents a strongly-typed filter in a ``parallel_pipeline`` algorithm, 
with its template parameters specifying the filter input and output types.
A ``filter`` can be constructed from a functor or by composing two ``filter`` objects with
``operator&()``. The same ``filter`` object can be reused in multiple ``&`` expressions.

The ``filter`` class should only be used in conjunction with ``parallel_pipeline`` functions.

.. code:: cpp

    // Defined in header <tbb/parallel_pipeline.h>

    namespace tbb {

        template<typename InputType, typename OutputType>
        class filter {
        public:
            filter() = default;
            filter( const filter& rhs ) = default;
            filter( filter&& rhs ) = default;
            void operator=(const filter& rhs) = default;
            void operator=( filter&& rhs ) = default;

            template<typename Body>
            filter( filter_mode mode, const Body& body );

            filter& operator&=( const filter<OutputType,OutputType>& right );

            void clear();
        }

        template<typename T, typename U, typename Body>
        filter<T,U> make_filter( filter::mode mode, const Body& f );
        template<typename T, typename V, typename U>
        filter<T,U> operator&( const filter<T,V>& left, const filter<V,U>& right );

    }

Requirements:

* If `InputType` is ``void``, a ``Body`` type must meet the :doc:`StartFilterBody requirements <../../../named_requirements/algorithms/filter_body>`.
* If `OutputType` is ``void``, a ``Body`` type must meet the :doc:`OutputFilterBody requirements <../../../named_requirements/algorithms/filter_body>`.
* If `InputType` and `OutputType` are not ``void``, a ``Body`` type must meet the :doc:`MiddleFilterBody requirements <../../../named_requirements/algorithms/filter_body>`.
* If `InputType` and `OutputType` are ``void``, a ``Body`` type must meet the :doc:`SingleFilterBody requirements <../../../named_requirements/algorithms/filter_body>`.

filter_mode Enumeration
-----------------------

.. toctree::

    filter_mode_enum.rst

Member functions
----------------

.. cpp:function:: filter()

    Constructs an undefined filter.

    .. caution::

        The effect of using an undefined filter by ``operator&()`` or ``parallel_pipeline`` is undefined.

.. cpp:function:: template<typename Body> \
                  filter( filter_mode mode, const Body& body )

    Constructs a ``filter`` that uses a copy of a provided ``body`` to map an input value
    of type *InputType* to an output value of type *OutputType*, and that operates in the specified ``mode``.

.. cpp:function:: void clear()

    Sets ``*this`` to an undefined filter.

Non-member functions
--------------------

.. cpp:function:: template<typename T, typename U, typename Func> \
                  filter<T, U> make_filter( filter::mode mode, const Func& f )

    Returns ``filter<T, U>(mode, f)``.

.. cpp:function:: template<typename T, typename V, typename U> \
                  filter<T,U> operator&( const filter<T,V>& left, const filter<V,U>& right )

    Returns a ``filter`` representing the composition of filters *left* and *right*.
    The composition behaves as if the output value of *left* becomes the input value of *right*.

Deduction Guides
----------------

.. code:: cpp

    template<typename Body>
    filter(filter_mode, Body) -> filter<filter_input<Body>, filter_output<Body>>;

Where:

* ``filter_input<Body>`` is an alias to the ``Body::operator()`` input parameter type.
  If ``Body::operator()`` input parameter type is ``flow_control`` then ``filter_input<Body>`` is ``void``.
* ``filter_output<Body>`` is an alias to the ``Body::operator()`` return type.
