.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

######
Binary
######

The binary primitive computes a result of a binary elementwise operation
between tensors source 0 and source 1.

.. math::

   \dst(\overline{x}) = \src_0(\overline{x}) \mathbin{op} \src_1(\overline{x}),

where :math:`\overline{x} = (x_0, \ldots, x_n)` and :math:`op` is an operator
like addition, multiplication, maximum or minimum. Variable names follow the
standard :ref:`conventions-label`.

********************
Forward and Backward
********************

The binary primitive does not have a notion of forward or backward
propagations.

*******************
Execution Arguments
*******************

When executed, the inputs and outputs should be mapped to an execution
argument index as specified by the following table.

====================== ========================
Primitive input/output Execution argument index
====================== ========================
:math:`\src_0`         |DNNL_ARG_SRC_0|
:math:`\src_1`         |DNNL_ARG_SRC_1|
:math:`\dst`           |DNNL_ARG_DST|
====================== ========================

*****************
Operation Details
*****************

- The binary primitive requires all source and destination tensors to have
  the same number of dimensions.

- The binary primitive supports implicit broadcast semantics for source 1. It
  means that if some dimension has value of one, this value will be used to
  compute an operation with each point of source 0 for this dimension.

- The :math:`\dst` memory format can be either specified explicitly or by
  |memory::format_tag::any| (recommended), in which case the
  primitive will derive the most appropriate memory format based on the format
  of the source 0 tensor.

- Destination memory descriptor should completely match source 0 memory
  descriptor.

- The binary primitive supports in-place operations, meaning that source 0
  tensor may be used as the destination, in which case its data will be
  overwritten.

***********************
Post-ops and Attributes
***********************

The following attributes should be supported:

+-----------+--------------------------------------------------+--------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+
| Type      | Operation                                        | Description                                                                    | Restrictions                                                                                                |
+===========+==================================================+================================================================================+=============================================================================================================+
| Attribute | :any:`Scales <dnnl::primitive_attr::set_scales>` | Scales the corresponding input tensor by the given scale factor(s).            | The corresponding tensor has integer data type. Only one scale per tensor is supported. Input tensors only. |
+-----------+--------------------------------------------------+--------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+
| Post-op   | :any:`Sum <dnnl::post_ops::append_sum>`          | Adds the operation result to the destination tensor instead of overwriting it. | Must precede eltwise post-op.                                                                               |
+-----------+--------------------------------------------------+--------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+
| Post-op   | :any:`Eltwise <dnnl::post_ops::append_eltwise>`  | Applies an elementwise operation to the result.                                |                                                                                                             |
+-----------+--------------------------------------------------+--------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+

******************
Data Types Support
******************

The source and destination tensors may have |_f32|, |_bf16|, |_s8| or |_u8|
data types.

*******************
Data Representation
*******************

The binary primitive works with arbitrary data tensors. There is no special
meaning associated with any of tensors dimensions.

***
API
***

.. doxygenstruct:: dnnl::binary
   :project: oneDNN
   :members:


.. vim: ts=3 sw=3 et spell spelllang=en
