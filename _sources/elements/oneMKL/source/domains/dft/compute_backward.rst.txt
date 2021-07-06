.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_dft_compute_backward:

compute_backward
=================

This function computes the backward transform defined by an instantiation of the :ref:`onemkl_dft_descriptor` class.

.. _onemkl_dft_compute_backward_description:

.. rubric:: Description

The compute_backward function accepts the :ref:`onemkl_dft_descriptor` and one or more data parameters and in the case of USM data, any ``syc::event`` dependencies.  Given a successfully configured and committed descriptor, this function computes the backward transform, that is, the :ref:`transform<onemkl_dft_formula>` with the plus sign, :math:`\delta=+1`, in the exponent.

The configuration parameters ``config_param::COMPLEX_STORAGE``, ``config_param::REAL_STORAGE`` and ``config_param::CONJUGATE_EVEN_STORAGE`` define the layout of the input and output data and must be properly set in a call to :ref:`onemkl_dft_descriptor_set_value`.

.. note::
   The compute_backward function may need to access the internals and private/protected members of the :ref:`onemkl_dft_descriptor` class.  This could be done, for instance, by labeling it as a friend function to the descriptor class.   


.. onemkl_dft_compute_backward_buffer:

compute_backward (Buffer version)
---------------------------------

.. rubric:: Syntax (In-place transform)

.. code-block:: cpp

   namespace oneapi::mkl::dft {

      template <typename descriptor_type, typename data_type>
      void compute_backward( descriptor_type            &desc,
                             sycl::buffer<data_type, 1> &inout );

   }

.. rubric:: Syntax (In-place transform, using ``config_param::COMPLEX_STORAGE=config_value::REAL_REAL`` :ref:`data format<onemkl_dft_complex_storage>` )

.. code-block:: cpp

   namespace oneapi::mkl::dft {

      template <typename descriptor_type, typename data_type>
      void compute_backward( descriptor_type            &desc, 
                             sycl::buffer<data_type, 1> &inout_re,
                             sycl::buffer<data_type, 1> &inout_im);
   }


.. rubric:: Syntax (Out-of-place transform)

.. code-block:: cpp

   namespace oneapi::mkl::dft {
   
      template <typename descriptor_type, typename input_type, typename output_type>
      void compute_backward( descriptor_type              &desc,
                             sycl::buffer<input_type, 1>  &in, 
                             sycl::buffer<output_type, 1> &out);
   }

.. rubric:: Syntax (Out-of-place transform, using ``config_param::COMPLEX_STORAGE=config_value::REAL_REAL`` :ref:`data format<onemkl_dft_complex_storage>` )

.. code-block:: cpp

   namespace oneapi::mkl::dft {

      template <typename descriptor_type, typename input_type, typename output_type>
      void compute_backward( descriptor_type              &desc,
                             sycl::buffer<input_type, 1>  &in_re,
                             sycl::buffer<input_type, 1>  &in_im,
                             sycl::buffer<output_type, 1> &out_re,
                             sycl::buffer<output_type, 1> &out_im);

   }

.. container:: section

   .. rubric:: Input Parameters

   :ref:`desc<onemkl_dft_descriptor>`
      A fully configured and committed discrete Fourier transform descriptor class object, defining the type of backward transformation and data layout to be applied. At commit time, the ``sycl::queue`` has already been provided.

   inout
      Sycl buffer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house both the input and output data sequences for the in-place transformation. Corresponds to the choice of ``config_value::INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.


   inout_re
      Sycl buffer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the real part of both the input and output data sequences for the in-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   inout_im
      Sycl buffer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the imaginary part of both the input and output data sequences for the in-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   in
      Sycl buffer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the input data sequence for the out-of-place transformation. Corresponds to the choice of ``config_value::NOT_INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   in_re
      Sycl buffer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the real part of input data sequence for the out-of-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::NOT_INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   in_im
      Sycl buffer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the imaginary part of input data sequence for the out-of-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::NOT_INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.



.. container:: section

   .. rubric:: Output Parameters

   inout
      Sycl buffer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house both the input and output data sequences for the in-place transformation. Corresponds to the choice of ``config_value::INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   inout_re
      Sycl buffer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the real part of both the input and output data sequences for the in-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   inout_im
      Sycl buffer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the imaginary part of both the input and output data sequences for the in-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   out
      Sycl buffer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the output data sequence for the out-of-place transformation. Corresponds to the choice of ``config_value::NOT_INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   out_re
      Sycl buffer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the real part of output data sequence for the out-of-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::NOT_INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   out_im
      Sycl buffer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the imaginary part of output data sequence for the out-of-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::NOT_INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

.. container:: section

   .. rubric:: Throws

   The `oneapi::mkl::dft::compute_backward()` routine shall throw the following exceptions if the associated condition is detected. An implementation may throw additional implementation-specific exception(s) in case of error conditions not covered here:

   :ref:`oneapi::mkl::invalid_argument()<onemkl_exception_invalid_argument>`
      If the provided :ref:`onemkl_dft_descriptor` class is invalid, for instance, if it is a nullptr or if the value of ``config_param::COMMIT_STATUS`` in descriptor is not ``config_param::COMMITTED``.




.. onemkl_dft_compute_backward_usm:

compute_backward (USM version)
---------------------------------

.. rubric:: Syntax (In-place transform)

.. code-block:: cpp

   namespace oneapi::mkl::dft {
   
      template <typename descriptor_type, typename data_type>
      sycl::event compute_backward( descriptor_type                               &desc,
                                    data_type                                     *inout,
                                    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});
   }

.. rubric:: Syntax (In-place transform, using ``config_param::COMPLEX_STORAGE=config_value::REAL_REAL`` :ref:`data format<onemkl_dft_complex_storage>` )

.. code-block:: cpp

   namespace oneapi::mkl::dft {
      
      template <typename descriptor_type, typename data_type>
      sycl::event compute_backward(descriptor_type                               &desc,
                                   data_type                                     *inout_re,
                                   data_type                                     *inout_im,
                                   const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

   }


.. rubric:: Syntax (Out-of-place transform)

.. code-block:: cpp

   namespace oneapi::mkl::dft {
      
      template <typename descriptor_type, typename input_type, typename output_type>
      sycl::event compute_backward( descriptor_type                               &desc,
                                    input_type                                    *in,
                                    output_type                                   *out,
                                    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

   }


.. rubric:: Syntax (Out-of-place transform, using ``config_param::COMPLEX_STORAGE=config_value::REAL_REAL`` :ref:`data format<onemkl_dft_complex_storage>` )

.. code-block:: cpp

   namespace oneapi::mkl::dft {
      
      template <typename descriptor_type, typename input_type, typename output_type>
      sycl::event compute_backward( descriptor_type                               &desc,
                                    input_type                                    *in_re,
                                    input_type                                    *in_im,
                                    output_type                                   *out_re,
                                    output_type                                   *out_im,
                                    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

   }

.. container:: section

   .. rubric:: Input Parameters

   :ref:`desc<onemkl_dft_descriptor>`
      A fully configured and committed discrete Fourier transform descriptor class object, defining the type of backward transformation and data layout to be applied. At commit time, the ``sycl::queue`` has already been provided.

   inout
      USM pointer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house both the input and output data sequences for the in-place transformation. Corresponds to the choice of ``config_value::INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   inout_re
      USM pointer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the real part of both the input and output data sequences for the in-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   inout_im
      USM pointer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the imaginary part of both the input and output data sequences for the in-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   in
      USM pointer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the input data sequence for the out-of-place transformation. Corresponds to the choice of ``config_value::NOT_INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   in_re
      USM pointer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the real part of the input data sequence for the out-of-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::NOT_INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.
  
   in_im
      USM pointer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the imaginary part of the input data sequence for the out-of-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::NOT_INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.
  
   dependencies
      A vector of ``sycl::event``'s that represent the previously enqueued tasks that must be finished before this transformation can be started.

.. container:: section

   .. rubric:: Output Parameters


   inout
      USM pointer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house both the input and output data sequences for the in-place transformation. Corresponds to the choice of ``config_value::INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   inout_re
      USM pointer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the real part of both the input and output data sequences for the in-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   inout_im
      USM pointer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the imaginary part of both the input and output data sequences for the in-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.


   out
      USM pointer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the output data sequence for the out-of-place transformation. Corresponds to the choice of ``config_value::NOT_INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.

   out_re
      USM pointer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the real part of the output data sequence for the out-of-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::NOT_INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.
  
   out_im
      USM pointer containing an array of length no less than is specified at the :ref:`descriptor construction<onemkl_dft_descriptor_constructor>` time to house the imaginary part of the output data sequence for the out-of-place transformation when using the ``config_value::REAL_REAL`` format for the ``config_param::COMPLEX_STORAGE`` configuration parameter. Corresponds to the choice of ``config_value::NOT_INPLACE`` for the configuration parameter ``config_param::PLACEMENT``.
 
.. container:: section

   .. rubric:: Throws

   The `oneapi::mkl::dft::compute_backward()` routine shall throw the following exceptions if the associated condition is detected. An implementation may throw additional implementation-specific exception(s) in case of error conditions not covered here:
   
   :ref:`oneapi::mkl::invalid_argument()<onemkl_exception_invalid_argument>`
      If the provided :ref:`onemkl_dft_descriptor` class is invalid, for instance, if it is a nullptr or if the value of ``config_param::COMMIT_STATUS`` in descriptor is not ``config_param::COMMITTED``.  It will also be thrown if the input/output pointers are NULL.


.. container:: section

   .. rubric:: Return Values

   This function returns a ``sycl::event`` that allows to track progress of this transformation, and can be passed as a dependency to other routines that may depend on the results of this transformation to be finished before proceeding with the other operations.


**Parent topic:** :ref:`onemkl_dft`


