.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

.. _inner_product-label:

#############
Inner Product
#############

The inner product primitive (sometimes called *fully connected layer*) treats
each activation in the minibatch as a vector and computes its product with a
weights 2D tensor producing a 2D tensor as an output.

*******
Forward
*******

Let :math:`\src`, :math:`\weights`, :math:`\bias` and :math:`\dst` be :math:`N
\times IC`, :math:`OC \times IC`, :math:`OC`, and :math:`N \times OC` tensors,
respectively. Variable names follow the standard :ref:`conventions-label`.
Then:

.. math:: \dst(n, oc) = \bias(oc) + \sum_{ic=0}^{IC-1} \src(n, ic) \cdot \weights(oc, ic)

In cases where the :math:`\src` and :math:`\weights` tensors have spatial dimensions, they are flattened to 2D. For example, if they are 4D :math:`N \times IC' \times IH \times IW` and :math:`OC \times IC' \times KH \times KW` tensors, then the formula above is applied with :math:`IC = IC' \cdot IH \cdot IW`. In such cases, the :math:`\src` and :math:`\weights` tensors must have equal spatial dimensions (e.g. :math:`KH = IH` and :math:`KW = IW` for 4D tensors).

Difference Between Forward Training and Forward Inference
=========================================================

There is no difference between the |forward_training| and |forward_inference|
propagation kinds.

********
Backward
********

The backward propagation computes :math:`\diffsrc` based on :math:`\diffdst`
and :math:`\weights`.

The weights update computes :math:`\diffweights` and :math:`\diffbias` based
on :math:`\diffdst` and :math:`\src`.

.. note::

   The *optimized* memory formats :math:`\src` and :math:`\weights` might be
   different on forward propagation, backward propagation, and weights update.

Execution Arguments
===================

When executed, the inputs and outputs should be mapped to an execution
argument index as specified by the following table.

========================= ========================
Primitive input/output    Execution argument index
========================= ========================
:math:`\src`              |DNNL_ARG_SRC|
:math:`\weights`          |DNNL_ARG_WEIGHTS|
:math:`\bias`             |DNNL_ARG_BIAS|
:math:`\dst`              |DNNL_ARG_DST|
:math:`\diffsrc`          |DNNL_ARG_DIFF_SRC|
:math:`\diffweights`      |DNNL_ARG_DIFF_WEIGHTS|
:math:`\diffbias`         |DNNL_ARG_DIFF_BIAS|
:math:`\diffdst`          |DNNL_ARG_DIFF_DST|
========================= ========================


*****************
Operation Details
*****************

N/A

******************
Data Types Support
******************

Inner product primitive supports the following combination of data types for
source, destination, weights, and bias.

.. note::

   Here we abbreviate data types names for readability. For example, |_f32| is
   abbreviated to |f32|.

================== ============= ============= ======================== ========================
Propagation        Source        Weights       Destination              Bias
================== ============= ============= ======================== ========================
forward / backward |f32|         |f32|         |f32|                    |f32|
forward            |f16|         |f16|         |f16|                    |f16|
forward            |u8|, |s8|    |s8|          |u8|, |s8|, |s32|, |f32| |u8|, |s8|, |s32|, |f32|
forward            |bf16|        |bf16|        |f32|, |bf16|            |f32|, |bf16|
backward           |f32|, |bf16| |bf16|        |bf16|
weights update     |bf16|        |f32|, |bf16| |bf16|                   |f32|, |bf16|
================== ============= ============= ======================== ========================

*******************
Data Representation
*******************

Like other CNN primitives, the inner product primitive expects the following
tensors:

+---------+-----------------------------------------------+--------------------+----------------------------------------------------+
| Spatial | Source                                        | Destination        | Weights                                            |
+=========+===============================================+====================+====================================================+
| 1D      | :math:`N \times C \times W`                   | :math:`N \times C` | :math:`OC \times IC \times KW`                     |
+---------+-----------------------------------------------+--------------------+----------------------------------------------------+
| 2D      | :math:`N \times C \times H \times W`          | :math:`N \times C` | :math:`OC \times IC \times KH \times KW`           |
+---------+-----------------------------------------------+--------------------+----------------------------------------------------+
| 3D      | :math:`N \times C \times D \times H \times W` | :math:`N \times C` | :math:`OC \times IC \times KD \times KH \times KW` |
+---------+-----------------------------------------------+--------------------+----------------------------------------------------+

Memory format of data and weights memory objects is critical for inner product
primitive performance. In the oneDNN programming model, inner product
primitive is one of the few primitives that support the placeholder format
|any| and can define data and weight memory objects formats based on the
primitive parameters. When using |any| it is necessary to first create an
inner product primitive descriptor and then query it for the actual data and
weight memory objects formats.

The table below shows the combinations for which **plain** memory formats the
inner product primitive is optimized for. For the destination tensor (which is
always :math:`N \times C`) the memory format is always |nc| (|ab|).

+---------+---------------------------------+---------------------------------------------+
| Spatial | Source / Weights logical tensor | Implementation optimized for memory formats |
+=========+=================================+=============================================+
| 0D      | NC / OI                         | |nc| (|ab|) / |oi| (|ab|)                   |
+---------+---------------------------------+---------------------------------------------+
| 0D      | NC / OI                         | |nc| (|ab|) / |io| (|ba|)                   |
+---------+---------------------------------+---------------------------------------------+
| 1D      | NCW / OIW                       | |ncw| (|abc|) / |oiw| (|abc|)               |
+---------+---------------------------------+---------------------------------------------+
| 1D      | NCW / OIW                       | |nwc| (|acb|) / |wio| (|cba|)               |
+---------+---------------------------------+---------------------------------------------+
| 2D      | NCHW / OIHW                     | |nchw| (|abcd|) / |oihw| (|abcd|)           |
+---------+---------------------------------+---------------------------------------------+
| 2D      | NCHW / OIHW                     | |nhwc| (|acdb|) / |hwio| (|cdba|)           |
+---------+---------------------------------+---------------------------------------------+
| 3D      | NCDHW / OIDHW                   | |ncdhw| (|abcde|) / |oidhw| (|abcde|)       |
+---------+---------------------------------+---------------------------------------------+
| 3D      | NCDHW / OIDHW                   | |ndhwc| (|acdeb|) / |dhwio| (|cdeba|)       |
+---------+---------------------------------+---------------------------------------------+

***********************
Post-ops and Attributes
***********************

The following post-ops should be supported by inner product primitives:

+-------------+-----------+---------------------------------------------------------------+-------------------------------------------------------------------------------+--------------------------+
| Propagation | Type      | Operation                                                     | Description                                                                   | Restrictions             |
+=============+===========+===============================================================+===============================================================================+==========================+
| forward     | attribute | :any:`Output scale <dnnl::primitive_attr::set_output_scales>` | Scales the result of inner product by given scale factor(s)                   | int8 inner products only |
+-------------+-----------+---------------------------------------------------------------+-------------------------------------------------------------------------------+--------------------------+
| forward     | post-op   | :any:`Eltwise <dnnl::post_ops::append_eltwise>`               | Applies an elementwise operation to the result                                |                          |
+-------------+-----------+---------------------------------------------------------------+-------------------------------------------------------------------------------+--------------------------+
| forward     | post-op   | :any:`Sum <dnnl::post_ops::append_sum>`                       | Adds the operation result to the destination tensor instead of overwriting it |                          |
+-------------+-----------+---------------------------------------------------------------+-------------------------------------------------------------------------------+--------------------------+

***
API
***

.. doxygenstruct:: dnnl::inner_product_forward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::inner_product_backward_data
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::inner_product_backward_weights
   :project: oneDNN
   :members:

.. vim: ts=3 sw=3 et spell spelllang=en
