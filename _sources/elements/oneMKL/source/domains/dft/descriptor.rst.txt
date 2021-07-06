.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_dft_descriptor:

descriptor
==========

The descriptor class defines a discrete Fourier transform problem to be computed.

.. rubric:: Description

The discrete Fourier transform problem is defined through the use of the ``oneapi::mkl::dft::descriptor`` class which lives in the ``oneapi::mkl::dft::`` namespace. The enum and config_param values associated with the descriptor class can be found in :ref:`onemkl_dft_enums` including :ref:`onemkl_dft_enum_precision`, :ref:`onemkl_dft_enum_domain` and :ref:`onemkl_dft_enum_config_param`. The descriptor class allows to set several configuration parameters using set_value (and query using get_value) and then upon call to :ref:`onemkl_dft_descriptor_commit` with a ``sycl::queue``, is ready to be used in computations on the specified device.  

This class is then passed to a :ref:`onemkl_dft_compute_forward` or :ref:`onemkl_dft_compute_backward` function along with the data for the actual transformation to be applied. 

.. note::
   The :ref:`onemkl_dft_compute_forward` and :ref:`onemkl_dft_compute_backward` functions may need to be able to access the internals of the descriptor to apply the transform, this could be done for instance, by labeling them as friend functions of the descriptor class.


descriptor class
----------------

.. rubric:: Syntax

The descriptor class lives in the ``oneapi::mkl::dft`` namespace.

.. code-block:: cpp

   namespace oneapi::mkl::dft {

      template <oneapi::mkl::dft::precision prec, oneapi::mkl::dft::domain dom>
      class descriptor {
       public:
          
          // Syntax for 1-dimensional DFT
          descriptor(std::int64_t length);
          
          // Syntax for d-dimensional DFT
          descriptor(std::vector<std::int64_t> dimensions);
          
          ~descriptor();
      
      
          void set_value(config_param param, ...);
          
          void get_value(config_param param, ...);
      
          void commit(sycl::queue &queue);
      
       };


   }
	

.. container:: section

   .. rubric:: Descriptor class template parameters
      
   :ref:`onemkl_dft_enum_precision` prec
      Specifies the floating-point precision in which the transform is to be carried out.

   :ref:`onemkl_dft_enum_domain` dom
      Specifies the forward domain for the transformations.

.. container:: section

   .. _onemkl_dft_descriptor_member_table:

   .. rubric:: Descriptor class member functions

   .. list-table:: 
       :header-rows: 1

       * -     Routines
         -     Description   
       * -     :ref:`constructors<onemkl_dft_descriptor_constructor>`
         -     Initialize descriptor for 1-dimensional or N-dimensional transformations
       * -     :ref:`onemkl_dft_descriptor_set_value`
         -     Sets one particular configuration parameter with the specified configuration value.
       * -     :ref:`onemkl_dft_descriptor_get_value`
         -     Gets the configuration value of one particular configuration parameter.
       * -     :ref:`onemkl_dft_descriptor_commit`
         -     Performs all initialization for the actual FFT computation.


.. _onemkl_dft_descriptor_constructor:

Descriptor class constructors
++++++++++++++++++++++++++++++

The constructors for the discrete Fourier transform ``descriptor`` class with default 
configuration settings for a given precision, forward :ref:`onemkl_dft_enum_domain` type 
and dimension of the transform.

The constructors allocate memory for the descriptor data
structure and instantiate it with all the default
configuration settings for the precision, (forward) :ref:`onemkl_dft_enum_domain`, and
dimensions of the transform. The constructors do not perform any
significant computational work, such as computation of twiddle
factors. The function :ref:`onemkl_dft_descriptor_commit` does this work 
after use of the function :ref:`onemkl_dft_descriptor_set_value` to set values 
of all necessary parameters.

.. rubric:: Syntax (one-dimensional transform)

.. code-block:: cpp
   
   namespace oneapi::mkl::dft {

      template <oneapi::mkl::dft::precision prec, oneapi::mkl::dft::domain dom>
      descriptor<prec,dom>(std::int64_t length);

   }


.. rubric:: Syntax (multi-dimensional transform)

.. code-block:: cpp
   
   namespace oneapi::mkl::dft {

      template <oneapi::mkl::dft::precision prec, oneapi::mkl::dft::domain dom>
      descriptor<prec,dom>(std::vector<std::int64_t> dimensions);

   }


.. container:: section

   .. rubric:: Input Parameters

   length
      dimension(length) of data for a 1-dimensional transform.

   dimensions
      vector of :math:`d\geq 0` dimensions(lengths) of data for a d-dimensional transform.

.. container:: section

   .. rubric:: Throws

   The `descriptor()` constructor shall throw the following exceptions if the associated condition is detected. An implementation may throw additional implementation-specific exception(s) in case of error conditions not covered here:

   :ref:`oneapi::mkl::host_bad_alloc()<onemkl_exception_host_bad_alloc>`
      If any memory allocations on host have failed, for instance due to insufficient memory.

   :ref:`oneapi::mkl::unimplemented()<onemkl_exception_unimplemented>`
      If length of ``dimensions`` vector is larger than is supported by the library implementation.
   

**Descriptor class member table:** :ref:`onemkl_dft_descriptor_member_table`



.. _onemkl_dft_descriptor_set_value:

set_value
++++++++++

Sets DFT configuration values before :ref:`onemkl_dft_descriptor_commit`.


.. rubric:: Description

This function sets one particular configuration parameter with
the specified configuration value. Each configuration parameter
is a named constant, and the configuration value must have the
corresponding type, which can be a named constant or a native
type. For available configuration parameters and the
corresponding configuration values, see :ref:`onemkl_dft_enum_config_param`.
All calls to ``set_param`` must be done before :ref:`onemkl_dft_descriptor_commit`.

.. rubric:: Syntax

.. code-block:: cpp

   namespace oneapi::mkl::dft {

      template <oneapi::mkl::dft::precision prec, oneapi::mkl::dft::domain dom>
      void descriptor<prec,dom>::set_value(config_param param, ...);

   }

.. container:: section

   .. rubric:: Input Parameters

   param
      The enum value of :ref:`onemkl_dft_enum_config_param` to be set.

   ...
      The corresponding value or container corresponding to the specific parameter. Defined in :ref:`onemkl_dft_enum_config_param`.

   
.. container:: section

   .. rubric:: Throws

   The `descriptor::set_value()` routine shall throw the following exceptions if the associated condition is detected. An implementation may throw additional implementation-specific exception(s) in case of error conditions not covered here:

   :ref:`oneapi::mkl::invalid_argument()<onemkl_exception_invalid_argument>`
      If the provided :ref:`onemkl_dft_enum_config_param` or config_value is not valid.

   :ref:`oneapi::mkl::unimplemented()<onemkl_exception_unimplemented>`
      If the provided :ref:`onemkl_dft_enum_config_param` or config_value is valid, but not supported by the library implementation.
 
   
**Descriptor class member table:** :ref:`onemkl_dft_descriptor_member_table`


.. _onemkl_dft_descriptor_get_value:

get_value
++++++++++

Retrieves current DFT configuration values.

.. rubric:: Description

This function gets one particular configuration parameter with
the specified configuration value. Each configuration parameter
is a named constant, and the configuration value must have the
corresponding type, which can be a named constant or a native
type. For available configuration parameters and the
corresponding configuration values, see :ref:`onemkl_dft_enum_config_param`.

.. rubric:: Syntax

.. code-block:: cpp

   namespace oneapi::mkl::dft {

      template <oneapi::mkl::dft::precision prec, oneapi::mkl::dft::domain dom>
      void descriptor<prec,dom>::get_value(config_param param, ...);

   }

.. container:: section

   .. rubric:: Input Parameters

   param
      The enum value of :ref:`onemkl_dft_enum_config_param` to be retrieved.

   ...
      The corresponding value or container corresponding to the specific parameter. Defined in :ref:`onemkl_dft_enum_config_param`.

.. container:: section

   .. rubric:: Throws

   The `descriptor::get_value()` routine shall throw the following exceptions if the associated condition is detected. An implementation may throw additional implementation-specific exception(s) in case of error conditions not covered here:
   
   :ref:`oneapi::mkl::invalid_argument()<onemkl_exception_invalid_argument>`
      If the requested :ref:`onemkl_dft_enum_config_param` is not correct.



**Descriptor class member table:** :ref:`onemkl_dft_descriptor_member_table`



.. _onemkl_dft_descriptor_commit:

commit
+++++++

Finalizes DFT descriptor after all configuration parameters have been set.

.. rubric:: Description

This function completes initialization of a previously created
descriptor, which is required before the descriptor can be used
for FFT computations. Typically, committing the
descriptor performs all initialization that is required for the
actual FFT computation on the device specified through input queue. 
The initialization performed by the function may involve exploring different
factorizations of the input length to find the optimal
computation method.

All calls to the :ref:`onemkl_dft_descriptor_set_value` function to change configuration
parameters of a descriptor need to happen after the constructor call for 
the :ref:`onemkl_dft_descriptor` class and before a call to :ref:`onemkl_dft_descriptor_commit`.
Typically, a commit function call is immediately followed by a computation 
function call (see :ref:`onemkl_dft_compute_forward` or :ref:`onemkl_dft_compute_backward`)


.. rubric:: Syntax

.. code-block:: cpp

   namespace oneapi::mkl::dft {

      template <oneapi::mkl::dft::precision prec, oneapi::mkl::dft::domain dom>
      void descriptor<prec,dom>::commit(sycl::queue& queue);

   }

.. container:: section

   .. rubric:: Input Parameters

   queue 
      Valid DPC++ queue specifying the device and context on which the transformation will be executed.

.. container:: section

   .. rubric:: Throws

   The following oneMKL exceptions may be thrown in this function:

   The `descriptor::commit()` routine shall throw the following exceptions if the associated condition is detected. An implementation may throw additional implementation-specific exception(s) in case of error conditions not covered here:
   
   :ref:`oneapi::mkl::invalid_argument()<onemkl_exception_invalid_argument>`
      If the queue is found to be invalid in any way.

   :ref:`oneapi::mkl::host_bad_alloc()<onemkl_exception_host_bad_alloc>`
      If any host side only memory allocations fail, for instance due to lack of memory.

   :ref:`oneapi::mkl::device_bad_alloc()<onemkl_exception_device_bad_alloc>`
      If any device or shared memory allocation fail.
 


**Descriptor class member table:** :ref:`onemkl_dft_descriptor_member_table`


**Parent topic:** :ref:`onemkl_dft`


   
