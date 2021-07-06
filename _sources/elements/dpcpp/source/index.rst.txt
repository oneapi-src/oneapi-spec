.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onedpcpp-section:

=====
DPC++
=====

Overview
--------

|dpcpp_full_name| (DPC++) is the direct programming language and
associated direct programming APIs of oneAPI.  It provides the
features needed to define data parallel functions and to launch them
on devices.  The language is comprised of the following components:

- C++.  Every DPC++ program is also a C++ program.  A
  compliant DPC++ implementation must support the C++17 Core Language
  (as specified in Sections 1-19 of ISO/IEC 14882:2017) or
  newer.  See the `C++ Standard`_.

- SYCL.  DPC++ builds on the SYCL specification from The Khronos Group.
  The SYCL language enables
  the definition of data parallel functions that can be offloaded to
  devices and defines runtime APIs and classes that are used to
  orchestrate the offloaded functions.

- DPC++ Language extensions. A compliant DPC++ implementation must
  support the specified language features.  These include
  unified shared memory (USM), ordered queues, and reductions. Some
  extensions are required only when the DPC++
  implementation supports a specific class of device, as summarized in the
  `Extensions Table`_. An implementation supports a class of device if
  it can target hardware that responds “true” for a DPC++
  device type query, either through explicit support built into the
  implementation, or by using a lower layer that can support those
  device classes such as the oneAPI Level Zero 
  (Level Zero).  A DPC++ implementation must pass the 
  conformance tests for all extensions that are required (`Extensions
  Table`_) for the classes of devices that the implementation can
  support.  (See `SYCL Extensions`_.)

This specification requires a minimum of C++17 Core Language support and
DPC++ extensions. These version and feature coverage requirements
will evolve over time, with specific versions of C++ and SYCL being required,
some additional extensions being required, and some DPC++ extensions no longer
required if covered by newer C++ or SYCL versions directly.

.. table:: DPC++ Extensions Table: Support requirements for DPC++
           implementations above SYCL 1.2.1
   :name: Extensions Table

   ===========================  ========================  ====================  ====================  ====================  =============
   Feature                      Where defined             CPU                   GPU                   FPGA                  Test [#test]_
   ===========================  ========================  ====================  ====================  ====================  =============
   Accessor simplifications     `SYCL 2020 provisional`_  Required              Required              Required              NA [#na]_
   bit_cast                     `SYCL 2020 provisional`_  Required              Required              Required              NA [#na]_
   Deduction guides             `SYCL 2020 provisional`_  Required              Required              Required              NA [#na]_
   Device specific queries      `SYCL 2020 provisional`_  Not required [#tmp]_  Not required [#tmp]_  Not required [#tmp]_  NA [#na]_
   Extended atomics             `SYCL 2020 provisional`_  Required [#ea]_       Required [#ea]_       Not required [#tmp]_  NA [#na]_
   Kernel func type attributes  `SYCL 2020 provisional`_  Required              Required              Required              NA [#na]_
   In-order queues              `SYCL 2020 provisional`_  Required              Required              Required              NA [#na]_
   Math array                   `SYCL 2020 provisional`_  Not required [#tmp]_  Not required [#tmp]_  Not required [#tmp]_  NA [#na]_
   Optional lambda name         `SYCL 2020 provisional`_  Required              Required              Required              NA [#na]_
   Queue shortcuts              `SYCL 2020 provisional`_  Required              Required              Required              NA [#na]_
   Required work-group size     `SYCL 2020 provisional`_  Required              Required              Required              NA [#na]_
   Standard layout relaxed      `SYCL 2020 provisional`_  Required              Required              Required              NA [#na]_
   Unified Shared Memory        `SYCL 2020 provisional`_  Required [#USM]_      Required [#USM]_      Required [#USM]_      `usm <https://github.com/intel/llvm/tree/sycl/sycl/test/usm>`__
   `Accessor properties`_       DPC++ extension           Required [#aprop]_    Required [#aprop]_    Required [#aprop]_    NA [#na]_
   `CXX standard library`_      DPC++ extension           Required              Required              Not required [#tmp]_  NA [#na]_
   `Data flow pipes`_           DPC++ extension           Not required          Not required          Required              `fpga_tests <https://github.com/intel/llvm/tree/sycl/sycl/test/fpga_tests>`__
   `Enqueued barriers`_         DPC++ extension           Required              Required              Required              NA [#na]_
   `Group algorithms`_          DPC++ extension           Required              Required              Not required [#tmp]_  NA [#na]_
   `Group mask`_                DPC++ extension           Not required [#tmp]_  Not required [#tmp]_  Not required [#tmp]_  NA [#na]_
   `Parallel for shortcuts`_    DPC++ extension           Required              Required              Required              NA [#na]_
   `Pinned memory property`_    DPC++ extension           Required              Required              Required              NA [#na]_
   `Reductions`_                DPC++ extension           Required [#redc]_     Required [#redc]_     Not required [#tmp]_  NA [#na]_
   `Restrict all arguments`_    DPC++ extension           Required              Required              Required              NA [#na]_
   `Static local mem query`_    DPC++ extension           Not required [#tmp]_  Not required [#tmp]_  Not required [#tmp]_  NA [#na]_
   `Sub-groups`_                DPC++ extension           Required              Required              Not required          `sub_group <https://github.com/intel/llvm/tree/sycl/sycl/test/sub_group>`__
   `Sub-group algorithms`_      DPC++ extension           Required [#sga]_      Required [#sga]_      Not required          `sub_group <https://github.com/intel/llvm/tree/sycl/sycl/test/sub_group>`__
   ===========================  ========================  ====================  ====================  ====================  =============


..   ==========================  ================  ================  ====================  =============

.. _`Accessor properties`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions/accessor_properties
.. _`CXX standard library`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions/C-CXX-StandardLibrary
.. _`Data flow pipes`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions/DataFlowPipes
.. _`Enqueued barriers`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions/EnqueueBarrier
.. _`Group algorithms`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions/GroupAlgorithms
.. _`Group mask`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions/GroupMask
.. _`Parallel for shortcuts`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions/ParallelForSimplification
.. _`Pinned memory property`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions/UsePinnedMemoryProperty
.. _`Reductions`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions/Reduction
.. _`Restrict all arguments`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions/KernelRestrictAll
.. _`Static local mem query`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions/StaticLocalMemoryQuery
.. _`Sub-groups`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions/SubGroup
.. _`Sub-group algorithms`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions/SubGroupAlgorithms

.. [#test] Test directory within `extension tests`_
.. [#USM] Minimum of explicit USM support
.. [#na] Not yet available.
.. [#tmp] Likely to be required in the future

.. [#redc] DPC++ requirement is for one dimensional reductions, single reduction variable support
.. [#sga] DPC++ requirement is for sub-group algorithms that have equivalent group algorithms
.. [#ea] DPC++ requirement does not include support for atomics in the generic address space
.. [#aprop] DPC++ requirement is for the general property mechanism, and not specific properties within it

Detailed API and Language Descriptions
--------------------------------------

The `SYCL 1.2.1 Specification`_ describes the SYCL APIs and language.  DPC++ extensions on top of SYCL
are described in the `SYCL Extensions`_ repository.  Some features defined in the 
`SYCL 2020 Provisional Specification`_ but not in the `SYCL 1.2.1 Specification`_ are required in
DPC++, as summarized in `Extensions Table`_, and most replace DPC++ extensions that were required in previous
versions of this specification.


A brief summary of the required features from `SYCL 2020 Provisional Specification`_ (above
`SYCL 1.2.1 Specification`_) follows:

-  Accessor simplifications - simplification of the accessor interface, reduction of verbosity in common
   code, and removal of need to specify template arguments in common cases.  Section 4.7.6 of the
   `SYCL 2020 Provisional Specification`_.
-  bit_cast - inclusion of C++20 (p0476r2) ``std::bit_cast`` as ``sycl::bit_cast``.  Section 3.8.2 of the
   `SYCL 2020 Provisional Specification`_.
-  Deduction guides - simplifies common code patterns and reduces code length and verbosity by enabling
   Class Template Argument Deduction (CTAD) from modern C++.  Distributed throughout the
   `SYCL 2020 Provisional Specification`_.
-  Device specific queries - kernel property queries associated with a specific device.  Section 4.12 of the
   `SYCL 2020 Provisional Specification`_.
-  Extended atomics - alignment with C++20 ``std::atomic_ref``, including some tweaks for memory models in SYCL.
   Support for floating-point types and shorthand operators. Section 4.17.3 of the `SYCL 2020 Provisional Specification`_.
   Additional atomic-related queries are defined in Table 4.19, and some changes to fences and barriers are reflected
   in Section 4.17.1 (both in the `SYCL 2020 Provisional Specification`_).
-  Kernel function type attributes - definition of kernel attributes as function type attributes that allows
   them to be applied to lambdas.  Definition of some core attributes.  Section 5.7 of the
   `SYCL 2020 Provisional Specification`_.
-  In-order queues - defines simple in-order semantics for queues, to simplify common coding patterns.
   Section 4.6.5 of the `SYCL 2020 Provisional Specification`_.
-  Math array - contiguous fixed-size portable container.  Section 4.16.3 of the
   `SYCL 2020 Provisional Specification`_.
-  Optional lambda name - removes requirement to manually name lambdas that define kernels.
   Simplifies coding and enables composability with libraries.  Lambdas can still be manually named, if
   desired, such as when debugging or interfacing with a ``sycl::program`` object.
   Section 4.14.2 of the `SYCL 2020 Provisional Specification`_.
-  Queue shortcuts - defines kernel invocation functions directly on the queue classes, to simplify code patterns
   where dependencies and/or accessors do not need to be created within the additional command group scope.  Reduces
   code verbosity in some common patterns.  Section 4.6.5 of the `SYCL 2020 Provisional Specification`_.
-  Required work-group size - defines an attribute that can be applied to kernels (including lambda definitions of kernels)
   which signals that the kernel will only be invoked with a specific work-group size.  This is an optimization attribute
   that enables optimizations based on additional user-driven information.  Section 5.7 of the
   `SYCL 2020 Provisional Specification`_.
-  Standard layout relaxed - removes the requirement that data shared by a host and device(s) must be C++ standard layout
   types.  Requires device compilers to validate layout compatibility. Section 4.14.4 of the `SYCL 2020 Provisional Specification`_.
-  Unified Shared Memory (USM) - defines pointer based memory accesses and management interfaces. Provides
   the ability to create allocations that are visible and have consistent pointer values across both
   host and device(s).  Different USM capability levels are defined, corresponding to different levels
   of device and implementation support.  Section 4.8 of the `SYCL 2020 Provisional Specification`_.


A brief summary of the extensions is as follows:

-  Accessor properties - compile-time accessor properties that are visible to the compiler.
-  CXX standard library - enable subset of the C and C++ standard libraries in device code.
-  Data flow pipes - enable efficient First-In, First-Out (FIFO) communication in DPC++, a mechanism commonly
   used when describing algorithms for spatial architectures such as FPGAs. 
-  Enqueued barriers - simplifies dependence creation and tracking for some common programming patterns by allowing
   coarser grained synchronization within a queue without manual creation of fine grained dependencies.
-  Group algorithms - defines collective operations that operate across groups of work-items, including broadcast,
   reduce, and scan.  Improves productivity by providing common algorithms without explicit coding, and enables optimized
   implementations to exist for combinations of device and runtime.
-  Group mask - defines a type that can represent a set of work-items from a group, and collective operations that create
   or operate on that type such as ballot and count.
-  Parallel for shortcuts - simplification of common patterns such as invoking a kernel with a scalar range.
-  Pinned memory property - optimization indicating that a buffer should use a specific memory resource if possible,
   to accelerate movement of data between host and devices in some implementations.
-  Reductions - provides a reduction abstraction to the ND-range form of *parallel_for*.  Improves productivity
   by providing the common reduction pattern without explicit coding, and enables optimized
   implementations to exist for combinations of device, runtime, and reduction properties.
-  Restrict all arguments - defines an attribute that can be applied to kernels (including lambda definitions of kernels)
   which signals that there will be no memory aliasing between any pointer arguments that are passed to or captured
   by a kernel.  This is an optimization attribute that can have large impact when the developer knows more about the
   kernel arguments than a compiler can infer or safely assume.
-  Static local memory query - query for the amount of local memory used by a compiler and unavailable for dynamic use.
-  Subgroups - defines a grouping of work-items within a work-group. Synchronization
   of work-items in a sub-group can occur independently of work-items in other sub-groups, and
   sub-groups expose communication operations across work-items in the group.  Subgroups commonly
   map to SIMD hardware where it exists.
-  Subgroup algorithms - defines collective operations across work-items in a sub-group that are available
   only for sub-groups.  Also enables algorithms from the more generic "group algorithms" extension as sub-group
   collective operations.

Open Source Implementation
--------------------------

An `open source implementation`_ is available under
an LLVM license.  Details on incomplete features and known issues are
available in the `Release Notes`_ (and the `Getting Started Guide`_
until the release notes are available).

Testing
-------

A DPC++ implementation must pass:

  1. The `extension tests`_ for any extension implemented from the `Extensions Table`_.
     Each extension in the `Extensions Table`_ lists the name of the directory that contains
     corresponding tests, within the `extension tests`_ tree.

Acknowledgment
---------------

We thank the DPC++ and oneDPL `Technical Advisory Board <https://github.com/oneapi-src/oneAPI-tab>`__ for their valuable feedback,
and the Khronos SYCL working group for their efforts defining and evolving the SYCL specification.


.. _`C++ Standard`: https://isocpp.org/std/the-standard
.. _`SYCL 1.2.1 Specification`: https://www.khronos.org/registry/SYCL/specs/sycl-1.2.1.pdf
.. _`SYCL 2020 Provisional Specification`: https://www.khronos.org/registry/SYCL/specs/sycl-2020-provisional.pdf
.. _`SYCL 2020 Provisional`: https://www.khronos.org/registry/SYCL/specs/sycl-2020-provisional.pdf
.. _`SYCL Adopters`: https://www.khronos.org/sycl/adopters/
.. _`SYCL Extensions`: https://github.com/intel/llvm/tree/sycl/sycl/doc/extensions
.. _`open source implementation`: https://github.com/intel/llvm/tree/sycl/
.. _`conformance test suite`: https://github.com/KhronosGroup/SYCL-CTS
.. _`extension tests`: https://github.com/intel/llvm/tree/sycl/sycl/test
.. _`Release Notes`: https://github.com/intel/llvm/tree/sycl/sycl/ReleaseNotes.md
.. _`Getting Started Guide`: https://github.com/intel/llvm/blob/sycl/sycl/doc/GetStartedGuide.md#known-issues-and-limitations
.. _`joining the Khronos Group`: https://www.khronos.org/members/
.. _`Khronos SYCL GitHub project`: https://github.com/KhronosGroup/SYCL-Docs
