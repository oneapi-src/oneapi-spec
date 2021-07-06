.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

.. _rnn-label:

###
RNN
###

The RNN primitive computes a stack of unrolled recurrent cells, as depicted in
Figure 1. :math:`\bias`, :math:`\srciter` and :math:`\dstiter` are optional
parameters. If not provided, :math:`\bias` and :math:`\srciter` default to 0.
Variable names follow the standard :ref:`conventions-label`.

.. image:: ../_static/unrolled_stack_rnn.jpg

The RNN primitive supports four modes for evaluation direction:

- ``left2right`` will process the input data timestamps by increasing order,

- ``right2left`` will process the input data timestamps by decreasing order,

- ``bidirectional_concat`` will process all the stacked layers from
  ``left2right`` and from ``right2left`` independently, and will concatenate
  the output in :math:`\dstlayer` over the channel dimension,

- ``bidirectional_sum`` will process all the stacked layers from
  ``left2right`` and from ``right2left`` independently, and will sum the two
  outputs to :math:`\dstlayer`.

Even though the RNN primitive supports passing a different number of channels
for :math:`\srclayer`, :math:`\srciter`, :math:`\dstlayer`, and
:math:`\dstiter`, we always require the following conditions in order for the
dimension to be consistent:

- :math:`channels(\dstlayer) = channels(\dstiter)`,

- when :math:`T > 1`, :math:`channels(\srciter) = channels(\dstiter)`,

- when :math:`L > 1`, :math:`channels(\srclayer) = channels(\dstlayer)`,

- when using the ``bidirectional_concat`` direction,
  :math:`channels(\dstlayer) = 2 * channels(\dstiter)`.

The general formula for the execution of a stack of unrolled recurrent cells
depends on the current iteration of the previous layer (:math:`h_{t,l-1}` and
:math:`c_{t,l-1}`) and the previous iteration of the current layer
(:math:`h_{t-1, l}`). Here is the exact equation for non-LSTM cells:

.. math::

   h_{t, l} = Cell(h_{t, l-1}, h_{t-1, l})

where :math:`t`, :math:`l` are the indices of the timestamp and the layer of
the cell being executed.

And here is the equation for LSTM cells:

.. math::

   (h_{t, l},c_{t,l}) = Cell(h_{t, l-1}, h_{t-1, l}, c_{t-1,l})

where :math:`t`, :math:`l` are the indices of the timestamp and the layer of
the cell being executed.

**************
Cell Functions
**************

The RNN API provides four cell functions:

- :ref:`Vanilla RNN <vanilla_rnn-label>`, a single-gate recurrent cell,

- :ref:`LSTM <lstm-label>`, a four-gate long short-term memory cell,

- :ref:`GRU <gru-label>`, a three-gate gated recurrent unit cell,

- :ref:`Linear-before-reset GRU <lbr_gru-label>`, a three-gate recurrent unit
  cell with the linear layer before the reset gate.

.. _vanilla_rnn-label:

Vanilla RNN
===========

A single-gate recurrent cell initialized with
|vanilla_rnn_forward::desc| or
|vanilla_rnn_forward::desc| as in the following example.

.. code:: cpp

       auto vanilla_rnn_desc = dnnl::vanilla_rnn_forward::desc(
           aprop, activation, direction, src_layer_desc, src_iter_desc,
           weights_layer_desc, weights_iter_desc, bias_desc,
           dst_layer_desc, dst_iter_desc);

The Vanilla RNN cell should support the ReLU, Tanh and Sigmoid activation
functions.  The following equations defines the mathematical operation
performed by the Vanilla RNN cell for the forward pass:

.. math::

   a_t &= W \cdot h_{t,l-1} + U \cdot h_{t-1, l} + B \\
   h_t &= activation(a_t)

.. _lstm-label:

LSTM
====

LSTM (or Vanilla LSTM)
----------------------

A four-gate long short-term memory recurrent cell initialized with
|lstm_forward::desc| or |lstm_backward::desc| as in the
following example.

.. code:: cpp

       auto lstm_desc = dnnl::lstm_forward::desc(
           aprop, direction, src_layer_desc, src_iter_h_desc, src_iter_c_desc,
           weights_layer_desc, weights_iter_desc, bias_desc, dst_layer_desc,
           dst_iter_h_desc, dst_iter_c_desc);

Note that for all tensors with a dimension depending on the gates number, we
implicitly require the order of these gates to be :math:`i`, :math:`f`,
:math:`\tilde c`, and :math:`o`. The following equation gives the mathematical
description of these gates and output for the forward pass:

.. math::

   i_t &= \sigma(W_i \cdot h_{t,l-1} + U_i \cdot h_{t-1, l} + B_i) \\
   f_t &= \sigma(W_f \cdot h_{t,l-1} + U_f \cdot h_{t-1, l} + B_f) \\
   \\
   \tilde c_t &= tanh(W_{\tilde c} \cdot h_{t,l-1} + U_{\tilde c} \cdot h_{t-1, l} + B_{\tilde c}) \\
   c_t &= f_t * c_{t-1} + i_t * \tilde c_t \\
   \\
   o_t &= \sigma(W_o \cdot h_{t,l-1} + U_o \cdot h_{t-1, l} + B_o) \\
   h_t &= tanh(c_t) * o_t

where :math:`W_*` are stored in :math:`\weightslayer`, :math:`U_*` are stored
in :math:`\weightsiter` and :math:`B_*` are stored in :math:`\bias`.

.. note::

   In order for the dimensions to be consistent, we require
   :math:`channels(\srciterc) = channels(\dstiterc) = channels(\dstiter)`.

LSTM with Peephole
------------------

A four-gate long short-term memory recurrent cell with peephole initialized
with |lstm_forward::desc| or |lstm_backward::desc| as in
the following example.

.. code:: cpp

       auto lstm_desc = dnnl::lstm_forward::desc(
           aprop, direction, src_layer_desc, src_iter_h_desc, src_iter_c_desc,
           weights_layer_desc, weights_iter_desc, weights_peephole_desc,
           bias_desc, dst_layer_desc, dst_iter_h_desc, dst_iter_c_desc);

Similarly to vanilla LSTM, we implicitly require the order of these gates to
be :math:`i`, :math:`f`, :math:`\tilde c`, and :math:`o`. For peephole
weights, the gates order is:math:`i`, :math:`f`, :math:`o`. The following
equation gives the mathematical description of these gates and output for the
forward pass:

.. math::

   i_t &= \sigma(W_i \cdot h_{t,l-1} + U_i \cdot h_{t-1, l} + P_i \cdot c_{t-1} + B_i) \\
   f_t &= \sigma(W_f \cdot h_{t,l-1} + U_f \cdot h_{t-1, l} + P_f \cdot c_{t-1} + B_f) \\
   \\
   \tilde c_t &= tanh(W_{\tilde c} \cdot h_{t,l-1} + U_{\tilde c} \cdot h_{t-1, l} + B_{\tilde c}) \\
   c_t &= f_t * c_{t-1} + i_t * \tilde c_t \\
   \\
   o_t &= \sigma(W_o \cdot h_{t,l-1} + U_o \cdot h_{t-1, l} + P_o \cdot c_t + B_o) \\
   h_t &= tanh(c_t) * o_t

where :math:`P_*` are stored in ``weights_peephole``, and the other parameters
are the same as in vanilla LSTM.

.. note::

   If the ``weights_peephole_desc`` passed to the operation descriptor
   constructor is a zero memory descriptor, the primitive will behave the same
   as in LSTM primitive without peephole.

LSTM with Projection
--------------------

A four-gate long short-term memory recurrent cell with projection initialized
with |lstm_forward::desc| or |lstm_backward::desc| as in
the following example.

.. code:: cpp

       auto lstm_desc = dnnl::lstm_forward::desc(
           aprop, direction, src_layer_desc, src_iter_h_desc, src_iter_c_desc,
           weights_layer_desc, weights_iter_desc, weights_peephole_desc,
           weights_projection_desc, bias_desc, dst_layer_desc, dst_iter_h_desc,
           dst_iter_c_desc);

Similarly to vanilla LSTM, we implicitly require the order of the gates to be
`i`, :math:`f`, :math:`\tilde c`, and :math:`o` for all tensors with a
dimension depending on the gates. The following equation gives the
mathematical description of these gates and output for the forward pass (for
simplicity, LSTM without peephole is shown):

.. math::

       i_t &= \sigma(W_i \cdot h_{t,l-1} + U_i \cdot h_{t-1,l} + B_i) \\
       f_t &= \sigma(W_f \cdot h_{t,l-1} + U_f \cdot h_{t-1,l} + B_f) \\
       & \\
       \tilde{c}_t &= \tanh(W_{\tilde{c}} \cdot h_{t,l-1} + U_{\tilde{c}} \cdot h_{t-1,l} + B_{\tilde{c}}) \\
       c_t &= f_t * c_{t-1} + i_t * \tilde{c}_t \\
       & \\
       o_t &= \sigma(W_o \cdot h_{t,l-1} + U_o \cdot h_{t-1,l} + B_o) \\
       h_t &= R \cdot (\tanh(c_t) * o_t)

where :math:`R` is stored in ``weights_projection``, and the other parameters
are the same as in vanilla LSTM.

.. note::

   If the ``weights_projection_desc`` passed to the operation descriptor
   constructor is a zero memory descriptor, the primitive will behave the same
   as in LSTM primitive without projection.

.. _gru-label:

GRU
===

A three-gate gated recurrent unit cell, initialized with
|gru_forward::desc| or |gru_backward::desc| as in the
following example.

.. code:: cpp

       auto gru_desc = dnnl::gru_forward::desc(
           aprop, direction, src_layer_desc, src_iter_desc,
           weights_layer_desc, weights_iter_desc, bias_desc,
           dst_layer_desc, dst_iter_desc);

Note that for all tensors with a dimension depending on the gates number, we
implicitly require the order of these gates to be:math:`u`, :math:`r`,
and :math:`o`. The following equation gives the mathematical definition of
these gates.

.. math::

   u_t &= \sigma(W_u \cdot h_{t,l-1} + U_u \cdot h_{t-1, l} + B_u) \\
   r_t &= \sigma(W_r \cdot h_{t,l-1} + U_r \cdot h_{t-1, l} + B_r) \\
   o_t &= tanh(W_o \cdot h_{t,l-1} + U_o \cdot (r_t * h_{t-1, l}) + B_o) \\
   h_t &= u_t * h_{t-1, l} + (1 - u_t) * o_t

where :math:`W_*` are in :math:`\weightslayer`, :math:`U_*` are in
:math:`\weightsiter`, and :math:`B_*` are stored in :math:`\bias`.

.. note::

   If you need to replace :math:`u_t` by :math:`(1-u_t)` when computing
   :math:`h_t`, you can achieve this by multiplying :math:`W_u`, :math:`U_u`
   and :math:`B_u` by :math:`-1`.  This is possible as :math:`u_t = \sigma(W_u
   \cdot h_{t,l-1} + U_u \cdot h_{t-1, l} + B_u)`, and :math:`1 – \sigma(a) =
   \sigma(-a)`.

.. _lbr_gru-label:

Linear-Before-Reset GRU
=======================

A three-gate gated recurrent unit cell with linear layer applied before the
reset gate, initialized with |lbr_gru_forward::desc| or
|lbr_gru_backward::desc| as in the following example.

.. code:: cpp

       auto lbr_gru_desc = dnnl::lbr_gru_forward::desc(
           aprop, direction, src_layer_desc, src_iter_desc,
           weights_layer_desc, weights_iter_desc, bias_desc,
           dst_layer_desc, dst_iter_desc);

The following equation describes the mathematical behavior of the
Linear-Before-Reset GRU cell.

.. math::

   u_t &= \sigma(W_u \cdot h_{t,l-1} + U_u \cdot h_{t-1, l} + B_u) \\
   r_t &= \sigma(W_r \cdot h_{t,l-1} + U_r \cdot h_{t-1, l} + B_r) \\
   o_t &= tanh(W_o \cdot h_{t,l-1} + r_t * (U_o \cdot h_{t-1, l} + B_{u'}) + B_o) \\
   h_t &= u_t * h_{t-1, l} + (1 - u_t) * o_t

Note that for all tensors with a dimension depending on the gates number,
except the bias, we implicitly require the order of these gates to be
:math:`u`, :math:`r`, and :math:`o`. For the :math:`\bias` tensor, we
implicitly require the order of the gates to be :math:`u`, :math:`r`,
:math:`o`, and :math:`u'`.

.. note::

   If you need to replace :math:`u_t` by :math:`(1-u_t)` when computing
   :math:`h_t`, you can achieve this by multiplying :math:`W_u`, :math:`U_u`
   and :math:`B_u` by :math:`-1`.  This is possible as :math:`u_t = \sigma(W_u
   \cdot h_{t,l-1} + U_u \cdot h_{t-1, l} + B_u)`, and :math:`1 – \sigma(a) =
   \sigma(-a)`.

*******************
Execution Arguments
*******************

When executed, the inputs and outputs should be mapped to an execution
argument index as specified by the following table.

=================================== ================================
Primitive input/output              Execution argument index
=================================== ================================
:math:`\srclayer`                   |DNNL_ARG_SRC_LAYER|
:math:`\srciter`                    |DNNL_ARG_SRC_ITER|
:math:`\srciterc`                   |DNNL_ARG_SRC_ITER_C|
:math:`\weightslayer`               |DNNL_ARG_WEIGHTS_LAYER|
:math:`\weightsiter`                |DNNL_ARG_WEIGHTS_ITER|
:math:`\weightspeephole`            |DNNL_ARG_WEIGHTS_PEEPHOLE|
:math:`\weightsprojection`          |DNNL_ARG_WEIGHTS_PROJECTION|
:math:`\bias`                       |DNNL_ARG_BIAS|
:math:`\dstlayer`                   |DNNL_ARG_DST_LAYER|
:math:`\dstiter`                    |DNNL_ARG_DST_ITER|
:math:`\dstiterc`                   |DNNL_ARG_DST_ITER_C|
:math:`\workspace`                  |DNNL_ARG_WORKSPACE|
:math:`\diffsrclayer`               |DNNL_ARG_DIFF_SRC_LAYER|
:math:`\diffsrciter`                |DNNL_ARG_DIFF_SRC_ITER|
:math:`\diffsrciterc`               |DNNL_ARG_DIFF_SRC_ITER_C|
:math:`\diffweightslayer`           |DNNL_ARG_DIFF_WEIGHTS_LAYER|
:math:`\diffweightsiter`            |DNNL_ARG_DIFF_WEIGHTS_ITER|
:math:`\diffweightspeephole`        |DNNL_ARG_DIFF_WEIGHTS_PEEPHOLE|
:math:`\diffweightsprojection`      |DNNL_ARG_DIFF_WEIGHTS_PROJECTION|
:math:`\diffbias`                   |DNNL_ARG_DIFF_BIAS|
:math:`\diffdstlayer`               |DNNL_ARG_DIFF_DST_LAYER|
:math:`\diffdstiter`                |DNNL_ARG_DIFF_DST_ITER|
:math:`\diffdstiterc`               |DNNL_ARG_DIFF_DST_ITER_C|
=================================== ================================

*****************
Operation Details
*****************

N/A

******************
Data Types Support
******************

The following table lists the combination of data types that should be
supported by the RNN primitive for each input and output memory object.

.. note::

   Here we abbreviate data types names for readability. For example, |_f32| is
   abbreviated to |f32|.

+------------------------+--------------+-----------+---------------+-------------+----------+-------------+
| **Propagation**        | **Cell**     | **Input** | **Recurrent** | **Weights** | **Bias** | **Output**  |
|                        | **Function** | **Data**  | **Data** (1)  |             |          | **Data**    |
+------------------------+--------------+-----------+---------------+-------------+----------+-------------+
| Forward / Backward     | All          | |f32|     | |f32|         | |f32|       | |f32|    | |f32|       |
+------------------------+--------------+-----------+---------------+-------------+----------+-------------+
| Forward / Backward (2) | All (3)      | |bf16|    | |bf16|        | |bf16|      | |f32|    | |bf16|      |
+------------------------+--------------+-----------+---------------+-------------+----------+-------------+
| Forward                | All (3)      | |f16|     | |f16|         | |f16|       | |f16|    | |f16|       |
+------------------------+--------------+-----------+---------------+-------------+----------+-------------+
| Forward inference      | Vanilla LSTM | |u8|      | |u8|          | |s8|        | |f32|    | |u8|, |f32| |
+------------------------+--------------+-----------+---------------+-------------+----------+-------------+

(1) With LSTM and Peephole LSTM cells, the cell state data type is always f32.

(2) In backward propagation, all ``diff_*`` tensors are in f32.

(3) Projection LSTM is not defined yet.

Data Representation
===================

In the oneDNN programming model, the RNN primitive is one of a few that
support the placeholder memory format #dnnl::memory::format_tag::any
(shortened to ``any`` from now on) and can define data and weight memory
objects format based on the primitive parameters.

The following table summarizes the data layouts supported by the RNN
primitive.

+------------------+---------------+-------------------------+----------------------+-----------------------+
| **Input/Output** | **Recurrent** | **Layer and Iteration** | **Peephole Weights** | **Projection LSTM**   |
| **Data**         | **Data**      | **Weights**             | **and Bias**         | **Weights**           |
+------------------+---------------+-------------------------+----------------------+-----------------------+
| |any|            | |any|         | |any|                   | |ldgo|               | |any|, |ldio|         |
|                  |               |                         |                      | (Forward propagation) |
+------------------+---------------+-------------------------+----------------------+-----------------------+
| |ntc|, |tnc|     | |ldnc|        | |ldigo|, |ldgoi|        | |ldgo|               | |any|, |ldio|         |
|                  |               |                         |                      | (Forward propagation) |
+------------------+---------------+-------------------------+----------------------+-----------------------+

While an RNN primitive can be created with memory formats specified
explicitly, the performance is likely to be sub-optimal. When using |any| it
is necessary to first create an RNN primitive descriptor and then query it for
the actual data and weight memory objects formats.

.. note::

   The RNN primitive should support padded tensors and views. So even if two
   memory descriptors share the same data layout, they might still be
   different.

Post-ops and Attributes
=======================

Currently post-ops and attributes are only used by the int8 variant of LSTM.

.. TODO quantization

***
API
***

.. doxygenenum:: dnnl::rnn_flags
   :project: oneDNN

.. doxygenenum:: dnnl::rnn_direction
   :project: oneDNN

.. doxygenstruct:: dnnl::vanilla_rnn_forward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::vanilla_rnn_backward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::lstm_forward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::lstm_backward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::gru_forward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::gru_backward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::lbr_gru_forward
   :project: oneDNN
   :members:

.. doxygenstruct:: dnnl::lbr_gru_backward
   :project: oneDNN
   :members:


.. vim: ts=3 sw=3 et spell spelllang=en
