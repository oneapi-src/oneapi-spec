.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

###
Sum
###

The sum primitive sums :math:`N` tensors. The variable names follow the
standard :ref:`conventions-label`.

.. math::

       \dst(\overline{x}) =
           \sum\limits_{i = 1}^{N}
           scales(i) \cdot
           \src_i(\overline{x})

The sum primitive does not have a notion of forward or backward propagations.
The backward propagation for the sum operation is simply an identity
operation.

*******************
Execution Arguments
*******************

When executed, the inputs and outputs should be mapped to an execution argument index as specified by the following table.

====================== ========================
primitive input/output execution argument index
====================== ========================
:math:`\src`           |DNNL_ARG_MULTIPLE_SRC|
:math:`\dst`           |DNNL_ARG_DST|
====================== ========================

*****************
Operation Details
*****************

- The :math:`\dst` memory format can be either specified by a user or derived
  the most appropriate one by the primitive. The recommended way is to allow
  the primitive to choose the appropriate format.

- The sum primitive requires all source and destination tensors to have the
  same shape. Implicit broadcasting is not supported.

***********************
Post-ops and Attributes
***********************

The sum primitive does not support any post-ops or attributes.

******************
Data Types Support
******************

The sum primitive supports arbitrary data types for source and destination
tensors.

*******************
Data Representation
*******************

Sources, Destination
====================

The sum primitive works with arbitrary data tensors. There is no special
meaning associated with any logical dimensions.

***
API
***

.. doxygenstruct:: dnnl::sum
   :project: oneDNN
   :members:

.. vim: ts=3 sw=3 et spell spelllang=en
