.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

######
Concat
######

A primitive to concatenate data by arbitrary dimension.

..
  TODO this is confusing. Document what ou and in are. Why do we need C at
  all?

The concat primitive concatenates :math:`N` tensors over ``concat_dimension``
(here denoted as :math:`C`), and is defined as

.. math::

       \dst(\overline{ou}, c, \overline{in}) =
           \src_i(\overline{ou}, c', \overline{in}),

where

- :math:`c = C_1 + \ldots + C_{i-1} + c'`,

- :math:`\overline{ou}` is the outermost indices (to the left from concat
  axis),

- :math:`\overline{in}` is the innermost indices (to the right from concat
  axis), and

Variable names follow the standard :ref:`conventions-label`.

********************
Forward and Backward
********************

The concat primitive does not have a notion of forward or backward
propagations. The backward propagation for the concatenation operation is
simply an identity operation.

*******************
Execution Arguments
*******************

When executed, the inputs and outputs should be mapped to an execution
argument index as specified by the following table.

====================== ========================
Primitive input/output Execution argument index
====================== ========================
:math:`\src`           |DNNL_ARG_MULTIPLE_SRC|
:math:`\dst`           |DNNL_ARG_DST|
====================== ========================

*****************
Operation Details
*****************

1. The :math:`\dst` memory format can be either specified by a user or derived
   by the primitive. The recommended way is to allow the primitive to choose
   the most appropriate format.

2. The concat primitive requires all source and destination tensors to have
   the same shape except for the ``concat_dimension``. The destination
   dimension for the ``concat_dimension`` must be equal to the sum of the
   ``concat_dimension`` dimensions of the sources (i.e. :math:`C = \sum_i
   C_i`). Implicit broadcasting is not supported.

******************
Data Types Support
******************

The concat primitive supports arbitrary data types for source and destination
tensors. However, it is required that all source tensors are of the same data
type (but not necessarily matching the data type of the destination tensor).

*******************
Data Representation
*******************

The concat primitive does not assign any special meaning associated with any
logical dimensions.

***********************
Post-ops and Attributes
***********************

The concat primitive does not support any post-ops or attributes.

***
API
***

.. doxygenstruct:: dnnl::concat
   :project: oneDNN
   :members:

.. vim: ts=3 sw=3 et spell spelllang=en
