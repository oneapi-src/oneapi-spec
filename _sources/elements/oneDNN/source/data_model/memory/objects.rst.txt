.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

##############################
Memory Descriptors and Objects
##############################

***********
Descriptors
***********

Memory descriptor is an engine-agnostic logical description of data (number of
dimensions, dimension sizes, and data type), and, optionally, the information
about the physical format of data in memory. If this information is not known
yet, a memory descriptor can be created with format tag set to |_any|. This
allows compute-intensive primitives to chose the most appropriate format for
the computations.  The user is then responsible for reordering their data into
the new format if the formats do not match. See
:ref:`memory_format_propagation-label`.

A memory descriptor can be initialized either by specifying dimensions, and
memory format tag or strides for each of them.

User can query amount of memory required by a memory descriptor using the
|memory::desc::get_size| function. The size of data in general
cannot be computed as the product of dimensions multiplied by the size of the
data type. So users are required to use this function for better code
portability.

Two memory descriptors can be compared using the equality and inequality
operators. The comparison is especially useful when checking whether it is
necessary to reorder data from the user's data format to a primitive's format.

Along with ordinary memory descriptors with all dimensions being positive,
oneDNN supports *zero-volume* memory descriptors with one or more dimensions
set to zero. This is used to support the NumPy\* convention. If a zero-volume
memory is passed to a primitive, the primitive typically does not perform any
computations with this memory. For example:

- The concatenation primitive would ignore all memory object with zeroes in the
  concatenation dimension / axis.

- A forward convolution with a source memory object with zero in the minibatch
  dimension would always produce a destination memory object with a zero in the
  minibatch dimension and perform no computations.

- However, a forward convolution with a zero in one of the weights dimensions
  is ill-defined and is considered to be an error by the library because there
  is no clear definition on what the output values should be.

Data handle of a zero-volume memory is never accessed.

.. rubric:: API

.. doxygenstruct:: dnnl::memory::desc
   :project: oneDNN
   :members:

*******
Objects
*******

Memory objects combine memory descriptors with storage for data (a data handle).
With USM, the data handle is simply a pointer to ``void``. The data handle can
be queried using |memory::get_data_handle| and set using
|memory::set_data_handle|. The underlying SYCL buffer, when used, can be queried
using |sycl_interop::get_buffer| and set using |sycl_interop::set_buffer|. In
addition, the memory descriptor and the engine underlying a memory object can
be queried using |memory::get_desc| and |memory::get_engine| respectively.

***
API
***

.. doxygenstruct:: dnnl::memory
   :project: oneDNN
   :members: memory, get_desc, get_engine, get_data_handle, set_data_handle, map_data, unmap_data

.. doxygenenum:: dnnl::sycl_interop::memory_kind
   :project: oneDNN

.. doxygenfunction:: dnnl::sycl_interop::make_memory(const memory::desc &adesc, const engine &aengine, memory_kind akind, void *ahandle = DNNL_MEMORY_ALLOCATE)
   :project: oneDNN

.. doxygenfunction:: dnnl::sycl_interop::make_memory(const memory::desc &adesc, const stream &astream, memory_kind akind, void *ahandle = DNNL_MEMORY_ALLOCATE)
   :project: oneDNN

.. doxygenfunction:: dnnl::sycl_interop::make_memory(const memory::desc &adesc, const engine &aengine, cl::sycl::buffer<T, ndims> abuffer)
   :project: oneDNN

.. doxygenfunction:: dnnl::sycl_interop::make_memory(const memory::desc &adesc, const stream &astream, cl::sycl::buffer<T, ndims> abuffer)
   :project: oneDNN

.. doxygenfunction:: dnnl::sycl_interop::get_memory_kind
   :project: oneDNN

.. doxygenfunction:: dnnl::sycl_interop::set_buffer(memory &amemory, cl::sycl::buffer<T, ndims> abuffer)
   :project: oneDNN

.. doxygenfunction:: dnnl::sycl_interop::set_buffer(memory &amemory, cl::sycl::buffer<T, ndims> abuffer, stream &astream)
   :project: oneDNN

.. doxygenfunction:: dnnl::sycl_interop::get_buffer
   :project: oneDNN

.. doxygendefine:: DNNL_MEMORY_NONE
   :project: oneDNN

.. doxygendefine:: DNNL_MEMORY_ALLOCATE
   :project: oneDNN

.. vim: ts=3 sw=3 et spell spelllang=en
