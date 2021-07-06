.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_dft_config_number_of_transforms:

Number of Transforms
--------------------

If you need to perform a large number of identical DFTs, you can do this in a single call to a compute* function with the value of this configuration parameter equal to the actual number of the transforms. The default value is 1. You can set this parameter to a positive integer value using the ``std::int64_t`` data type. 

When setting the number of transforms to a value greater than one, you also need to specify the distance between the forward data sets and the distance between the backward data sets using the ``config_param::FWD_DISTANCE`` and ``config_param::BWD_DISTANCE`` configuration parameters corresponding to the specified :ref:`onemkl_dft_enum_domain`.  

.. note::
   * The data sets must not have common elements
   * All the sets of data in each domain must be located within the same memory block.


**Parent topic** :ref:`onemkl_dft_enums`


