.. SPDX-FileCopyrightText: 2019-2020 Intel Corporation
..
.. SPDX-License-Identifier: CC-BY-4.0

.. _onemkl_dft_config_storage_formats:

Storage Formats
---------------

Depending on the value of the :ref:`onemkl_dft_enum_domain` template value, the implementation of the DFT supports several storage schemes for input and output data. (See ``Charles Van Loan, Computational Frameworks for the Fast Fourier Transform , SIAM, Philadelphia, 1992`` for motivation of these schemes).

The data elements are placed within contiguous memory blocks, defined with generalized strides (see :ref:`onemkl_dft_config_strides`). For multiple transforms, all sets of data should be located within the same memory block, and the data sets should be placed at the same distance from each other (see :ref:`NUMBER_OF TRANSFORMS<onemkl_dft_config_number_of_transforms>` and ``:config_param::FWD_DISTANCE``, ``config_param::BWD_DISTANCE`` ).

The input data and strides sizes are stored and offsets counted in terms of elements of the data type (complex or real) based on the storage format and :ref:`forward domain<onemkl_dft_enum_domain>` as seen in :ref:`Element types for complex-to-complex transformation and COMPLEX_STORAGE <onemkl_dft_config_data_element_types_complex>`, :ref:`Element types for real-to-complex transformations and REAL_STORAGE<onemkl_dft_config_data_element_types_real>` and :ref:`Element types for real-to-complex transformations and CONJUGATE_EVEN_STORAGE<onemkl_dft_config_data_element_types_conjugate_even>`.



.. _onemkl_dft_complex_storage:

COMPLEX_STORAGE
+++++++++++++++

For the :ref:`onemkl_dft_enum_domain` template parameter with value ``COMPLEX``, both input and output sequences belong to the complex domain. In this case, the configuration parameter COMPLEX_STORAGE can have one of the two values:``COMPLEX_COMPLEX`` (default) or ``REAL_REAL`` .

.. _onemkl_dft_complex_storage_complex_complex:

.. rubric:: COMPLEX_COMPLEX

With the ``config_value::COMPLEX_COMPLEX`` storage, complex-valued data sequences are stored in a single complex container (array/``sycl::buffer``), AZ, so that a complex-valued element :math:`z_{k_1, k_2,\dots ,k_d}` of the m-th d-dimensional sequence is accessed at :math:`AZ[m*\text{distance} + \text{stride}_0 + k_1*\text{stride}_1 + k_2*\text{stride}_2 + \dots + k_d *\text{stride}_d ]` as a structure consisting of the real and imaginary parts. This code illustrates the use of ``config_value::COMPLEX_COMPLEX`` storage with three dimensions (:math:`n_1,n_2,n_3`) and m batches:

.. code-block:: cpp

   std::complex<datatype> * AZ; // 2*sizeof(datatype)*n1*n2*n3*m
   std::vector<std::int64_t> ios; // length 4 of sizes
   std::int64_t iodist;

   // ...

   // on input: Z(k1,k2,k3,m)
   //   = AZ[ ios[0] + k1*ios[1] + k2*ios[2] + k3*ios[3] + m*iodist ]
   compute_forward(descr, AZ); // complex-to-complex in-place FFT
   // on output: Z{k1,k2,k3,m} 
   //   = AZ[ ios[0] + k1*ios[1] + k2*ios[2] + k3*ios[3] + m*iodist ]




.. _onemkl_dft_complex_storage_real_real:

.. rubric:: REAL_REAL

With the ``config_value::REAL_REAL`` storage, complex-valued data sequences are stored by two real containers (arrays/``sycl::buffer``'s), AR and AI, so that a complex-valued element :math:`z_{k_1, k_2, \dots, k_d}` of the m-th d-dimensional sequence has real part :math:`AR[m*\text{distance} + \text{stride}_0 + k_1*\text{stride}_1 + k_2*\text{stride}_2 + \dots + k_d*\text{stride}_d ]` and imaginary part :math:`AI[m*\text{distance} + \text{stride}_0 + k_1*\text{stride}_1 + k_2*\text{stride}_2 + \dots + k_d*\text{stride}_d ]`. This code illustrates the use of ``config_value::REAL_REAL`` storage with three dimensions (:math:`n_1,n_2,n_3`) and m batches:

.. code-block:: cpp

   datatype * AR; // sizeof(datatype)*n1*n2*n3*m
   datatype * AI; // sizeof(datatype)*n1*n2*n3*m
   std::vector<std::int64_t> ios; // length 4 of strides
   std::int64_t iodist;

   // ...

   // on input: Z(k1,k2,k3,m)
   //   =   AR[ ios[0] + k1*ios[1] + k2*ios[2] + k3*ios[3] + m*iodist ]
   //   + i*AI[ ios[0] + k1*ios[1] + k2*ios[2] + k3*ios[3] + m*iodist ]
   compute_forward(descr, AR, AI); // complex-to-complex in-place FFT
   // on output: Z{k1,k2,k3,m} 
   //   =   AR[ ios[0] + k1*ios[1] + k2*ios[2] + k3*ios[3] + m*iodist ]
   //   + i*AI[ ios[0] + k1*ios[1] + k2*ios[2] + k3*ios[3] + m*iodist ]


.. _onemkl_dft_real_storage:

REAL_STORAGE
++++++++++++

For the :ref:`onemkl_dft_enum_domain` template parameter with value ``REAL``, only the value of ``REAL_REAL`` is supported.

.. _onemkl_dft_real_storage_real_real:

.. rubric:: REAL_REAL

With the ``REAL_REAL`` storage, real-valued data sequences in a real domain are stored by one real container (array/``sycl::buffer``), AR, so that a real-valued element :math:`r_{k_1, k_2, \dots, k_d}` of the m-th d-dimensional sequence is accessed as :math:`AR[m*\text{distance} + \text{stride}_0 + k_1*\text{stride}_1 + k_2*\text{stride}_2 + \dots + k_d*\text{stride}_d ]`. This code illustrates the use of ``config_value::REAL_REAL`` storage with three dimensions (:math:`n_1,n_2,n_3`) and m batches:

.. code-block:: cpp

   datatype * AR; // sizeof(datatype)*n1*n2*n3*m
   datatype * AI; // sizeof(datatype)*n1*n2*n3*m
   std::vector<std::int64_t> ios; // length 4 of strides
   std::int64_t iodist;

   // ...

   // on input: R(k1,k2,k3,m)
   //   =   AR[ ios[0] + k1*ios[1] + k2*ios[2] + k3*ios[3] + m*iodist ]
   compute_forward(descr, AR, AI); // real-to-complex in-place FFT
   // on output: Z{k1,k2,k3,m} 
   //   =   AR[ ios[0] + k1*ios[1] + k2*ios[2] + k3*ios[3] + m*iodist ]
   //   + i*AI[ ios[0] + k1*ios[1] + k2*ios[2] + k3*ios[3] + m*iodist ]




.. _onemkl_dft_conjugate_even_storage:

CONJUGATE_EVEN_STORAGE
++++++++++++++++++++++

For the :ref:`onemkl_dft_enum_domain` template parameter with value ``REAL`` and considered as a conjugate-even domain, the value of ``config_value::COMPLEX_COMPLEX`` is supported. The conjugate-even symmetry of the data enables storing only about a half of the whole mathematical result, so that one part of it can be directly referenced in the memory while the other part can be reconstructed depending on the selected storage configuration. The ``config_param::PACKED_FORMAT`` configuration parameter defines how the data is packed.  Possible values for ``config_param::PACKED_FORMAT`` depend on the values of the ``config_param::CONJUGATE_EVEN_STORAGE`` configuration parameter.

.. tabularcolumns:: l|c|

.. list-table::
     :header-rows: 1
     :class: longtable

     * -   CONJUGATE_EVEN_STORAGE
       -   Supported PACKED_FORMATS
     * -   :ref:`onemkl_dft_conjugate_even_storage_complex_complex`
       -   ``config_value::CCE_FORMAT`` can be used with transforms of any dimension.



.. _onemkl_dft_conjugate_even_storage_complex_complex:

.. rubric:: COMPLEX_COMPLEX

There is only one ``config_param::PACKED_FORMAT`` supported by the ``config_value::COMPLEX_COMPLEX`` value for ``config_param::CONJUGATE_EVEN_STORAGE``, mainly the ``config_value::CCE_FORMAT``.  The complex-valued data sequence consists of one complex container (array/``sycl::buffer``), AZ, so that a complex-valued element :math:`z_{k_1, k_2, \dots, k_d}` of the m-th d-dimensional sequence can be accessed or reconstructed as follows:

Consider a d-dimensional real-to-complex transform.

Because the input sequence, R, is real-valued, the mathematical result, Z, has conjugate-even symmetry:
:math:`z_{k_1, k_2, \dots, k_d} = \text{conjugate}( z_{n_1-k_1, n_2-k_2, \dots, n_d-k_d} )`,
where index arithmetic is performed modulo the length of the respective dimension. Obviously, the first element of the result is real-valued:
:math:`z_{0, 0, \dots, 0} = \text{conjugate}( z_{0, 0, \dots, 0} )`.

For dimensions with even lengths, some of the other elements are real-valued as well. For example, if :math:`n_s` is even, then
:math:`z_{0, 0, \dots, \frac{n_s}{2}, 0, \dots, 0} = \text{conjugate}( z_{0, 0, \dots, \frac{n_s}{2}, 0, \dots, 0} )`.
With the conjugate-even symmetry, approximately a half of the result suffices to fully reconstruct it. For an arbitrary dimension, :math:`h` , it suffices to store elements :math:`z_{k_1, \dots, k_h , \dots, k_d}` for the following indices:

* :math:`k_h = 0, \dots, \left[ \frac{n_h}{2}\right]`
* :math:`k_i = 0, \dots, n_i-1`, where :math:`i = 1,\dots, d` and :math:`i \neq h` 

and assuming that integer division rounds down.

The symmetry property enables reconstructing the remaining elements: for :math:`k_h = \left[ \frac{n_h}{2}\right] + 1, \dots , n_h - 1`. The halved dimension is always assumed to be the dimension for which storage is contiguous in memory (see strides), for example in a 2D row-major format, it is the last dimension and for 2D column-major format it is the first dimension.

.. _onemkl_dft_complex_complex_cce_1d_even_or_odd:

.. rubric:: Packed complex domain formats for a 1D real-to-complex transformation considered as a conjugate-even-domain with :ref:`onemkl_dft_conjugate_even_storage_complex_complex` storage and :math:`n=2L` (even size) or :math:`n=2L+1` (odd size).

.. tabularcolumns:: l|c|c|c|c|c|c|c|

.. list-table::
     :header-rows: 1
     :class: longtable

     * -   :math:`k=`
       -   0
       -   1
       -   2
       -   :math:`\dots`
       -   L-2
       -   L-1
       -   L
     * -   CCE
       -   :math:`Z_0`
       -   :math:`Z_1`
       -   :math:`Z_2`
       -   :math:`\dots`
       -   :math:`Z_{L-2}`
       -   :math:`Z_{L-1}`
       -   :math:`Z_{L}`


.. _onemkl_dft_complex_complex_cce_2d_even_even:

.. rubric:: Packed complex domain formats for a 2D :math:`n_1\times n_2` real-to-complex transformations considered as a conjugate-even-domain with :ref:`onemkl_dft_conjugate_even_storage_complex_complex` storage and :math:`n_1=2K` (even size) and :math:`n_2=2L` (even size) using row-major input data.

.. tabularcolumns:: |c|c|c|c|c|c|c|

.. list-table::
     :header-rows: 1
     :stub-columns: 1
     :class: longtable

     * -   :math:`k_1\backslash k_2`
       -   :math:`0`
       -   1
       -   2
       -   :math:`\dots`
       -   L-1
       -   L
     * -   :math:`0`
       -   :math:`Z_{0,0}`
       -   :math:`Z_{0,1}`
       -   :math:`Z_{0,2}`
       -   :math:`\dots`
       -   :math:`Z_{0,L-1}`
       -   :math:`Z_{0,L}`
     * -   1
       -   :math:`Z_{1,0}`
       -   :math:`Z_{1,1}`
       -   :math:`Z_{1,2}`
       -   :math:`\dots`
       -   :math:`Z_{1,L-1}`
       -   :math:`Z_{1,L}`
     * -   2
       -   :math:`Z_{2,0}`
       -   :math:`Z_{2,1}`
       -   :math:`Z_{2,2}`
       -   :math:`\dots`
       -   :math:`Z_{2,L-1}`
       -   :math:`Z_{2,L}`
     * -   :math:`\dots`
       -   :math:`\dots`
       -   :math:`\dots`
       -   :math:`\dots`
       -   :math:`\dots`
       -   :math:`\dots`
       -   :math:`\dots`
     * -   :math:`n_1-2`
       -   :math:`Z_{n_1-2,0}`
       -   :math:`Z_{n_1-2,1}`
       -   :math:`Z_{n_1-2,2}`
       -   :math:`\dots`
       -   :math:`Z_{n_1-2,L-1}`
       -   :math:`Z_{n_1-2,L}`
     * -   :math:`n_1-1`
       -   :math:`Z_{n_1-1,0}`
       -   :math:`Z_{n_1-1,1}`
       -   :math:`Z_{n_1-1,2}`
       -   :math:`\dots`
       -   :math:`Z_{n_1-1,L-1}`
       -   :math:`Z_{n_1-1,L}`
 


The following code illustrates usage of the ``config_value::COMPLEX_COMPLEX`` storage for a two-dimensional conjugate-even domain with row-major input data:

.. code-block:: cpp

   datatype * AR;                // sizeof(datatype)*n1*n2*m
   std::complex<datatype> * AZ;  // sizeof(datatype)*n1*n2*m
   std::vector<std::int64_t> is; // length 3 of input strides
   std::vector<std::int64_t> os; // length 3 of output strides
   std::int64_t idist, odist;

   // ...

   // on input: R(k1,k2,m)
   //   =   AR[ is[0] + k1*is[1] + k2*is[2] + m*idist ]
   compute_forward(descr, AR, AZ); // real-to-complex out-of-place FFT
   // on output: 
   // for k2=0,n2/2:      Z{k1,k2,m} = AZ[os[0] + k1*os[1] + k2*os[2] + m*odist]
   // for k2=n2/2+1,n2-1: Z{k1,k2,m} = conj(AZ[os[0] + (n1-k1)%n1*os[1] 
   //                                                + (n2-k2)%n2*os[2] + m*odist])

For the backward transform, the input and output parameters and layouts exchange roles.  Set the strides describing the layout in the backward/forward domain as input/output strides, respectively. For example:

.. code-block:: cpp
   
   // ...
   descr.set_value(config_param::INPUT_STRIDES,  fwd_domain_strides);
   descr.set_value(config_param::OUTPUT_STRIDES, bwd_domain_strides);
   descr.commit(queue);
   compute_forward(descr, ...);
   // ...
   descr.set_value(config_param::INPUT_STRIDES,  bwd_domain_strides);
   descr.set_value(config_param::OUTPUT_STRIDES, fwd_domain_strides);
   descr.commit(queue);
   compute_backward(descr, ...);




**Parent topic** :ref:`onemkl_dft_enums`


