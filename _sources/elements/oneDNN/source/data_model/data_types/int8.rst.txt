.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

####
Int8
####

To push higher performance during inference computations, recent work has
focused on computations that use activations and weights stored at lower
precision to achieve higher throughput. Int8 computations offer improved
performance over higher-precision types because they enable packing more
computations into a single instruction, at the cost of reduced (but
acceptable) accuracy.

********
Workflow
********

The :ref:`attributes-quantization-label` describes what kind of quantization
model oneDNN supports.

*******
Support
*******

oneDNN supports int8 computations for inference by allowing to specify that
primitives input and output memory objects use int8 data types.


.. vim: ts=3 sw=3 et spell spelllang=en
