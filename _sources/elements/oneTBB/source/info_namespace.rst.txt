.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

==============
info Namespace
==============
**[info_namespace]**

Interfaces to query information about execution environment.

.. code:: cpp

   // Declared in info.h

    namespace tbb {
        using numa_node_id = /*implementation-defined*/;
        namespace info {
            std::vector<numa_node_id> numa_nodes();
            int default_concurrency(numa_node_id id = tbb::task_arena::automatic);
        }
    }

Types
-----

``numa_node_id`` - Represents NUMA node identifier.

Functions
---------

.. cpp:function:: std::vector<numa_node_id> numa_nodes()

    Returns the vector of integral indexes that indicate available NUMA nodes.

    .. note::
        If error occurs during system topology parsing, returns vector containing single element
        that equals to ``task_arena::automatic``.

.. cpp:function:: int default_concurrency(numa_node_id id = tbb::task_arena::automatic)

    Returns concurrency level of the given NUMA node. If argument is not specified, returns default
    concurrency level for current library configuration.
