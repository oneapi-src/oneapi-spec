.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_dft_config_strides:

INPUT_STRIDES and OUTPUT_STRIDES
--------------------------------

The FFT interface provides configuration parameters that define the layout of multidimensional data in the computer memory. For d-dimensional data set, :math:`X`, defined by dimensions :math:`n_1\times n_2 \times\dots\times n_d` , the layout describes where a particular element :math:`X(k_1, k_2, \dots, k_d )` of the data set is located. The memory address of the element :math:`X(k_1, k_2, \dots, k_d )` is expressed by the formula:
:math:`X(k_1, k_2, \dots, k_d ) =` the :math:`+ s_0 + k_1*s_1 + k_2*s_2 + \dots + k_d*s_d`-th element of the container (``sycl::buffer`` or USM pointer) provided to the compute function,
where :math:`s_0` is the displacement and :math:`s_1 , \dots, s_d` are generalized strides. The configuration parameters ``config_param::INPUT_STRIDES`` and ``config_param::OUTPUT_STRIDES`` enable you to get and set these values. The configuration value is a :math:`d+1`` lengthed ``std::vector<std::int64_t>`` of values :math:`(s_0, s_1, \dots, s_d )`.

The offset is counted in elements of the data type (complex or real) defined by the descriptor configuration as tabulated below. 

The computation functions take containers(``sycl::buffer`` or USM pointer) which are typed according to the descriptor configuration parameters. Specifically, the :ref:`forward domain<onemkl_dft_enum_domain>` which defines the type of transformation and the :ref:`storage format<onemkl_dft_config_storage_formats>` configuration parameters: ``config_param::COMPLEX_STORAGE``, ``config_param::REAL_STORAGE`` and ``config_param::CONJUGATE_EVEN_STORAGE`` define the type of the elements as shown here:

.. container:: section
 
   .. _onemkl_dft_config_data_element_types_complex:

   .. rubric:: Assumed Element Types using complex-to-complex transform and ``config_param::COMPLEX_STORAGE``:

   .. list-table::
        :header-rows: 1
        :class: longtable

        * -   COMPLEX_STORAGE
          -   Element type of forward data
          -   Element type of backward data
        * -   :ref:`onemkl_dft_complex_storage_complex_complex`
          -   Complex
          -   Complex
        * -   :ref:`onemkl_dft_complex_storage_real_real`
          -   Real
          -   Real

   .. _onemkl_dft_config_data_element_types_real:

   .. rubric:: Assumed Element Types using real-to-complex transform and ``config_param::REAL_STORAGE``:

   .. list-table::
        :header-rows: 1
        :class: longtable

        * -   REAL_STORAGE
          -   Element type of forward data
          -   Element type of backward data
        * -   :ref:`onemkl_dft_real_storage_real_real`
          -   Real
          -   Real

   .. _onemkl_dft_config_data_element_types_conjugate_even:

   .. rubric:: Assumed Element Types using real-to-complex transform and ``config_param::CONJUGATE_EVEN_STORAGE``:

   .. list-table::
        :header-rows: 1
        :class: longtable

        * -   CONJUGATE_EVEN_STORAGE
          -   Element type of forward data
          -   Element type of backward data
        * -   :ref:`onemkl_dft_conjugate_even_storage_complex_complex`
          -   Real
          -   Complex


The ``config_param::INPUT_STRIDES`` configuration parameter defines the layout of the input data, while the element type is defined by the forward domain for the :ref:`onemkl_dft_compute_forward` function and by the backward domain for the :ref:`onemkl_dft_compute_backward` function. The ``config_param::OUTPUT_STRIDES`` configuration parameter defines the layout of the output data, while the element type is defined by the backward domain for the :ref:`onemkl_dft_compute_forward` function and by the forward domain for :ref:`onemkl_dft_compute_backward` function.

For in-place transforms ( ``config_param::PLACEMENT=config_value::INPLACE`` ), the configuration set by ``config_param::OUTPUT_STRIDES`` is ignored when the element types in the forward and backward domains are the same. If they are different, set ``config_param::OUTPUT_STRIDES`` explicitly (even though the transform is in-place). Ensure a consistent configuration for in-place transforms, that is, the locations of the first elements on input and output must coincide in each dimension.


**Parent topic** :ref:`onemkl_dft_enums`


