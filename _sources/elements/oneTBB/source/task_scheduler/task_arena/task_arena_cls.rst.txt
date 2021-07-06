.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

==========
task_arena
==========
**[scheduler.task_arena]**

A class that represents an explicit, user-managed task scheduler arena.

.. code:: cpp

    // Defined in header <tbb/task_arena.h>

    namespace tbb {

        class task_arena {
        public:
            static const int automatic = /* unspecified */;
            static const int not_initialized = /* unspecified */;
            enum class priority : /* unspecified type */ {
                low = /* unspecified */,
                normal = /* unspecified */,
                high = /* unspecified */
            };
            struct attach {};
            struct constraints {
                numa_node_id numa_node;
                int max_concurrency;

                constraints(numa_node_id numa_node_       = task_arena::automatic,
                            int          max_concurrency_ = task_arena::automatic);
            };

            task_arena(int max_concurrency = automatic, unsigned reserved_for_masters = 1,
                       priority a_priority = priority::normal);
            task_arena(constraints a_constraints, unsigned reserved_for_masters = 1,
                       priority a_priority = priority::normal);
            task_arena(const task_arena &s);
            explicit task_arena(task_arena::attach);
            ~task_arena();

            void initialize();
            void initialize(int max_concurrency, unsigned reserved_for_masters = 1,
                            priority a_priority = priority::normal);
            void initialize(constraints a_constraints, unsigned reserved_for_masters = 1,
                            priority a_priority = priority::normal);
            void initialize(task_arena::attach);
            void terminate();

            bool is_active() const;
            int max_concurrency() const;

            template<typename F> auto execute(F&& f) -> decltype(f());
            template<typename F> void enqueue(F&& f);
        };

    } // namespace tbb

A ``task_arena`` class represents a place where threads may share and execute tasks.

The number of threads that may simultaneously execute tasks in a ``task_arena`` is limited by its concurrency level.

Each user thread that invokes any parallel construction outside an explicit ``task_arena`` uses an implicit
task arena representation object associated with the calling thread.

The tasks spawned or enqueued into one arena cannot be executed in another arena.

Each ``task_arena`` has a ``priority``. The tasks from ``task_arena`` with higher priority are given
a precedence in execution over the tasks from ``task_arena`` with lower priority.

.. note::

    The ``task_arena`` constructors do not create an internal task arena representation object.
    It may already exist in case of the "attaching" constructor; otherwise, it is created
    by an explicit call to ``task_arena::initialize`` or lazily on first use.

Member types and constants
--------------------------

.. cpp:member:: static const int automatic

    When passed as ``max_concurrency`` to the specific constructor, arena
    concurrency is automatically set based on the hardware configuration.

.. cpp:member:: static const int not_initialized

    When returned by a method or function, indicates that there is no active ``task_arena``
    or that the ``task_arena`` object has not yet been initialized.

.. cpp:enum:: priority::low

    When passed to a constructor or the ``initialize`` method, the initialized ``task_arena``
    has a lowered priority.

.. cpp:enum:: priority::normal

    When passed to a constructor or the ``initialize`` method, the initialized ``task_arena``
    has regular priority.

.. cpp:enum:: priority::high

    When passed to a constructor or the ``initialize`` method, the initialized ``task_arena``
    has a raised priority.

.. cpp:struct:: attach

    A tag for constructing a ``task_arena`` with attach.

.. cpp:struct:: constraints

    Represents limitations applied to threads within ``task_arena``.

    ``numa_node`` - An integral logical index uniquely identifying a NUMA node.
    All threads joining the ``task_arena`` are bound to this NUMA node.

    .. note::

        NUMA node ID is considered valid if it was obtained through tbb::info::numa_nodes().

    ``max_concurrency`` - The maximum number of threads that can participate in work processing
    within the ``task_arena`` at the same time.

Member functions
----------------

.. cpp:function:: task_arena(int max_concurrency = automatic, unsigned reserved_for_masters = 1, priority a_priority = priority::normal)

    Creates a ``task_arena`` with a certain concurrency limit (``max_concurrency``) and priority
    (``a_priority``).  Some portion of the limit can be reserved for application threads with
    ``reserved_for_masters``.  The amount for reservation cannot exceed the limit.

    .. caution::

        If ``max_concurrency`` and ``reserved_for_masters`` are
        explicitly set to be equal and greater than 1, oneTBB worker threads will never
        join the arena. As a result, the execution guarantee for enqueued tasks is not valid
        in such arena. Do not use ``task_arena::enqueue()`` with an arena set to have no worker threads.

.. cpp:function:: task_arena(constraints a_constraints, unsigned reserved_for_masters = 1, priority a_priority = priority::normal)

    Creates a ``task_arena`` with a certain constraints(``a_constraints``) and priority
    (``a_priority``).  Some portion of the limit can be reserved for application threads with
    ``reserved_for_masters``.  The amount for reservation cannot exceed the concurrency limit specified in ``constraints``.

    .. caution::

        If ``constraints::max_concurrency`` and ``reserved_for_masters`` are
        explicitly set to be equal and greater than 1, oneTBB worker threads will never
        join the arena. As a result, the execution guarantee for enqueued tasks is not valid
        in such arena. Do not use ``task_arena::enqueue()`` with an arena set to have no worker threads.

    If ``constraints::numa_node`` is specified, then all threads that enter the arena are automatically
    pinned to corresponding NUMA node.

.. cpp:function:: task_arena(const task_arena&)

    Copies settings from another ``task_arena`` instance.

.. cpp:function:: explicit task_arena(task_arena::attach)

    Creates an instance of ``task_arena`` that is connected to the internal task arena representation currently used by the calling thread.
    If no such arena exists yet, creates a ``task_arena`` with default parameters.

    .. note::

        Unlike other constructors, this one automatically initializes
        the new ``task_arena`` when connecting to an already existing arena.

.. cpp:function:: ~task_arena()

    Destroys the ``task_arena`` instance, but the destruction may not be synchronized with any task execution inside this ``task_arena``.
    It means that an internal task arena representation associated with this ``task_arena`` instance can be destroyed later.
    Not thread-safe for concurrent invocations of other methods.

.. cpp:function:: void initialize()

    Performs actual initialization of internal task arena representation.

    .. note::

        After the call to ``initialize``, the arena parameters are fixed and cannot be changed.

.. cpp:function:: void initialize(int max_concurrency, unsigned reserved_for_masters = 1, priority a_priority = priority::normal)

    Same as above, but overrides previous arena parameters.

.. cpp:function:: void initialize(constraints a_constraints, unsigned reserved_for_masters = 1, priority a_priority = priority::normal)

    Same as above.

.. cpp:function:: void initialize(task_arena::attach)

    If an instance of class ``task_arena::attach`` is specified as the argument, and there is
    an internal task arena representation currently used by the calling thread, the method ignores arena
    parameters and connects ``task_arena`` to that internal task arena representation.
    The method has no effect when called for an already initialized ``task_arena``.

.. cpp:function:: void terminate()

    Removes the reference to the internal task arena representation without destroying the
    task_arena object, which can then be re-used. Not thread safe for concurrent invocations of other methods.

.. cpp:function:: bool is_active() const

    Returns ``true`` if the ``task_arena`` has been initialized; ``false``, otherwise.

.. cpp:function:: int max_concurrency() const

    Returns the concurrency level of the ``task_arena``.
    Does not require the ``task_arena`` to be initialized and does not perform initialization.

.. cpp:function:: template<F> void enqueue(F&& f)

    Enqueues a task into the ``task_arena`` to process the specified functor and immediately returns.
    The ``F`` type must meet the `Function Objects` requirements from the [function.objects] ISO C++ Standard section.
    The task is scheduled for eventual execution by a worker thread even if no thread ever explicitly waits for the task to complete.
    If the total number of worker threads is zero, a special additional worker thread is created to execute enqueued tasks.

    .. note::

        The method does not require the calling thread to join the arena; that is, any number
        of threads outside of the arena can submit work to it without blocking.

    .. caution::

        There is no guarantee that tasks enqueued into an arena execute concurrently with
        respect to any other tasks there.

    .. caution::

        An exception thrown and not caught in the functor results in undefined behavior.

.. cpp:function:: template<F> auto execute(F&& f) -> decltype(f())

    Executes the specified functor in the ``task_arena`` and returns the value returned by the functor.
    The ``F`` type must meet the `Function Objects` requirements from [function.objects] ISO C++ Standard section.

    The calling thread joins the ``task_arena`` if possible, and executes the functor.
    Upon return it restores the previous task scheduler state and floating-point settings.

    If joining the ``task_arena`` is not possible, the call wraps the functor into a task,
    enqueues it into the arena, waits using an OS kernel synchronization object
    for another opportunity to join, and finishes after the task completion.

    An exception thrown in the functor will be captured and re-thrown from ``execute``.

    .. note::

        Any number of threads outside of the arena can submit work to the arena and be blocked.
        However, only the maximal number of threads specified for the arena can participate in executing the work.

Example
-------

The example demonstrates ``task_arena`` NUMA support API. Each constructed ``task_arena`` is pinned
to the corresponding NUMA node.

.. code:: cpp

    #include "tbb/task_group.h"
    #include "tbb/task_arena.h"

    #include <vector>

    int main() {
        std::vector<tbb::numa_node_id> numa_nodes = tbb::info::numa_nodes();
        std::vector<tbb::task_arena> arenas(numa_nodes.size());
        std::vector<tbb::task_group> task_groups(numa_nodes.size());

        for (int i = 0; i < numa_nodes.size(); i++) {
            arenas[i].initialize(tbb::task_arena::constraints(numa_nodes[i]));
        }

        for (int i = 0; i < numa_nodes.size(); i++) {
            arenas[i].execute([&task_groups, i] {
                task_groups[i].run([] {
                    /* executed by the thread pinned to specified NUMA node */
                });
            });
        }

        for (int i = 0; i < numa_nodes.size(); i++) {
            arenas[i].execute([&task_groups, i] {
                task_groups[i].wait();
            });
        }

        return 0;
    }


See also:

* :doc:`task_group <../task_group/task_group_cls>`
* :doc:`task_scheduler_observer <task_scheduler_observer_cls>`
