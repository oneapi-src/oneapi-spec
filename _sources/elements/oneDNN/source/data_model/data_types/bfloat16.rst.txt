.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

########
Bfloat16
########

.. note::

   In this section we abbreviate data types names for readability. For example,
   |_f32| is abbreviated to |f32|.

Bfloat16 (|bf16|) is a 16-bit floating point data type based on the IEEE 32-bit
single-precision floating point data type (|f32|).

Both |bf16| and |f32| have an 8-bit exponent. However, while |f32| has a 23-bit
mantissa, |bf16| has only a 7-bit one, keeping only the most significant bits.
As a result, while these data types support a very close numerical range of
values, |bf16| has a significantly reduced precision. Therefore, |bf16| occupies
a spot between |f32| and the IEEE 16-bit half-precision floating point data
type, |f16|.  Compared directly to |f16|, which has a 5-bit exponent and a
10-bit mantissa, |bf16| trades increased range for reduced precision.

.. image:: ../../_static/img_bf16_diagram.png
   :width: 600
   :alt: Diagram depicting the bit-wise layout of f32, bf16, and f16 floating point data types

More details of the bfloat16 data type can be found `here
<https://en.wikipedia.org/wiki/Bfloat16_floating-point_format>`__.

One of the advantages of using |bf16| versus |f32| is reduced memory footprint
and, hence, increased memory access throughput.

********
Workflow
********

The main difference between implementing training with the |f32| data type and
with the |bf16| data type is the way the weights updates are treated. With the
|f32| data type, the weights gradients have the same data type as the weights
themselves. This is not necessarily the case with the |bf16| data type as oneDNN
allows some flexibility here. For example, one could maintain a master copy of
all the weights, computing weights gradients in |f32| and converting the result
to |bf16| afterwards.

*******
Support
*******

Most of the primitives can support the |bf16| data type for source and weights
tensors. Destination tensors can be specified to have either the |bf16| or |f32|
data type. The latter is intended for cases in which the output is to be fed to
operations that do not support bfloat16 or require higher precision.

.. vim: ts=3 sw=3 et spell spelllang=en
