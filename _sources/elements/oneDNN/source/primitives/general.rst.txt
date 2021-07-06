.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. default-domain:: cpp

.. include:: /elements/oneDNN/source/replacements.inc.rst

##################
Common Definitions
##################

This section lists common types and definitions used by all or multiple
primitives.

*************************
Base Class for Primitives
*************************

.. doxygenstruct:: dnnl::primitive
   :project: oneDNN
   :members:

.. doxygenfunction:: dnnl::sycl_interop::execute
   :project: oneDNN

*************************************
Base Class for Primitives Descriptors
*************************************

There is no common base class for operation descriptors because they are very
different between different primitives. However, there is a common base class
for primitive descriptors.

.. doxygenstruct:: dnnl::primitive_desc_base
   :project: oneDNN
   :members:

It is further derived from to provide base class for all primitives that have
operation descriptors.

.. doxygenstruct:: dnnl::primitive_desc
   :project: oneDNN
   :members:

The |reorder|, |sum| and |concat| primitives
also subclass |primitive_desc| to implement their primitive
descriptors.

RNN primitives further subclass the |primitive_desc_base| to
provide utility functions for frequently queried memory descriptors.

.. doxygenstruct:: dnnl::rnn_primitive_desc_base
   :project: oneDNN
   :members:

*******************
Common Enumerations
*******************

.. doxygenenum:: dnnl::prop_kind
   :project: oneDNN

.. doxygenenum:: dnnl::algorithm
   :project: oneDNN

******************************
Normalization Primitives Flags
******************************

.. doxygenenum:: dnnl::normalization_flags
   :project: oneDNN

**************************
Execution argument indices
**************************

.. doxygendefine:: DNNL_ARG_SRC_0
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_SRC
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_SRC_LAYER
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_FROM
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_SRC_1
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_SRC_ITER
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_SRC_2
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_SRC_ITER_C
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DST_0
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DST
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_TO
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DST_LAYER
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DST_1
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DST_ITER
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DST_2
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DST_ITER_C
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_WEIGHTS_0
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_WEIGHTS
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_SCALE_SHIFT
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_WEIGHTS_LAYER
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_WEIGHTS_1
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_WEIGHTS_ITER
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_BIAS
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_MEAN
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_VARIANCE
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_WORKSPACE
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_SCRATCHPAD
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_SRC_0
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_SRC
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_SRC_LAYER
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_SRC_1
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_SRC_ITER
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_SRC_2
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_SRC_ITER_C
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_DST_0
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_DST
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_DST_LAYER
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_DST_1
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_DST_ITER
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_DST_2
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_DST_ITER_C
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_WEIGHTS_0
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_WEIGHTS
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_SCALE_SHIFT
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_WEIGHTS_LAYER
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_WEIGHTS_1
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_WEIGHTS_ITER
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_DIFF_BIAS
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_ATTR_OUTPUT_SCALES
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_MULTIPLE_SRC
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_MULTIPLE_DST
   :project: oneDNN

.. doxygendefine:: DNNL_ARG_ATTR_ZERO_POINTS
   :project: oneDNN

.. doxygendefine:: DNNL_RUNTIME_DIM_VAL
   :project: oneDNN

.. doxygendefine:: DNNL_RUNTIME_SIZE_VAL
   :project: oneDNN

.. doxygendefine:: DNNL_RUNTIME_F32_VAL
   :project: oneDNN

.. doxygendefine:: DNNL_RUNTIME_S32_VAL
   :project: oneDNN

.. vim: ts=3 sw=3 et spell spelllang=en
