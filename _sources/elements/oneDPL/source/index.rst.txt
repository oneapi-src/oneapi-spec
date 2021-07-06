.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _oneDPL-section:

======
oneDPL
======

The |dpl_full_name| (oneDPL) provides the functionality
specified in the `C++ standard`_, with extensions to support data parallelism
and offloading to devices, and with extensions to simplify its usage for 
implementing data parallel algorithms.

The library is comprised of the following components:

- A subset of the `C++ standard`_ library which you can use with
  buffers and data parallel kernels.

- Parallel STL algorithms, complemented with execution
  policies and companion APIs for running on oneAPI devices.
  (See :doc:`Extensions to Parallel STL <pstl>`.)

- Extensions: an additional set of library classes and functions that
  are known to be useful in practice but are not yet included into
  C++ or SYCL specifications. (See :doc:`Specific API of oneDPL <extensions>`.)


.. toctree::

   common.rst
   stdlib.rst
   pstl.rst
   extensions.rst

.. _`C++ Standard`: https://isocpp.org/std/the-standard
