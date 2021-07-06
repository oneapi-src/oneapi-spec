.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_dft_config_distance:

FORWARD_DISTANCE and BACKWARD_DISTANCE
--------------------------------------

The FFT interface enables computation of multiple transforms. To compute multiple transforms, you need to specify the data distribution of the multiple sets of data. The distance between the first data elements of consecutive data sets, ``FORWARD_DISTANCE`` for forward :ref:`onemkl_dft_enum_domain` data or ``BACKWARD_DISTANCE`` for backward :ref:`onemkl_dft_enum_domain` data, specifies the distribution. The configuration setting is a value of ``std::int64_t`` data type.

The default value for both configuration settings is one. You must set this parameter explicitly if the number of transforms is greater than one (see :ref:`onemkl_dft_config_number_of_transforms` ).

The distance is counted in elements of the data type defined by the descriptor configuration (rather than by the type of the variable passed to the computation functions). Specifically, the :ref:`onemkl_dft_enum_domain` template parameter, and the ``COMPLEX_STORAGE``, ``REAL_STORAGE`` and ``CONJUGATE_EVEN_STORAGE`` configuration parameters described in :ref:`onemkl_dft_config_storage_formats` define the type of the elements as shown in the :ref:`complex_storage<onemkl_dft_config_data_element_types_complex>`, :ref:`real_storage<onemkl_dft_config_data_element_types_real>` and :ref:`conjugate_even_storage<onemkl_dft_config_data_element_types_conjugate_even>` tables.

For in-place transforms ( ``PLACEMENT=INPLACE`` ), the configuration set by ``FORWARD_DISTANCE`` and ``BACKWARD_DISTANCE`` should be consistent, that is, the locations of the data sets for input and output must coincide.


**Parent topic:** :ref:`onemkl_dft_enums`

