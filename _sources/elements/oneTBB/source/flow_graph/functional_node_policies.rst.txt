.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

=======================
Function Nodes Policies
=======================
**[flow_graph.function_node_policies]**

``function_node``, ``multifunction_node``, ``async_node`` and ``continue_node`` can be specified
by the ``Policy`` parameter, which is represented as a set of tag classes. This parameter affects behavior
of node execution.

.. code:: cpp

    // Defined in header <tbb/flow_graph.h>

    namespace tbb {
    namespace flow {

        class queueing { /*unspecified*/ };
        class rejecting { /*unspecified*/ };
        class lightweight { /*unspecified*/ };
        class queueing_lightweight { /*unspecified*/ };
        class rejecting_lightweight { /*unspecified*/ };

    } // namespace flow
    } // namespace tbb

Each policy class satisfies the `CopyConstructible` requirements from [copyconstructible]
ISO C++ Standard sections.

Queueing
--------

This policy defines behavior for input messages acceptance. The ``queueing`` policy means that input
messages that cannot be processed right away are kept to be processed when possible.

Rejecting
---------

This policy defines behavior for input messages acceptance. The ``rejecting`` policy means that input
messages that cannot be processed right away are not accepted by the node and it is responsibility
of a predecessor to handle this.

Lightweight
-----------

This policy helps to reduce the overhead associated with the execution scheduling of the node.

For functional nodes that have a default value for the ``Policy`` template parameter, specifying
the ``lightweight`` policy results in extending the behavior of the default value of ``Policy``
with the behavior defined by the ``lightweight`` policy. For example, if the default value of
``Policy`` is ``queueing``, specifying ``lightweight`` as the ``Policy`` value is equivalent to
specifying ``queueing_lightweight``.

Example
~~~~~~~

The example below shows the application of the ``lightweight`` policy to a
graph with a pipeline topology. It is reasonable to apply the ``lightweight``
policy to the second and third nodes because the bodies of these nodes are small. This
allows the second and third nodes to execute without task scheduling overhead. The
``lightweight`` policy is not specified for the first node in order to permit
concurrent invocations of the graph.

.. include:: ./examples/lightweight_policy.cpp
    :code: cpp
