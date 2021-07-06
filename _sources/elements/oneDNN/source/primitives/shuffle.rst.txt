.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

#######
Shuffle
#######

The shuffle primitive shuffles data along the shuffle axis (here is designated
as :math:`C`) with the group parameter :math:`G`. Namely, the shuffle axis is
thought to be a 2D tensor of size :math:`(\frac{C}{G} \times G)` and it is
being transposed to :math:`(G \times \frac{C}{G})`. Variable names follow the
standard :ref:`conventions-label`.

The formal definition is shown below:

*******
Forward
*******

.. math::

       \dst(\overline{ou}, c, \overline{in}) =
       \src(\overline{ou}, c', \overline{in})

where

- :math:`c` dimension is called a shuffle ``axis``,

- :math:`G` is a ``group_size``,

- :math:`\overline{ou}` is the outermost indices (to the left from shuffle
  axis),

- :math:`\overline{in}` is the innermost indices (to the right from shuffle
  axis), and

- :math:`c'` and :math:`c` relate to each other as define by the system:

.. math::

       \begin{cases}
           c  &= u + v \cdot \frac{C}{G}, \\
           c' &= u \cdot G + v, \\
       \end{cases}

Here, :math:`0 \leq u < \frac{C}{G}` and :math:`0 \leq v < G`.

Difference Between Forward Training and Forward Inference
=========================================================

There is no difference between the |forward_training| and |forward_inference|
propagation kinds.

********
Backward
********

The backward propagation computes :math:`\diffsrc(ou, c, in)`, based on
:math:`\diffdst(ou, c, in)`.

Essentially, backward propagation is the same as forward propagation with
:math:`g` replaced by :math:`C / g`.

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

1. The memory format and data type for ``src`` and ``dst`` are assumed to be
   the same, and in the API are typically referred as ``data`` (e.g., see
   ``data_desc`` in |shuffle_forward::desc::desc|). The same holds
   for ``diff_src`` and ``diff_dst``. The corresponding memory descriptors are
   referred to as ``diff_data_desc``.

******************
Data Types Support
******************

The shuffle primitive supports the following combinations of data types:

.. note::

   Here we abbreviate data types names for readability. For example, |_f32| is
   abbreviated to |f32|.

================== ====================
Propagation        Source / Destination
================== ====================
forward / backward |f32|, |bf16|
forward            |s32|, |s8|, |u8|
================== ====================

************
Data Layouts
************

The shuffle primitive works with arbitrary data tensors. There is no special
meaning associated with any logical dimensions. However, the shuffle axis is
typically referred to as channels (hence in formulas we use :math:`c`).

Shuffle operation typically appear in CNN topologies. Hence, in the library
the shuffle primitive is optimized for the corresponding memory formats:

+---------+----------------+--------------+----------------------------------------------------+
| Spatial | Logical tensor | Shuffle Axis | Implementations optimized for memory formats       |
+=========+================+==============+====================================================+
| 2D      | NCHW           | 1 (C)        | |nchw| (|abcd|), |nhwc| (|acdb|), *optimized^*     |
+---------+----------------+--------------+----------------------------------------------------+
| 3D      | NCDHW          | 1 (C)        | |ncdhw| (|abcde|), |ndhwc| (|acdeb|), *optimized^* |
+---------+----------------+--------------+----------------------------------------------------+

Here *optimized^* means the format that comes out of any preceding
compute-intensive primitive.

***********************
Post-ops and Attributes
***********************

The shuffle primitive does not have to support any post-ops or attributes.

***
API
***

.. doxygenstruct:: dnnl::shuffle_forward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::shuffle_backward
   :project: oneDNN
   :members:


.. vim: ts=3 sw=3 et spell spelllang=en
