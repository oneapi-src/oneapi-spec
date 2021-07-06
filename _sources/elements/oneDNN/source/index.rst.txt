.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp
.. _`open source implementation`: https://github.com/oneapi-src/oneDNN/
.. _`README`: https://github.com/oneapi-src/oneDNN/blob/master/README.md

.. _oneDNN-section:

######
oneDNN
######

|dnn_full_name| (oneDNN) is a performance library containing building blocks
for for deep learning applications and frameworks. oneDNN supports:

* CNN primitives (Convolutions, Inner product, Pooling, etc.)
* RNN primitives (LSTM, Vanilla, RNN, GRU)
* Normalizations (LRN, Batch, Layer)
* Elementwise operations (ReLU, Tanh, ELU, Abs, etc.)
* Softmax, Sum, Concat, Shuffle
* Reorders from/to optimized data layouts
* 8-bit integer, 16-, 32-bit, and bfloat16 floating point data types

.. literalinclude:: example.cpp
   :language: cpp
   :lines: 69-

.. toctree::
   :maxdepth: 1

   introduction.rst
   conventions.rst
   execution_model/index.rst
   data_model/index.rst
   primitives/index.rst

**************************
Open Source Implementation
**************************

Intel has published an `open source implementation`_ with the Apache
license.

********************
Implementation Notes
********************

This specification provides high-level descriptions for oneDNN operations and
does not cover all the implementation-specific details of the `open source
implementation`_.  Specifically, it does not cover highly-optimized memory
formats and integration with profiling tools, etc. This is done intentionally
to improve specification portability. Code that uses API defined in this
specification is expected to be portable across open source implementation and
any potential other implementations of this specification to a reasonable
extent.

In the future this section will be extended with more details on how different
implementations of this specification should cooperate and co-exist.

*******
Testing
*******

Intel's binary distribution of oneDNN contains example code that you
can be used to test library functionality.

The `open source implementation`_ includes a comprehensive test suite.
Consult the `README`_ for directions.

.. vim: ts=3 sw=3 et spell spelllang=en
