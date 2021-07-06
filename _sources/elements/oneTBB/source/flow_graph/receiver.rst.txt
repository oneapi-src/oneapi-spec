.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

========
receiver
========
**[flow_graph.receiver]**

A base class for all nodes that may receive messages.

.. code:: cpp

    namespace tbb {
    namespace flow {

        template< typename T >
        class receiver { /*unspecified*/ };

    } // namespace flow
    } // namespace tbb

The ``T`` type is a message type.
