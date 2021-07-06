.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

#######
Pooling
#######

The pooling primitive performs forward or backward max or average pooling
operation on 1D, 2D, or 3D spatial data.

The pooling operation is defined by the following formulas. We show formulas
only for 2D spatial data which are straightforward to generalize to cases of
higher and lower dimensions. Variable names follow the standard
:ref:`conventions-label`.

*******
Forward
*******

Max pooling:

.. math::

       \dst(n, c, oh, ow) =
           \max\limits_{kh, kw}
           \left(
               \src(n, c, oh \cdot SH + kh - PH_L, ow \cdot SW +kw - PW_L)
           \right)

Average pooling:

.. math::

       \dst(n, c, oh, ow) =
           \frac{1}{DENOM}
           \sum\limits_{kh, kw}
               \src(n, c, oh \cdot SH + kh - PH_L, ow \cdot SW +kw - PW_L)

Here output spatial dimensions are calculated similarly to how they are done
for :ref:`convolution-label`.

Average pooling supports two algorithms:

- |pooling_avg_include_padding|, in which case :math:`DENOM = KH \cdot KW`,

- |pooling_avg_exclude_padding|, in which case :math:`DENOM` equals to the
  size of overlap between an averaging window and images.

Difference Between Forward Training and Forward Inference
=========================================================

Max pooling requires a ``workspace`` for the |forward_training| propagation
kind, and does not require it for |forward_inference| (see details below).

********
Backward
********

The backward propagation computes :math:`\diffsrc(n, c, h, w)`, based on
:math:`\diffdst(n, c, h, w)` and, in case of max pooling, ``workspace``.

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
workspace              |DNNL_ARG_WORKSPACE|
:math:`\diffsrc`       |DNNL_ARG_DIFF_SRC|
:math:`\diffdst`       |DNNL_ARG_DIFF_DST|
====================== ========================

*****************
Operation Details
*****************

1. During training, max pooling requires a workspace on forward
   (|forward_training|) and backward passes to save indices where a maximum
   was found. The workspace format is opaque, and the indices cannot be
   restored from it. However, one can use backward pooling to perform
   up-sampling (used in some detection topologies). The workspace can be
   created via |pooling_forward::primitive_desc::workspace_desc|.

2. A user can use memory format tag |any| for ``dst`` memory descriptor when
   creating pooling forward propagation. The library would derive the
   appropriate format from the ``src`` memory descriptor. However, the ``src``
   itself must be defined. Similarly, a user can use memory format tag |any|
   for the ``diff_src`` memory descriptor when creating pooling backward
   propagation.

*****************
Data Type Support
*****************

The pooling primitive supports the following combinations of data types.

.. note::

   Here we abbreviate data types names for readability. For example, |_f32| is
   abbreviated to |f32|.

+--------------------+----------------------+--------------------------------------------------------+
| Propagation        | Source / Destination | Accumulation data type (used for average pooling only) |
+====================+======================+========================================================+
| forward / backward | |f32|, |bf16|        | |f32|                                                  |
+--------------------+----------------------+--------------------------------------------------------+
| forward            | |f16|                | |f16|                                                  |
+--------------------+----------------------+--------------------------------------------------------+
| forward            | |s8|, |u8|, |s32|    | |s32|                                                  |
+--------------------+----------------------+--------------------------------------------------------+

*******************
Data Representation
*******************

Source, Destination, and Their Gradients
========================================

Like other CNN primitives, the pooling primitive expects data to be an
:math:`N \times C \times W` tensor for the 1D spatial case, an :math:`N \times
C \times H \times W` tensor for the 2D spatial case, and an :math:`N \times C
\times D \times H \times W` tensor for the 3D spatial case.

The pooling primitive is optimized for the following memory formats:

+---------+----------------+-------------+----------------------------------------------------+
| Spatial | Logical tensor | Data type   | Implementations optimized for memory formats       |
+=========+================+=============+====================================================+
| 1D      | NCW            | f32         | |ncw| (|abc|), |nwc| (|acb|), *optimized^*         |
+---------+----------------+-------------+----------------------------------------------------+
| 1D      | NCW            | s32, s8, u8 | |nwc| (|acb|), *optimized^*                        |
+---------+----------------+-------------+----------------------------------------------------+
| 2D      | NCHW           | f32         | |nchw| (|abcd|), |nhwc| (|acdb|), *optimized^*     |
+---------+----------------+-------------+----------------------------------------------------+
| 2D      | NCHW           | s32, s8, u8 | |nhwc| (|acdb|), *optimized^*                      |
+---------+----------------+-------------+----------------------------------------------------+
| 3D      | NCDHW          | f32         | |ncdhw| (|abcde|), |ndhwc| (|acdeb|), *optimized^* |
+---------+----------------+-------------+----------------------------------------------------+
| 3D      | NCDHW          | s32, s8, u8 | |ndhwc| (|acdeb|), *optimized^*                    |
+---------+----------------+-------------+----------------------------------------------------+

Here *optimized^* means the format that comes out of any preceding
compute-intensive primitive.

***********************
Post-ops and Attributes
***********************

The pooling primitive does not support any post-ops or attributes.

***
API
***

.. doxygenstruct:: dnnl::pooling_forward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::pooling_backward
   :project: oneDNN
   :members:

.. vim: ts=3 sw=3 et spell spelllang=en
