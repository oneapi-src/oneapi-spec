.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

.. _data_types-label:

##########
Data types
##########

oneDNN supports multiple data types. However, the 32-bit IEEE single-precision
floating-point data type is the fundamental type in oneDNN. It is the only
data type that must be supported by an implementation. All the other types
discussed below are optional.

Primitives operating on the single-precision floating-point data type consume
data, produce, and store intermediate results using the same data type.

Moreover, single-precision floating-point data type is often used for
intermediate results in the mixed precision computations because it provides
better accuracy. For example, the elementwise primitive and elementwise
post-ops always use it internally.

oneDNN uses the following enumeration to refer to data types it supports:

.. doxygenenum:: dnnl::memory::data_type
   :project: oneDNN

oneDNN supports training and inference with the following data types:

========== ========================================================
Usage mode Data types
========== ========================================================
inference  |_f32|, |_bf16|, |_f16|, |_s8|/|_u8|
training   |_f32|, |_bf16|
========== ========================================================

.. note::

   Using lower precision arithmetic may require changes in the deep learning
   model implementation.

Individual primitives may have additional limitations with respect to data
type support based on the precision requirements. The list of data types
supported by each primitive is included in the corresponding sections of the
specification guide.

.. toctree::
   :maxdepth: 1

   bfloat16.rst
   int8.rst

.. vim: ts=3 sw=3 et spell spelllang=en
