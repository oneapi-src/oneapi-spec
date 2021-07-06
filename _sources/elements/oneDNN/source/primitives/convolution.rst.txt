.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

.. _convolution-label:

#############################
Convolution and Deconvolution
#############################

The convolution and deconvolution primitives compute forward, backward, or
weight update for a batched convolution or deconvolution operations on 1D, 2D,
or 3D spatial data with bias.

The operations are defined by the following formulas. We show formulas only
for 2D spatial data which are straightforward to generalize to cases of higher
and lower dimensions. Variable names follow the standard
:ref:`conventions-label`.

*******
Forward
*******

Let :math:`\src`, :math:`\weights` and :math:`\dst` be :math:`N \times IC
\times IH \times IW`, :math:`OC \times IC \times KH \times KW`, and :math:`N
\times OC \times OH \times OW` tensors respectively. Let :math:`\bias` be a 1D
tensor with :math:`OC` elements.

Furthermore, let the remaining convolution parameters be:

+----------------------------------+--------------+--------------+--------------+-------------------------------------------------------------------------------------------------------------------+
| Parameter                        | Depth        | Height       | Width        | Comment                                                                                                           |
+==================================+==============+==============+==============+===================================================================================================================+
| Padding: Front, top, and left    | :math:`PD_L` | :math:`PH_L` | :math:`PW_L` | In the API ``padding_l`` indicates the corresponding vector of paddings (``_l`` in the name stands for **left**)  |
+----------------------------------+--------------+--------------+--------------+-------------------------------------------------------------------------------------------------------------------+
| Padding: Back, bottom, and right | :math:`PD_R` | :math:`PH_R` | :math:`PW_R` | In the API ``padding_r`` indicates the corresponding vector of paddings (``_r`` in the name stands for **right**) |
+----------------------------------+--------------+--------------+--------------+-------------------------------------------------------------------------------------------------------------------+
| Stride                           | :math:`SD`   | :math:`SH`   | :math:`SW`   | Convolution without strides is defined by setting the stride parameters to 1                                      |
+----------------------------------+--------------+--------------+--------------+-------------------------------------------------------------------------------------------------------------------+
| Dilation                         | :math:`DD`   | :math:`DH`   | :math:`DW`   | Non-dilated convolution is defined by setting the dilation parameters to 0                                        |
+----------------------------------+--------------+--------------+--------------+-------------------------------------------------------------------------------------------------------------------+

The following formulas show how oneDNN computes convolutions. They are broken
down into several types to simplify the exposition, but in reality the
convolution types can be combined.

To further simplify the formulas, we assume that :math:`\src(n, ic, ih, iw) =
0` if :math:`ih < 0`, or :math:`ih \geq IH`, or :math:`iw < 0`, or :math:`iw
\geq IW`.

Regular Convolution
===================

.. math::
   \dst(n, oc, oh, ow) & = \bias(oc) \\
   + \sum_{ic=0}^{IC-1} \sum_{kh=0}^{KH-1} \sum_{kw=0}^{KW-1} &
   \src(n, ic, oh', ow') \cdot \weights(oc, ic, kh, kw).

Here:

- :math:`oh' = oh \cdot SH + kh - PH_L`,

- :math:`ow' = ow \cdot SW + kw - PW_L`,

- :math:`OH = \left\lfloor{\frac{IH - KH + PH_L + PH_R}{SH}} \right\rfloor + 1`,

- :math:`OW = \left\lfloor{\frac{IW - KW + PW_L + PW_R}{SW}} \right\rfloor + 1`.

Convolution with Groups
=======================

oneDNN adds a separate groups dimension to memory objects representing
:math:`\weights` tensors and represents weights as :math:`G \times OC_G \times
IC_G \times KH \times KW` 5D tensors for 2D convolutions with groups.

.. math::

       \dst(n, g \cdot OC_G + oc_g, oh, ow) & = \bias(g \cdot OC_G + oc_g) \\
            + \sum_{ic_g=0}^{IC_G-1} \sum_{kh=0}^{KH-1} \sum_{kw=0}^{KW-1} &
              \src(n, g \cdot IC_G + ic_g, oh', ow')
              \cdot
              \weights(g, oc_g, ic_g, kh, kw),

where

- :math:`IC_G = \frac{IC}{G}`,

- :math:`OC_G = \frac{OC}{G}`, and

- :math:`oc_g \in [0, OC_G)`.

The case when :math:`OC_G = IC_G = 1` is also known as *a depthwise convolution*.

Convolution with Dilation
=========================

.. math::

       \dst(n, oc, oh, ow) & = \bias(oc) + \\
            + \sum_{ic=0}^{IC-1} \sum_{kh=0}^{KH-1} \sum_{kw=0}^{KW-1} &
              \src(n, ic, oh'', ow'')
              \cdot
              \weights(oc, ic, kh, kw).

Here:

- :math:`oh'' = oh \cdot SH + kh \cdot (DH + 1) - PH_L`,

- :math:`ow'' = ow \cdot SW + kw \cdot (DW + 1) - PW_L`,

- :math:`OH = \left\lfloor{\frac{IH - DKH + PH_L + PH_R}{SH}}  \right\rfloor +
  1,` where :math:`DKH = 1 + (KH - 1) \cdot (DH + 1)`, and

- :math:`OW = \left\lfloor{\frac{IW - DKW + PW_L + PW_R}{SW}}  \right\rfloor +
  1,` where :math:`DKW = 1 + (KW - 1) \cdot (DW + 1)`.


Deconvolution (Transposed Convolution)
======================================

Deconvolutions (also called fractionally-strided convolutions or transposed
convolutions) can be defined by swapping the forward and backward passes of a
convolution. One way to put it is to note that the weights define a
convolution, but whether it is a direct convolution or a transposed
convolution is determined by how the forward and backward passes are computed.

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

*******************
Execution Arguments
*******************

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

Convolution primitive supports the following combination of data types for
source, destination, and weights memory objects.

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

Like other CNN primitives, the convolution primitive expects the following
tensors:

+---------+-----------------------------------------------+----------------------------------------------------------------+
| Spatial | Source / Destination                          | Weights                                                        |
+=========+===============================================+================================================================+
| 1D      | :math:`N \times C \times W`                   | :math:`[G \times ] OC \times IC \times KW`                     |
+---------+-----------------------------------------------+----------------------------------------------------------------+
| 2D      | :math:`N \times C \times H \times W`          | :math:`[G \times ] OC \times IC \times KH \times KW`           |
+---------+-----------------------------------------------+----------------------------------------------------------------+
| 3D      | :math:`N \times C \times D \times H \times W` | :math:`[G \times ] OC \times IC \times KD \times KH \times KW` |
+---------+-----------------------------------------------+----------------------------------------------------------------+

Memory format of data and weights memory objects is critical for convolution
primitive performance. In the oneDNN programming model, convolution is one of
the few primitives that support the placeholder memory format tag |any| and
can define data and weight memory objects format based on the primitive
parameters. When using |any| it is necessary to first create a convolution
primitive descriptor and then query it for the actual data and weight memory
objects formats.

While convolution primitives can be created with memory formats specified
explicitly, the performance is likely to be suboptimal.

The table below shows the combinations for which *plain* memory formats the
convolution primitive is optimized for.

+------------+--------------------+--------------------------+------------------------------------------------------------+
| | Spatial  | | Convolution Type | | Data /                 | | Implementation optimized                                 |
|            |                    | | Weights logical tensor | | for memory formats                                       |
+------------+--------------------+--------------------------+------------------------------------------------------------+
| 1D, 2D, 3D |                    | |any|                    | *optimized*                                                |
+------------+--------------------+--------------------------+------------------------------------------------------------+
| 1D         | f32, bf16          | NCW / OIW, GOIW          | |ncw| (|abc|) / |oiw| (|abc|), |goiw| (|abcd|)             |
+------------+--------------------+--------------------------+------------------------------------------------------------+
| 1D         | f32, bf16          | NCW / OIW, GOIW          | |nwc| (|acb|) / |wio| (|cba|), |wigo| (|dcab|)             |
+------------+--------------------+--------------------------+------------------------------------------------------------+
| 1D         | int8               | NCW / OIW                | |nwc| (|acb|) / |wio| (|cba|)                              |
+------------+--------------------+--------------------------+------------------------------------------------------------+
| 2D         | f32, bf16          | NCHW / OIHW, GOIHW       | |nchw| (|abcd|) / |oihw| (|abcd|), |goihw| (|abcde|)       |
+------------+--------------------+--------------------------+------------------------------------------------------------+
| 2D         | f32, bf16          | NCHW / OIHW, GOIHW       | |nhwc| (|acdb|) / |hwio| (|cdba|), |hwigo| (|decab|)       |
+------------+--------------------+--------------------------+------------------------------------------------------------+
| 2D         | int8               | NCHW / OIHW, GOIHW       | |nhwc| (|acdb|) / |hwio| (|cdba|), |hwigo| (|decab|)       |
+------------+--------------------+--------------------------+------------------------------------------------------------+
| 3D         | f32, bf16          | NCDHW / OIDHW, GOIDHW    | |ncdhw| (|abcde|) / |oidhw| (|abcde|), |goidhw| (|abcdef|) |
+------------+--------------------+--------------------------+------------------------------------------------------------+
| 3D         | f32, bf16          | NCDHW / OIDHW, GOIDHW    | |ndhwc| (|acdeb|) / |dhwio| (|cdeba|), |dhwigo| (|defcab|) |
+------------+--------------------+--------------------------+------------------------------------------------------------+
| 3D         | int8               | NCDHW / OIDHW            | |ndhwc| (|acdeb|) / |dhwio| (|cdeba|)                      |
+------------+--------------------+--------------------------+------------------------------------------------------------+

***********************
Post-ops and Attributes
***********************

Post-ops and attributes enable you to modify the behavior of the convolution
primitive by applying the output scale to the result of the primitive and by
chaining certain operations after the primitive. The following attributes and
post-ops are supported:

+-------------+-----------+---------------------------------------------------------------+-------------------------------------------------------------------------------+------------------------+
| Propagation | Type      | Operation                                                     | Description                                                                   | Restrictions           |
+=============+===========+===============================================================+===============================================================================+========================+
| forward     | attribute | :any:`Output scale <dnnl::primitive_attr::set_output_scales>` | Scales the result of convolution by given scale factor(s)                     | int8 convolutions only |
+-------------+-----------+---------------------------------------------------------------+-------------------------------------------------------------------------------+------------------------+
| forward     | post-op   | :any:`Eltwise <dnnl::post_ops::append_eltwise>`               | Applies an elementwise operation to the result                                |                        |
+-------------+-----------+---------------------------------------------------------------+-------------------------------------------------------------------------------+------------------------+
| forward     | post-op   | :any:`Sum <dnnl::post_ops::append_sum>`                       | Adds the operation result to the destination tensor instead of overwriting it |                        |
+-------------+-----------+---------------------------------------------------------------+-------------------------------------------------------------------------------+------------------------+

The primitive supports dynamic quantization via run-time output scales. That
means a user could configure attributes with output scales set to the
|DNNL_RUNTIME_F32_VAL| wildcard value instead of the actual scales,
if the scales are not known at the primitive descriptor creation stage. In
this case, the user must provide the scales as an additional input memory
object with argument |DNNL_ARG_ATTR_OUTPUT_SCALES| during the
execution stage.

.. note::

   The library does not prevent using post-ops in training, but note that not
   all post-ops are feasible for training usage. For instance, using ReLU with
   non-zero negative slope parameter as a post-op would not produce an
   additional output ``workspace`` that is required to compute backward
   propagation correctly. Hence, in this particular case one should use
   separate convolution and eltwise primitives for training.

The following post-ops chaining should be supported by the library:

======================== ============================================
Type of convolutions     Post-ops sequence supported
======================== ============================================
f32 and bf16 convolution eltwise, sum, sum -> eltwise
int8 convolution         eltwise, sum, sum -> eltwise, eltwise -> sum
======================== ============================================

The attributes and post-ops take effect in the following sequence:

- Output scale attribute,

- Post-ops, in order they were attached.

The operations during attributes and post-ops applying are done in single
precision floating point data type. The conversion to the actual destination
data type happens just before the actual storing.

Example 1
=========

Consider the following pseudo code:

.. TODO replace pseudocode with real code

::

       attribute attr;
       attr.set_output_scale(alpha);
       attr.set_post_ops({
               { sum={scale=beta} },
               { eltwise={scale=gamma, type=tanh, alpha=ignore, beta=ignored }
           });

       convolution_forward(src, weights, dst, attr)

The would lead to the following:

.. math::

       \dst(\overline{x}) =
           \gamma \cdot \tanh \left(
               \alpha \cdot conv(\src, \weights) +
               \beta  \cdot \dst(\overline{x})
           \right)

Example 2
=========

The following pseudo code:

::

       attribute attr;
       attr.set_output_scale(alpha);
       attr.set_post_ops({
               { eltwise={scale=gamma, type=relu, alpha=eta, beta=ignored }
               { sum={scale=beta} },
           });

       convolution_forward(src, weights, dst, attr)

That would lead to the following:

.. math::

       \dst(\overline{x}) =
           \beta \cdot \dst(\overline{x}) +
           \gamma \cdot ReLU \left(
               \alpha \cdot conv(\src, \weights),
               \eta
           \right)

**********
Algorithms
**********

oneDNN implementations may implement convolution primitives using several
different algorithms which can be chosen by the user.

- *Direct* (|algorithm::convolution_direct|). The convolution
  operation is computed directly using SIMD instructions. This also includes
  implicit GEMM formulations which notably may require workspace.

- *Winograd* (|algorithm::convolution_winograd|). This algorithm
  reduces computational complexity of convolution at the expense of accuracy
  loss and additional memory operations. The implementation is based on the
  `Fast Algorithms for Convolutional Neural Networks by A. Lavin and S. Gray
  <https://arxiv.org/abs/1509.09308>`__. The Winograd algorithm often results
  in the best performance, but it is applicable only to particular shapes.
  Moreover, Winograd only supports int8 and f32 data types.

- *Auto* (|algorithm::convolution_auto|). In this case the library
  should automatically select the *best* algorithm based on the heuristics
  that take into account tensor shapes and the number of logical processors
  available.

***
API
***

.. doxygenstruct:: dnnl::convolution_forward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::convolution_backward_data
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::convolution_backward_weights
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::deconvolution_forward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::deconvolution_backward_data
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::deconvolution_backward_weights
   :project: oneDNN
   :members:

.. vim: ts=3 sw=3 et spell spelllang=en
