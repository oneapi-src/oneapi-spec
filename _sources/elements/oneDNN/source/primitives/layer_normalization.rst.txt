.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

.. _layer_normalization-label:

###################
Layer normalization
###################

The layer normalization primitive performs a forward or backward layer
normalization operation on a 2-5D data tensor.

The layer normalization operation performs normalization over the last logical
axis of the data tensor and is defined by the following formulas. We show
formulas only for 3D data, which are straightforward to generalize to cases of
higher dimensions. Variable names follow the standard
:ref:`conventions-label`.

*******
Forward
*******

.. math::

       \dst(t, n, c) =
          \gamma(c) \cdot
          \frac{\src(t, n, c) - \mu(t, n)} {\sqrt{\sigma^2(t, n) + \varepsilon}}
          + \beta(c),

where

- :math:`\gamma(c), \beta(c)` are optional scale and shift for a channel (see
  the |use_scaleshift| flag),

- :math:`\mu(t, n), \sigma^2(t, n)` are mean and variance (see
  |use_global_stats| flag), and

- :math:`\varepsilon` is a constant to improve numerical stability.

Mean and variance are computed at runtime or provided by a user. When mean and
variance are computed at runtime, the following formulas are used:

- :math:`\mu(t, n) = \frac{1}{C} \sum\limits_{c} \src(t, n, c)_{}`,

- :math:`\sigma^2(t, n) = \frac{1}{C} \sum\limits_{c} {}_{} (\src(t, n, c) -
  \mu(t, n))^2`.

The :math:`\gamma(c)` and :math:`\beta(c)` tensors are considered learnable.

Difference Between Forward Training and Forward Inference
=========================================================

If mean and variance are computed at runtime (i.e., |use_global_stats| is not
set), they become outputs for the propagation kind |forward_training| (because
they would be required during the backward propagation). Data layout for mean
and variance must be specified during initialization of the layer
normalization descriptor by passing the memory descriptor for statistics
(e.g., by passing ``stat_desc`` in
|layer_normalization_forward::desc::desc|). Mean and variance are
not exposed for the propagation kind |forward_inference|.

********
Backward
********

The backward propagation computes :math:`\diffsrc(t, n, c)`,
:math:`\diffgamma(c)^*`, and :math:`\diffbeta(c)^*` based on
:math:`\diffdst(t, n, c)`, :math:`src(t, n, c)`, :math:`\mu(t, n)`,
:math:`\sigma^2(t, n)`, :math:`\gamma(c) ^*`, and :math:`\beta(c) ^*`.

The tensors marked with an asterisk are used only when the primitive is
configured to use :math:`\gamma(c)`, and :math:`\beta(c)` (i.e.,
|use_scaleshift| is set).

*******************
Execution Arguments
*******************

Depending on the flags and propagation kind, the layer normalization primitive
requires different inputs and outputs. For clarity, a summary is shown below.

+----------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+
|                                        | |forward_inference|                                                                                  | |forward_training|                                                                                   | |backward|                                                                                                                                                        | |backward_data|        |
+========================================+======================================================================================================+======================================================================================================+===================================================================================================================================================================+========================+
| |normalization_flags_none|             | *In*: :math:`\src`  *Out*: :math:`\dst`                                                              | *In*: :math:`\src`  *Out*: :math:`\dst`, :math:`\mu`, :math:`\sigma^2`                               | *In*: :math:`\diffdst`, :math:`\src`, :math:`\mu`, :math:`\sigma^2` *Out*: :math:`\diffsrc`                                                                       | Same as for |backward| |
+----------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+
| |use_global_stats|                     | *In*: :math:`\src`, :math:`\mu`, :math:`\sigma^2` *Out*: :math:`\dst`                                | *In*: :math:`\src`, :math:`\mu`, :math:`\sigma^2` *Out*: :math:`\dst`                                | *In*: :math:`\diffdst`, :math:`\src`, :math:`\mu`, :math:`\sigma^2` *Out*: :math:`\diffsrc`                                                                       | Same as for |backward| |
+----------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+
| |use_scaleshift|                       | *In*: :math:`\src`, :math:`\gamma`, :math:`\beta` *Out*: :math:`\dst`                                | *In*: :math:`\src`, :math:`\gamma`, :math:`\beta` *Out*: :math:`\dst`, :math:`\mu`, :math:`\sigma^2` | *In*: :math:`\diffdst`, :math:`\src`, :math:`\mu`, :math:`\sigma^2`, :math:`\gamma`, :math:`\beta` *Out*: :math:`\diffsrc`, :math:`\diffgamma`, :math:`\diffbeta` | Not supported          |
+----------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+
| |use_global_stats| \| |use_scaleshift| | *In*: :math:`\src`, :math:`\mu`, :math:`\sigma^2`, :math:`\gamma`, :math:`\beta` *Out*: :math:`\dst` | *In*: :math:`\src`, :math:`\mu`, :math:`\sigma^2`, :math:`\gamma`, :math:`\beta` *Out*: :math:`\dst` | *In*: :math:`\diffdst`, :math:`\src`, :math:`\mu`, :math:`\sigma^2`, :math:`\gamma`, :math:`\beta` *Out*: :math:`\diffsrc`, :math:`\diffgamma`, :math:`\diffbeta` | Not supported          |
+----------------------------------------+------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------+

When executed, the inputs and outputs should be mapped to an execution
argument index as specified by the following table.

=============================================== =========================
Primitive input/output                          Execution argument index
=============================================== =========================
:math:`\src`                                    |DNNL_ARG_SRC|
:math:`\gamma, \beta`                           |DNNL_ARG_SCALE_SHIFT|
mean (:math:`\mu`)                              |DNNL_ARG_MEAN|
variance (:math:`\sigma`)                       |DNNL_ARG_VARIANCE|
:math:`\dst`                                    |DNNL_ARG_DST|
:math:`\diffdst`                                |DNNL_ARG_DIFF_DST|
:math:`\diffsrc`                                |DNNL_ARG_DIFF_SRC|
:math:`\diffgamma`, :math:`\diffbeta`           |DNNL_ARG_DIFF_SCALE_SHIFT|
=============================================== =========================

*****************
Operation Details
*****************

1. The different flavors of the primitive are partially controlled by the
   ``flags`` parameter that is passed to the operation descriptor
   initialization function (e.g.,
   |layer_normalization_forward::desc::desc|). Multiple flags can
   be combined using the bitwise OR operator (``|``).

2. For forward propagation, the mean and variance might be either computed at
   runtime (in which case they are outputs of the primitive) or provided by a
   user (in which case they are inputs). In the latter case, a user must set
   the |use_global_stats| flag. For the backward propagation, the mean and
   variance are always input parameters.

3. The memory format and data type for ``src`` and ``dst`` are assumed to be
   the same, and in the API they are typically referred to as ``data`` (e.g.,
   see ``data_desc`` in dnnl::layer_normalization_forward::desc::desc()). The
   same is true for ``diff_src`` and ``diff_dst``. The corresponding memory
   descriptors are referred to as ``diff_data_desc``.

4. Both forward and backward propagation support in-place operations, meaning
   that :math:`\src` can be used as input and output for forward propagation,
   and :math:`\diffdst` can be used as input and output for backward
   propagation. In case of an in-place operation, the original data will be
   overwritten. Note, however, that backward propagation requires original
   :math:`\src`, hence the corresponding forward propagation should not be
   performed in-place.

******************
Data Types Support
******************

The layer normalization supports the following combinations of data types.

.. note::

   Here we abbreviate data types names for readability. For example, |_f32| is
   abbreviated to |f32|.

================== ==================== ============================
Propagation        Source / Destination Mean / Variance / ScaleShift
================== ==================== ============================
forward / backward |f32|                |f32|
forward            |f16|                |f32|
================== ==================== ============================

*******************
Data Representation
*******************

Mean and Variance
=================

The mean (:math:`\mu`) and variance (:math:`\sigma^2`) are separate tensors
with number of dimensions equal to (:math:`data\_ndims - 1`) and size
:math:`(data\_dim[0], data\_dim[1], ..., data\_dim[ndims - 2])`.

The corresponding memory object can have an arbitrary memory format. Unless
mean and variance are computed at runtime and not exposed (i.e., propagation
kind is |forward_inference| and |use_global_stats| is not set), the user
should provide a memory descriptor for statistics when initializing the layer
normalization descriptor. For best performance, it is advised to use the
memory format that follows the data memory format; i.e., if the data format is
|tnc|, the best performance can be expected for statistics with the |tn|
format and suboptimal for statistics with the |nt| format.

Scale and Shift
===============

If used, the scale (:math:`\gamma`) and shift (:math:`\beta`) are combined in
a single 2D tensor of shape :math:`2 \times C`.

The format of the corresponding memory object must be |nc| (|ab|).

Source, Destination, and Their Gradients
========================================

The layer normalization primitive works with an arbitrary data tensor;
however, it was designed for RNN data tensors (i.e., |nc|, |tnc|, |ldnc|).
Unlike CNN data tensors, RNN data tensors have a single feature dimension.
Layer normalization performs normalization over the last logical dimension
(feature dimension for RNN tensors) across non-feature dimensions.

The layer normalization primitive is optimized for the following memory formats:

============== ============================================
Logical tensor Implementations optimized for memory formats
============== ============================================
NC             |nc| (|ab|)
TNC            |tnc| (|abc|), |ntc| (|bac|)
LDNC           |ldnc| (|abcd|)
============== ============================================

***
API
***

.. doxygenstruct:: dnnl::layer_normalization_forward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::layer_normalization_backward
   :project: oneDNN
   :members:

.. vim: ts=3 sw=3 et spell spelllang=en
