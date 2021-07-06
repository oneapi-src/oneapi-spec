.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. _conventions-label:

###########
Conventions
###########

oneDNN specification relies on a set of standard naming conventions for
variables. This section describes these conventions.

***********************
Variable (Tensor) Names
***********************

Neural network models consist of operations of the following form:

.. math::  \dst = f(\src, \weights),

where :math:`\dst` and :math:`\src` are activation tensors, and
:math:`\weights` are learnable tensors.

The backward propagation therefore consists in computing the gradients with
respect to the :math:`\src`and :math:`\weights` respectively:

.. math::  \diffsrc = \mathrm{d} f_{\src}(\diffdst, \src, \weights, \dst),

and

.. math::  \diffweights = \mathrm{d} f_{\weights}(\diffdst, \src, \weights, \dst).

While oneDNN uses *src*, *dst*, and *weights* as generic names for the
activations and learnable tensors, for a specific operation there might be
commonly used and widely known specific names for these tensors. For instance,
the :ref:`convolution <convolution-label>` operation has a learnable tensor
called *bias*. For usability reasons, oneDNN primitives use such names in
initialization and other functions.

oneDNN uses the following commonly used notations for tensors:

+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| Name                 | Meaning                                                                                                                       |
+======================+===============================================================================================================================+
| ``src``              | Source tensor                                                                                                                 |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| ``dst``              | Destination tensor                                                                                                            |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| ``weights``          | Weights tensor                                                                                                                |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| ``bias``             | Bias tensor (used in :ref:`convolution <convolution-label>`, :ref:`inner product <inner_product-label>` and other primitives) |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| ``scale_shift``      | Scale and shift tensors (used in :ref:`batch_normalization-label` and :ref:`layer_normalization-label` primitives)            |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| ``workspace``        | Workspace tensor that carries additional information from the forward propagation to the backward propagation                 |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| ``scratchpad``       | Temporary tensor that is required to store the intermediate results                                                           |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| ``diff_src``         | Gradient tensor with respect to the source                                                                                    |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| ``diff_dst``         | Gradient tensor with respect to the destination                                                                               |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| ``diff_weights``     | Gradient tensor with respect to the weights                                                                                   |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| ``diff_bias``        | Gradient tensor with respect to the bias                                                                                      |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| ``diff_scale_shift`` | Gradient tensor with respect to the scale and shift                                                                           |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| ``*_layer``          | RNN layer data or weights tensors                                                                                             |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+
| ``*_iter``           | RNN recurrent data or weights tensors                                                                                         |
+----------------------+-------------------------------------------------------------------------------------------------------------------------------+

*********************
RNN-Specific Notation
*********************

The following notations are used when describing RNN primitives.

================= ====================================
Name              Semantics
================= ====================================
:math:`\cdot`     matrix multiply operator
:math:`*`         elementwise multiplication operator
W                 input weights
U                 recurrent weights
:math:`\Box^T`    transposition
B                 bias
h                 hidden state
a                 intermediate value
x                 input
:math:`\Box_t`    timestamp index
:math:`\Box_l`    layer index
activation        tanh, relu, logistic
c                 cell state
:math:`\tilde{c}` candidate state
i                 input gate
f                 forget gate
o                 output gate
u                 update gate
r                 reset gate
================= ====================================

