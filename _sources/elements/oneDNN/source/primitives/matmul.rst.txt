.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

#####################
Matrix Multiplication
#####################


The matrix multiplication (MatMul) primitive computes the product of two 2D
tensors with optional bias addition. Variable names follow the standard
:ref:`conventions-label`.

.. math::

       \dst(m, n) =
           \sum_{k=0}^{K} \left(
               \src(m, k) \cdot \weights(k, n)
           \right) +
           \bias(m, n)

The MatMul primitive also supports batching multiple independent matrix
multiplication operations, in which case the tensors must be 3D:

.. math::

       \dst(mb, m, n) =
           \sum_{k=0}^{K} \left(
               \src(mb, m, k) \cdot \weights(mb, k, n)
           \right) +
           \bias(mb, m, n)

The bias tensor is optional and supports implicit broadcast semantics: any of
its dimensions can be 1 and the same value would be used across the
corresponding dimension. However, :math:`\bias` must have the same number of
dimensions as the :math:`\dst`.

*******************
Execution Arguments
*******************

When executed, the inputs and outputs should be mapped to an execution
argument index as specified by the following table.

====================== ========================
Primitive input/output Execution argument index
====================== ========================
:math:`\src`           |DNNL_ARG_SRC|
:math:`\weights`       |DNNL_ARG_WEIGHTS|
:math:`\bias`          |DNNL_ARG_BIAS|
:math:`\dst`           |DNNL_ARG_DST|
====================== ========================

*****************
Operation Details
*****************

The MatMul primitive supports input and output tensors with run-time specified
shapes and memory formats. The run-time specified dimensions or strides are
specified using the |DNNL_RUNTIME_DIM_VAL| wildcard value during the primitive
initialization and creation stage. At the execution stage, the user must pass
fully specified memory objects so that the primitive is able to perform the
computations. Note that the less information about shapes or format is
available at the creation stage, the less performant execution will be. In
particular, if the shape is not known at creation stage, one cannot use the
special format tag |any| to enable an implementation to choose the most
appropriate memory format for the corresponding input or output shapes. On the
other hand, run-time specified shapes enable users to create a primitive once
and use it in different situations.

******************
Data Types Support
******************

The MatMul primitive supports the following combinations of data types for
source, destination, weights, and bias tensors.

.. note::

   Here we abbreviate data types names for readability. For example, |_f32| is
   abbreviated to |f32|.

========== ========== ========================= ========================
Source     Weights    Destination               Bias
========== ========== ========================= ========================
|f32|      |f32|       |f32|                    |f32|
|f16|      |f16|       |f16|                    |f16|
|bf16|     |bf16|      |bf16|                   |bf16|, |f32|
|u8|, |s8| |s8|, |u8|  |u8|, |s8|, |s32|, |f32| |u8|, |s8|, |s32|, |f32|
========== ========== ========================= ========================

*******************
Data Representation
*******************

The MatMul primitive expects the following tensors:

+------+------------------------------+------------------------------+------------------------------+-------------------------------------------------------------+
| Dims | Source                       | Weights                      | Destination                  | Bias (optional)                                             |
+======+==============================+==============================+==============================+=============================================================+
| 2D   | :math:`M \times K`           | :math:`K \times N`           | :math:`M \times N`           | :math:`(M \text{ or } 1)` :math:`\times (N \text{ or } 1)`  |
+------+------------------------------+------------------------------+------------------------------+-------------------------------------------------------------+
| 3D   | :math:`MB \times M \times K` | :math:`MB \times K \times N` | :math:`MB \times M \times N` | :math:`(MB \text{ or } 1)` :math:`\times (M \text{ or } 1)` |
|      |                              |                              |                              | :math:`\times (N \text{ or } 1)`                            |
+------+------------------------------+------------------------------+------------------------------+-------------------------------------------------------------+

The MatMul primitive is generally optimized for the case in which memory
objects use plain memory formats (with some restrictions; see the table
below). However, it is recommended to use the placeholder memory format |any|
if an input tensor is reused across multiple executions. In this case, the
primitive will set the most appropriate memory format for the corresponding
input tensor.

The table below shows the combinations of memory formats for which the MatMul
primitive is optimized. The memory format of the destination tensor should
always be |ab| for the 2D case and |abc| for the 3D one.

+------+-----------------------------------------------------------------------------+------------------------------------------------------+
| Dims | Logical tensors                                                             | MatMul is optimized for the following memory formats |
+======+=============================================================================+======================================================+
| 2D   | Source: :math:`M \times K`, Weights: :math:`K \times N`                     | Source: |ab| or |ba|, Weights: |ab| or |ba|          |
+------+-----------------------------------------------------------------------------+------------------------------------------------------+
| 3D   | Source: :math:`MB \times M \times K`, Weights: :math:`MB \times K \times N` | Source: |abc| or |acb|, Weights: |abc| or |acb|      |
+------+-----------------------------------------------------------------------------+------------------------------------------------------+

***********************
Attributes and Post-ops
***********************

Attributes and post-ops enable modifying the behavior of the MatMul primitive.
The following attributes and post-ops are supported:

+-----------+----------------------------------------------------------------+-------------------------------------------------------------------------------+------------------------+
| Type      | Operation                                                      | Description                                                                   | Restrictions           |
+===========+================================================================+===============================================================================+========================+
| Attribute | :any:`Output scales <dnnl::primitive_attr::set_output_scales>` | Scales the result by given scale factor(s)                                    |                        |
+-----------+----------------------------------------------------------------+-------------------------------------------------------------------------------+------------------------+
| Attribute | :any:`Zero points <dnnl::primitive_attr::set_zero_points>`     | Sets zero point(s) for the corresponding tensors                              | Int8 computations only |
+-----------+----------------------------------------------------------------+-------------------------------------------------------------------------------+------------------------+
| Post-op   | :any:`Eltwise <dnnl::post_ops::append_eltwise>`                | Applies an elementwise operation to the result                                |                        |
+-----------+----------------------------------------------------------------+-------------------------------------------------------------------------------+------------------------+
| Post-op   | :any:`Sum <dnnl::post_ops::append_sum>`                        | Adds the operation result to the destination tensor instead of overwriting it |                        |
+-----------+----------------------------------------------------------------+-------------------------------------------------------------------------------+------------------------+

To facilitate dynamic quantization, the primitive should support run-time
output scales. That means a user could configure attributes with output scales
set to the |DNNL_RUNTIME_F32_VAL| wildcard value instead of the actual scales,
if the scales are not known at the primitive descriptor creation stage. In
this case, the user must provide the scales as an additional input memory
object with argument |DNNL_ARG_ATTR_OUTPUT_SCALES| during the execution stage.

Similarly to run-time output scales, the primitive supports run-time zero
points. The wildcard value for zero points is |DNNL_RUNTIME_S32_VAL|. During
the execution stage, the corresponding memory object needs to be passed in the
argument with index set to (``DNNL_ARG_ATTR_ZERO_POINTS |
DNNL_ARG_${MEMORY}``). For instance, source tensor zero points memory argument
would be passed with index (``DNNL_ARG_ATTR_ZERO_POINTS | DNNL_ARG_SRC``).

***
API
***

.. doxygenstruct:: dnnl::matmul
   :project: oneDNN
   :members:

.. vim: ts=3 sw=3 et spell spelllang=en
