.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

.. _batch_normalization-label:

###################
Batch Normalization
###################

The batch normalization primitive performs a forward or backward batch
normalization operation on tensors with number of dimensions equal to 2 or
more. Variable names follow the standard :ref:`conventions-label`.

The batch normalization operation is defined by the following formulas. We
show formulas only for 2D spatial data which are straightforward to generalize
to cases of higher and lower dimensions.

The different flavors of the primitive are controlled by the ``flags``
parameter that is passed to the operation descriptor initialization function
like |batch_normalization_forward::desc::desc|. Multiple flags can
be combined using the bitwise OR operator (``|``).

*******
Forward
*******

.. math::

       \dst(n, c, h, w) =
          \gamma(c) \cdot
          \frac{\src(n, c, h, w) - \mu(c)} {\sqrt{\sigma^2(c) + \varepsilon}}
          + \beta(c),

where

- :math:`\gamma(c)` and :math:`\beta(c)` are optional scale and shift for a
  channel (controlled using the |use_scaleshift| flag),

- :math:`\mu(c)` and :math:`\sigma^2(c)` are mean and variance for a channel
  (controlled using the |use_global_stats| flag), and

- :math:`\varepsilon` is a constant to improve numerical stability.

Mean and variance are computed at runtime or provided by a user. When mean and
variance are computed at runtime, the following formulas are used:

- :math:`\mu(c) = \frac{1}{NHW} \sum\limits_{nhw} \src(n, c, h, w)_{}`,

- :math:`\sigma^2(c)
  = \frac{1}{NHW} \sum\limits_{nhw} {}_{} (\src(n, c, h, w) - \mu(c))^2`.

The :math:`\gamma(c)` and :math:`\beta(c)` tensors are considered learnable.

In the training mode, the primitive also optionally supports fusion with ReLU
activation with zero negative slope applied to the result (see
|fuse_norm_relu| flag).

.. note::

   The batch normalization primitive computes population mean and variance and
   not the sample or unbiased versions that are typically used to compute
   running mean and variance. \* Using the mean and variance computed by the
   batch normalization primitive, running mean and variance :math:`\hat\mu_i`
   and :math:`\hat\sigma^2_i` where :math:`i` is iteration number, can be
   computed as:

   .. math::

          \hat\mu_{i+1} = \alpha \cdot \hat\mu_i + (1 - \alpha) \cdot \mu, \\
          \hat\sigma^2_{i+1} = \alpha \cdot \hat\sigma^2_i + (1 - \alpha) \cdot \sigma^2.

Difference Between Forward Training and Forward Inference
=========================================================

- If mean and variance are computed at runtime (i.e., |use_global_stats| is
  not set), they become outputs for the propagation kind |forward_training|
  (because they would be required during the backward propagation) and are not
  exposed for the propagation kind |forward_inference|.

- If batch normalization is created with ReLU fusion (i.e., |fuse_norm_relu|
  is set), for the propagation kind |forward_training| the primitive would
  produce a ``workspace`` memory as one extra output. This memory is required
  to compute the backward propagation. When the primitive is executed with
  propagation kind |forward_inference|, the workspace is not produced.
  Behavior would be the same as creating a batch normalization primitive with
  ReLU as a post-op (see section below).

********
Backward
********

The backward propagation computes :math:`\diffsrc(n, c, h, w)`,
:math:`\diffgamma(c)^*`, and :math:`\diffbeta(c)^*` based on
:math:`\diffdst(n, c, h, w)`, :math:`\src(n, c, h, w)`, :math:`\mu(c)`,
:math:`\sigma^2(c)`, :math:`\gamma(c) ^*`, and :math:`\beta(c) ^*`.

The tensors marked with an asterisk are used only when the primitive is
configured to use :math:`\gamma(c)` and :math:`\beta(c)` (i.e.,
|use_scaleshift| is set).

*******************
Execution Arguments
*******************

Depending on the flags and propagation kind, the batch normalization primitive
requires different inputs and outputs. For clarity, a summary is shown below.

+----------------------------------------+-------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+
|                                        | |forward_inference|                                                                                   | |forward_training|                                                                                    | |backward|                                                                                                                                                         | |backward_data|                                                                              |
+========================================+=======================================================================================================+=======================================================================================================+====================================================================================================================================================================+==============================================================================================+
| |normalization_flags_none|             | *In*: :math:`\src`; *Out*: :math:`\dst`                                                               | *In*: :math:`\src`; *Out*: :math:`\dst`, :math:`\mu`, :math:`\sigma^2`                                | *In*: :math:`\diffdst`, :math:`\src`, :math:`\mu`, :math:`\sigma^2`; *Out*: :math:`\diffsrc`                                                                       | Same as for |backward|                                                                       |
+----------------------------------------+-------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+
| |use_global_stats|                     | *In*: :math:`\src`, :math:`\mu`, :math:`\sigma^2`; *Out*: :math:`\dst`                                | *In*: :math:`\src`, :math:`\mu`, :math:`\sigma^2`; *Out*: :math:`\dst`                                | *In*: :math:`\diffdst`, :math:`\src`, :math:`\mu`, :math:`\sigma^2`; *Out*: :math:`\diffsrc`                                                                       | Same as for |backward|                                                                       |
+----------------------------------------+-------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+
| |use_scaleshift|                       | *In*: :math:`\src`, :math:`\gamma`, :math:`\beta`; *Out*: :math:`\dst`                                | *In*: :math:`\src`, :math:`\gamma`, :math:`\beta`; *Out*: :math:`\dst`, :math:`\mu`, :math:`\sigma^2` | *In*: :math:`\diffdst`, :math:`\src`, :math:`\mu`, :math:`\sigma^2`, :math:`\gamma`, :math:`\beta`; *Out*: :math:`\diffsrc`, :math:`\diffgamma`, :math:`\diffbeta` | Not supported                                                                                |
+----------------------------------------+-------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+
| |use_global_stats| \| |use_scaleshift| | *In*: :math:`\src`, :math:`\mu`, :math:`\sigma^2`, :math:`\gamma`, :math:`\beta`; *Out*: :math:`\dst` | *In*: :math:`\src`, :math:`\mu`, :math:`\sigma^2`, :math:`\gamma`, :math:`\beta`; *Out*: :math:`\dst` | *In*: :math:`\diffdst`, :math:`\src`, :math:`\mu`, :math:`\sigma^2`, :math:`\gamma`, :math:`\beta`; *Out*: :math:`\diffsrc`, :math:`\diffgamma`, :math:`\diffbeta` | Not supported                                                                                |
+----------------------------------------+-------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+
| ``flags`` \| |fuse_norm_relu|          | *In*: same as with ``flags``; *Out*: same as with ``flags``                                           | *In*: same as with ``flags``; *Out*: same as with ``flags``, workspace                                | *In*: same as with ``flags``, workspace; *Out*: same as with ``flags``                                                                                             | Same as for |backward| if ``flags`` do not contain |use_scaleshift|; not supported otherwise |
+----------------------------------------+-------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+

When executed, the inputs and outputs should be mapped to an execution
argument index as specified by the following table.

============================= =========================
Primitive input/output        Execution argument index
============================= =========================
:math:`\src`                  |DNNL_ARG_SRC|
:math:`\gamma, \beta`         |DNNL_ARG_SCALE_SHIFT|
mean (:math:`\mu`)            |DNNL_ARG_MEAN|
variance (:math:`\sigma`)     |DNNL_ARG_VARIANCE|
:math:`\dst`                  |DNNL_ARG_DST|
workspace                     |DNNL_ARG_WORKSPACE|
:math:`\diffdst`              |DNNL_ARG_DIFF_DST|
:math:`\diffsrc`              |DNNL_ARG_DIFF_SRC|
:math:`\diffgamma, \diffbeta` |DNNL_ARG_DIFF_SCALE_SHIFT|
============================= =========================

*****************
Operation Details
*****************

1. For forward propagation, the mean and variance might be either computed at
   runtime (in which case they are outputs of the primitive) or provided by a
   user (in which case they are inputs). In the latter case, a user must set
   the |use_global_stats| flag. For the backward propagation, the mean and
   variance are always input parameters.

2. The memory format and data type for ``src`` and ``dst`` are assumed to be
   the same, and in the API they are typically referred to as ``data`` (e.g.,
   see ``data_desc`` in |batch_normalization_forward::desc::desc|).
   The same is true for ``diff_src`` and ``diff_dst``. The corresponding
   memory descriptors are referred to as ``diff_data_desc``.

3. Both forward and backward propagation support in-place operations, meaning
   that :math:`\src` can be used as input and output for forward propagation,
   and :math:`\diffdst` can be used as input and output for backward
   propagation. In case of an in-place operation, the original data will be
   overwritten. Note, however, that backward propagation requires original
   :math:`\src`, hence the corresponding forward propagation should not be
   performed in-place.

4. As mentioned above, the batch normalization primitive can be fused with
   ReLU activation even in the training mode. In this case, on the forward
   propagation the primitive has one additional output, ``workspace``, that
   should be passed during the backward propagation.

******************
Data Types Support
******************

The operation supports the following combinations of data types.

.. note::

   Here we abbreviate data types names for readability. For example, |_f32| is
   abbreviated to |f32|.

================== ==================== ============================
Propagation        Source / Destination Mean / Variance / ScaleShift
================== ==================== ============================
forward / backward |f32|, |bf16|        |f32|
forward            |f16|                |f32|
forward            |s8|                 |f32|
================== ==================== ============================

*******************
Data Representation
*******************

Source, Destination, and Their Gradients
========================================

Like other CNN primitives, the batch normalization primitive expects data to
be :math:`N \times C \times SP_n \times \cdots \times SP_0` tensor.

The batch normalization primitive is optimized for the following memory
formats:

======= ============== ==================================================================
Spatial Logical tensor Implementations optimized for memory formats
======= ============== ==================================================================
0D      NC             |nc| (|ab|)
1D      NCW            |ncw| (|abc|), |nwc| (|acb|), *optimized*
2D      NCHW           |nchw| (|abcd|), |nhwc| (|acdb|), *optimized*
3D      NCDHW          |ncdhw| (|abcde|), |ndhwc| (|acdeb|), *optimized*
======= ============== ==================================================================

Here *optimized* means the format chosen by the preceding compute-intensive
primitive.

Statistics Tensors
==================

The mean (:math:`\mu`) and variance (:math:`\sigma^2`) are separate 1D tensors
of size :math:`C`.

The format of the corresponding memory object must be |x| (|a|).

If used, the scale (:math:`\gamma`) and shift (:math:`\beta`) are combined in
a single 2D tensor of shape :math:`2 \times C`.

The format of the corresponding memory object must be |nc| (|ab|).

***********************
Post-ops and Attributes
***********************

+-------------+---------+-----------+---------------------------------------------+
| Propagation | Type    | Operation | Description                                 |
+=============+=========+===========+=============================================+
| forward     | post-op | eltwise   | Applies an eltwise operation to the output. |
+-------------+---------+-----------+---------------------------------------------+

.. note::

   Using ReLU as a post-op does not produce additional output in the
   ``workspace`` that is required to compute backward propagation correctly.
   Hence, one should use the |fuse_norm_relu| flag for training.

***
API
***

.. doxygenstruct:: dnnl::batch_normalization_forward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::batch_normalization_backward
   :project: oneDNN
   :members:

.. vim: ts=3 sw=3 et spell spelllang=en
