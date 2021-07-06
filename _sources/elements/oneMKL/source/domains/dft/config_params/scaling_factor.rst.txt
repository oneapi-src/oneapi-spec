.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_dft_config_scale:

Forward and Backward Scale
---------------------------

The forward and backward transformations are each associated with a scale factor, :math:`\sigma`, having the default value of 1. For example, for a one-dimensional transform of length n , you can use the default scale of 1 for the forward transform and set the scale factor for the backward transform to be 1/ n , thus making the backward transform the inverse of the forward transform. Use real floating point data type corresponding to :ref:`onemkl_dft_enum_precision`.


**Parent topic** :ref:`onemkl_dft_enums`
