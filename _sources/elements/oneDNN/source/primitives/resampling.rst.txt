.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

##########
Resampling
##########

The resampling primitive computes forward or backward resampling operation on
1D, 2D, or 3D spatial data. Resampling performs spatial scaling of original
tensor using one of the supported interpolation algorithms:

- Nearest Neighbor

- Linear (or Bilinear for 2D spatial tensor, Trilinear for 3D spatial tensor).

Resampling operation is defined by the source tensor and scaling factors in
each spatial dimension. Upsampling and downsampling are the alternative terms
for resampling that are used when all scaling factors are greater (upsampling)
or less (downsampling) than one.

The resampling operation is defined by the following formulas. We show
formulas only for 2D spatial data which are straightforward to generalize to
cases of higher and lower dimensions. Variable names follow the standard
:ref:`conventions-label`.

Let :math:`\src` and :math:`\dst` be :math:`N \times C \times IH \times IW`
and :math:`N \times C \times OH \times OW` tensors respectively. Let
:math:`F_h = \frac{OH}{IH}` and :math:`F_w = \frac{OW}{IW}` define scaling
factors in each spatial dimension.

The following formulas show how oneDNN computes resampling for nearest
neighbor and bilinear interpolation methods. To further simplify the formulas,
we assume the following:

- :math:`\src(n, ic, ih, iw) = 0` if :math:`ih < 0` or :math:`iw < 0`,

- :math:`\src(n, ic, ih, iw) = \src(n, ic, IH - 1, iw)` if :math:`ih \geq IH`,

- :math:`\src(n, ic, ih, iw) = \src(n, ic, ih, IW - 1)` if :math:`iw \geq IW`.

*******
Forward
*******

Nearest Neighbor Resampling
===========================

.. math:: \dst(n, c, oh, ow) =  \src(n, c, ih, iw)

where

-  :math:`ih = [\frac{oh + 0.5} {F_h} - 0.5]`,
-  :math:`iw = [\frac{ow + 0.5} {F_w} - 0.5]`.

Bilinear Resampling
====================

.. math::

       \dst(n, c, oh, ow) =
               \src(n, c, ih_0, iw_0) \cdot W_{ih} \cdot W_{iw} + \\
               \src(n, c, ih_1, iw_0) \cdot (1 - W_{ih}) \cdot W_{iw} + \\
               \src(n, c, ih_0, iw_1) \cdot W_{ih} \cdot (1 - W_{iw}) + \\
               \src(n, c, ih_1, iw_1) \cdot (1 - W_{ih}) \cdot (1 - W_{iw}) \\

where

- :math:`ih_0 = \left\lfloor{\frac {oh + 0.5} {F_h} - 0.5}\right\rfloor`,

- :math:`ih_1 = \left\lceil {\frac {oh + 0.5} {F_h} - 0.5}\right\rceil`,

- :math:`iw_0 = \left\lfloor{\frac {ow + 0.5} {F_w} - 0.5}\right\rfloor`,

- :math:`iw_1 = \left\lceil {\frac {ow + 0.5} {F_w} - 0.5}\right\rceil`,

- :math:`W_{ih} = \frac{oh + 0.5}{F_h} - 0.5 - ih_0`,

- :math:`W_{iw} = \frac{ow + 0.5}{F_w} - 0.5 - iw_0`.

Difference Between Forward Training and Forward Inference
=========================================================

There is no difference between the |forward_training| and |forward_inference|
propagation kinds.

********
Backward
********

The backward propagation computes :math:`\diffsrc` based on :math:`\diffdst`.

*******************
Execution Arguments
*******************

When executed, the inputs and outputs should be mapped to an execution
argument index as specified by the following table.

====================== ========================
Primitive input/output Execution argument index
====================== ========================
:math:`\src`           |DNNL_ARG_SRC|
:math:`\dst`           |DNNL_ARG_DST|
:math:`\diffsrc`       |DNNL_ARG_DIFF_SRC|
:math:`\diffdst`       |DNNL_ARG_DIFF_DST|
====================== ========================

*****************
Operation Details
*****************

1. Resampling implementation supports data with arbitrary data tag (|nchw|,
   |nhwc|, etc.) but memory tags for ``src`` and ``dst`` are expected to be
   the same. Resampling primitive supports ``dst`` and ``diff_src`` memory tag
   |any| and can define destination format based on source format.

2. Resampling descriptor can be created by specifying the source and
   destination memory descriptors, only the source descriptor and floating
   point factors, or the source and destination memory descriptors and
   factors.  In case when user does not provide the destination descriptor,
   the destination dimensions are deduced using the factors:
   :math:`output\_spatial\_size = \left\lfloor{\frac{input\_spatial\_size} {F}}\right\rfloor`.

.. note::

   Resampling algorithm uses factors as defined by the relation :math:`F =
   \frac{output\_spatial\_size} {input\_spatial\_size}` that do not
   necessarily equal to the ones passed by the user.

******************
Data Types Support
******************

Resampling primitive supports the following combination of data types for
source and destination memory objects.

.. note::

   Here we abbreviate data types names for readability. For example, |_f32| is
   abbreviated to |f32|.

================== ====================
Propagation        Source / Destination
================== ====================
forward / backward |f32|, |bf16|
forward            |f16|, |s8|, |u8|
================== ====================

***********************
Post-ops and Attributes
***********************

The resampling primitive does not support any post-ops or attributes.

***
API
***

.. doxygenstruct:: dnnl::resampling_forward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::resampling_backward
   :project: oneDNN
   :members:


.. vim: ts=3 sw=3 et spell spelllang=en
