.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

#######
Softmax
#######

The softmax primitive performs softmax along a particular axis on data with
arbitrary dimensions. All other axes are treated as independent (batch).

In general form, the operation is defined by the following formulas. The
variable names follow the standard :ref:`conventions-label`.

*******
Forward
*******

.. math::

       \dst(\overline{ou}, c, \overline{in}) =
           \frac
           {e^{\src(\overline{ou}, c, \overline{in}) - \nu(\overline{ou}, \overline{in})}}
           {
               \sum\limits_{ic}
                   e^{\src(\overline{ou}, ic, \overline{in}) - \nu(\overline{ou}, \overline{in})}
           },

where

- :math:`c` axis over which the softmax computation is computed on,

- :math:`\overline{ou}` is the outermost index (to the left of softmax axis),

- :math:`\overline{in}` is the innermost index (to the right of softmax
  axis), and

- :math:`\nu` is used to produce more accurate results and defined as:

.. math::

       \nu(\overline{ou}, \overline{in}) =
           \max\limits_{ic}
           \src(\overline{ou}, ic, \overline{in})

Difference Between Forward Training and Forward Inference
=========================================================

There is no difference between the |forward_training| and |forward_inference|
propagation kinds.

********
Backward
********

The backward propagation computes :math:`\diffsrc(ou, c, in)`, based on
:math:`\diffdst(ou, c, in)` and :math:`\dst(ou, c, in)`.

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

1. Both forward and backward propagation support in-place operations, meaning
   that ``src`` can be used as input and output for forward propagation, and
   ``diff_dst`` can be used as input and output for backward propagation. In
   case of in-place operation, the original data will be overwritten.

***********************
Post-ops and Attributes
***********************

The softmax primitive does not have to support any post-ops or attributes.

******************
Data Types Support
******************

The softmax primitive supports the following combinations of data types.

.. note::

   Here we abbreviate data types names for readability. For example, |_f32| is
   abbreviated to |f32|.

================== ====================
Propagation        Source / Destination
================== ====================
forward / backward |bf16|, |f32|
forward            |f16|
================== ====================

*******************
Data Representation
*******************

Source, Destination, and Their Gradients
========================================

The softmax primitive works with arbitrary data tensors. There is no special
meaning associated with any logical dimensions. However, the softmax axis is
typically referred to as channels (hence in formulas we use :math:`c`).

***
API
***

.. doxygenstruct:: dnnl::softmax_forward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::softmax_backward
   :project: oneDNN
   :members:


.. vim: ts=3 sw=3 et spell spelllang=en
